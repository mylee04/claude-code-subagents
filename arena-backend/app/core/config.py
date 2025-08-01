"""
Configuration settings for Claude Arena Backend
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Claude Arena - Agent XP Tracking"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database Settings
    DATABASE_URL: str = "sqlite+aiosqlite:///./arena.db"  # Default to SQLite for development
    DATABASE_ECHO: bool = False
    
    # Authentication (placeholder for future implementation)
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # WebSocket Settings
    WS_HEARTBEAT_INTERVAL: int = 30  # seconds
    WS_MAX_CONNECTIONS_PER_USER: int = 5
    
    # XP Calculation Settings
    XP_BASE_MULTIPLIER: float = 1.0
    XP_QUALITY_WEIGHT: float = 0.3
    XP_SPEED_WEIGHT: float = 0.2
    XP_COMPLEXITY_WEIGHT: float = 0.5
    
    # Achievement Settings
    ACHIEVEMENT_XP_BONUS: float = 1.5  # Bonus multiplier for achievement XP
    
    # Performance Settings
    CACHE_TTL: int = 300  # 5 minutes
    MAX_QUERY_LIMIT: int = 1000
    DEFAULT_PAGE_SIZE: int = 20
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Rate Limiting (placeholder for future implementation)
    RATE_LIMIT_PER_MINUTE: int = 100
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v):
        # Support environment variable override
        return os.getenv("DATABASE_URL", v)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Environment-specific configurations
class DevelopmentSettings(Settings):
    """Development environment settings"""
    DEBUG: bool = True
    DATABASE_ECHO: bool = True
    LOG_LEVEL: str = "DEBUG"


class ProductionSettings(Settings):
    """Production environment settings"""
    DEBUG: bool = False
    DATABASE_ECHO: bool = False
    LOG_LEVEL: str = "WARNING"
    
    # Override with secure defaults
    ALLOWED_ORIGINS: List[str] = []  # Must be explicitly set in production
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if v == "your-secret-key-change-in-production":
            raise ValueError("Secret key must be changed in production")
        return v


class TestSettings(Settings):
    """Test environment settings"""
    DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"


# Environment-based configuration
def get_settings() -> Settings:
    """Get settings based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionSettings()
    elif env == "test":
        return TestSettings()
    else:
        return DevelopmentSettings()


# Use environment-specific settings
settings = get_settings()