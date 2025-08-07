"""
Catalog endpoints for browsing albums, tracks, and artists.
"""
import hashlib
import json
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status, Request, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy import and_, or_, desc, asc, func
from sqlalchemy.orm import Session, joinedload
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.deps.auth import get_db, get_current_user, get_current_verified_user
from app.core.config import settings
from app.models.music import Album, Track, ArtistProfile, Genre, AudioFile, AudioQuality
from app.models.user import User

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


# Pydantic models for responses
class TrackSummary(BaseModel):
    """Track summary for album listings."""
    id: str
    title: str
    track_number: int
    duration_seconds: float
    is_explicit: bool
    preview_url: Optional[str]
    
    class Config:
        from_attributes = True


class ArtistSummary(BaseModel):
    """Artist summary for listings."""
    id: str
    stage_name: str
    is_verified: bool
    country: Optional[str]
    
    class Config:
        from_attributes = True


class AlbumSummary(BaseModel):
    """Album summary for listings."""
    id: str
    title: str
    release_date: str
    genre: Genre
    cover_art_url: Optional[str]
    artist: ArtistSummary
    track_count: int
    total_duration: float
    is_published: bool
    
    class Config:
        from_attributes = True


class AlbumDetail(BaseModel):
    """Detailed album information."""
    id: str
    title: str
    description: Optional[str]
    release_date: str
    genre: Genre
    subgenre: Optional[str]
    tags: List[str]
    cover_art_url: Optional[str]
    cover_art_color: Optional[str]
    label: Optional[str]
    catalog_number: Optional[str]
    upc: Optional[str]
    is_published: bool
    is_explicit: bool
    total_plays: int
    total_sales: int
    artist: ArtistSummary
    tracks: List[TrackSummary]
    created_at: datetime
    
    class Config:
        from_attributes = True


class TrackDetail(BaseModel):
    """Detailed track information."""
    id: str
    title: str
    track_number: int
    disc_number: int
    duration_seconds: float
    bpm: Optional[int]
    key: Optional[str]
    isrc: Optional[str]
    lyrics: Optional[str]
    credits: Dict[str, Any]
    featuring_artists: List[str]
    is_explicit: bool
    is_instrumental: bool
    preview_url: Optional[str]
    preview_start_time: float
    waveform_data: Optional[Dict[str, Any]]
    play_count: int
    skip_rate: float
    album: AlbumSummary
    available_formats: List[str]
    
    class Config:
        from_attributes = True


class ArtistDetail(BaseModel):
    """Detailed artist information."""
    id: str
    stage_name: str
    bio: Optional[str]
    country: Optional[str]
    website: Optional[str]
    spotify_url: Optional[str]
    apple_music_url: Optional[str]
    soundcloud_url: Optional[str]
    instagram_url: Optional[str]
    twitter_url: Optional[str]
    facebook_url: Optional[str]
    youtube_url: Optional[str]
    is_verified: bool
    verification_date: Optional[datetime]
    total_plays: int
    total_sales: int
    monthly_listeners: int
    albums: List[AlbumSummary]
    
    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class SearchResult(BaseModel):
    """Search results with different categories."""
    albums: List[AlbumSummary]
    tracks: List[TrackDetail]
    artists: List[ArtistSummary]
    total_results: int


# Utility functions
def create_cache_key(prefix: str, **kwargs) -> str:
    """Create cache key from parameters."""
    sorted_params = sorted(kwargs.items())
    params_str = json.dumps(sorted_params, sort_keys=True)
    cache_key = f"{prefix}:{hashlib.md5(params_str.encode()).hexdigest()}"
    return cache_key


def paginate_query(query, page: int, page_size: int):
    """Apply pagination to SQLAlchemy query."""
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1
    }


def add_album_summary_fields(album):
    """Add computed fields to album."""
    album.track_count = len(album.tracks)
    album.total_duration = sum(track.duration_seconds for track in album.tracks)
    return album


