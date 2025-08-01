"""
Agent Tracking API Router
Personal agent XP tracking, performance metrics, and team leaderboards
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc, asc
from sqlalchemy.orm import selectinload

from ..core.database import get_db
from ..core.auth import get_current_user  # Placeholder for auth system
from ..models.database import User, Agent, AgentStats, XPEvent
from ..schemas.xp_tracking import (
    XPEventCreate, XPEventResponse, AgentStats as AgentStatsSchema,
    AgentStatsDetailed, LeaderboardEntry, PaginationParams,
    XPTrendData, AgentUsageAnalytics
)
from ..services.xp_calculator import XPCalculationEngine
from ..services.achievement_service import AchievementService
from ..services.notification_service import NotificationService


router = APIRouter(prefix="/api/v1/agents", tags=["Agent Tracking"])


@router.post("/{agent_name}/xp", response_model=XPEventResponse)
async def track_agent_xp(
    agent_name: str,
    event: XPEventCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Track XP event for a specific agent
    Calculates XP, updates agent stats, checks achievements
    """
    # Initialize services
    xp_calculator = XPCalculationEngine()
    achievement_service = AchievementService(db, xp_calculator)
    notification_service = NotificationService()
    
    try:
        # Get or create agent
        agent = await get_or_create_agent(db, agent_name)
        
        # Get current agent stats for context
        agent_stats = await get_user_agent_stats(db, current_user.id, agent.id)
        
        # Calculate XP with context
        context = {
            "streak_days": agent_stats.streak_days if agent_stats else 0,
            "current_level": agent_stats.level if agent_stats else 1,
            "avg_task_time": agent_stats.avg_task_time if agent_stats else 0
        }
        
        xp_result = xp_calculator.calculate_xp(event, context)
        
        # Create XP event record
        xp_event = XPEvent(
            user_id=current_user.id,
            agent_id=agent.id,
            action_type=event.action_type.value,
            base_points=xp_result.base_points,
            multiplier=xp_result.multiplier_total,
            bonus_points=xp_result.bonus_points,
            total_xp=xp_result.total_xp,
            task_description=event.task_description,
            task_complexity=event.task_complexity.value if event.task_complexity else None,
            task_duration=event.task_duration,
            success=event.success,
            response_quality=event.response_quality,
            user_satisfaction=event.user_satisfaction,
            code_quality=event.code_quality,
            evidence_type=event.evidence_type.value if event.evidence_type else None,
            evidence_data=event.evidence_data,
            metadata={
                **event.metadata or {},
                "calculation_breakdown": xp_result.breakdown
            }
        )
        
        db.add(xp_event)
        
        # Update or create agent stats
        if not agent_stats:
            agent_stats = AgentStats(
                user_id=current_user.id,
                agent_id=agent.id,
                level=1,
                xp=0
            )
            db.add(agent_stats)
        
        # Calculate level before XP addition
        level_before = agent_stats.level
        
        # Update agent stats
        agent_stats.xp += xp_result.total_xp
        agent_stats.total_calls += 1
        agent_stats.last_used = datetime.utcnow()
        
        if event.success:
            agent_stats.successful_tasks += 1
        else:
            agent_stats.failed_tasks += 1
            if event.action_type == "error_resolution":
                agent_stats.errors_resolved += 1
        
        # Update performance metrics
        if event.task_duration:
            total_time = agent_stats.total_task_time + event.task_duration
            agent_stats.avg_task_time = total_time / max(agent_stats.total_calls, 1)
            agent_stats.total_task_time = total_time
            
            if not agent_stats.fastest_completion or event.task_duration < agent_stats.fastest_completion:
                agent_stats.fastest_completion = event.task_duration
        
        # Update quality metrics
        if event.response_quality:
            current_avg = agent_stats.response_quality_avg
            total_quality_tasks = agent_stats.successful_tasks
            agent_stats.response_quality_avg = (
                (current_avg * (total_quality_tasks - 1) + event.response_quality) / total_quality_tasks
            )
        
        # Calculate new level
        level_after = xp_calculator.calculate_level(agent_stats.xp)
        agent_stats.level = level_after
        level_up = level_after > level_before
        
        # Update user's total XP
        current_user.total_xp += xp_result.total_xp
        current_user.current_level = xp_calculator.calculate_level(current_user.total_xp)
        current_user.last_active = datetime.utcnow()
        
        # Check for achievements
        achievements = await achievement_service.check_and_unlock_achievements(
            current_user.id, agent.id, context
        )
        
        await db.commit()
        
        # Prepare response
        response = XPEventResponse(
            id=xp_event.id,
            xp_gained=xp_result.total_xp,
            total_xp=agent_stats.xp,
            level_before=level_before,
            level_after=level_after,
            level_up=level_up,
            achievements_unlocked=[a.name for a in achievements]
        )
        
        # Send real-time notifications
        background_tasks.add_task(
            notification_service.send_xp_notification,
            current_user.id,
            agent_name,
            response
        )
        
        return response
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to track XP: {str(e)}")


