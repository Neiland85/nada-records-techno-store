"""
Audio upload endpoints for artists to upload music content.
"""
import os
import uuid
import hashlib
import tempfile
import asyncio
from datetime import datetime, date
from typing import List, Optional, Dict, Any, BinaryIO
from pathlib import Path

import aiofiles
import librosa
import numpy as np
from fastapi import (
    APIRouter, Depends, HTTPException, UploadFile, File, Form,
    status, WebSocket, WebSocketDisconnect, BackgroundTasks
)
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
from pydub import AudioSegment
from mutagen import File as MutagenFile
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.deps.auth import get_db, get_current_artist_user, PermissionChecker
from app.core.config import settings
from app.models.music import Album, Track, AudioFile, Genre, AudioFormat, AudioQuality
from app.models.user import User

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

# Constants
SUPPORTED_AUDIO_FORMATS = ["mp3", "wav", "flac", "aac", "ogg"]
MAX_CHUNK_SIZE = 1024 * 1024  # 1MB chunks
TEMP_UPLOAD_DIR = Path(settings.TEMP_UPLOAD_DIR)

# Ensure temp directory exists
TEMP_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Pydantic models
class AlbumCreate(BaseModel):
    """Album creation request."""
    title: str
    description: Optional[str] = None
    release_date: date
    genre: Genre
    subgenre: Optional[str] = None
    tags: List[str] = []
    label: Optional[str] = None
    catalog_number: Optional[str] = None
    upc: Optional[str] = None
    is_explicit: bool = False
    
    @validator('title')
    def validate_title(cls, v):
        if len(v.strip()) < 1:
            raise ValueError('Title cannot be empty')
        if len(v) > 200:
            raise ValueError('Title too long')
        return v.strip()
    
    @validator('tags')
    def validate_tags(cls, v):
        if len(v) > 10:
            raise ValueError('Too many tags (max 10)')
        return [tag.strip().lower() for tag in v if tag.strip()]


class TrackMetadata(BaseModel):
    """Track metadata for upload."""
    title: str
    track_number: int
    disc_number: int = 1
    featuring_artists: List[str] = []
    isrc: Optional[str] = None
    lyrics: Optional[str] = None
    credits: Dict[str, Any] = {}
    is_explicit: bool = False
    is_instrumental: bool = False
    
    @validator('title')
    def validate_title(cls, v):
        if len(v.strip()) < 1:
            raise ValueError('Title cannot be empty')
        if len(v) > 200:
            raise ValueError('Title too long')
        return v.strip()
    
    @validator('track_number')
    def validate_track_number(cls, v):
        if v < 1 or v > 999:
            raise ValueError('Track number must be between 1 and 999')
        return v


class ChunkUploadRequest(BaseModel):
    """Chunk upload request."""
    chunk_index: int
    total_chunks: int
    file_name: str
    file_size: int
    upload_id: str
    checksum: str


class UploadResponse(BaseModel):
    """Upload response."""
    upload_id: str
    status: str
    message: str
    progress: Optional[float] = None
    file_info: Optional[Dict[str, Any]] = None


class ProcessingStatus(BaseModel):
    """Processing status response."""
    track_id: str
    status: str
    progress: float
    message: str
    error: Optional[str] = None
    waveform_data: Optional[List[float]] = None