# Albums endpoints
@router.get("/albums", response_model=PaginatedResponse)
@limiter.limit("100/minute")
async def get_albums(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    genre: Optional[Genre] = Query(None, description="Filter by genre"),
    artist_id: Optional[str] = Query(None, description="Filter by artist"),
    sort_by: str = Query("release_date", description="Sort by: release_date, title, plays, created_at"),
    sort_order: str = Query("desc", description="Sort order: asc, desc"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    published_only: bool = Query(True, description="Show only published albums"),
    db: Session = Depends(get_db)
):
    """Get paginated list of albums with filtering and sorting."""
    
    # Build query
    query = db.query(Album).options(
        joinedload(Album.artist),
        joinedload(Album.tracks)
    )
    
    # Apply filters
    if published_only:
        query = query.filter(Album.is_published == True)
    
    if genre:
        query = query.filter(Album.genre == genre)
    
    if artist_id:
        query = query.filter(Album.artist_id == artist_id)
    
    if search:
        search_filter = or_(
            Album.title.ilike(f"%{search}%"),
            Album.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Apply sorting
    sort_column = getattr(Album, sort_by, Album.release_date)
    if sort_order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))
    
    # Paginate
    result = paginate_query(query, page, page_size)
    
    # Add computed fields
    albums = []
    for album in result["items"]:
        album_dict = album.__dict__.copy()
        album_dict["track_count"] = len(album.tracks)
        album_dict["total_duration"] = sum(track.duration_seconds for track in album.tracks)
        albums.append(AlbumSummary.from_orm(album))
    
    result["items"] = albums
    return result


@router.get("/albums/{album_id}", response_model=AlbumDetail)
@limiter.limit("200/minute")
async def get_album(
    request: Request,
    album_id: str,
    db: Session = Depends(get_db)
):
    """Get detailed album information."""
    
    album = db.query(Album).options(
        joinedload(Album.artist),
        joinedload(Album.tracks)
    ).filter(Album.id == album_id).first()
    
    if not album:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found"
        )
    
    if not album.is_published:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not available"
        )
    
    return AlbumDetail.from_orm(album)


# Tracks endpoints
@router.get("/tracks/search")
@limiter.limit("100/minute")
async def search_tracks(
    request: Request,
    q: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    genre: Optional[Genre] = Query(None),
    bpm_min: Optional[int] = Query(None, ge=60, le=200),
    bpm_max: Optional[int] = Query(None, ge=60, le=200),
    duration_min: Optional[int] = Query(None, ge=30, description="Minimum duration in seconds"),
    duration_max: Optional[int] = Query(None, le=600, description="Maximum duration in seconds"),
    key: Optional[str] = Query(None, description="Musical key"),
    db: Session = Depends(get_db)
):
    """Search tracks with full-text search and filters."""
    
    # Build query
    query = db.query(Track).join(Album).join(ArtistProfile).options(
        joinedload(Track.album).joinedload(Album.artist)
    )
    
    # Only published albums
    query = query.filter(Album.is_published == True)
    
    # Text search
    search_filter = or_(
        Track.title.ilike(f"%{q}%"),
        Album.title.ilike(f"%{q}%"),
        ArtistProfile.stage_name.ilike(f"%{q}%"),
        Track.featuring_artists.astext.ilike(f"%{q}%")
    )
    query = query.filter(search_filter)
    
    # Apply filters
    if genre:
        query = query.filter(Album.genre == genre)
    
    if bpm_min:
        query = query.filter(Track.bpm >= bpm_min)
    
    if bpm_max:
        query = query.filter(Track.bpm <= bpm_max)
    
    if duration_min:
        query = query.filter(Track.duration_seconds >= duration_min)
    
    if duration_max:
        query = query.filter(Track.duration_seconds <= duration_max)
    
    if key:
        query = query.filter(Track.key.ilike(f"%{key}%"))
    
    # Order by relevance (play count for now)
    query = query.order_by(desc(Track.play_count))
    
    # Paginate
    result = paginate_query(query, page, page_size)
    
    # Convert to TrackDetail
    tracks = []
    for track in result["items"]:
        # Get available formats
        formats = db.query(AudioFile.format).filter(
            AudioFile.track_id == track.id,
            AudioFile.is_processed == True
        ).distinct().all()
        
        track_dict = track.__dict__.copy()
        track_dict["available_formats"] = [f[0] for f in formats]
        tracks.append(TrackDetail.from_orm(track))
    
    result["items"] = tracks
    return result


