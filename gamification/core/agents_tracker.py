#!/usr/bin/env python3
"""
SubAgents XP Tracker
Monitors Claude Code interactions and tracks agent performance with real log data
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Import the new agent registry and log parser for enhanced tracking
try:
    from agent_registry import AgentRegistry
    REGISTRY_AVAILABLE = True
except ImportError:
    REGISTRY_AVAILABLE = False

try:
    from log_parser import ClaudeCodeLogParser
    LOG_PARSER_AVAILABLE = True
except ImportError:
    LOG_PARSER_AVAILABLE = False

class AgentsTracker:
    def __init__(self, data_file: str = ".claude/agents-tracker.json"):
        self.data_file = Path(data_file)
        self.data = self._load_data()
        
        # Initialize agent registry and log parser if available
        self.registry = AgentRegistry() if REGISTRY_AVAILABLE else None
        self.log_parser = ClaudeCodeLogParser() if LOG_PARSER_AVAILABLE else None
        
    def _load_data(self) -> Dict:
        """Load existing tracking data or create new"""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        
        # Initialize new tracking data
        return {
            "agents": {},
            "missions": [],
            "achievements_unlocked": [],
            "total_xp": 0,
            "stats": {
                "total_missions": 0,
                "success_rate": 0,
                "avg_completion_time": 0
            },
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_data(self):
        """Persist tracking data"""
        self.data["last_updated"] = datetime.now().isoformat()
        self.data_file.parent.mkdir(exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def log_agent_call(self, agent_name: str, task: str, success: bool, 
                      error_msg: Optional[str] = None, duration_seconds: float = 0,
                      session_data: Optional[Dict] = None):
        """Log when an agent is called and track its performance with realistic XP"""
        
        # Update agent registry stats if available
        if self.registry:
            # Calculate XP for registry (simpler calculation)
            registry_xp = 50 if success else 10
            self.registry.update_agent_stats(agent_name, success, registry_xp)
        
        # Initialize agent if first time
        if agent_name not in self.data["agents"]:
            self.data["agents"][agent_name] = {
                "level": 1,
                "xp": 0,
                "total_calls": 0,
                "successful_tasks": 0,
                "failed_tasks": 0,
                "errors_resolved": 0,
                "avg_task_time": 0,
                "specialties": [],
                "achievements": [],
                "last_used": datetime.now().isoformat(),
                "daily_streak": 0,
                "last_login_date": None
            }
        
        agent = self.data["agents"][agent_name]
        agent["total_calls"] += 1
        agent["last_used"] = datetime.now().isoformat()
        
        # Update daily streak
        today = datetime.now().date().isoformat()
        if agent["last_login_date"] != today:
            if agent["last_login_date"] == (datetime.now().date() - timedelta(days=1)).isoformat():
                agent["daily_streak"] += 1
            else:
                agent["daily_streak"] = 1
            agent["last_login_date"] = today
        
        # Calculate XP using new system
        from xp_system_redesign import XPSystemRedesign
        redesign = XPSystemRedesign()
        
        # Create session data for XP calculation
        if session_data is None:
            session_data = {}
        
        # Add task complexity based on task description
        if "tasks" not in session_data:
            complexity = self._determine_task_complexity(task)
            session_data["tasks"] = [{"complexity": complexity}]
        
        # Add performance bonuses
        if success:
            agent["successful_tasks"] += 1
            session_data["zero_errors"] = True
            
            if duration_seconds > 0 and duration_seconds < 60:
                session_data["fast_completion"] = True
                
            if agent["failed_tasks"] == 0 or (agent["successful_tasks"] / max(agent["total_calls"], 1)) > 0.9:
                session_data["first_try_success"] = True
        else:
            agent["failed_tasks"] += 1
            if error_msg and "resolved" in error_msg.lower():
                agent["errors_resolved"] += 1
        
        # Add daily engagement bonuses
        session_data["daily_login"] = True
        session_data["streak_days"] = agent["daily_streak"]
        
        # Calculate XP
        xp_gained, xp_breakdown = redesign.calculate_session_xp(session_data)
        
        # Update XP and check for level up
        agent["xp"] += xp_gained
        old_level = agent["level"]
        agent["level"] = self._calculate_level(agent["xp"])
        
        # Log the mission
        mission = {
            "id": len(self.data["missions"]) + 1,
            "agent": agent_name,
            "task": task,
            "success": success,
            "xp_gained": xp_gained,
            "xp_breakdown": xp_breakdown,
            "duration": duration_seconds,
            "timestamp": datetime.now().isoformat(),
            "error": error_msg
        }
        self.data["missions"].append(mission)
        
        # Check for achievements
        self._check_achievements(agent_name, agent, old_level)
        
        # Update global stats
        self.data["total_xp"] = sum(a["xp"] for a in self.data["agents"].values())
        self._update_stats()
        
        self._save_data()
        
        return {
            "xp_gained": xp_gained,
            "xp_breakdown": xp_breakdown,
            "new_level": agent["level"],
            "level_up": agent["level"] > old_level,
            "total_xp": agent["xp"]
        }
    
    def _determine_task_complexity(self, task: str) -> str:
        """Determine task complexity from description"""
        task_lower = task.lower()
        
        # Complex task indicators
        complex_keywords = ["architecture", "refactor", "implement", "design", "system", "framework", "api", "database"]
        medium_keywords = ["debug", "fix", "update", "modify", "enhance", "optimize", "test", "analyze"]
        
        if any(keyword in task_lower for keyword in complex_keywords):
            return "complex"
        elif any(keyword in task_lower for keyword in medium_keywords):
            return "medium"
        else:
            return "simple"
    
    def _calculate_level(self, xp: int) -> int:
        """Calculate level based on realistic XP thresholds"""
        # Import the new XP system for level calculation
        from xp_system_redesign import XPSystemRedesign
        redesign = XPSystemRedesign()
        return redesign.get_level_from_xp(xp)
    
    def _check_achievements(self, agent_name: str, agent: Dict, old_level: int):
        """Check and unlock achievements"""
        achievements = []
        
        # First Blood - First successful task
        if agent["successful_tasks"] == 1 and "first-blood" not in agent["achievements"]:
            achievements.append("first-blood")
            agent["xp"] += 50  # Achievement bonus
            
        # Speed Demon - 5 tasks completed in under 1 minute
        fast_tasks = [m for m in self.data["missions"] 
                     if m["agent"] == agent_name and m["duration"] < 60]
        if len(fast_tasks) >= 5 and "speed-demon" not in agent["achievements"]:
            achievements.append("speed-demon")
            agent["xp"] += 100
            
        # Bug Hunter - Resolved 10 errors
        if agent["errors_resolved"] >= 10 and "bug-hunter" not in agent["achievements"]:
            achievements.append("bug-hunter")
            agent["xp"] += 150
            
        # Level achievements
        if agent["level"] > old_level:
            if agent["level"] == 3 and "expert" not in agent["achievements"]:
                achievements.append("expert")
                agent["xp"] += 100
            elif agent["level"] == 5 and "elite" not in agent["achievements"]:
                achievements.append("elite")
                agent["xp"] += 200
        
        # Add achievements
        for achievement in achievements:
            agent["achievements"].append(achievement)
            self.data["achievements_unlocked"].append({
                "agent": agent_name,
                "achievement": achievement,
                "timestamp": datetime.now().isoformat()
            })
    
    def _update_stats(self):
        """Update global statistics"""
        missions = self.data["missions"]
        if missions:
            successful = sum(1 for m in missions if m["success"])
            self.data["stats"]["total_missions"] = len(missions)
            self.data["stats"]["success_rate"] = (successful / len(missions)) * 100
            
            durations = [m["duration"] for m in missions if m["duration"] > 0]
            if durations:
                self.data["stats"]["avg_completion_time"] = sum(durations) / len(durations)
    
    def get_tier_info(self, level: int) -> Dict:
        """Get tier information for a level"""
        from xp_system_redesign import XPSystemRedesign
        redesign = XPSystemRedesign()
        return redesign.get_tier_info(level)
    
    def get_leaderboard(self) -> List[Dict]:
        """Get agent leaderboard sorted by XP"""
        agents = []
        for name, data in self.data["agents"].items():
            agents.append({
                "name": name,
                "level": data["level"],
                "xp": data["xp"],
                "missions": data["successful_tasks"],
                "achievements": len(data["achievements"])
            })
        return sorted(agents, key=lambda x: x["xp"], reverse=True)
    
    def get_agent_card(self, agent_name: str) -> str:
        """Generate ASCII trading card for an agent"""
        if agent_name not in self.data["agents"]:
            return "Agent not found!"
            
        agent = self.data["agents"][agent_name]
        level_stars = "★" * agent["level"] + "☆" * (5 - agent["level"])
        
        # Calculate skill bars
        success_rate = (agent["successful_tasks"] / max(agent["total_calls"], 1)) * 100
        speed_score = min(100, (60 / max(self.data["stats"]["avg_completion_time"], 1)) * 100)
        
        card = f"""
