#!/usr/bin/env python3
"""
Claude Arena Backend Server Launcher
Starts the FastAPI server with proper configuration
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import uvicorn
from app.core.config import settings


def main():
    """Main server launcher"""
    print("🎮 Starting Claude Arena Backend Server...")
    print(f"📍 Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"🔧 Debug Mode: {settings.DEBUG}")
    print(f"🗄️  Database: {settings.DATABASE_URL}")
    print("=" * 50)
    
    # Server configuration
    config = {
        "app": "app.main:app",
        "host": "0.0.0.0",
        "port": int(os.getenv("PORT", 8000)),
        "reload": settings.DEBUG,
        "log_level": settings.LOG_LEVEL.lower(),
        "access_log": True,
        "use_colors": True,
    }
    
    # Add SSL for production
    if not settings.DEBUG and os.getenv("SSL_KEYFILE") and os.getenv("SSL_CERTFILE"):
        config.update({
            "ssl_keyfile": os.getenv("SSL_KEYFILE"),
            "ssl_certfile": os.getenv("SSL_CERTFILE"),
        })
    
    # Start server
    try:
        uvicorn.run(**config)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()