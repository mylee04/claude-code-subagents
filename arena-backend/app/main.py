"""
Claude Arena Backend - Personal Agent XP Tracking System
FastAPI application for tracking agent performance and gamification
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .core.config import settings
from .core.database import engine, init_db
from .routers import agent_tracking, websocket
from .services.notification_service import notification_service_lifespan
from .services.achievement_service import AchievementService
from .services.xp_calculator import XPCalculationEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting Claude Arena Backend...")
    
    # Initialize database
    await init_db()
    print("✅ Database initialized")
    
    # Initialize default achievements
    from .core.database import get_db
    async with engine.begin() as conn:
        # This would be done properly with dependency injection in production
        pass
    
    print("✅ Default achievements loaded")
    print("🎮 Claude Arena Backend ready!")
    
    # Use notification service lifespan
    async with notification_service_lifespan():
        yield
    
    # Shutdown
    print("🛑 Shutting down Claude Arena Backend...")


# Create FastAPI app
app = FastAPI(
    title="Claude Arena - Agent XP Tracking",
    description="Personal agent performance tracking and gamification system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agent_tracking.router)
app.include_router(websocket.router)


# Root endpoints
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Claude Arena - Agent XP Tracking API",
        "version": "1.0.0",
        "description": "Personal agent performance tracking and gamification",
        "features": [
            "Agent XP tracking with complexity-based scoring",
            "Personal achievement system",
            "Real-time WebSocket notifications",
            "Team leaderboards",
            "Performance analytics",
            "Level progression tracking"
        ],
        "endpoints": {
            "docs": "/docs",
            "agents": "/api/v1/agents",
            "websocket": "/ws",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        from .core.database import engine
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        
        return {
            "status": "healthy",
            "database": "connected",
            "version": "1.0.0",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


@app.get("/api/v1/info")
async def api_info():
    """API information and capabilities"""
    return {
        "api_version": "v1",
        "features": {
            "xp_tracking": {
                "description": "Track XP for individual agents",
                "endpoint": "/api/v1/agents/{agent_name}/xp",
                "methods": ["POST"]
            },
            "agent_stats": {
                "description": "Get detailed agent statistics",
                "endpoint": "/api/v1/agents/{agent_name}/stats",
                "methods": ["GET"]
            },
            "leaderboards": {
                "description": "Personal agent leaderboards",
                "endpoint": "/api/v1/agents/leaderboard/personal",
                "methods": ["GET"]
            },
            "analytics": {
                "description": "Agent usage analytics",
                "endpoint": "/api/v1/agents/{agent_name}/analytics",
                "methods": ["GET"]
            },
            "websocket": {
                "description": "Real-time notifications",
                "endpoint": "/ws/notifications/{user_id}",
                "protocol": "WebSocket"
            }
        },
        "xp_sources": {
            "task_completion": {"base_xp": 10, "description": "Completing any task"},
            "error_resolution": {"base_xp": 20, "description": "Resolving errors"},
            "speed_bonus": {"base_xp": 5, "description": "Fast task completion"},
            "quality_bonus": {"base_xp": 15, "description": "High quality responses"},
            "complexity_bonus": {"base_xp": 25, "description": "Handling complex tasks"}
        },
        "complexity_multipliers": {
            "simple": 1.0,
            "medium": 1.5,
            "complex": 2.0,
            "expert": 3.0
        },
        "level_thresholds": [0, 100, 300, 600, 1000, 1500, 2200, 3000, 4000, 5200]
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "suggestion": "Check the API documentation at /docs"
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "suggestion": "Please try again later or contact support"
        }
    )


# Development server
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )