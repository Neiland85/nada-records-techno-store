#!/usr/bin/env python3
"""
Database initialization script for Nada Records Techno Store.

This script creates all tables, indexes, and seeds initial data required
for the application to function properly.
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, List

# Add the parent directory to the path so we can import app modules
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.base import Base
from app.models.user import User, UserRole
from app.models.music import Genre, AudioFormat, LicenseType, Track, Album
from app.models.commerce import Order, OrderStatus, PaymentMethod

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseInitializer:
    """Handles database initialization and seeding."""
    
    def __init__(self):
        """Initialize the database initializer with async engine."""
        self.async_engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DB_ECHO_LOG,
            future=True
        )
        self.async_session = sessionmaker(
            self.async_engine, 
            class_=AsyncSession, 
            expire_on_commit=False
        )
    
    async def create_tables(self) -> bool:
        """Create all database tables."""
        try:
            logger.info("Creating database tables...")
            async with self.async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ Database tables created successfully")
            return True
        except SQLAlchemyError as e:
            logger.error(f"❌ Error creating tables: {e}")
            return False
    
    async def create_indexes(self) -> bool:
        """Create additional indexes for performance."""
        try:
            logger.info("Creating database indexes...")
            async with self.async_engine.begin() as conn:
                # Full-text search indexes
                await conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_tracks_search 
                    ON tracks USING gin(to_tsvector('english', title || ' ' || COALESCE(description, '')))
                """))
                
                await conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_albums_search 
                    ON albums USING gin(to_tsvector('english', title || ' ' || COALESCE(description, '')))
                """))
                
                # Performance indexes
                await conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_tracks_genre_id ON tracks(genre_id)
                """))
                
                await conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_tracks_bpm ON tracks(bpm)
                """))
                
                await conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_tracks_key ON tracks(musical_key)
                """))
                
                await conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id)
                """))
                
                await conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)
                """))
                
            logger.info("✅ Database indexes created successfully")
            return True
        except SQLAlchemyError as e:
            logger.error(f"❌ Error creating indexes: {e}")
            return False
    
    async def seed_genres(self, session: AsyncSession) -> bool:
        """Seed initial music genres."""
        try:
            logger.info("Seeding music genres...")
            genres_data = [
                {"name": "Techno", "description": "Electronic dance music with repetitive beats"},
                {"name": "House", "description": "Four-on-the-floor electronic dance music"},
                {"name": "Trance", "description": "Electronic music with hypnotic rhythms"},
                {"name": "Progressive House", "description": "Longer progressive house tracks"},
                {"name": "Minimal Techno", "description": "Stripped-down techno style"},
                {"name": "Deep House", "description": "Deeper, more soulful house music"},
                {"name": "Tech House", "description": "Fusion of techno and house"},
                {"name": "Ambient", "description": "Atmospheric electronic music"},
                {"name": "Drum & Bass", "description": "Fast electronic music with breakbeats"},
                {"name": "Dubstep", "description": "Electronic music with syncopated rhythms"},
            ]
            
            for genre_data in genres_data:
                genre = Genre(**genre_data)
                session.add(genre)
            
            await session.commit()
            logger.info(f"✅ Seeded {len(genres_data)} genres")
            return True
        except SQLAlchemyError as e:
            logger.error(f"❌ Error seeding genres: {e}")
            await session.rollback()
            return False
    
    async def seed_audio_formats(self, session: AsyncSession) -> bool:
        """Seed supported audio formats."""
        try:
            logger.info("Seeding audio formats...")
            formats_data = [
                {
                    "name": "MP3", 
                    "extension": "mp3", 
                    "mime_type": "audio/mpeg",
                    "quality": "lossy",
                    "max_bitrate": 320
                },
                {
                    "name": "WAV", 
                    "extension": "wav", 
                    "mime_type": "audio/wav",
                    "quality": "lossless",
                    "max_bitrate": 1411
                },
                {
                    "name": "FLAC", 
                    "extension": "flac", 
                    "mime_type": "audio/flac",
                    "quality": "lossless",
                    "max_bitrate": 1411
                },
                {
                    "name": "AAC", 
                    "extension": "m4a", 
                    "mime_type": "audio/aac",
                    "quality": "lossy",
                    "max_bitrate": 320
                },
            ]
            
            for format_data in formats_data:
                audio_format = AudioFormat(**format_data)
                session.add(audio_format)
            
            await session.commit()
            logger.info(f"✅ Seeded {len(formats_data)} audio formats")
            return True
        except SQLAlchemyError as e:
            logger.error(f"❌ Error seeding audio formats: {e}")
            await session.rollback()
            return False
    
    async def seed_license_types(self, session: AsyncSession) -> bool:
        """Seed license types for tracks."""
        try:
            logger.info("Seeding license types...")
            licenses_data = [
                {
                    "name": "Standard License",
                    "description": "Standard commercial use license",
                    "commercial_use": True,
                    "modification_allowed": False,
                    "distribution_allowed": True,
                    "price_multiplier": 1.0
                },
                {
                    "name": "Extended License",
                    "description": "Extended commercial use with modifications",
                    "commercial_use": True,
                    "modification_allowed": True,
                    "distribution_allowed": True,
                    "price_multiplier": 2.5
                },
                {
                    "name": "Exclusive License",
                    "description": "Exclusive rights to the track",
                    "commercial_use": True,
                    "modification_allowed": True,
                    "distribution_allowed": True,
                    "price_multiplier": 10.0
                },
                {
                    "name": "Personal License",
                    "description": "Personal use only, no commercial rights",
                    "commercial_use": False,
                    "modification_allowed": False,
                    "distribution_allowed": False,
                    "price_multiplier": 0.5
                },
            ]
            
            for license_data in licenses_data:
                license_type = LicenseType(**license_data)
                session.add(license_type)
            
            await session.commit()
            logger.info(f"✅ Seeded {len(licenses_data)} license types")
            return True
        except SQLAlchemyError as e:
            logger.error(f"❌ Error seeding license types: {e}")
            await session.rollback()
            return False
    
    async def create_admin_user(self, session: AsyncSession) -> bool:
        """Create the initial admin user."""
        try:
            logger.info("Creating admin user...")
            
            # Check if admin user already exists
            admin_user = await session.get(User, {"email": "admin@nadarecords.com"})
            if admin_user:
                logger.info("ℹ️  Admin user already exists")
                return True
            
            admin_data = {
                "email": "admin@nadarecords.com",
                "username": "admin",
                "full_name": "Admin User",
                "role": UserRole.ADMIN,
                "is_active": True,
                "is_verified": True,
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # password: admin123
            }
            
            admin_user = User(**admin_data)
            session.add(admin_user)
            await session.commit()
            
            logger.info("✅ Admin user created successfully")
            logger.info("📧 Email: admin@nadarecords.com")
            logger.info("🔑 Password: admin123")
            return True
        except SQLAlchemyError as e:
            logger.error(f"❌ Error creating admin user: {e}")
            await session.rollback()
            return False
    
    async def initialize_database(self) -> bool:
        """Run complete database initialization."""
        try:
            logger.info("🚀 Starting database initialization...")
            
            # Create tables
            if not await self.create_tables():
                return False
            
            # Create indexes
            if not await self.create_indexes():
                return False
            
            # Seed data
            async with self.async_session() as session:
                if not await self.seed_genres(session):
                    return False
                
                if not await self.seed_audio_formats(session):
                    return False
                
                if not await self.seed_license_types(session):
                    return False
                
                if not await self.create_admin_user(session):
                    return False
            
            logger.info("🎉 Database initialization completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            return False
        finally:
            await self.async_engine.dispose()


async def main():
    """Main entry point for database initialization."""
    try:
        logger.info("🎵 Nada Records Techno Store - Database Initialization")
        logger.info("=" * 60)
        
        # Initialize database
        db_initializer = DatabaseInitializer()
        success = await db_initializer.initialize_database()
        
        if success:
            logger.info("✅ Database ready for development!")
            logger.info("🌐 You can now start the application")
            sys.exit(0)
        else:
            logger.error("❌ Database initialization failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("\n⚠️  Database initialization interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
