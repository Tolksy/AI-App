"""
Database configuration and initialization
"""

import asyncio
import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings, DATABASE_CONFIG

logger = logging.getLogger(__name__)

# Database engines
engine = None
async_engine = None
SessionLocal = None

async def init_db():
    """Initialize database connection"""
    try:
        global engine, async_engine, SessionLocal
        
        # Create SQLite engine
        engine = create_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False}
        )
        
        # Create async engine for SQLite
        async_engine = create_async_engine(
            f"sqlite+aiosqlite:///./ai_system.db",
            echo=settings.DEBUG,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False}
        )
        
        # Create session factory
        SessionLocal = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        logger.info("✅ Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def get_db():
    """Get database session"""
    return SessionLocal()

async def get_vector_store():
    """Get vector store instance"""
    # This would return the configured vector store
    return None

async def get_conversation_memory():
    """Get conversation memory instance"""
    # This would return the conversation memory
    return None

