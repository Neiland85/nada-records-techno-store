"""
User and artist profile schemas.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, HttpUrl


class UserBase(BaseModel):
    """Base user fields."""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=8)
    terms_accepted: bool = Field(True)


class UserUpdate(BaseModel):
    """User update schema."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    bio: Optional[str] = Field(None, max_length=500)


class UserResponse(UserBase):
    """User response schema."""
    id: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    artist_profile: Optional["ArtistProfileResponse"] = None
    
    class Config:
        from_attributes = True


# Artist Profile Schemas
class ArtistProfileBase(BaseModel):
    """Base artist profile fields."""
    stage_name: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=2000)
    country: Optional[str] = Field(None, max_length=2, description="ISO country code")
    
    # Social media links
    website: Optional[HttpUrl] = None
    spotify_url: Optional[HttpUrl] = None
    apple_music_url: Optional[HttpUrl] = None
    soundcloud_url: Optional[HttpUrl] = None
    instagram_url: Optional[HttpUrl] = None
    twitter_url: Optional[HttpUrl] = None
    facebook_url: Optional[HttpUrl] = None
    youtube_url: Optional[HttpUrl] = None


class ArtistProfileCreate(ArtistProfileBase):
    """Artist profile creation schema."""
    pass


class ArtistProfileUpdate(BaseModel):
    """Artist profile update schema."""
    stage_name: Optional[str] = Field(None, min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=2000)
    country: Optional[str] = Field(None, max_length=2)
    
    # Social media links
    website: Optional[HttpUrl] = None
    spotify_url: Optional[HttpUrl] = None
    apple_music_url: Optional[HttpUrl] = None
    soundcloud_url: Optional[HttpUrl] = None
    instagram_url: Optional[HttpUrl] = None
    twitter_url: Optional[HttpUrl] = None
    facebook_url: Optional[HttpUrl] = None
    youtube_url: Optional[HttpUrl] = None


class ArtistProfileResponse(ArtistProfileBase):
    """Artist profile response schema."""
    id: str
    user_id: str
    is_verified: bool
    verification_date: Optional[datetime] = None
    total_plays: int
    total_sales: int
    monthly_listeners: int
    payout_enabled: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Forward reference resolution
UserResponse.model_rebuild()
