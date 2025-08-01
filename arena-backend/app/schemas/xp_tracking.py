"""
Pydantic V2 schemas for XP tracking system
Type-safe request/response models with advanced validation
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from uuid import UUID

from pydantic import BaseModel, Field, validator, root_validator
from pydantic.types import conint, confloat, constr


# Enums for controlled values
class XPActionType(str, Enum):
    TASK_COMPLETION = "task_completion"
    ERROR_RESOLUTION = "error_resolution"
    SPEED_BONUS = "speed_bonus"
    QUALITY_BONUS = "quality_bonus"
    COMPLEXITY_BONUS = "complexity_bonus"
    STREAK_BONUS = "streak_bonus"
    FIRST_USE = "first_use"
    MILESTONE = "milestone"
    ACHIEVEMENT_UNLOCK = "achievement_unlock"


class TaskComplexity(str, Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"
    EXPERT = "expert"


class PrivacyLevel(str, Enum):
    PUBLIC = "public"
    UNLISTED = "unlisted"
    PRIVATE = "private"


class AchievementRarity(str, Enum):
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class EvidenceType(str, Enum):
    SPEED_IMPROVEMENT = "speed_improvement"
    BUG_RESOLUTION = "bug_resolution"
    CODE_QUALITY = "code_quality"
    USER_SATISFACTION = "user_satisfaction"
    COMPLEXITY_HANDLING = "complexity_handling"
    INNOVATION = "innovation"


# Base schemas
class BaseResponse(BaseModel):
    """Base response model with success indicator"""
    success: bool = True
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PaginationParams(BaseModel):
    """Standard pagination parameters"""
    page: conint(ge=1) = 1
    page_size: conint(ge=1, le=100) = 20
    sort_by: Optional[str] = None
    sort_order: Optional[str] = Field(default="desc", regex="^(asc|desc)$")


# XP Event schemas
class XPMultiplier(BaseModel):
    """XP multiplier configuration"""
    type: str = Field(..., description="Type of multiplier (streak, difficulty, etc.)")
    value: confloat(ge=0.1, le=10.0) = Field(..., description="Multiplier value")
    reason: Optional[str] = None


class XPEventCreate(BaseModel):
    """Request to create an XP event"""
    user_id: UUID
    agent_name: str = Field(..., min_length=1, max_length=100)
    action_type: XPActionType
    
    # Task details
    task_description: Optional[str] = Field(None, max_length=2000)
    task_complexity: Optional[TaskComplexity] = None
    task_duration: Optional[confloat(ge=0)] = None
    success: bool = True
    
    # XP calculation
    base_points: conint(ge=0) = Field(..., description="Base XP points before multipliers")
    multipliers: List[XPMultiplier] = Field(default_factory=list)
    bonus_points: conint(ge=0) = 0
    
    # Quality metrics (0.0 to 1.0)
    response_quality: Optional[confloat(ge=0.0, le=1.0)] = None
    user_satisfaction: Optional[confloat(ge=0.0, le=1.0)] = None
    code_quality: Optional[confloat(ge=0.0, le=1.0)] = None
    
    # Evidence
    evidence_type: Optional[EvidenceType] = None
    evidence_data: Optional[Dict[str, Any]] = None
    
    # Additional metadata
    metadata: Optional[Dict[str, Any]] = None

    @validator('multipliers')
    def validate_multipliers(cls, v):
        if len(v) > 10:  # Reasonable limit
            raise ValueError("Too many multipliers")
        return v


class XPEventResponse(BaseModel):
    """Response after XP event creation"""
    id: UUID
    xp_gained: int
    total_xp: int
    level_before: int
    level_after: int
    level_up: bool
    achievements_unlocked: List[str] = Field(default_factory=list)
    
    class Config:
        from_attributes = True


class XPCalculationResult(BaseModel):
    """Result of XP calculation"""
    base_points: int
    multiplier_total: float
    bonus_points: int
    total_xp: int
    breakdown: Dict[str, Any]


# Agent schemas
class AgentCreate(BaseModel):
    """Create new agent definition"""
    name: constr(min_length=1, max_length=100)
    display_name: constr(min_length=1, max_length=200)
    description: Optional[str] = None
    category: constr(min_length=1, max_length=50)
    specialties: Optional[List[str]] = None


class AgentStats(BaseModel):
    """Agent statistics for a user"""
    agent_id: UUID
    agent_name: str
    level: int
    xp: int
    total_calls: int
    successful_tasks: int
    failed_tasks: int
    success_rate: float
    avg_task_time: float
    last_used: datetime
    
    class Config:
        from_attributes = True


class AgentStatsDetailed(AgentStats):
    """Detailed agent statistics"""
    errors_resolved: int
    fastest_completion: Optional[float]
    response_quality_avg: float
    user_satisfaction_avg: float
    complexity_handled_avg: float
    streak_days: int
    longest_streak: int
    
    class Config:
        from_attributes = True


# User and Profile schemas
class UserProfileResponse(BaseModel):
    """User profile with XP data"""
    id: UUID
    username: str
    total_xp: int
    current_level: int
    
    # Activity
    created_at: datetime
    last_active: datetime
    
    # Privacy settings
    profile_public: bool
    leaderboard_visible: bool
    achievements_public: bool
    
    # Stats summary
    total_agents_used: int
    total_tasks_completed: int
    achievements_count: int
    
    class Config:
        from_attributes = True


class UserStatsResponse(BaseModel):
    """Comprehensive user statistics"""
    profile: UserProfileResponse
    agent_stats: List[AgentStats]
    recent_achievements: List[str]
    level_progress: Dict[str, Any]
    performance_metrics: Dict[str, float]


# Achievement schemas
class AchievementCondition(BaseModel):
    """Achievement unlock condition"""
    type: str = Field(..., description="Condition type (xp_threshold, task_count, etc.)")
    value: Union[int, float, str] = Field(..., description="Target value")
    agent_specific: bool = False
    timeframe: Optional[str] = None  # "daily", "weekly", "monthly", "all_time"


class AchievementCreate(BaseModel):
    """Create new achievement"""
    name: constr(min_length=1, max_length=100)
    display_name: constr(min_length=1, max_length=200)
    description: constr(min_length=1, max_length=1000)
    category: constr(min_length=1, max_length=50)
    rarity: AchievementRarity
    xp_reward: conint(ge=0) = 0
    unlock_conditions: List[AchievementCondition]
    icon: Optional[str] = None
    color: Optional[str] = None


class AchievementResponse(BaseModel):
    """Achievement information"""
    id: UUID
    name: str
    display_name: str
    description: str
    category: str
    rarity: AchievementRarity
    xp_reward: int
    icon: Optional[str]
    color: Optional[str]
    unlocked_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Leaderboard schemas
class LeaderboardEntry(BaseModel):
    """Single leaderboard entry"""
    rank: int
    user_id: UUID
    username: str
    total_xp: int
    level: int
    agent_count: int
    achievements_count: int
    badge: Optional[str] = None


class LeaderboardResponse(BaseModel):
    """Leaderboard with pagination"""
    entries: List[LeaderboardEntry]
    total_users: int
    current_page: int
    total_pages: int
    user_rank: Optional[int] = None  # Current user's rank if authenticated


class AgentLeaderboardEntry(BaseModel):
    """Agent-specific leaderboard entry"""
    rank: int
    user_id: UUID
    username: str
    agent_name: str
    level: int
    xp: int
    success_rate: float
    avg_task_time: float


# WebSocket schemas
class WebSocketMessage(BaseModel):
    """Base WebSocket message"""
    type: str
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class XPNotification(BaseModel):
    """Real-time XP notification"""
    user_id: UUID
    agent_name: str
    xp_gained: int
    total_xp: int
    level_up: bool
    new_level: Optional[int] = None
    achievements: List[str] = Field(default_factory=list)
    
    def to_websocket_message(self) -> WebSocketMessage:
        return WebSocketMessage(
            type="xp_update",
            data=self.dict()
        )


class LeaderboardUpdate(BaseModel):
    """Real-time leaderboard update"""
    category: str
    top_entries: List[LeaderboardEntry]
    updated_users: List[UUID] = Field(default_factory=list)
    
    def to_websocket_message(self) -> WebSocketMessage:
        return WebSocketMessage(
            type="leaderboard_update",
            data=self.dict()
        )


# Conversation sharing schemas
class ConversationShareCreate(BaseModel):
    """Create shared conversation"""
    title: constr(min_length=1, max_length=200)
    content: constr(min_length=1)
    summary: Optional[str] = None
    agents_used: List[str] = Field(..., min_items=1)
    xp_earned: conint(ge=0) = 0
    difficulty_level: Optional[TaskComplexity] = None
    privacy_level: PrivacyLevel = PrivacyLevel.PUBLIC
    tags: Optional[List[str]] = None
    category: Optional[str] = None


class ConversationShareResponse(BaseModel):
    """Shared conversation response"""
    id: UUID
    title: str
    content: str
    summary: Optional[str]
    agents_used: List[str]
    xp_earned: int
    difficulty_level: Optional[str]
    privacy_level: str
    tags: Optional[List[str]]
    category: Optional[str]
    views: int
    likes: int
    shares: int
    created_at: datetime
    author: str
    
    class Config:
        from_attributes = True


# Bulk operations
class BulkXPEventCreate(BaseModel):
    """Create multiple XP events in batch"""
    events: List[XPEventCreate] = Field(..., min_items=1, max_items=100)


class BulkXPEventResponse(BaseModel):
    """Bulk XP event creation response"""
    created_count: int
    failed_count: int
    results: List[XPEventResponse]
    errors: List[str] = Field(default_factory=list)


# Analytics schemas
class XPTrendData(BaseModel):
    """XP trend analytics"""
    period: str  # "daily", "weekly", "monthly"
    data_points: List[Dict[str, Any]]
    total_xp: int
    growth_rate: float


class AgentUsageAnalytics(BaseModel):
    """Agent usage analytics"""
    agent_name: str
    total_uses: int
    unique_users: int
    avg_session_duration: float
    success_rate: float
    xp_generated: int
    trend_data: List[Dict[str, Any]]


class SystemMetricsResponse(BaseModel):
    """System-wide metrics"""
    total_users: int
    active_users_24h: int
    total_xp_earned: int
    total_tasks_completed: int
    avg_response_time: float
    top_agents: List[str]
    achievement_unlock_rate: float