# WebSocket connection manager
class ConnectionManager:
    """Manage WebSocket connections for upload progress."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, upload_id: str):
        await websocket.accept()
        self.active_connections[upload_id] = websocket
    
    def disconnect(self, upload_id: str):
        if upload_id in self.active_connections:
            del self.active_connections[upload_id]
    
    async def send_progress(self, upload_id: str, data: dict):
        if upload_id in self.active_connections:
            try:
                await self.active_connections[upload_id].send_json(data)
            except:
                # Remove disconnected client
                self.disconnect(upload_id)


manager = ConnectionManager()


# Utility functions
def get_file_extension(filename: str) -> str:
    """Get file extension."""
    return filename.lower().split('.')[-1] if '.' in filename else ''


def validate_audio_file(file_path: Path) -> Dict[str, Any]:
    """Validate audio file and extract metadata."""
    try:
        # Check file format
        extension = get_file_extension(file_path.name)
        if extension not in SUPPORTED_AUDIO_FORMATS:
            raise ValueError(f"Unsupported format: {extension}")
        
        # Load with mutagen for metadata
        audio_file = MutagenFile(file_path)
        if audio_file is None:
            raise ValueError("Cannot read audio file")
        
        # Load with librosa for analysis
        y, sr = librosa.load(file_path, sr=None)
        duration = len(y) / sr
        
        # Extract BPM
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = int(tempo) if tempo > 0 else None
        
        # Extract key (simplified)
        chromagram = librosa.feature.chroma_stft(y=y, sr=sr)
        key_index = np.argmax(np.mean(chromagram, axis=1))
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        key = keys[key_index]
        
        # File info
        file_info = {
            "duration_seconds": float(duration),
            "sample_rate": int(sr),
            "channels": 1 if y.ndim == 1 else y.shape[0],
            "bitrate": getattr(audio_file.info, 'bitrate', 0),
            "format": extension,
            "bpm": bpm,
            "key": key,
            "file_size": file_path.stat().st_size
        }
        
        return file_info
        
    except Exception as e:
        raise ValueError(f"Audio validation failed: {str(e)}")


def generate_waveform_data(file_path: Path, points: int = 1000) -> List[float]:
    """Generate waveform data for visualization."""
    try:
        y, sr = librosa.load(file_path, sr=22050)
        
        # Downsample for visualization
        hop_length = len(y) // points
        if hop_length < 1:
            hop_length = 1
        
        # Calculate RMS energy
        rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
        
        # Normalize to 0-1 range
        if len(rms) > 0:
            rms = (rms - np.min(rms)) / (np.max(rms) - np.min(rms) + 1e-10)
        
        # Ensure we have the right number of points
        if len(rms) > points:
            rms = rms[:points]
        elif len(rms) < points:
            # Pad with zeros
            rms = np.pad(rms, (0, points - len(rms)), 'constant')
        
        return rms.tolist()
        
    except Exception as e:
        print(f"Waveform generation failed: {e}")
        return [0.0] * points


def create_preview(file_path: Path, output_path: Path) -> bool:
    """Create 30-second preview of the track."""
    try:
        # Load audio
        audio = AudioSegment.from_file(file_path)
        
        # Calculate preview start (around 25% into the track)
        duration_ms = len(audio)
        start_ms = min(duration_ms * 0.25, duration_ms - 30000)
        start_ms = max(0, start_ms)
        
        # Extract 30-second preview
        preview_duration = min(30000, duration_ms - start_ms)
        preview = audio[start_ms:start_ms + preview_duration]
        
        # Apply fade in/out
        fade_duration = min(500, preview_duration // 10)
        preview = preview.fade_in(fade_duration).fade_out(fade_duration)
        
        # Export as MP3
        preview.export(output_path, format="mp3", bitrate="128k")
        
        return True
        
    except Exception as e:
        print(f"Preview creation failed: {e}")
        return False


def calculate_file_checksum(file_path: Path) -> str:
    """Calculate SHA-256 checksum of file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


# Endpoints
@router.post("/albums/create", response_model=Dict[str, Any])
@limiter.limit("10/minute")
async def create_album(
    album_data: AlbumCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_artist_user)
):
    """Create a new album for the artist."""
    
    # Check if album title already exists for this artist
    existing_album = db.query(Album).filter(
        Album.artist_id == current_user.artist_profile.id,
        Album.title == album_data.title
    ).first()
    
    if existing_album:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Album with this title already exists"
        )
    
    # Create album
    album = Album(
        artist_id=current_user.artist_profile.id,
        title=album_data.title,
        description=album_data.description,
        release_date=album_data.release_date,
        genre=album_data.genre,
        subgenre=album_data.subgenre,
        tags=album_data.tags,
        label=album_data.label,
        catalog_number=album_data.catalog_number,
        upc=album_data.upc,
        is_explicit=album_data.is_explicit,
        is_published=False  # Default to unpublished
    )
    
    db.add(album)
    db.commit()
    db.refresh(album)
    
    return {
        "album_id": str(album.id),
        "title": album.title,
        "status": "created",
        "message": "Album created successfully"
    }


@router.post("/tracks/upload-init", response_model=UploadResponse)
@limiter.limit("20/minute")
async def initialize_upload(
    file_name: str = Form(...),
    file_size: int = Form(...),
    album_id: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_artist_user)
):
    """Initialize chunked file upload."""
    
    # Validate file size
    if file_size > settings.MAX_AUDIO_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Max size: {settings.MAX_AUDIO_FILE_SIZE_MB}MB"
        )
    
    # Validate file format
    extension = get_file_extension(file_name)
    if extension not in SUPPORTED_AUDIO_FORMATS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported format. Supported: {', '.join(SUPPORTED_AUDIO_FORMATS)}"
        )
    
    # Verify album ownership
    album = db.query(Album).filter(
        Album.id == album_id,
        Album.artist_id == current_user.artist_profile.id
    ).first()
    
    if not album:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found or access denied"
        )
    
    # Generate upload ID
    upload_id = str(uuid.uuid4())
    
    # Create temp directory for this upload
    upload_dir = TEMP_UPLOAD_DIR / upload_id
    upload_dir.mkdir(exist_ok=True)
    
    return UploadResponse(
        upload_id=upload_id,
        status="initialized",
        message="Upload initialized successfully"
    )


