"""
User model for authentication and authorization.
"""

from enum import Enum
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, SoftDeleteMixin

# Constants to avoid string duplication
CASCADE_ALL_DELETE_ORPHAN = "all, delete-orphan"
PERMISSION_MANAGE_PROFILE = "manage_profile"


class UserRole(str, Enum):
    """User role enumeration."""

    ADMIN = "admin"
    ARTIST = "artist"
    CUSTOMER = "customer"


class User(BaseModel, SoftDeleteMixin):
    """User model with authentication and profile information."""

    __tablename__ = "users"

    # Authentication fields
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    # Profile fields
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    display_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(String(1000), nullable=True)

    # Role and permissions
    role = Column(
        SQLEnum(UserRole),
        default=UserRole.CUSTOMER,
        nullable=False,
        index=True)

    # Account status
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    is_verified = Column(Boolean, default=False, nullable=False, index=True)
    is_superuser = Column(Boolean, default=False, nullable=False)

    # Additional fields
    phone_number = Column(String(20), nullable=True)
    country = Column(String(2), nullable=True)  # ISO country code
    language = Column(
        String(5),
        default="en",
        nullable=False)  # Language preference
    timezone = Column(String(50), default="UTC", nullable=False)

    # OAuth fields (for future social login)
    oauth_provider = Column(String(50), nullable=True)
    oauth_provider_id = Column(String(255), nullable=True)

    # Relationships
    artist_profile = relationship(
        "ArtistProfile",
        back_populates="user",
        uselist=False,
        cascade=CASCADE_ALL_DELETE_ORPHAN,
    )
    orders = relationship(
        "Order", back_populates="user", cascade=CASCADE_ALL_DELETE_ORPHAN
    )
    sessions = relationship(
        "UserSession", back_populates="user", cascade=CASCADE_ALL_DELETE_ORPHAN
    )

    # Indexes
    __table_args__ = (
        Index("idx_user_email_active", "email", "is_active"),
        Index("idx_user_role_active", "role", "is_active"),
        Index("idx_oauth_provider", "oauth_provider", "oauth_provider_id"),
    )

    @property
    def full_name(self) -> str:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.display_name or self.username

    @property
    def is_artist(self) -> bool:
        """Check if user is an artist."""
        return self.role == UserRole.ARTIST

    @property
    def is_admin(self) -> bool:
        """Check if user is an admin."""
        return self.role == UserRole.ADMIN or self.is_superuser

    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission."""
        # Implement permission checking logic
        if self.is_superuser:
            return True

        # Add role-based permission logic here
        permissions_map = {
            UserRole.ADMIN: ["*"],  # All permissions
            UserRole.ARTIST: [
                "upload_music",
                "manage_albums",
                "view_analytics",
                PERMISSION_MANAGE_PROFILE,
            ],
            UserRole.CUSTOMER: [
                "purchase_music",
                "download_purchases",
                PERMISSION_MANAGE_PROFILE,
            ],
        }

        role_permissions = permissions_map.get(self.role, [])
        return "*" in role_permissions or permission in role_permissions


class UserSession(BaseModel):
    """User session tracking for security and analytics."""

    __tablename__ = "user_sessions"

    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    refresh_token = Column(
        String(500),
        unique=True,
        nullable=False,
        index=True)

    # Session information
    ip_address = Column(String(45), nullable=True)  # Support IPv6
    user_agent = Column(String(500), nullable=True)
    device_type = Column(String(50), nullable=True)

    # Token tracking
    access_token_jti = Column(String(255), nullable=True, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    revoked_at = Column(DateTime(timezone=True), nullable=True)

    # Activity tracking
    last_activity = Column(DateTime(timezone=True), nullable=False)

    # Relationships
    user = relationship("User", back_populates="sessions")

    @property
    def is_revoked(self) -> bool:
        """Verifica si la sesión ha sido revocada."""
        return self.revoked_at is not None
