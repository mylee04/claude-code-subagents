"""
Achievement System Service for Claude Arena
Handles achievement definitions, progress tracking, and unlock logic
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from ..models.database import Achievement, UserAchievement, User, AgentStats, XPEvent, Agent
from ..schemas.xp_tracking import AchievementCreate, AchievementResponse, AchievementRarity
from .xp_calculator import XPCalculationEngine


class AchievementService:
    """
    High-performance achievement system with real-time unlocking
    """
    
    def __init__(self, db: AsyncSession, xp_calculator: XPCalculationEngine):
        self.db = db
        self.xp_calculator = xp_calculator
        
        # Pre-defined achievement templates
        self.achievement_templates = self._load_achievement_templates()
    
    def _load_achievement_templates(self) -> Dict[str, Dict]:
        """Load predefined achievement templates"""
        return {
            # Level-based achievements
            "first_steps": {
                "name": "first_steps",
                "display_name": "First Steps",
                "description": "Complete your first task with any agent",
                "category": "milestone",
                "rarity": AchievementRarity.COMMON,
                "xp_reward": 50,
                "icon": "🎯",
                "color": "#4CAF50",
                "conditions": [{"type": "task_count", "value": 1}]
            },
            "agent_explorer": {
                "name": "agent_explorer",
                "display_name": "Agent Explorer",
                "description": "Use 5 different agents successfully",
                "category": "exploration",
                "rarity": AchievementRarity.COMMON,
                "xp_reward": 100,
                "icon": "🗺️",
                "color": "#2196F3",
                "conditions": [{"type": "unique_agents", "value": 5}]
            },
            "speed_demon": {
                "name": "speed_demon",
                "display_name": "Speed Demon",
                "description": "Complete 10 tasks in under 30 seconds each",
                "category": "performance",
                "rarity": AchievementRarity.RARE,
                "xp_reward": 200,
                "icon": "⚡",
                "color": "#FFD700",
                "conditions": [{"type": "speed_tasks", "value": 10, "duration": 30}]
            },
            "quality_master": {
                "name": "quality_master",
                "display_name": "Quality Master",
                "description": "Achieve 95%+ quality rating on 20 tasks",
                "category": "quality",
                "rarity": AchievementRarity.RARE,
                "xp_reward": 250,
                "icon": "💎",
                "color": "#9C27B0",
                "conditions": [{"type": "quality_tasks", "value": 20, "threshold": 0.95}]
            },
            "bug_hunter": {
                "name": "bug_hunter",
                "display_name": "Bug Hunter",
                "description": "Successfully resolve 25 error situations",
                "category": "troubleshooting",
                "rarity": AchievementRarity.RARE,
                "xp_reward": 300,
                "icon": "🐛",
                "color": "#FF5722",
                "conditions": [{"type": "errors_resolved", "value": 25}]
            },
            "streak_warrior": {
                "name": "streak_warrior",
                "display_name": "Streak Warrior",
                "description": "Maintain a 7-day activity streak",
                "category": "dedication",
                "rarity": AchievementRarity.RARE,
                "xp_reward": 400,
                "icon": "🔥",
                "color": "#FF9800",
                "conditions": [{"type": "streak_days", "value": 7}]
            },
            "elite_trainer": {
                "name": "elite_trainer",
                "display_name": "Elite Trainer",
                "description": "Reach Level 5 with any agent",
                "category": "mastery",
                "rarity": AchievementRarity.EPIC,
                "xp_reward": 500,
                "icon": "⭐",
                "color": "#FFD700",
                "conditions": [{"type": "agent_level", "value": 5}]
            },
            "perfectionist": {
                "name": "perfectionist",
                "display_name": "Perfectionist",
                "description": "Achieve 100% quality rating on 5 expert-level tasks",
                "category": "excellence",
                "rarity": AchievementRarity.EPIC,
                "xp_reward": 750,
                "icon": "🏆",
                "color": "#8BC34A",
                "conditions": [
                    {"type": "perfect_expert_tasks", "value": 5, "quality": 1.0, "complexity": "expert"}
                ]
            },
            "agent_whisperer": {
                "name": "agent_whisperer",
                "display_name": "Agent Whisperer",
                "description": "Successfully use 20 different agents",
                "category": "mastery",
                "rarity": AchievementRarity.EPIC,
                "xp_reward": 1000,
                "icon": "🎭",
                "color": "#673AB7",
                "conditions": [{"type": "unique_agents", "value": 20}]
            },
            "arena_legend": {
                "name": "arena_legend",
                "display_name": "Arena Legend",
                "description": "Reach Level 10 overall and unlock 15 achievements",
                "category": "legendary",
                "rarity": AchievementRarity.LEGENDARY,
                "xp_reward": 2000,
                "icon": "👑",
                "color": "#FFD700",
                "conditions": [
                    {"type": "user_level", "value": 10},
                    {"type": "achievement_count", "value": 15}
                ]
            }
        }
    
    async def initialize_default_achievements(self) -> None:
        """Initialize default achievements in database"""
        for template in self.achievement_templates.values():
            # Check if achievement already exists
            result = await self.db.execute(
                select(Achievement).where(Achievement.name == template["name"])
            )
            if result.scalar_one_or_none():
                continue
            
            # Create new achievement
            achievement = Achievement(
                name=template["name"],
                display_name=template["display_name"],
                description=template["description"],
                category=template["category"],
                rarity=template["rarity"],
                xp_reward=template["xp_reward"],
                icon=template.get("icon"),
                color=template.get("color"),
                unlock_conditions=template["conditions"]
            )
            self.db.add(achievement)
        
        await self.db.commit()
    
    async def check_and_unlock_achievements(
        self, 
        user_id: UUID,
        agent_id: Optional[UUID] = None,
        context: Optional[Dict] = None
    ) -> List[AchievementResponse]:
        """
        Check for achievement unlocks and create UserAchievement records
        Returns list of newly unlocked achievements
        """
        unlocked_achievements = []
        
        # Get user's current achievements
        user_achievements = await self.db.execute(
            select(UserAchievement.achievement_id)
            .where(UserAchievement.user_id == user_id)
        )
        unlocked_ids = {row[0] for row in user_achievements.fetchall()}
        
        # Get all active achievements not yet unlocked by user
        achievements = await self.db.execute(
            select(Achievement)
            .where(
                and_(
                    Achievement.is_active == True,
                    ~Achievement.id.in_(unlocked_ids) if unlocked_ids else True
                )
            )
        )
        
        # Get comprehensive user stats for checking conditions
        user_stats = await self._get_user_stats(user_id)
        agent_stats = await self._get_agent_stats(user_id, agent_id) if agent_id else {}
        
        # Check each achievement's conditions
        for achievement in achievements.scalars():
            if await self._check_achievement_conditions(
                achievement, user_stats, agent_stats, context
            ):
                # Unlock the achievement
                user_achievement = UserAchievement(
                    user_id=user_id,
                    achievement_id=achievement.id,
                    agent_id=agent_id,
                    xp_earned=achievement.xp_reward,
                    progress_data=context or {}
                )
                self.db.add(user_achievement)
                
                # Add XP reward to user
                await self._add_achievement_xp(user_id, achievement.xp_reward)
                
                unlocked_achievements.append(
                    AchievementResponse.from_orm(achievement)
                )
        
        if unlocked_achievements:
            await self.db.commit()
        
        return unlocked_achievements
    
    async def _get_user_stats(self, user_id: UUID) -> Dict[str, Any]:
        """Get comprehensive user statistics for achievement checking"""
        # Basic user data
        user = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user_data = user.scalar_one_or_none()
        if not user_data:
            return {}
        
        # XP events statistics
        xp_stats = await self.db.execute(
            select(
                func.count(XPEvent.id).label("total_tasks"),
                func.sum(XPEvent.total_xp).label("total_xp"),
                func.count(func.distinct(XPEvent.agent_id)).label("unique_agents"),
                func.avg(XPEvent.task_duration).label("avg_duration"),
                func.count(
                    XPEvent.id.filter(XPEvent.success == True)
                ).label("successful_tasks"),
                func.count(
                    XPEvent.id.filter(XPEvent.action_type == "error_resolution")
                ).label("errors_resolved")
            )
            .where(XPEvent.user_id == user_id)
        )
        stats = xp_stats.fetchone()
        
        # Quality statistics
        quality_stats = await self.db.execute(
            select(
                func.count(
                    XPEvent.id.filter(XPEvent.response_quality >= 0.95)
                ).label("high_quality_tasks"),
                func.count(
                    XPEvent.id.filter(
                        and_(
                            XPEvent.response_quality == 1.0,
                            XPEvent.task_complexity == "expert"
                        )
                    )
                ).label("perfect_expert_tasks")
            )
            .where(XPEvent.user_id == user_id)
        )
        quality = quality_stats.fetchone()
        
        # Speed statistics
        speed_stats = await self.db.execute(
            select(
                func.count(
                    XPEvent.id.filter(XPEvent.task_duration <= 30)
                ).label("fast_tasks")
            )
            .where(
                and_(
                    XPEvent.user_id == user_id,
                    XPEvent.task_duration.isnot(None)
                )
            )
        )
        speed = speed_stats.fetchone()
        
        # Achievement count
        achievement_count = await self.db.execute(
            select(func.count(UserAchievement.id))
            .where(UserAchievement.user_id == user_id)
        )
        
        # Calculate streak (simplified - would need more complex logic for real streaks)
        recent_activity = await self.db.execute(
            select(func.date(XPEvent.timestamp))
            .where(
                and_(
                    XPEvent.user_id == user_id,
                    XPEvent.timestamp >= datetime.utcnow() - timedelta(days=30)
                )
            )
            .distinct()
            .order_by(func.date(XPEvent.timestamp).desc())
        )
        active_dates = [row[0] for row in recent_activity.fetchall()]
        streak_days = self._calculate_streak(active_dates)
        
        return {
            "user_level": self.xp_calculator.calculate_level(user_data.total_xp),
            "total_xp": user_data.total_xp,
            "total_tasks": stats.total_tasks or 0,
            "unique_agents": stats.unique_agents or 0,
            "successful_tasks": stats.successful_tasks or 0,
            "errors_resolved": stats.errors_resolved or 0,
            "high_quality_tasks": quality.high_quality_tasks or 0,
            "perfect_expert_tasks": quality.perfect_expert_tasks or 0,
            "fast_tasks": speed.fast_tasks or 0,
            "achievement_count": achievement_count.scalar() or 0,
            "streak_days": streak_days,
            "avg_duration": stats.avg_duration or 0
        }
    
    async def _get_agent_stats(self, user_id: UUID, agent_id: UUID) -> Dict[str, Any]:
        """Get agent-specific statistics"""
        agent_stats = await self.db.execute(
            select(AgentStats)
            .where(
                and_(
                    AgentStats.user_id == user_id,
                    AgentStats.agent_id == agent_id
                )
            )
        )
        stats = agent_stats.scalar_one_or_none()
        
        if not stats:
            return {}
        
        return {
            "level": stats.level,
            "xp": stats.xp,
            "total_calls": stats.total_calls,
            "successful_tasks": stats.successful_tasks,
            "errors_resolved": stats.errors_resolved,
            "avg_task_time": stats.avg_task_time,
            "streak_days": stats.streak_days
        }
    
    def _calculate_streak(self, active_dates: List) -> int:
        """Calculate current activity streak"""
        if not active_dates:
            return 0
        
        # Sort dates in descending order
        sorted_dates = sorted(active_dates, reverse=True)
        
        # Check for consecutive days starting from today
        today = datetime.utcnow().date()
        streak = 0
        
        for i, date in enumerate(sorted_dates):
            expected_date = today - timedelta(days=i)
            if date == expected_date:
                streak += 1
            else:
                break
        
        return streak
    
    async def _check_achievement_conditions(
        self,
        achievement: Achievement,
        user_stats: Dict,
        agent_stats: Dict,
        context: Optional[Dict]
    ) -> bool:
        """Check if all conditions for an achievement are met"""
        conditions = achievement.unlock_conditions
        
        for condition in conditions:
            condition_type = condition["type"]
            target_value = condition["value"]
            
            if condition_type == "task_count":
                if user_stats.get("total_tasks", 0) < target_value:
                    return False
                    
            elif condition_type == "unique_agents":
                if user_stats.get("unique_agents", 0) < target_value:
                    return False
                    
            elif condition_type == "user_level":
                if user_stats.get("user_level", 1) < target_value:
                    return False
                    
            elif condition_type == "agent_level":
                if agent_stats.get("level", 1) < target_value:
                    return False
                    
            elif condition_type == "errors_resolved":
                if user_stats.get("errors_resolved", 0) < target_value:
                    return False
                    
            elif condition_type == "streak_days":
                if user_stats.get("streak_days", 0) < target_value:
                    return False
                    
            elif condition_type == "speed_tasks":
                if user_stats.get("fast_tasks", 0) < target_value:
                    return False
                    
            elif condition_type == "quality_tasks":
                if user_stats.get("high_quality_tasks", 0) < target_value:
                    return False
                    
            elif condition_type == "perfect_expert_tasks":
                if user_stats.get("perfect_expert_tasks", 0) < target_value:
                    return False
                    
            elif condition_type == "achievement_count":
                if user_stats.get("achievement_count", 0) < target_value:
                    return False
        
        return True
    
    async def _add_achievement_xp(self, user_id: UUID, xp_amount: int) -> None:
        """Add XP reward from achievement to user's total"""
        user = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user_data = user.scalar_one()
        
        user_data.total_xp += xp_amount
        user_data.current_level = self.xp_calculator.calculate_level(user_data.total_xp)
    
    async def get_user_achievements(self, user_id: UUID) -> List[AchievementResponse]:
        """Get all achievements unlocked by a user"""
        result = await self.db.execute(
            select(Achievement, UserAchievement.unlocked_at)
            .join(UserAchievement)
            .where(UserAchievement.user_id == user_id)
            .order_by(UserAchievement.unlocked_at.desc())
        )
        
        achievements = []
        for achievement, unlocked_at in result.fetchall():
            achievement_data = AchievementResponse.from_orm(achievement)
            achievement_data.unlocked_at = unlocked_at
            achievements.append(achievement_data)
        
        return achievements
    
    async def get_achievement_progress(self, user_id: UUID, achievement_id: UUID) -> Dict[str, Any]:
        """Get progress towards a specific achievement"""
        achievement = await self.db.execute(
            select(Achievement).where(Achievement.id == achievement_id)
        )
        achievement_data = achievement.scalar_one_or_none()
        
        if not achievement_data:
            return {"error": "Achievement not found"}
        
        # Check if already unlocked
        unlocked = await self.db.execute(
            select(UserAchievement)
            .where(
                and_(
                    UserAchievement.user_id == user_id,
                    UserAchievement.achievement_id == achievement_id
                )
            )
        )
        
        if unlocked.scalar_one_or_none():
            return {
                "achievement_id": achievement_id,
                "unlocked": True,
                "progress": 100.0,
                "unlocked_at": unlocked.scalar_one().unlocked_at
            }
        
        # Calculate current progress
        user_stats = await self._get_user_stats(user_id)
        conditions = achievement_data.unlock_conditions
        
        progress_items = []
        total_progress = 0
        
        for condition in conditions:
            condition_type = condition["type"]
            target_value = condition["value"]
            current_value = user_stats.get(condition_type.replace("_", "_"), 0)
            
            progress = min(100, (current_value / target_value) * 100)
            progress_items.append({
                "condition": condition_type,
                "current": current_value,
                "target": target_value,
                "progress": progress
            })
            total_progress += progress
        
        return {
            "achievement_id": achievement_id,
            "unlocked": False,
            "progress": total_progress / len(conditions) if conditions else 0,
            "condition_progress": progress_items
        }