@router.post("/tracks/upload-chunk", response_model=UploadResponse)
@limiter.limit("200/minute")
async def upload_chunk(
    chunk_index: int = Form(...),
    total_chunks: int = Form(...),
    upload_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_artist_user)
):
    """Upload a file chunk."""
    
    upload_dir = TEMP_UPLOAD_DIR / upload_id
    
    if not upload_dir.exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Upload session not found"
        )
    
    # Save chunk
    chunk_path = upload_dir / f"chunk_{chunk_index:05d}"
    
    try:
        async with aiofiles.open(chunk_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Send progress update
        progress = ((chunk_index + 1) / total_chunks) * 100
        await manager.send_progress(upload_id, {
            "type": "upload_progress",
            "progress": progress,
            "message": f"Uploaded chunk {chunk_index + 1}/{total_chunks}"
        })
        
        return UploadResponse(
            upload_id=upload_id,
            status="chunk_uploaded",
            message=f"Chunk {chunk_index + 1}/{total_chunks} uploaded",
            progress=progress
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save chunk: {str(e)}"
        )


@router.post("/tracks/upload-complete", response_model=UploadResponse)
@limiter.limit("10/minute")
async def complete_upload(
    upload_id: str = Form(...),
    file_name: str = Form(...),
    expected_checksum: str = Form(...),
    track_metadata: str = Form(...),  # JSON string
    album_id: str = Form(...),
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_artist_user)
):
    """Complete file upload and start processing."""
    
    import json
    
    try:
        # Parse track metadata
        metadata = json.loads(track_metadata)
        track_data = TrackMetadata(**metadata)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid track metadata: {str(e)}"
        )
    
    upload_dir = TEMP_UPLOAD_DIR / upload_id
    
    if not upload_dir.exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Upload session not found"
        )
    
    # Verify album ownership
    album = db.query(Album).filter(
        Album.id == album_id,
        Album.artist_id == current_user.artist_profile.id
    ).first()
    
    if not album:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found or access denied"
        )
    
    # Check if track number already exists
    existing_track = db.query(Track).filter(
        Track.album_id == album.id,
        Track.track_number == track_data.track_number,
        Track.disc_number == track_data.disc_number
    ).first()
    
    if existing_track:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Track {track_data.disc_number}.{track_data.track_number} already exists"
        )
    
    try:
        # Combine chunks
        final_file_path = upload_dir / file_name
        
        await manager.send_progress(upload_id, {
            "type": "processing",
            "progress": 10,
            "message": "Combining file chunks..."
        })
        
        # Combine chunks in order
        chunk_files = sorted(upload_dir.glob("chunk_*"))
        with open(final_file_path, 'wb') as final_file:
            for chunk_file in chunk_files:
                with open(chunk_file, 'rb') as cf:
                    final_file.write(cf.read())
                chunk_file.unlink()  # Delete chunk after combining
        
        # Verify checksum
        actual_checksum = calculate_file_checksum(final_file_path)
        if actual_checksum != expected_checksum:
            raise ValueError("File checksum mismatch")
        
        await manager.send_progress(upload_id, {
            "type": "processing",
            "progress": 30,
            "message": "Validating audio file..."
        })
        
        # Validate and extract audio metadata
        file_info = validate_audio_file(final_file_path)
        
        # Create track record
        track = Track(
            album_id=album.id,
            title=track_data.title,
            track_number=track_data.track_number,
            disc_number=track_data.disc_number,
            duration_seconds=file_info["duration_seconds"],
            bpm=file_info.get("bpm"),
            key=file_info.get("key"),
            isrc=track_data.isrc,
            lyrics=track_data.lyrics,
            credits=track_data.credits,
            featuring_artists=track_data.featuring_artists,
            is_explicit=track_data.is_explicit,
            is_instrumental=track_data.is_instrumental
        )
        
        db.add(track)
        db.commit()
        db.refresh(track)
        
        # Schedule background processing
        background_tasks.add_task(
            process_audio_file,
            track.id,
            final_file_path,
            upload_id,
            db
        )
        
        return UploadResponse(
            upload_id=upload_id,
            status="processing",
            message="File uploaded successfully, processing started",
            progress=50,
            file_info=file_info
        )
        
    except Exception as e:
        # Cleanup on error
        if upload_dir.exists():
            import shutil
            shutil.rmtree(upload_dir)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload processing failed: {str(e)}"
        )