@router.get("/{agent_name}/stats", response_model=AgentStatsDetailed)
async def get_agent_stats(
    agent_name: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed statistics for a specific agent"""
    # Get agent
    agent_result = await db.execute(
        select(Agent).where(Agent.name == agent_name)
    )
    agent = agent_result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Get agent stats
    stats_result = await db.execute(
        select(AgentStats)
        .where(
            and_(
                AgentStats.user_id == current_user.id,
                AgentStats.agent_id == agent.id
            )
        )
    )
    stats = stats_result.scalar_one_or_none()
    
    if not stats:
        # Return default stats for unused agent
        return AgentStatsDetailed(
            agent_id=agent.id,
            agent_name=agent.name,
            level=1,
            xp=0,
            total_calls=0,
            successful_tasks=0,
            failed_tasks=0,
            success_rate=0.0,
            avg_task_time=0.0,
            last_used=datetime.utcnow(),
            errors_resolved=0,
            fastest_completion=None,
            response_quality_avg=0.0,
            user_satisfaction_avg=0.0,
            complexity_handled_avg=0.0,
            streak_days=0,
            longest_streak=0
        )
    
    # Calculate success rate
    success_rate = stats.successful_tasks / max(stats.total_calls, 1) * 100
    
    return AgentStatsDetailed(
        agent_id=agent.id,
        agent_name=agent.name,
        level=stats.level,
        xp=stats.xp,
        total_calls=stats.total_calls,
        successful_tasks=stats.successful_tasks,
        failed_tasks=stats.failed_tasks,
        success_rate=success_rate,
        avg_task_time=stats.avg_task_time,
        last_used=stats.last_used,
        errors_resolved=stats.errors_resolved,
        fastest_completion=stats.fastest_completion,
        response_quality_avg=stats.response_quality_avg,
        user_satisfaction_avg=stats.user_satisfaction_avg,
        complexity_handled_avg=stats.complexity_handled_avg,
        streak_days=stats.streak_days,
        longest_streak=stats.longest_streak
    )


@router.get("/leaderboard/personal", response_model=List[AgentStatsSchema])
async def get_personal_agent_leaderboard(
    sort_by: str = Query("xp", regex="^(xp|level|success_rate|avg_task_time)$"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get personal agent leaderboard for current user"""
    
    # Build query based on sort parameter
    if sort_by == "xp":
        order_by = desc(AgentStats.xp)
    elif sort_by == "level":
        order_by = desc(AgentStats.level)
    elif sort_by == "success_rate":
        # Calculate success rate in query
        success_rate = (AgentStats.successful_tasks.cast(func.float()) / 
                       func.greatest(AgentStats.total_calls, 1) * 100)
        order_by = desc(success_rate)
    else:  # avg_task_time
        order_by = asc(AgentStats.avg_task_time)
    
    # Execute query
    result = await db.execute(
        select(AgentStats, Agent.name)
        .join(Agent)
        .where(AgentStats.user_id == current_user.id)
        .order_by(order_by)
        .limit(limit)
    )
    
    leaderboard = []
    for stats, agent_name in result.fetchall():
        success_rate = stats.successful_tasks / max(stats.total_calls, 1) * 100
        
        leaderboard.append(AgentStatsSchema(
            agent_id=stats.agent_id,
            agent_name=agent_name,
            level=stats.level,
            xp=stats.xp,
            total_calls=stats.total_calls,
            successful_tasks=stats.successful_tasks,
            failed_tasks=stats.failed_tasks,
            success_rate=success_rate,
            avg_task_time=stats.avg_task_time,
            last_used=stats.last_used
        ))
    
    return leaderboard


@router.get("/{agent_name}/analytics", response_model=AgentUsageAnalytics)
async def get_agent_analytics(
    agent_name: str,
    period: str = Query("weekly", regex="^(daily|weekly|monthly)$"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed analytics for an agent"""
    
    # Get agent
    agent_result = await db.execute(
        select(Agent).where(Agent.name == agent_name)
    )
    agent = agent_result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Calculate date range
    now = datetime.utcnow()
    if period == "daily":
        start_date = now - timedelta(days=30)
        date_format = "%Y-%m-%d"
    elif period == "weekly":
        start_date = now - timedelta(weeks=12)
        date_format = "%Y-W%U"
    else:  # monthly
        start_date = now - timedelta(days=365)
        date_format = "%Y-%m"
    
    # Get usage statistics
    usage_stats = await db.execute(
        select(
            func.count(XPEvent.id).label("total_uses"),
            func.avg(XPEvent.task_duration).label("avg_duration"),
            func.sum(func.case([(XPEvent.success == True, 1)], else_=0)).label("successful"),
            func.sum(XPEvent.total_xp).label("total_xp")
        )
        .where(
            and_(
                XPEvent.user_id == current_user.id,
                XPEvent.agent_id == agent.id,
                XPEvent.timestamp >= start_date
            )
        )
    )
    stats = usage_stats.fetchone()
    
    total_uses = stats.total_uses or 0
    success_rate = (stats.successful / total_uses * 100) if total_uses > 0 else 0
    
    # Get trend data
    trend_data = await db.execute(
        select(
            func.date_format(XPEvent.timestamp, date_format).label("period"),
            func.count(XPEvent.id).label("uses"),
            func.sum(XPEvent.total_xp).label("xp"),
            func.avg(XPEvent.task_duration).label("avg_duration")
        )
        .where(
            and_(
                XPEvent.user_id == current_user.id,
                XPEvent.agent_id == agent.id,
                XPEvent.timestamp >= start_date
            )
        )
        .group_by(func.date_format(XPEvent.timestamp, date_format))
        .order_by(func.date_format(XPEvent.timestamp, date_format))
    )
    
    trend_points = []
    for row in trend_data.fetchall():
        trend_points.append({
            "period": row.period,
            "uses": row.uses,
            "xp": row.xp or 0,
            "avg_duration": float(row.avg_duration) if row.avg_duration else 0
        })
    
    return AgentUsageAnalytics(
        agent_name=agent_name,
        total_uses=total_uses,
        unique_users=1,  # For personal tracking, always 1
        avg_session_duration=float(stats.avg_duration) if stats.avg_duration else 0,
        success_rate=success_rate,
        xp_generated=stats.total_xp or 0,
        trend_data=trend_points
    )


@router.get("/performance/summary")
async def get_performance_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get overall performance summary across all agents"""
    
    # Get summary statistics
    summary_stats = await db.execute(
        select(
            func.count(func.distinct(AgentStats.agent_id)).label("unique_agents"),
            func.sum(AgentStats.xp).label("total_xp"),
            func.avg(AgentStats.level).label("avg_level"),
            func.sum(AgentStats.successful_tasks).label("total_tasks"),
            func.sum(AgentStats.errors_resolved).label("total_errors_resolved")
        )
        .where(AgentStats.user_id == current_user.id)
    )
    stats = summary_stats.fetchone()
    
    # Get recent activity (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_activity = await db.execute(
        select(
            func.count(XPEvent.id).label("recent_tasks"),
            func.sum(XPEvent.total_xp).label("recent_xp")
        )
        .where(
            and_(
                XPEvent.user_id == current_user.id,
                XPEvent.timestamp >= week_ago
            )
        )
    )
    recent = recent_activity.fetchone()
    
    # Get top performing agents
    top_agents = await db.execute(
        select(Agent.name, AgentStats.xp, AgentStats.level)
        .join(Agent)
        .where(AgentStats.user_id == current_user.id)
        .order_by(desc(AgentStats.xp))
        .limit(5)
    )
    
    return {
        "summary": {
            "unique_agents": stats.unique_agents or 0,
            "total_xp": current_user.total_xp,
            "current_level": current_user.current_level,
            "avg_agent_level": float(stats.avg_level) if stats.avg_level else 0,
            "total_tasks": stats.total_tasks or 0,
            "errors_resolved": stats.total_errors_resolved or 0
        },
        "recent_activity": {
            "tasks_last_7_days": recent.recent_tasks or 0,
            "xp_last_7_days": recent.recent_xp or 0
        },
        "top_agents": [
            {"name": name, "xp": xp, "level": level}
            for name, xp, level in top_agents.fetchall()
        ]
    }


# Helper functions
async def get_or_create_agent(db: AsyncSession, agent_name: str) -> Agent:
    """Get existing agent or create new one"""
    result = await db.execute(
        select(Agent).where(Agent.name == agent_name)
    )
    agent = result.scalar_one_or_none()
    
    if not agent:
        # Create new agent
        agent = Agent(
            name=agent_name,
            display_name=agent_name.replace("-", " ").title(),
            category="development"  # Default category
        )
        db.add(agent)
        await db.flush()  # Get the ID
    
    return agent


async def get_user_agent_stats(db: AsyncSession, user_id: UUID, agent_id: UUID) -> Optional[AgentStats]:
    """Get agent stats for a specific user"""
    result = await db.execute(
        select(AgentStats)
        .where(
            and_(
                AgentStats.user_id == user_id,
                AgentStats.agent_id == agent_id
            )
        )
    )
    return result.scalar_one_or_none()