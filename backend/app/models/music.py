"""
Music-related models: Artist, Album, Track, AudioFile.
"""
from enum import Enum
from typing import Optional

from sqlalchemy import (
    Boolean, Column, Date, DateTime, Enum as SQLEnum, Float, ForeignKey,
    Integer, JSON, String, Text, UniqueConstraint, Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, SoftDeleteMixin


class Genre(str, Enum):
    """Music genre enumeration."""
    ELECTRONIC = "electronic"
    HIP_HOP = "hip_hop"
    POP = "pop"
    ROCK = "rock"
    JAZZ = "jazz"
    CLASSICAL = "classical"
    REGGAE = "reggae"
    COUNTRY = "country"
    BLUES = "blues"
    METAL = "metal"
    FOLK = "folk"
    LATIN = "latin"
    RNB = "rnb"
    WORLD = "world"
    OTHER = "other"


class AudioFormat(str, Enum):
    """Audio file format enumeration."""
    MP3 = "mp3"
    WAV = "wav"
    FLAC = "flac"
    AAC = "aac"
    OGG = "ogg"


class AudioQuality(str, Enum):
    """Audio quality preset enumeration."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    PREVIEW = "preview"


class ArtistProfile(BaseModel, SoftDeleteMixin):
    """Artist profile with extended information."""
    
    __tablename__ = "artist_profiles"
    
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )
    
    # Artist information
    stage_name = Column(String(100), unique=True, nullable=False, index=True)
    bio = Column(Text, nullable=True)
    country = Column(String(2), nullable=True)  # ISO country code
    
    # Social media links
    website = Column(String(500), nullable=True)
    spotify_url = Column(String(500), nullable=True)
    apple_music_url = Column(String(500), nullable=True)
    soundcloud_url = Column(String(500), nullable=True)
    instagram_url = Column(String(500), nullable=True)
    twitter_url = Column(String(500), nullable=True)
    facebook_url = Column(String(500), nullable=True)
    youtube_url = Column(String(500), nullable=True)
    
    # Verification and status
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_date = Column(DateTime(timezone=True), nullable=True)
    
    # Analytics
    total_plays = Column(Integer, default=0, nullable=False)
    total_sales = Column(Integer, default=0, nullable=False)
    monthly_listeners = Column(Integer, default=0, nullable=False)
    
    # Payment information
    stripe_account_id = Column(String(255), nullable=True)
    payout_enabled = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="artist_profile")
    albums = relationship(
        "Album",
        back_populates="artist",
        cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_artist_verified", "is_verified"),
        Index("idx_artist_stage_name", "stage_name"),
    )


class Album(BaseModel, SoftDeleteMixin):
    """Album model containing tracks."""
    
    __tablename__ = "albums"
    
    artist_id = Column(
        UUID(as_uuid=True),
        ForeignKey("artist_profiles.id"),
        nullable=False,
        index=True
    )
    
    # Album information
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    release_date = Column(Date, nullable=False, index=True)
    
    # Metadata
    genre = Column(SQLEnum(Genre), nullable=False, index=True)
    subgenre = Column(String(50), nullable=True)
    tags = Column(JSON, default=list, nullable=False)  # List of tags
    
    # Album art
    cover_art_url = Column(String(500), nullable=True)
    cover_art_color = Column(String(7), nullable=True)  # Dominant color hex
    
    # Publishing information
    label = Column(String(100), nullable=True)
    catalog_number = Column(String(50), nullable=True)
    upc = Column(String(12), nullable=True, unique=True)  # Universal Product Code
    
    # Status
    is_published = Column(Boolean, default=False, nullable=False, index=True)
    is_explicit = Column(Boolean, default=False, nullable=False)
    
    # Analytics
    total_plays = Column(Integer, default=0, nullable=False)
    total_sales = Column(Integer, default=0, nullable=False)
    
    # Relationships
    artist = relationship("ArtistProfile", back_populates="albums")
    tracks = relationship(
        "Track",
        back_populates="album",
        cascade="all, delete-orphan",
        order_by="Track.track_number"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_album_artist_published", "artist_id", "is_published"),
        Index("idx_album_release_date", "release_date"),
        Index("idx_album_genre", "genre"),
        UniqueConstraint("artist_id", "title", name="uq_artist_album_title"),
    )


class Track(BaseModel, SoftDeleteMixin):
    """Individual track/song model."""
    
    __tablename__ = "tracks"
    
    album_id = Column(
        UUID(as_uuid=True),
        ForeignKey("albums.id"),
        nullable=False,
        index=True
    )
    
    # Track information
    title = Column(String(200), nullable=False, index=True)
    track_number = Column(Integer, nullable=False)
    disc_number = Column(Integer, default=1, nullable=False)
    
    # Audio metadata
    duration_seconds = Column(Float, nullable=False)  # Track duration
    bpm = Column(Integer, nullable=True)  # Beats per minute
    key = Column(String(10), nullable=True)  # Musical key (e.g., "C major")
    
    # Additional metadata
    isrc = Column(String(12), nullable=True, unique=True)  # International Standard Recording Code
    lyrics = Column(Text, nullable=True)
    credits = Column(JSON, default=dict, nullable=False)  # Producer, writer credits
    
    # Features
    featuring_artists = Column(JSON, default=list, nullable=False)  # List of artist names
    is_explicit = Column(Boolean, default=False, nullable=False)
    is_instrumental = Column(Boolean, default=False, nullable=False)
    
    # Preview
    preview_url = Column(String(500), nullable=True)
    preview_start_time = Column(Float, default=0, nullable=False)
    
    # Waveform data for visualization
    waveform_data = Column(JSON, nullable=True)  # Compressed waveform points
    
    # Analytics
    play_count = Column(Integer, default=0, nullable=False)
    skip_rate = Column(Float, default=0, nullable=False)  # Percentage of skips
    
    # Relationships
    album = relationship("Album", back_populates="tracks")
    audio_files = relationship(
        "AudioFile",
        back_populates="track",
        cascade="all, delete-orphan"
    )
    licenses = relationship(
        "License",
        back_populates="track",
        cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_track_album_number", "album_id", "track_number"),
        Index("idx_track_isrc", "isrc"),
        UniqueConstraint("album_id", "disc_number", "track_number", name="uq_album_disc_track"),
    )


class AudioFile(BaseModel):
    """Audio file storage and metadata."""
    
    __tablename__ = "audio_files"
    
    track_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tracks.id"),
        nullable=False,
        index=True
    )
    
    # File information
    format = Column(SQLEnum(AudioFormat), nullable=False)
    quality = Column(SQLEnum(AudioQuality), nullable=False)
    
    # Storage
    file_path = Column(String(500), nullable=False)  # S3/B2 path
    file_size_bytes = Column(Integer, nullable=False)
    checksum = Column(String(64), nullable=False)  # SHA-256 hash
    
    # Audio properties
    bitrate = Column(Integer, nullable=False)  # in kbps
    sample_rate = Column(Integer, nullable=False)  # in Hz
    channels = Column(Integer, default=2, nullable=False)  # Mono/Stereo
    
    # Processing status
    is_processed = Column(Boolean, default=False, nullable=False)
    processing_error = Column(Text, nullable=True)
    
    # Relationships
    track = relationship("Track", back_populates="audio_files")
    
    # Indexes
    __table_args__ = (
        Index("idx_audio_track_format_quality", "track_id", "format", "quality"),
        UniqueConstraint("track_id", "format", "quality", name="uq_track_format_quality"),
    )
