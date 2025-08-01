"""
Advanced XP Calculator Engine for Claude Arena
Handles complex XP calculations with multipliers, bonuses, and achievement tracking
"""

import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from uuid import UUID

from ..schemas.xp_tracking import (
    XPEventCreate, XPCalculationResult, XPMultiplier, 
    TaskComplexity, XPActionType, EvidenceType
)


class XPCalculationEngine:
    """
    High-performance XP calculation engine with configurable rules
    """
    
    # Base XP values for different action types
    BASE_XP_VALUES = {
        XPActionType.TASK_COMPLETION: 10,
        XPActionType.ERROR_RESOLUTION: 20,
        XPActionType.SPEED_BONUS: 5,
        XPActionType.QUALITY_BONUS: 15,
        XPActionType.COMPLEXITY_BONUS: 25,
        XPActionType.STREAK_BONUS: 10,
        XPActionType.FIRST_USE: 50,
        XPActionType.MILESTONE: 100,
        XPActionType.ACHIEVEMENT_UNLOCK: 0,  # Variable based on achievement
    }
    
    # Complexity multipliers
    COMPLEXITY_MULTIPLIERS = {
        TaskComplexity.SIMPLE: 1.0,
        TaskComplexity.MEDIUM: 1.5,
        TaskComplexity.COMPLEX: 2.0,
        TaskComplexity.EXPERT: 3.0,
    }
    
    # Quality thresholds for bonus calculations
    QUALITY_THRESHOLDS = {
        "excellent": 0.9,
        "good": 0.7,
        "average": 0.5,
    }
    
    # Level calculation thresholds (exponential curve) - NEW TIER SYSTEM
    @property
    def LEVEL_THRESHOLDS(self):
        """Generate level thresholds using the new exponential tier system"""
        return self._calculate_level_thresholds()
    
    def _calculate_level_thresholds(self):
        """Calculate XP thresholds for all levels with exponential scaling"""
        thresholds = [0]  # Level 1 starts at 0 XP
        
        # Levels 1-10: Start at 100 XP for level 2, increase by 50 per level
        current_xp = 0
        for level in range(2, 11):
            current_xp += 100 + (level - 2) * 50  # 100, 150, 200, 250, etc.
            thresholds.append(current_xp)
            
        # Levels 11-20: Increase by 100 per level
        for level in range(11, 21):
            current_xp += 100 * (level - 10) + 250  # Accelerated growth
            thresholds.append(current_xp)
            
        # Levels 21-30: Increase by 200 per level
        for level in range(21, 31):
            current_xp += 200 * (level - 20) + 450  # More accelerated
            thresholds.append(current_xp)
            
        # Levels 31-40: Increase by 500 per level
        for level in range(31, 41):
            current_xp += 500 * (level - 30) + 850  # Significant jump
            thresholds.append(current_xp)
            
        # Levels 41-50: Increase by 1000 per level
        for level in range(41, 51):
            current_xp += 1000 * (level - 40) + 1350  # Major jump
            thresholds.append(current_xp)
            
        # Levels 51-70: Increase by 2000 per level (Expert tier completion)
        for level in range(51, 71):
            current_xp += 2000 * (level - 50) + 2350
            thresholds.append(current_xp)
            
        # Levels 71-120: Increase by 5000 per level (Master tier)
        for level in range(71, 121):
            current_xp += 5000 * (level - 70) + 4350
            thresholds.append(current_xp)
            
        # Levels 121-200: Increase by 10000 per level (Grandmaster tier)
        for level in range(121, 201):
            current_xp += 10000 * (level - 120) + 9350
            thresholds.append(current_xp)
            
        # Levels 201-250: Increase by 25000 per level (Legend tier)
        for level in range(201, 251):
            current_xp += 25000 * (level - 200) + 19350
            thresholds.append(current_xp)
            
        return thresholds
    
    def __init__(self):
        self.evidence_bonuses = {
            EvidenceType.SPEED_IMPROVEMENT: 0.3,  # 30% bonus
            EvidenceType.BUG_RESOLUTION: 0.5,     # 50% bonus
            EvidenceType.CODE_QUALITY: 0.4,       # 40% bonus
            EvidenceType.USER_SATISFACTION: 0.2,  # 20% bonus
            EvidenceType.COMPLEXITY_HANDLING: 0.6, # 60% bonus
            EvidenceType.INNOVATION: 0.8,          # 80% bonus
        }
    
    def calculate_xp(self, event: XPEventCreate, context: Optional[Dict[str, Any]] = None) -> XPCalculationResult:
        """
        Calculate total XP for an event with all bonuses and multipliers
        """
        # Start with base points or calculate from action type
        base_points = event.base_points or self.BASE_XP_VALUES.get(event.action_type, 10)
        
        # Initialize calculation breakdown
        breakdown = {
            "base_points": base_points,
            "multipliers": {},
            "bonuses": {},
            "quality_adjustments": {},
            "evidence_bonus": 0,
            "complexity_multiplier": 1.0,
        }
        
        # Apply complexity multiplier
        complexity_multiplier = 1.0
        if event.task_complexity:
            complexity_multiplier = self.COMPLEXITY_MULTIPLIERS[event.task_complexity]
            breakdown["complexity_multiplier"] = complexity_multiplier
        
        # Calculate quality-based adjustments
        quality_multiplier = self._calculate_quality_multiplier(event, breakdown)
        
        # Apply speed bonuses
        speed_multiplier = self._calculate_speed_bonus(event, context, breakdown)
        
        # Apply evidence bonuses
        evidence_bonus = self._calculate_evidence_bonus(event, breakdown)
        
        # Apply custom multipliers
        custom_multiplier = 1.0
        for multiplier in event.multipliers:
            custom_multiplier *= multiplier.value
            breakdown["multipliers"][multiplier.type] = multiplier.value
        
        # Calculate streak bonuses from context
        streak_multiplier = self._calculate_streak_bonus(context, breakdown)
        
        # Apply success/failure modifier
        success_modifier = 1.0 if event.success else 0.3  # Partial XP for failures
        breakdown["success_modifier"] = success_modifier
        
        # Calculate total multiplier
        total_multiplier = (complexity_multiplier * quality_multiplier * 
                          speed_multiplier * custom_multiplier * 
                          streak_multiplier * success_modifier)
        
        # Calculate final XP
        calculated_xp = int(base_points * total_multiplier)
        total_xp = calculated_xp + event.bonus_points + evidence_bonus
        
        return XPCalculationResult(
            base_points=base_points,
            multiplier_total=total_multiplier,
            bonus_points=event.bonus_points + evidence_bonus,
            total_xp=total_xp,
            breakdown=breakdown
        )
    
    def _calculate_quality_multiplier(self, event: XPEventCreate, breakdown: Dict) -> float:
        """Calculate multiplier based on quality metrics"""
        quality_scores = []
        
        if event.response_quality is not None:
            quality_scores.append(event.response_quality)
            breakdown["quality_adjustments"]["response_quality"] = event.response_quality
        
        if event.user_satisfaction is not None:
            quality_scores.append(event.user_satisfaction)
            breakdown["quality_adjustments"]["user_satisfaction"] = event.user_satisfaction
        
        if event.code_quality is not None:
            quality_scores.append(event.code_quality)
            breakdown["quality_adjustments"]["code_quality"] = event.code_quality
        
        if not quality_scores:
            return 1.0
        
        avg_quality = sum(quality_scores) / len(quality_scores)
        
        # Convert quality score to multiplier (0.5x to 2.0x range)
        if avg_quality >= self.QUALITY_THRESHOLDS["excellent"]:
            multiplier = 2.0
        elif avg_quality >= self.QUALITY_THRESHOLDS["good"]:
            multiplier = 1.5
        elif avg_quality >= self.QUALITY_THRESHOLDS["average"]:
            multiplier = 1.0
        else:
            multiplier = 0.7
        
        breakdown["quality_adjustments"]["multiplier"] = multiplier
        return multiplier
    
    def _calculate_speed_bonus(self, event: XPEventCreate, context: Optional[Dict], breakdown: Dict) -> float:
        """Calculate speed-based bonus multiplier"""
        if not event.task_duration or not context:
            return 1.0
        
        # Get expected duration for task complexity
        expected_durations = {
            TaskComplexity.SIMPLE: 30,    # 30 seconds
            TaskComplexity.MEDIUM: 120,   # 2 minutes
            TaskComplexity.COMPLEX: 300,  # 5 minutes
            TaskComplexity.EXPERT: 600,   # 10 minutes
        }
        
        expected = expected_durations.get(event.task_complexity, 120)
        actual = event.task_duration
        
        if actual <= expected * 0.5:  # Completed in half the expected time
            multiplier = 1.5
        elif actual <= expected * 0.75:  # Completed in 3/4 the expected time
            multiplier = 1.25
        elif actual <= expected:  # Completed within expected time
            multiplier = 1.0
        else:  # Took longer than expected
            multiplier = max(0.8, 1.0 - (actual - expected) / expected * 0.2)
        
        breakdown["bonuses"]["speed_multiplier"] = multiplier
        return multiplier
    
    def _calculate_evidence_bonus(self, event: XPEventCreate, breakdown: Dict) -> int:
        """Calculate bonus points based on evidence of improvement"""
        if not event.evidence_type or not event.evidence_data:
            return 0
        
        base_bonus = self.evidence_bonuses.get(event.evidence_type, 0)
        evidence_points = int(event.base_points * base_bonus)
        
        # Scale bonus based on evidence strength
        if event.evidence_data.get("improvement_factor"):
            improvement = event.evidence_data["improvement_factor"]
            evidence_points = int(evidence_points * min(improvement, 2.0))
        
        breakdown["evidence_bonus"] = evidence_points
        return evidence_points
    
    def _calculate_streak_bonus(self, context: Optional[Dict], breakdown: Dict) -> float:
        """Calculate streak-based multiplier"""
        if not context or "streak_days" not in context:
            return 1.0
        
        streak_days = context["streak_days"]
        
        if streak_days >= 30:  # 30-day streak
            multiplier = 2.0
        elif streak_days >= 14:  # 2-week streak
            multiplier = 1.5
        elif streak_days >= 7:   # 1-week streak
            multiplier = 1.3
        elif streak_days >= 3:   # 3-day streak
            multiplier = 1.1
        else:
            multiplier = 1.0
        
        breakdown["bonuses"]["streak_multiplier"] = multiplier
        return multiplier
    
    def calculate_level(self, total_xp: int) -> int:
        """Calculate level based on total XP"""
        for level, threshold in enumerate(self.LEVEL_THRESHOLDS):
            if total_xp < threshold:
                return max(1, level)
        return len(self.LEVEL_THRESHOLDS)
    
    def get_level_progress(self, total_xp: int) -> Dict[str, Any]:
        """Get detailed level progress information"""
        current_level = self.calculate_level(total_xp)
        
        if current_level >= len(self.LEVEL_THRESHOLDS):
            # Max level reached
            return {
                "current_level": current_level,
                "current_xp": total_xp,
                "is_max_level": True,
                "progress_percent": 100.0,
                "xp_to_next": 0,
                "next_level_threshold": None
            }
        
        current_threshold = self.LEVEL_THRESHOLDS[current_level - 1] if current_level > 1 else 0
        next_threshold = self.LEVEL_THRESHOLDS[current_level]
        
        xp_in_level = total_xp - current_threshold
        xp_needed = next_threshold - current_threshold
        progress_percent = (xp_in_level / xp_needed) * 100 if xp_needed > 0 else 100
        
        return {
            "current_level": current_level,
            "current_xp": total_xp,
            "is_max_level": False,
            "progress_percent": round(progress_percent, 1),
            "xp_to_next": next_threshold - total_xp,
            "next_level_threshold": next_threshold,
            "xp_in_current_level": xp_in_level,
            "xp_needed_for_level": xp_needed
        }
    
    def calculate_achievement_xp(self, achievement_type: str, rarity: str, context: Dict) -> int:
        """Calculate XP reward for achievement unlocks"""
        base_rewards = {
            "common": 50,
            "rare": 100,
            "epic": 200,
            "legendary": 500
        }
        
        type_multipliers = {
            "usage": 1.0,
            "performance": 1.5,
            "mastery": 2.0,
            "milestone": 2.5,
            "special": 3.0
        }
        
        base_xp = base_rewards.get(rarity, 50)
        multiplier = type_multipliers.get(achievement_type, 1.0)
        
        return int(base_xp * multiplier)
    
    def predict_level_timeline(self, current_xp: int, daily_xp_avg: float) -> Dict[str, Any]:
        """Predict when user will reach next levels"""
        current_level = self.calculate_level(current_xp)
        predictions = []
        
        for target_level in range(current_level + 1, min(current_level + 6, len(self.LEVEL_THRESHOLDS) + 1)):
            xp_needed = self.LEVEL_THRESHOLDS[target_level - 1] - current_xp
            days_needed = xp_needed / daily_xp_avg if daily_xp_avg > 0 else float('inf')
            
            predictions.append({
                "level": target_level,
                "xp_needed": xp_needed,
                "days_estimated": round(days_needed, 1) if days_needed != float('inf') else None,
                "date_estimated": (datetime.utcnow() + timedelta(days=days_needed)).isoformat() if days_needed != float('inf') else None
            })
        
        return {
            "current_level": current_level,
            "current_xp": current_xp,
            "daily_avg": daily_xp_avg,
            "predictions": predictions
        }