┌─────────────────────────┐
│ {level_stars} {agent_name.upper():<15} │
├─────────────────────────┤
│    Level {agent["level"]} {"Elite" if agent["level"] >= 5 else "Expert" if agent["level"] >= 3 else "Agent"}      │
├─────────────────────────┤
│ Stats:                  │
│ • XP: {agent["xp"]:<6} 
│ • Missions: {agent["successful_tasks"]:<4}        │
│ • Success: {success_rate:.0f}%          │
├─────────────────────────┤
│ Achievements: {len(agent["achievements"]):<2}        │
│ Latest: {agent["achievements"][-1] if agent["achievements"] else "None":<14} │
└─────────────────────────┘
"""
        return card
    
    def get_enhanced_agent_info(self, agent_name: str) -> Dict:
        """Get enhanced agent information including registry metadata"""
        agent_info = {
            "name": agent_name,
            "stats": self.data["agents"].get(agent_name, {}),
            "registry_metadata": None
        }
        
        if self.registry:
            metadata = self.registry.get_agent_by_name(agent_name)
            if metadata:
                agent_info["registry_metadata"] = {
                    "description": metadata.description,
                    "category": metadata.category,
                    "tech_stack": metadata.tech_stack,
                    "specialties": metadata.specialties,
                    "difficulty_level": metadata.difficulty_level
                }
        
        return agent_info

    def generate_mission_report(self) -> str:
        """Generate a mission summary report"""
        stats = self.data["stats"]
        recent_missions = self.data["missions"][-5:]
        
        report = f"""
