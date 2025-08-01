"""
Database models for Claude Arena XP Tracking System
Using SQLAlchemy 2.0 with async support for high-performance operations
"""

from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4

from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, JSON, 
    ForeignKey, Index, UniqueConstraint, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """User profile with gamification data"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True)
    
    # XP and Level tracking
    total_xp = Column(Integer, default=0, index=True)
    current_level = Column(Integer, default=1, index=True)
    
    # Activity tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Privacy settings
    profile_public = Column(Boolean, default=True)
    leaderboard_visible = Column(Boolean, default=True)
    achievements_public = Column(Boolean, default=True)
    
    # Relationships
    agent_stats = relationship("AgentStats", back_populates="user", cascade="all, delete-orphan")
    xp_events = relationship("XPEvent", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("ConversationShare", back_populates="user", cascade="all, delete-orphan")


class Agent(Base):
    """Agent definitions with metadata"""
    __tablename__ = "agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), unique=True, nullable=False, index=True)
    display_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Agent classification
    category = Column(String(50), nullable=False, index=True)  # development, data, infrastructure, etc.
    specialties = Column(JSON, nullable=True)  # List of specialty areas
    
    # Performance metrics
    avg_response_time = Column(Float, default=0.0)
    success_rate = Column(Float, default=0.0)
    total_uses = Column(Integer, default=0)
    
    # Configuration
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    stats = relationship("AgentStats", back_populates="agent", cascade="all, delete-orphan")
    xp_events = relationship("XPEvent", back_populates="agent", cascade="all, delete-orphan")


class AgentStats(Base):
    """Per-user agent statistics and XP tracking"""
    __tablename__ = "agent_stats"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    
    # XP and Level
    xp = Column(Integer, default=0, index=True)
    level = Column(Integer, default=1, index=True)
    
    # Usage statistics
    total_calls = Column(Integer, default=0)
    successful_tasks = Column(Integer, default=0)
    failed_tasks = Column(Integer, default=0)
    errors_resolved = Column(Integer, default=0)
    
    # Performance metrics
    avg_task_time = Column(Float, default=0.0)
    fastest_completion = Column(Float, nullable=True)
    total_task_time = Column(Float, default=0.0)
    
    # Quality metrics
    response_quality_avg = Column(Float, default=0.0)
    user_satisfaction_avg = Column(Float, default=0.0)
    complexity_handled_avg = Column(Float, default=0.0)
    
    # Activity tracking
    first_used = Column(DateTime(timezone=True), server_default=func.now())
    last_used = Column(DateTime(timezone=True), server_default=func.now())
    streak_days = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="agent_stats")
    agent = relationship("Agent", back_populates="stats")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'agent_id'),
        Index('idx_agent_stats_user_xp', 'user_id', 'xp'),
        Index('idx_agent_stats_agent_level', 'agent_id', 'level'),
    )


class XPEvent(Base):
    """Individual XP earning events with detailed tracking"""
    __tablename__ = "xp_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    
    # XP Details
    action_type = Column(String(50), nullable=False, index=True)  # task_completion, error_resolution, etc.
    base_points = Column(Integer, nullable=False)
    multiplier = Column(Float, default=1.0)
    bonus_points = Column(Integer, default=0)
    total_xp = Column(Integer, nullable=False, index=True)
    
    # Task context
    task_description = Column(Text, nullable=True)
    task_complexity = Column(String(20), nullable=True, index=True)  # simple, medium, complex, expert
    task_duration = Column(Float, nullable=True)  # seconds
    success = Column(Boolean, nullable=False, index=True)
    
    # Quality metrics (0.0 to 1.0)
    response_quality = Column(Float, nullable=True)
    user_satisfaction = Column(Float, nullable=True)
    code_quality = Column(Float, nullable=True)
    
    # Metadata
    metadata = Column(JSON, nullable=True)  # Additional context
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Evidence tracking
    evidence_type = Column(String(50), nullable=True)  # speed_improvement, bug_resolution, etc.
    evidence_data = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="xp_events")
    agent = relationship("Agent", back_populates="xp_events")
    
    # Indexes
    __table_args__ = (
        Index('idx_xp_events_user_time', 'user_id', 'timestamp'),
        Index('idx_xp_events_agent_time', 'agent_id', 'timestamp'),
        Index('idx_xp_events_action_success', 'action_type', 'success'),
    )


class Achievement(Base):
    """Achievement definitions"""
    __tablename__ = "achievements"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    
    # Achievement properties
    category = Column(String(50), nullable=False, index=True)  # usage, performance, mastery, etc.
    rarity = Column(String(20), nullable=False, index=True)  # common, rare, epic, legendary
    xp_reward = Column(Integer, default=0)
    
    # Unlock conditions (JSON schema)
    unlock_conditions = Column(JSON, nullable=False)
    
    # Display properties
    icon = Column(String(100), nullable=True)
    color = Column(String(20), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user_achievements = relationship("UserAchievement", back_populates="achievement")


class UserAchievement(Base):
    """User-specific achievement unlocks"""
    __tablename__ = "user_achievements"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    achievement_id = Column(UUID(as_uuid=True), ForeignKey("achievements.id"), nullable=False)
    
    # Achievement context
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=True)  # If agent-specific
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Achievement progress tracking
    progress_data = Column(JSON, nullable=True)  # Context of unlock
    xp_earned = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'achievement_id'),
        Index('idx_user_achievements_user_time', 'user_id', 'unlocked_at'),
    )


class ConversationShare(Base):
    """Shared conversations with privacy controls"""
    __tablename__ = "conversation_shares"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Content
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    
    # XP and agent data
    agents_used = Column(JSON, nullable=False)  # List of agent names
    xp_earned = Column(Integer, default=0)
    difficulty_level = Column(String(20), nullable=True)
    
    # Privacy and sharing
    privacy_level = Column(String(20), default="public", index=True)  # public, unlisted, private
    is_featured = Column(Boolean, default=False)
    
    # Engagement metrics
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    
    # Tags and categorization
    tags = Column(JSON, nullable=True)  # List of tags
    category = Column(String(50), nullable=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    
    # Indexes
    __table_args__ = (
        Index('idx_conversation_shares_privacy_time', 'privacy_level', 'created_at'),
        Index('idx_conversation_shares_featured', 'is_featured', 'created_at'),
    )


class SystemMetrics(Base):
    """System-wide performance and usage metrics"""
    __tablename__ = "system_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Metric identification
    metric_type = Column(String(50), nullable=False, index=True)
    metric_name = Column(String(100), nullable=False)
    
    # Metric data
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=True)
    tags = Column(JSON, nullable=True)  # Additional categorization
    
    # Context
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_system_metrics_type_time', 'metric_type', 'timestamp'),
        Index('idx_system_metrics_agent_time', 'agent_id', 'timestamp'),
    )