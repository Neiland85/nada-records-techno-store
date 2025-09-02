"""
Music-related schemas for albums, tracks, and artists.
"""
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, Field, HttpUrl

from app.models.music import Genre, AudioFormat, AudioQuality


# Track Schemas
class TrackBase(BaseModel):
    """Base track fields."""
    title: str = Field(..., min_length=1, max_length=200)
    track_number: int = Field(..., ge=1)
    duration_seconds: Optional[int] = Field(None, ge=0)
    genre: Optional[Genre] = None
    bpm: Optional[int] = Field(None, ge=60, le=200)
    key_signature: Optional[str] = Field(None, max_length=10)
    price: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2)
    is_free: bool = False
    preview_start_time: Optional[int] = Field(None, ge=0, description="Preview start time in seconds")


class TrackCreate(TrackBase):
    """Track creation schema."""
    album_id: str


class TrackUpdate(BaseModel):
    """Track update schema."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    genre: Optional[Genre] = None
    bpm: Optional[int] = Field(None, ge=60, le=200)
    key_signature: Optional[str] = Field(None, max_length=10)
    price: Optional[Decimal] = Field(None, ge=0, max_digits=10, decimal_places=2)
    is_free: Optional[bool] = None
    preview_start_time: Optional[int] = Field(None, ge=0)


class TrackResponse(TrackBase):
    """Track response schema."""
    id: str
    album_id: str
    slug: str
    play_count: int
    download_count: int
    is_published: bool
    created_at: datetime
    updated_at: datetime
    
    # Audio files
    audio_files: List["AudioFileResponse"] = []
    
    class Config:
        from_attributes = True


# Album Schemas
class AlbumBase(BaseModel):
    """Base album fields."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    release_date: Optional[date] = None
    genre: Optional[Genre] = None
    total_price: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2)
    is_free: bool = False
    is_single: bool = False


class AlbumCreate(AlbumBase):
    """Album creation schema."""
    pass


class AlbumUpdate(BaseModel):
    """Album update schema."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    release_date: Optional[date] = None
    genre: Optional[Genre] = None
    total_price: Optional[Decimal] = Field(None, ge=0, max_digits=10, decimal_places=2)
    is_free: Optional[bool] = None


class AlbumResponse(AlbumBase):
    """Album response schema."""
    id: str
    artist_id: str
    slug: str
    cover_art_url: Optional[HttpUrl] = None
    total_tracks: int
    total_duration_seconds: int
    play_count: int
    download_count: int
    is_published: bool
    created_at: datetime
    updated_at: datetime
    
    # Relationships
    artist: "ArtistResponse"
    tracks: List[TrackResponse] = []
    
    class Config:
        from_attributes = True


# Audio File Schemas
class AudioFileBase(BaseModel):
    """Base audio file fields."""
    format: AudioFormat
    quality: AudioQuality
    bitrate: int = Field(..., ge=32, le=1411)
    sample_rate: int = Field(..., ge=8000, le=192000)
    file_size_bytes: int = Field(..., ge=0)


class AudioFileResponse(AudioFileBase):
    """Audio file response schema."""
    id: str
    track_id: str
    file_url: HttpUrl
    download_url: HttpUrl
    is_preview: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True


# Artist Schemas
class ArtistResponse(BaseModel):
    """Artist response schema (simplified for album/track responses)."""
    id: str
    stage_name: str
    is_verified: bool
    total_plays: int
    total_sales: int
    monthly_listeners: int
    
    class Config:
        from_attributes = True


# Forward reference resolution
TrackResponse.model_rebuild()
AlbumResponse.model_rebuild()