╔═══════════════════════════════════════════════════════════╗
║              ELITE SQUAD PERFORMANCE REPORT               ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Total Missions: {stats["total_missions"]:<6}                               ║
║  Success Rate: {stats["success_rate"]:.1f}%                                  ║
║  Avg Time: {stats["avg_completion_time"]:.1f}s                                     ║
║  Total Squad XP: {self.data["total_xp"]:,}                           ║
║                                                           ║
║  Recent Missions:                                         ║
"""
        for mission in recent_missions:
            status = "✓" if mission["success"] else "✗"
            report += f"║  {status} {mission['agent']:<15}: +{mission['xp_gained']:,} XP\n"
            
        report += "╚═══════════════════════════════════════════════════════════╝"
        return report


# CLI Interface
if __name__ == "__main__":
    import sys
    
    tracker = SquadTracker()
    
    if len(sys.argv) < 2:
        print("Usage: python squad-tracker.py [command]")
        print("Commands: log, leaderboard, card [agent], report")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "log" and len(sys.argv) >= 5:
        # Log agent call: squad-tracker.py log agent-name "task description" success/fail
        agent = sys.argv[2]
        task = sys.argv[3]
        success = sys.argv[4].lower() == "success"
        result = tracker.log_agent_call(agent, task, success)
        
        print(f"Mission logged! +{result['xp_gained']} XP")
        if result["level_up"]:
            print(f"🎉 LEVEL UP! {agent} is now Level {result['new_level']}!")
            
    elif command == "leaderboard":
        leaders = tracker.get_leaderboard()
        print("\n🏆 ELITE SQUAD LEADERBOARD")
        print("=" * 50)
        for i, agent in enumerate(leaders[:10], 1):
            level = agent['level']
            tier_info = tracker.get_tier_info(level)
            tier_display = f"{tier_info['tier']} {tier_info['color']}"
            print(f"{i}. {agent['name']:<20} Lv.{level:<3} {tier_display:<15} - {agent['xp']:,} XP")
            
    elif command == "card" and len(sys.argv) >= 3:
        agent_name = sys.argv[2]
        print(tracker.get_agent_card(agent_name))
        
    elif command == "report":
        print(tracker.generate_mission_report())
    
    else:
        print("Invalid command or arguments")