"""
Database models package.
"""

from app.models.base import Base, BaseModel, SoftDeleteMixin, TimestampMixin
from app.models.commerce import (DistributionPlatform, DistributionQueue,
                                 DistributionStatus, License, LicenseType,
                                 Order, OrderItem, OrderStatus, Payment,
                                 PaymentMethod, PaymentStatus)
from app.models.music import (Album, ArtistProfile, AudioFile, AudioFormat,
                              AudioQuality, Genre, Track)
from app.models.user import User, UserRole, UserSession

__all__ = [
    # Base models
    "Base",
    "BaseModel",
    "TimestampMixin",
    "SoftDeleteMixin",
    # User models
    "User",
    "UserRole",
    "UserSession",
    # Music models
    "ArtistProfile",
    "Album",
    "Track",
    "AudioFile",
    "Genre",
    "AudioFormat",
    "AudioQuality",
    # Commerce models
    "License",
    "Order",
    "OrderItem",
    "Payment",
    "DistributionQueue",
    "LicenseType",
    "OrderStatus",
    "PaymentStatus",
    "PaymentMethod",
    "DistributionStatus",
    "DistributionPlatform",
]