@router.get("/tracks/{track_id}", response_model=TrackDetail)
@limiter.limit("200/minute")
async def get_track(
    request: Request,
    track_id: str,
    db: Session = Depends(get_db)
):
    """Get detailed track information."""
    
    track = db.query(Track).options(
        joinedload(Track.album).joinedload(Album.artist)
    ).filter(Track.id == track_id).first()
    
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not found"
        )
    
    if not track.album.is_published:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not available"
        )
    
    # Get available formats
    formats = db.query(AudioFile.format).filter(
        AudioFile.track_id == track.id,
        AudioFile.is_processed == True
    ).distinct().all()
    
    track_dict = track.__dict__.copy()
    track_dict["available_formats"] = [f[0] for f in formats]
    
    return TrackDetail.from_orm(track)


@router.get("/tracks/{track_id}/stream")
@limiter.limit("500/minute")
async def stream_track(
    request: Request,
    track_id: str,
    quality: AudioQuality = Query(AudioQuality.HIGH, description="Audio quality"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user)
):
    """Stream track audio file."""
    
    # Get track and verify access
    track = db.query(Track).join(Album).filter(
        Track.id == track_id,
        Album.is_published == True
    ).first()
    
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not found"
        )
    
    # TODO: Check if user has purchased this track
    # For now, allow streaming for all verified users
    
    # Get audio file
    audio_file = db.query(AudioFile).filter(
        AudioFile.track_id == track.id,
        AudioFile.quality == quality,
        AudioFile.is_processed == True
    ).first()
    
    if not audio_file:
        # Try to get any available quality
        audio_file = db.query(AudioFile).filter(
            AudioFile.track_id == track.id,
            AudioFile.is_processed == True
        ).first()
    
    if not audio_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio file not available"
        )
    
    # Update play count
    track.play_count += 1
    db.commit()
    
    # TODO: Implement actual file streaming from storage
    # For now, return file info
    return {
        "track_id": track_id,
        "file_path": audio_file.file_path,
        "format": audio_file.format,
        "quality": audio_file.quality,
        "bitrate": audio_file.bitrate,
        "message": "File streaming would be implemented here"
    }


@router.get("/tracks/{track_id}/preview")
@limiter.limit("1000/minute")
async def get_track_preview(
    request: Request,
    track_id: str,
    db: Session = Depends(get_db)
):
    """Get track preview (30-second snippet)."""
    
    track = db.query(Track).join(Album).filter(
        Track.id == track_id,
        Album.is_published == True
    ).first()
    
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not found"
        )
    
    if not track.preview_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preview not available"
        )
    
    # TODO: Implement actual preview streaming
    return {
        "track_id": track_id,
        "preview_url": track.preview_url,
        "preview_start_time": track.preview_start_time,
        "duration": settings.PREVIEW_DURATION_SECONDS,
        "message": "Preview streaming would be implemented here"
    }