async def process_audio_file(track_id: str, file_path: Path, upload_id: str, db: Session):
    """Background task to process uploaded audio file."""
    
    try:
        # Update progress
        await manager.send_progress(upload_id, {
            "type": "processing",
            "progress": 60,
            "message": "Generating waveform data..."
        })
        
        # Generate waveform
        waveform_data = generate_waveform_data(file_path)
        
        await manager.send_progress(upload_id, {
            "type": "processing",
            "progress": 75,
            "message": "Creating preview..."
        })
        
        # Create preview
        preview_path = file_path.parent / f"preview_{file_path.name}"
        preview_created = create_preview(file_path, preview_path)
        
        await manager.send_progress(upload_id, {
            "type": "processing",
            "progress": 85,
            "message": "Saving audio files..."
        })
        
        # Get track from database
        track = db.query(Track).filter(Track.id == track_id).first()
        if track:
            # Update track with processing results
            track.waveform_data = {"points": waveform_data}
            
            if preview_created:
                # TODO: Upload preview to storage and set preview_url
                track.preview_url = f"/previews/{track.id}.mp3"
            
            # Create audio file records for different qualities
            file_info = validate_audio_file(file_path)
            
            # Original quality
            audio_file = AudioFile(
                track_id=track.id,
                format=AudioFormat(file_info["format"]),
                quality=AudioQuality.HIGH,
                file_path=str(file_path),  # TODO: Upload to storage
                file_size_bytes=file_info["file_size"],
                checksum=calculate_file_checksum(file_path),
                bitrate=file_info["bitrate"],
                sample_rate=file_info["sample_rate"],
                channels=file_info["channels"],
                is_processed=True
            )
            
            db.add(audio_file)
            db.commit()
        
        await manager.send_progress(upload_id, {
            "type": "completed",
            "progress": 100,
            "message": "Processing completed successfully",
            "track_id": track_id,
            "waveform_data": waveform_data
        })
        
        # Cleanup temp files
        import shutil
        shutil.rmtree(file_path.parent)
        
    except Exception as e:
        await manager.send_progress(upload_id, {
            "type": "error",
            "progress": 0,
            "message": f"Processing failed: {str(e)}",
            "error": str(e)
        })


@router.websocket("/upload/progress/{upload_id}")
async def upload_progress_websocket(websocket: WebSocket, upload_id: str):
    """WebSocket endpoint for real-time upload progress."""
    await manager.connect(websocket, upload_id)
    
    try:
        while True:
            # Keep connection alive
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(upload_id)


@router.get("/tracks/{track_id}/processing-status", response_model=ProcessingStatus)
@limiter.limit("60/minute")
async def get_processing_status(
    track_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_artist_user)
):
    """Get track processing status."""
    
    # Get track and verify ownership
    track = db.query(Track).join(Album).filter(
        Track.id == track_id,
        Album.artist_id == current_user.artist_profile.id
    ).first()
    
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not found or access denied"
        )
    
    # Check if audio files exist
    audio_files = db.query(AudioFile).filter(
        AudioFile.track_id == track.id,
        AudioFile.is_processed == True
    ).all()
    
    if audio_files:
        status_info = "completed"
        progress = 100.0
        message = "Processing completed"
        waveform = track.waveform_data.get("points", []) if track.waveform_data else []
    else:
        status_info = "processing"
        progress = 50.0
        message = "Processing in progress"
        waveform = []
    
    return ProcessingStatus(
        track_id=track_id,
        status=status_info,
        progress=progress,
        message=message,
        waveform_data=waveform
    )


@router.delete("/tracks/{track_id}")
@limiter.limit("20/minute")
async def delete_track(
    track_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_artist_user)
):
    """Delete a track and its associated files."""
    
    # Get track and verify ownership
    track = db.query(Track).join(Album).filter(
        Track.id == track_id,
        Album.artist_id == current_user.artist_profile.id
    ).first()
    
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not found or access denied"
        )
    
    # TODO: Delete audio files from storage
    
    # Delete from database (cascades to audio_files)
    db.delete(track)
    db.commit()
    
    return {"message": "Track deleted successfully"}


@router.post("/albums/{album_id}/publish")
@limiter.limit("10/minute")
async def publish_album(
    album_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_artist_user)
):
    """Publish an album to make it available for purchase."""
    
    # Get album and verify ownership
    album = db.query(Album).filter(
        Album.id == album_id,
        Album.artist_id == current_user.artist_profile.id
    ).first()
    
    if not album:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found or access denied"
        )
    
    if album.is_published:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Album is already published"
        )
    
    # Check if album has tracks
    track_count = db.query(Track).filter(Track.album_id == album.id).count()
    if track_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot publish album without tracks"
        )
    
    # Publish album
    album.is_published = True
    db.commit()
    
    return {
        "album_id": album_id,
        "status": "published",
        "message": "Album published successfully"
    }