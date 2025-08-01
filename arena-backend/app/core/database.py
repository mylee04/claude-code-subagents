"""
Database configuration and session management
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import text

from .config import settings
from ..models.database import Base


# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    future=True,
    # Connection pool settings
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,  # 1 hour
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=True,
    autocommit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to get database session
    Used with FastAPI's Depends()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database tables"""
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        
        # Verify connection
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


async def drop_db() -> None:
    """Drop all database tables (used in testing)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def check_db_connection() -> bool:
    """Check if database connection is working"""
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


# Database utilities
class DatabaseManager:
    """Database management utilities"""
    
    @staticmethod
    async def create_tables():
        """Create all database tables"""
        await init_db()
    
    @staticmethod
    async def reset_database():
        """Reset database (drop and recreate all tables)"""
        await drop_db()
        await init_db()
    
    @staticmethod
    async def get_table_info():
        """Get information about database tables"""
        async with engine.begin() as conn:
            # Get table names
            if "sqlite" in settings.DATABASE_URL:
                result = await conn.execute(text(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ))
            else:
                result = await conn.execute(text(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
                ))
            
            tables = [row[0] for row in result.fetchall()]
            return {"tables": tables, "count": len(tables)}
    
    @staticmethod
    async def get_stats():
        """Get database statistics"""
        async with engine.begin() as conn:
            stats = {}
            
            # Get row counts for main tables
            table_queries = {
                "users": "SELECT COUNT(*) FROM users",
                "agents": "SELECT COUNT(*) FROM agents", 
                "agent_stats": "SELECT COUNT(*) FROM agent_stats",
                "xp_events": "SELECT COUNT(*) FROM xp_events",
                "achievements": "SELECT COUNT(*) FROM achievements",
                "user_achievements": "SELECT COUNT(*) FROM user_achievements"
            }
            
            for table, query in table_queries.items():
                try:
                    result = await conn.execute(text(query))
                    stats[f"{table}_count"] = result.scalar()
                except Exception:
                    stats[f"{table}_count"] = 0
            
            return stats


# Connection pool monitoring
async def get_connection_pool_status():
    """Get connection pool status"""
    pool = engine.pool
    return {
        "size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "invalid": pool.invalid(),
    }