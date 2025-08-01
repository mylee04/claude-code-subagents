"""
Authentication utilities (placeholder implementation)
In production, this would integrate with your auth system
"""

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .database import get_db
from ..models.database import User


security = HTTPBearer()


# Placeholder User model for development
class MockUser:
    """Mock user for development/testing"""
    def __init__(self, user_id: UUID, username: str):
        self.id = user_id
        self.username = username
        self.total_xp = 0
        self.current_level = 1
        self.created_at = datetime.utcnow()
        self.last_active = datetime.utcnow()
        self.is_active = True
        self.profile_public = True
        self.leaderboard_visible = True
        self.achievements_public = True


# Mock users for development
MOCK_USERS = {
    "dev-user-1": MockUser(UUID("12345678-1234-5678-9012-123456789012"), "developer"),
    "dev-user-2": MockUser(UUID("87654321-4321-8765-2109-876543210987"), "tester"),
}


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user
    This is a placeholder implementation for development
    """
    token = credentials.credentials
    
    # For development, accept any token and return mock user
    if token in MOCK_USERS:
        mock_user = MOCK_USERS[token]
        
        # Check if user exists in database
        result = await db.execute(
            select(User).where(User.id == mock_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # Create user in database
            user = User(
                id=mock_user.id,
                username=mock_user.username,
                total_xp=mock_user.total_xp,
                current_level=mock_user.current_level,
                created_at=mock_user.created_at,
                last_active=mock_user.last_active,
                is_active=mock_user.is_active,
                profile_public=mock_user.profile_public,
                leaderboard_visible=mock_user.leaderboard_visible,
                achievements_public=mock_user.achievements_public
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        
        return user
    
    # For production, you would validate JWT tokens here
    # Example JWT validation:
    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     user_id = payload.get("sub")
    #     if user_id is None:
    #         raise credentials_exception
    # except JWTError:
    #     raise credentials_exception
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user_websocket(token: str, db: AsyncSession) -> User:
    """
    Get current user for WebSocket connections
    Placeholder implementation for development
    """
    if token in MOCK_USERS:
        mock_user = MOCK_USERS[token]
        
        # Check if user exists in database
        result = await db.execute(
            select(User).where(User.id == mock_user.id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            return user
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials"
    )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create JWT access token
    Placeholder implementation
    """
    # In production, you would create a proper JWT token here
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    
    # For development, return a simple token
    return f"mock-token-{data.get('sub', 'unknown')}"


# Development authentication helpers
def get_mock_token(username: str = "developer") -> str:
    """Get mock authentication token for development"""
    for token, user in MOCK_USERS.items():
        if user.username == username:
            return token
    return "dev-user-1"  # Default token


def create_mock_user(username: str, user_id: Optional[UUID] = None) -> str:
    """Create a mock user for development and return token"""
    if user_id is None:
        user_id = uuid4()
    
    token = f"mock-{username}"
    MOCK_USERS[token] = MockUser(user_id, username)
    return token


# Utility functions for production
async def verify_token(token: str) -> dict:
    """
    Verify JWT token and return payload
    Placeholder for production implementation
    """
    # In production:
    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     return payload
    # except JWTError:
    #     raise HTTPException(status_code=401, detail="Invalid token")
    
    # Development mock
    if token in MOCK_USERS:
        user = MOCK_USERS[token]
        return {
            "sub": str(user.id),
            "username": user.username,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
    
    raise HTTPException(status_code=401, detail="Invalid token")


async def get_user_by_id(user_id: UUID, db: AsyncSession) -> Optional[User]:
    """Get user by ID from database"""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


# Permission checking utilities
def check_user_permission(user: User, action: str, resource: Optional[str] = None) -> bool:
    """
    Check if user has permission for action
    Placeholder for role-based access control
    """
    # For development, all authenticated users have all permissions
    return user.is_active


class PermissionChecker:
    """Permission checking dependency"""
    
    def __init__(self, required_permission: str):
        self.required_permission = required_permission
    
    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if not check_user_permission(current_user, self.required_permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions: {self.required_permission}"
            )
        return current_user