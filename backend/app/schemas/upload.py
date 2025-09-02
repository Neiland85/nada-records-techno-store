"""
Upload-related schemas for file uploads and processing.
"""
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl

from app.models.music import AudioFormat, AudioQuality


class UploadResponse(BaseModel):
    """Response for file upload operations."""
    upload_id: str = Field(..., description="Unique upload identifier")
    file_url: Optional[HttpUrl] = Field(None, description="URL of uploaded file")
    file_size: int = Field(..., description="File size in bytes")
    status: str = Field(..., description="Upload status (uploading, processing, completed, failed)")
    message: str = Field(..., description="Status message")
    progress: float = Field(0.0, ge=0.0, le=100.0, description="Upload progress percentage")
    created_at: datetime = Field(..., description="Upload creation timestamp")


class AudioFileResponse(BaseModel):
    """Response for processed audio files."""
    id: str
    track_id: str
    format: AudioFormat
    quality: AudioQuality
    file_url: HttpUrl
    download_url: HttpUrl
    file_size_bytes: int
    bitrate: int
    sample_rate: int
    duration_seconds: float
    is_preview: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True


class AudioMetadata(BaseModel):
    """Audio file metadata extracted during processing."""
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    track_number: Optional[int] = None
    genre: Optional[str] = None
    year: Optional[int] = None
    duration_seconds: float
    bitrate: int
    sample_rate: int
    channels: int
    format: str
    file_size_bytes: int


class ProcessingOptions(BaseModel):
    """Options for audio processing."""
    generate_preview: bool = True
    preview_duration: int = Field(30, ge=10, le=60, description="Preview duration in seconds")
    preview_start_offset: int = Field(0, ge=0, description="Preview start offset in seconds")
    convert_formats: list[AudioFormat] = Field(default_factory=list, description="Formats to convert to")
    quality_levels: list[AudioQuality] = Field(default_factory=list, description="Quality levels to generate")
    normalize_audio: bool = False
    remove_silence: bool = False


class UploadProgress(BaseModel):
    """Upload progress information."""
    upload_id: str
    status: str = Field(..., description="Current status (uploading, processing, completed, failed)")
    progress: float = Field(..., ge=0.0, le=100.0, description="Progress percentage")
    current_step: str = Field(..., description="Current processing step")
    total_steps: int = Field(..., description="Total number of steps")
    completed_steps: int = Field(..., description="Number of completed steps")
    error_message: Optional[str] = None
    started_at: datetime
    updated_at: datetime
    estimated_completion: Optional[datetime] = None


class BulkUploadRequest(BaseModel):
    """Request for bulk file upload."""
    album_id: str
    processing_options: ProcessingOptions = ProcessingOptions()
    auto_extract_metadata: bool = True
    overwrite_existing: bool = False


class BulkUploadResponse(BaseModel):
    """Response for bulk upload operations."""
    batch_id: str
    total_files: int
    uploads: list[UploadResponse]
    processing_options: ProcessingOptions
    created_at: datetime
