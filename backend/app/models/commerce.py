"""
Commerce and transaction models: License, Order, Payment, Distribution.
"""
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    Boolean, Column, DateTime, Enum as SQLEnum, Float, ForeignKey,
    Integer, JSON, Numeric, String, Text, UniqueConstraint, Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class LicenseType(str, Enum):
    """License type enumeration."""
    PERSONAL = "personal"  # Personal use only
    COMMERCIAL = "commercial"  # Commercial use allowed
    EXCLUSIVE = "exclusive"  # Exclusive rights


class OrderStatus(str, Enum):
    """Order status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"


class PaymentStatus(str, Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"
    REFUNDED = "refunded"


class PaymentMethod(str, Enum):
    """Payment method enumeration."""
    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"
    CRYPTO = "crypto"


class DistributionStatus(str, Enum):
    """Distribution status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    LIVE = "live"
    TAKEDOWN_REQUESTED = "takedown_requested"
    REMOVED = "removed"


class DistributionPlatform(str, Enum):
    """Distribution platform enumeration."""
    SPOTIFY = "spotify"
    APPLE_MUSIC = "apple_music"
    YOUTUBE_MUSIC = "youtube_music"
    SOUNDCLOUD = "soundcloud"
    TIDAL = "tidal"
    DEEZER = "deezer"
    AMAZON_MUSIC = "amazon_music"


class License(BaseModel):
    """License types and pricing for tracks."""
    
    __tablename__ = "licenses"
    
    track_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tracks.id"),
        nullable=False,
        index=True
    )
    
    # License details
    type = Column(SQLEnum(LicenseType), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Pricing
    price = Column(Numeric(10, 2), nullable=False)  # Price in USD
    currency = Column(String(3), default="USD", nullable=False)
    
    # Terms
    usage_terms = Column(JSON, default=dict, nullable=False)
    max_streams = Column(Integer, nullable=True)  # None = unlimited
    max_downloads = Column(Integer, nullable=True)  # None = unlimited
    territory_restrictions = Column(JSON, default=list, nullable=False)  # List of country codes
    
    # Availability
    is_available = Column(Boolean, default=True, nullable=False)
    available_quantity = Column(Integer, nullable=True)  # None = unlimited
    sold_quantity = Column(Integer, default=0, nullable=False)
    
    # Relationships
    track = relationship("Track", back_populates="licenses")
    order_items = relationship("OrderItem", back_populates="license")
    
    # Indexes
    __table_args__ = (
        Index("idx_license_track_type", "track_id", "type"),
        Index("idx_license_available", "is_available"),
        UniqueConstraint("track_id", "type", name="uq_track_license_type"),
    )


class Order(BaseModel):
    """Customer order for music purchases."""
    
    __tablename__ = "orders"
    
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    # Order information
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(
        SQLEnum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False,
        index=True
    )
    
    # Pricing
    subtotal = Column(Numeric(10, 2), nullable=False)
    tax_amount = Column(Numeric(10, 2), default=0, nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    
    # Customer information
    customer_email = Column(String(255), nullable=False)
    customer_name = Column(String(200), nullable=True)
    billing_address = Column(JSON, nullable=True)
    
    # Additional information
    notes = Column(Text, nullable=True)
    metadata = Column(JSON, default=dict, nullable=False)
    
    # Timestamps
    completed_at = Column(DateTime(timezone=True), nullable=True)
    refunded_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
    payment = relationship(
        "Payment",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_order_user_status", "user_id", "status"),
        Index("idx_order_created", "created_at"),
    )


class OrderItem(BaseModel):
    """Individual items within an order."""
    
    __tablename__ = "order_items"
    
    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("orders.id"),
        nullable=False,
        index=True
    )
    license_id = Column(
        UUID(as_uuid=True),
        ForeignKey("licenses.id"),
        nullable=False,
        index=True
    )
    
    # Item details
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    
    # Download tracking
    download_count = Column(Integer, default=0, nullable=False)
    download_expiry = Column(DateTime(timezone=True), nullable=True)
    download_url = Column(String(500), nullable=True)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    license = relationship("License", back_populates="order_items")
    
    # Indexes
    __table_args__ = (
        Index("idx_order_item_order", "order_id"),
        UniqueConstraint("order_id", "license_id", name="uq_order_license"),
    )


class Payment(BaseModel):
    """Payment information for orders."""
    
    __tablename__ = "payments"
    
    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("orders.id"),
        unique=True,
        nullable=False
    )
    
    # Payment details
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    status = Column(
        SQLEnum(PaymentStatus),
        default=PaymentStatus.PENDING,
        nullable=False,
        index=True
    )
    method = Column(SQLEnum(PaymentMethod), nullable=False)
    
    # Stripe integration
    stripe_payment_intent_id = Column(String(255), unique=True, nullable=True)
    stripe_charge_id = Column(String(255), unique=True, nullable=True)
    stripe_refund_id = Column(String(255), nullable=True)
    stripe_customer_id = Column(String(255), nullable=True)
    
    # Transaction details
    transaction_id = Column(String(255), unique=True, nullable=True)
    gateway_response = Column(JSON, nullable=True)
    
    # Card information (last 4 digits only)
    card_last4 = Column(String(4), nullable=True)
    card_brand = Column(String(50), nullable=True)
    
    # Refund information
    refund_amount = Column(Numeric(10, 2), default=0, nullable=False)
    refund_reason = Column(Text, nullable=True)
    refunded_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    processed_at = Column(DateTime(timezone=True), nullable=True)
    failed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    order = relationship("Order", back_populates="payment")
    
    # Indexes
    __table_args__ = (
        Index("idx_payment_status", "status"),
        Index("idx_payment_stripe_intent", "stripe_payment_intent_id"),
    )


class DistributionQueue(BaseModel):
    """Queue for distributing music to external platforms."""
    
    __tablename__ = "distribution_queue"
    
    album_id = Column(
        UUID(as_uuid=True),
        ForeignKey("albums.id"),
        nullable=False,
        index=True
    )
    platform = Column(SQLEnum(DistributionPlatform), nullable=False)
    
    # Status tracking
    status = Column(
        SQLEnum(DistributionStatus),
        default=DistributionStatus.PENDING,
        nullable=False,
        index=True
    )
    
    # Submission details
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    rejected_at = Column(DateTime(timezone=True), nullable=True)
    live_at = Column(DateTime(timezone=True), nullable=True)
    
    # Platform-specific data
    platform_album_id = Column(String(255), nullable=True)
    platform_url = Column(String(500), nullable=True)
    submission_response = Column(JSON, nullable=True)
    
    # Error tracking
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    next_retry_at = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    metadata = Column(JSON, default=dict, nullable=False)
    
    # Relationships
    album = relationship("Album")
    
    # Indexes
    __table_args__ = (
        Index("idx_distribution_album_platform", "album_id", "platform"),
        Index("idx_distribution_status", "status"),
        Index("idx_distribution_retry", "status", "next_retry_at"),
        UniqueConstraint("album_id", "platform", name="uq_album_platform"),
    )