# Artists endpoints
@router.get("/artists", response_model=PaginatedResponse)
@limiter.limit("100/minute")
async def get_artists(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    country: Optional[str] = Query(None, description="Filter by country code"),
    verified_only: bool = Query(False, description="Show only verified artists"),
    sort_by: str = Query("monthly_listeners", description="Sort by: stage_name, monthly_listeners, total_plays"),
    sort_order: str = Query("desc", description="Sort order: asc, desc"),
    search: Optional[str] = Query(None, description="Search in stage name and bio"),
    db: Session = Depends(get_db)
):
    """Get paginated list of artists."""
    
    # Build query
    query = db.query(ArtistProfile).options(
        joinedload(ArtistProfile.albums)
    )
    
    # Apply filters
    if verified_only:
        query = query.filter(ArtistProfile.is_verified == True)
    
    if country:
        query = query.filter(ArtistProfile.country == country.upper())
    
    if search:
        search_filter = or_(
            ArtistProfile.stage_name.ilike(f"%{search}%"),
            ArtistProfile.bio.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Apply sorting
    sort_column = getattr(ArtistProfile, sort_by, ArtistProfile.monthly_listeners)
    if sort_order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))
    
    # Paginate
    result = paginate_query(query, page, page_size)
    
    # Convert to response model
    artists = [ArtistSummary.from_orm(artist) for artist in result["items"]]
    result["items"] = artists
    
    return result


@router.get("/artists/{artist_id}", response_model=ArtistDetail)
@limiter.limit("200/minute")
async def get_artist(
    request: Request,
    artist_id: str,
    db: Session = Depends(get_db)
):
    """Get detailed artist information."""
    
    artist = db.query(ArtistProfile).options(
        joinedload(ArtistProfile.albums).joinedload(Album.tracks)
    ).filter(ArtistProfile.id == artist_id).first()
    
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )
    
    # Only include published albums
    published_albums = [album for album in artist.albums if album.is_published]
    
    artist_dict = artist.__dict__.copy()
    artist_dict["albums"] = [add_album_summary_fields(album) for album in published_albums]
    
    return ArtistDetail.from_orm(artist)


# Global search endpoint
@router.get("/search", response_model=SearchResult)
@limiter.limit("50/minute")
async def global_search(
    request: Request,
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Results per category"),
    db: Session = Depends(get_db)
):
    """Global search across albums, tracks, and artists."""
    
    # Search albums
    albums_query = db.query(Album).join(ArtistProfile).options(
        joinedload(Album.artist),
        joinedload(Album.tracks)
    ).filter(
        Album.is_published == True,
        or_(
            Album.title.ilike(f"%{q}%"),
            Album.description.ilike(f"%{q}%"),
            ArtistProfile.stage_name.ilike(f"%{q}%")
        )
    ).order_by(desc(Album.total_plays)).limit(limit)
    
    albums = [AlbumSummary.from_orm(add_album_summary_fields(album)) for album in albums_query.all()]
    
    # Search tracks
    tracks_query = db.query(Track).join(Album).join(ArtistProfile).options(
        joinedload(Track.album).joinedload(Album.artist)
    ).filter(
        Album.is_published == True,
        or_(
            Track.title.ilike(f"%{q}%"),
            Album.title.ilike(f"%{q}%"),
            ArtistProfile.stage_name.ilike(f"%{q}%")
        )
    ).order_by(desc(Track.play_count)).limit(limit)
    
    tracks = []
    for track in tracks_query.all():
        # Get available formats
        formats = db.query(AudioFile.format).filter(
            AudioFile.track_id == track.id,
            AudioFile.is_processed == True
        ).distinct().all()
        
        track_dict = track.__dict__.copy()
        track_dict["available_formats"] = [f[0] for f in formats]
        tracks.append(TrackDetail.from_orm(track))
    
    # Search artists
    artists_query = db.query(ArtistProfile).filter(
        or_(
            ArtistProfile.stage_name.ilike(f"%{q}%"),
            ArtistProfile.bio.ilike(f"%{q}%")
        )
    ).order_by(desc(ArtistProfile.monthly_listeners)).limit(limit)
    
    artists = [ArtistSummary.from_orm(artist) for artist in artists_query.all()]
    
    total_results = len(albums) + len(tracks) + len(artists)
    
    return SearchResult(
        albums=albums,
        tracks=tracks,
        artists=artists,
        total_results=total_results
    )