class AchievementEngine:
    """
    Achievement detection and unlock engine
    """
    
    def __init__(self, xp_calculator: XPCalculationEngine):
        self.xp_calculator = xp_calculator
    
    def check_achievements(self, user_stats: Dict, agent_stats: Dict, event: XPEventCreate) -> List[str]:
        """
        Check for achievement unlocks based on current stats and new event
        Returns list of achievement names that should be unlocked
        """
        unlocked = []
        
        # XP-based achievements
        total_xp = user_stats.get("total_xp", 0)
        level = self.xp_calculator.calculate_level(total_xp)
        
        # Tier milestone achievements
        if level >= 11 and "adept_tier" not in user_stats.get("achievements", []):
            unlocked.append("adept_tier")
        
        if level >= 31 and "expert_tier" not in user_stats.get("achievements", []):
            unlocked.append("expert_tier")
            
        if level >= 71 and "master_tier" not in user_stats.get("achievements", []):
            unlocked.append("master_tier")
            
        if level >= 121 and "grandmaster_tier" not in user_stats.get("achievements", []):
            unlocked.append("grandmaster_tier")
            
        if level >= 201 and "legend_tier" not in user_stats.get("achievements", []):
            unlocked.append("legend_tier")
        
        # Usage-based achievements
        total_tasks = user_stats.get("total_tasks", 0)
        if total_tasks >= 100 and "centurion" not in user_stats.get("achievements", []):
            unlocked.append("centurion")
        
        if total_tasks >= 1000 and "legend" not in user_stats.get("achievements", []):
            unlocked.append("legend")
        
        # Speed achievements
        if (event.task_duration and event.task_duration < 10 and 
            "speed_demon" not in agent_stats.get("achievements", [])):
            unlocked.append("speed_demon")
        
        # Quality achievements
        if (event.response_quality and event.response_quality >= 0.95 and
            "perfectionist" not in agent_stats.get("achievements", [])):
            unlocked.append("perfectionist")
        
        # Streak achievements
        streak_days = user_stats.get("streak_days", 0)
        if streak_days >= 7 and "week_warrior" not in user_stats.get("achievements", []):
            unlocked.append("week_warrior")
        
        if streak_days >= 30 and "month_master" not in user_stats.get("achievements", []):
            unlocked.append("month_master")
        
        return unlocked
    
    def get_achievement_progress(self, user_stats: Dict, achievement_id: str) -> Dict[str, Any]:
        """
        Get progress towards a specific achievement
        """
        # This would typically query the database for achievement conditions
        # and calculate current progress
        pass