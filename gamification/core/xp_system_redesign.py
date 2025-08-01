#!/usr/bin/env python3
"""
SubAgents XP System Redesign
Realistic progression based on actual Claude Code usage metrics
"""

import json
import math
from datetime import datetime
from typing import Dict, List, Tuple

class XPSystemRedesign:
    def __init__(self):
        # Base XP rates for different actions
        self.base_rates = {
            # Token-based XP (input/output processing)
            "input_tokens_per_xp": 100,      # 1 XP per 100 input tokens
            "output_tokens_per_xp": 50,      # 1 XP per 50 output tokens  
            "cache_tokens_per_xp": 200,      # 1 XP per 200 cache tokens (bonus efficiency)
            
            # Task complexity XP
            "simple_task": 50,               # Quick edits, single file operations
            "medium_task": 200,              # Multi-file changes, debugging
            "complex_task": 500,             # Architecture changes, new features
            "mission_completion": 1000,      # Major project milestones
            
            # Tool usage XP
            "tool_use_base": 10,             # Base XP per tool use
            "tool_combo_multiplier": 1.2,    # Bonus for using multiple tools
            "efficient_tool_multiplier": 1.5, # Bonus for optimal tool selection
            
            # Performance bonuses (multipliers)
            "speed_multiplier": 2.0,         # Fast completion bonus
            "zero_errors_multiplier": 1.5,   # Error-free execution
            "first_try_success_multiplier": 1.3, # Success on first attempt
            
            # Daily engagement XP
            "daily_login": 100,              # Daily activity bonus
            "streak_7_days": 1000,           # Weekly streak bonus
            "streak_30_days": 5000,          # Monthly activity bonus
        }
        
        # Realistic level thresholds for achievable progression
        self.level_thresholds = self._calculate_realistic_thresholds()
        
    def _calculate_realistic_thresholds(self) -> List[int]:
        """Calculate XP thresholds for achievement-based progression"""
        thresholds = [0]  # Level 1 starts at 0 XP
        
        # Levels 2-10 (Novice): 1-2 weeks active use
        # Target: 5,000-15,000 XP (50-150 XP/day for 10-14 days)
        base_xp = 0
        for level in range(2, 11):
            increment = 200 + (level - 2) * 150  # 200, 350, 500, 650, etc.
            base_xp += increment
            thresholds.append(base_xp)
        
        # Levels 11-30 (Adept): Advanced skill development
        # Target: 15,000-60,000 XP - unlocks performance multipliers and streak bonuses
        for level in range(11, 31):
            increment = 800 + (level - 11) * 200  # Gradual increase
            base_xp += increment
            thresholds.append(base_xp)
        
        # Levels 31-70 (Expert): Mastery of complex workflows
        # Target: 60,000-300,000 XP - unlocks multi-tool combos and architecture rewards
        for level in range(31, 71):
            increment = 2000 + (level - 31) * 300
            base_xp += increment
            thresholds.append(base_xp)
        
        # Levels 71-120 (Master): Elite performance tier
        # Target: 300,000-800,000 XP - unlocks maximum multipliers and legendary bonuses
        for level in range(71, 121):
            increment = 8000 + (level - 71) * 500
            base_xp += increment
            thresholds.append(base_xp)
        
        # Levels 121-200 (Grandmaster): Legendary expertise
        # Target: 800,000-2,000,000 XP - unlocks prestige recognition and ultimate status
        for level in range(121, 201):
            increment = 15000 + (level - 121) * 1000
            base_xp += increment
            thresholds.append(base_xp)
        
        # Levels 201+ (Legend): Ultimate mastery achievement
        # Target: 2,000,000+ XP - mythical status and exclusive recognition
        for level in range(201, 301):
            increment = 30000 + (level - 201) * 2000
            base_xp += increment
            thresholds.append(base_xp)
            
        return thresholds
    
    def _get_tier_info(self, level):
        """Get tier information for a level"""
        if level <= 10:
            return {"tier": "Novice", "color": "🟢"}
        elif level <= 30:
            return {"tier": "Adept", "color": "🔵"}
        elif level <= 70:
            return {"tier": "Expert", "color": "🟡"}
        elif level <= 120:
            return {"tier": "Master", "color": "🟠"}
        elif level <= 200:
            return {"tier": "Grandmaster", "color": "🔴"}
        else:
            return {"tier": "Legend", "color": "💎"}
    
    def calculate_session_xp(self, session_data: Dict) -> Tuple[int, Dict]:
        """Calculate XP for a single Claude Code session"""
        total_xp = 0
        breakdown = {}
        
        # Token-based XP
        if "tokens" in session_data:
            tokens = session_data["tokens"]
            
            input_xp = tokens.get("input", 0) // self.base_rates["input_tokens_per_xp"]
            output_xp = tokens.get("output", 0) // self.base_rates["output_tokens_per_xp"]
            cache_xp = tokens.get("cache", 0) // self.base_rates["cache_tokens_per_xp"]
            
            token_xp = input_xp + output_xp + cache_xp
            total_xp += token_xp
            breakdown["tokens"] = {
                "input_xp": input_xp,
                "output_xp": output_xp,
                "cache_xp": cache_xp,
                "total": token_xp
            }
        
        # Task complexity XP
        if "tasks" in session_data:
            task_xp = 0
            for task in session_data["tasks"]:
                complexity = task.get("complexity", "simple")
                task_xp += self.base_rates.get(f"{complexity}_task", 50)
            
            total_xp += task_xp
            breakdown["tasks"] = task_xp
        
        # Tool usage XP
        if "tools_used" in session_data:
            tools = session_data["tools_used"]
            tool_xp = len(tools) * self.base_rates["tool_use_base"]
            
            # Multi-tool combo bonus
            if len(tools) > 3:
                tool_xp = int(tool_xp * self.base_rates["tool_combo_multiplier"])
            
            # Efficiency bonus for optimal tool selection
            if session_data.get("efficient_tools", False):
                tool_xp = int(tool_xp * self.base_rates["efficient_tool_multiplier"])
            
            total_xp += tool_xp
            breakdown["tools"] = tool_xp
        
        # Performance multipliers
        multiplier = 1.0
        multiplier_reasons = []
        
        if session_data.get("fast_completion", False):
            multiplier *= self.base_rates["speed_multiplier"]
            multiplier_reasons.append("Speed Demon")
        
        if session_data.get("zero_errors", False):
            multiplier *= self.base_rates["zero_errors_multiplier"] 
            multiplier_reasons.append("Flawless Execution")
        
        if session_data.get("first_try_success", False):
            multiplier *= self.base_rates["first_try_success_multiplier"]
            multiplier_reasons.append("First Try Success")
        
        # Apply multipliers
        if multiplier > 1.0:
            bonus_xp = int(total_xp * (multiplier - 1.0))
            total_xp = int(total_xp * multiplier)
            breakdown["performance_bonus"] = {
                "multiplier": multiplier,
                "bonus_xp": bonus_xp,
                "reasons": multiplier_reasons
            }
        
        # Daily engagement bonuses
        engagement_xp = 0
        if session_data.get("daily_login", False):
            engagement_xp += self.base_rates["daily_login"]
        
        if session_data.get("streak_days", 0) >= 7:
            engagement_xp += self.base_rates["streak_7_days"]
        
        if session_data.get("streak_days", 0) >= 30:
            engagement_xp += self.base_rates["streak_30_days"]
        
        if engagement_xp > 0:
            total_xp += engagement_xp
            breakdown["engagement"] = engagement_xp
        
        return total_xp, breakdown
    
    def get_level_from_xp(self, xp: int) -> int:
        """Get level based on XP using new thresholds"""
        for level, threshold in enumerate(self.level_thresholds):
            if xp < threshold:
                return level
        return len(self.level_thresholds)
    
    def get_xp_for_level(self, level: int) -> int:
        """Get XP required for a specific level"""
        if level <= 0:
            return 0
        if level >= len(self.level_thresholds):
            return self.level_thresholds[-1]
        return self.level_thresholds[level - 1]
    
    def get_tier_info(self, level: int) -> Dict:
        """Get tier information for a level"""
        if level <= 10:
            return {"tier": "Novice", "color": "🟢", "description": "Learning the basics"}
        elif level <= 30:
            return {"tier": "Adept", "color": "🔵", "description": "Developing expertise"}
        elif level <= 70:
            return {"tier": "Expert", "color": "🟡", "description": "Mastering techniques"}
        elif level <= 120:
            return {"tier": "Master", "color": "🟠", "description": "Elite performance"}
        elif level <= 200:
            return {"tier": "Grandmaster", "color": "🔴", "description": "Legendary status"}
        else:
            return {"tier": "Legend", "color": "💎", "description": "Ultimate mastery"}
    
    def calculate_progression_timeframes(self) -> Dict:
        """Calculate realistic timeframes for reaching each tier"""
        scenarios = {
            "casual_user": {"xp_per_day": 300, "description": "Casual daily use"},
            "regular_user": {"xp_per_day": 800, "description": "Regular active use"},  
            "power_user": {"xp_per_day": 1500, "description": "Heavy daily use"},
            "professional": {"xp_per_day": 2500, "description": "Professional daily use"}
        }
        
        milestones = [
            {"level": 10, "name": "Novice Mastery"},
            {"level": 30, "name": "Adept Status"},
            {"level": 70, "name": "Expert Tier"},
            {"level": 120, "name": "Master Rank"},
            {"level": 200, "name": "Grandmaster"},
            {"level": 250, "name": "Legend Status"}
        ]
        
        results = {}
        for scenario_name, scenario in scenarios.items():
            results[scenario_name] = {}
            daily_xp = scenario["xp_per_day"]
            
            for milestone in milestones:
                level = milestone["level"]
                if level < len(self.level_thresholds):
                    xp_needed = self.level_thresholds[level - 1]
                    sessions_needed = math.ceil(xp_needed / daily_xp)
                    
                    results[scenario_name][milestone["name"]] = {
                        "level": level,
                        "xp_needed": xp_needed,
                        "sessions_needed": sessions_needed,
                        "tier_info": self._get_tier_info(level)
                    }
        
        return results
    
    def display_progression_analysis(self):
        """Display comprehensive progression analysis"""
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                    REDESIGNED XP SYSTEM ANALYSIS                            ║")
        print("║                     Realistic Progression Timelines                         ║")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        
        # Show XP rates
        print("║                                                                              ║")
        print("║ 💰 XP EARNING OPPORTUNITIES:                                                ║")
        print("║ ─────────────────────────────────────────────────────────────────────── ║")
        print(f"║ • Input processing: 1 XP per {self.base_rates['input_tokens_per_xp']} tokens                             ║")
        print(f"║ • Output generation: 1 XP per {self.base_rates['output_tokens_per_xp']} tokens                            ║")
        print(f"║ • Simple task: {self.base_rates['simple_task']} XP                                                   ║")
        print(f"║ • Medium task: {self.base_rates['medium_task']} XP                                                  ║")
        print(f"║ • Complex task: {self.base_rates['complex_task']} XP                                                 ║")
        print(f"║ • Mission completion: {self.base_rates['mission_completion']} XP                                            ║")
        print(f"║ • Daily login bonus: {self.base_rates['daily_login']} XP                                             ║")
        print(f"║ • Weekly streak: {self.base_rates['streak_7_days']} XP                                              ║")
        print("║                                                                              ║")
        
        # Show realistic scenarios
        print("║ 📊 PROGRESSION SCENARIOS:                                                   ║")
        print("║ ─────────────────────────────────────────────────────────────────────── ║")
        
        timeframes = self.calculate_progression_timeframes()
        
        for scenario_name, scenario_data in timeframes.items():
            if scenario_name == "regular_user":  # Show detailed breakdown for regular user
                print(f"║                                                                              ║")
                print(f"║ 🎯 REGULAR USER TIMELINE (800 XP/day average):                             ║")
                print("║ ─────────────────────────────────────────────────────────────────────── ║")
                
                for milestone_name, data in scenario_data.items():
                    level = data["level"]
                    # tier_info already available from data
                    
                    sessions = data["sessions_needed"]
                    if sessions < 10:
                        session_str = f"{sessions} sessions"
                    elif sessions < 100:
                        session_str = f"{sessions} sessions"
                    else:
                        session_str = f"{sessions:,} sessions"
                    
                    tier_info = data["tier_info"]
                    print(f"║ • {milestone_name:<20} (Lv.{level}): {session_str:<15} {tier_info['color']} {tier_info['tier']:<12} ║")
        
        print("║                                                                              ║")
        print("║ 📈 COMPARISON WITH OLD SYSTEM:                                              ║")
        print("║ ─────────────────────────────────────────────────────────────────────── ║")
        
        # Compare specific milestones
        old_system_days = {
            "Expert (Lv.70)": 5977,  # From old calculation
            "Master (Lv.120)": 71902,
            "Grandmaster (Lv.200)": 403382
        }
        
        regular_user = timeframes["regular_user"]
        for old_milestone, old_days in old_system_days.items():
            milestone_name = old_milestone.split("(")[0].strip()
            if milestone_name == "Expert":
                new_days = regular_user["Expert Tier"]["days"]
            elif milestone_name == "Master":
                new_days = regular_user["Master Rank"]["days"]  
            elif milestone_name == "Grandmaster":
                new_days = regular_user["Grandmaster"]["days"]
            
            improvement = old_days / new_days
            print(f"║ • {old_milestone:<20}: {old_days:>6} → {new_days:>3} days ({improvement:.0f}x faster) ║")
        
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
    
    def generate_sample_sessions(self) -> List[Dict]:
        """Generate sample session data to demonstrate XP calculations"""
        return [
            {
                "name": "Quick Code Edit",
                "tokens": {"input": 500, "output": 200, "cache": 100},
                "tasks": [{"complexity": "simple"}],
                "tools_used": ["Edit", "Read"],
                "zero_errors": True,
                "daily_login": True
            },
            {
                "name": "Complex Feature Implementation", 
                "tokens": {"input": 2000, "output": 1500, "cache": 500},
                "tasks": [{"complexity": "complex"}, {"complexity": "medium"}],
                "tools_used": ["Grep", "Edit", "MultiEdit", "Bash", "Write"],
                "efficient_tools": True,
                "fast_completion": True,
                "first_try_success": True,
                "streak_days": 7
            },
            {
                "name": "Debug Session",
                "tokens": {"input": 1200, "output": 800, "cache": 300},
                "tasks": [{"complexity": "medium"}, {"complexity": "simple"}],
                "tools_used": ["Grep", "Read", "Edit", "Bash"],
                "zero_errors": True,
                "daily_login": True
            }
        ]
    
    def demonstrate_xp_calculation(self):
        """Show examples of XP calculations"""
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                        XP CALCULATION EXAMPLES                              ║")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        
        samples = self.generate_sample_sessions()
        
        for i, session in enumerate(samples, 1):
            xp, breakdown = self.calculate_session_xp(session)
            
            print("║                                                                              ║")
            print(f"║ {i}. {session['name'].upper():<68} ║")
            print("║ ─────────────────────────────────────────────────────────────────────── ║")
            
            # Show breakdown
            if "tokens" in breakdown:
                token_data = breakdown["tokens"]
                print(f"║ • Token processing: {token_data['total']:<3} XP                                          ║")
            
            if "tasks" in breakdown:
                print(f"║ • Task completion: {breakdown['tasks']:<3} XP                                           ║")
            
            if "tools" in breakdown:
                print(f"║ • Tool usage: {breakdown['tools']:<3} XP                                               ║")
            
            if "performance_bonus" in breakdown:
                bonus_data = breakdown["performance_bonus"]
                reasons = ", ".join(bonus_data["reasons"])
                print(f"║ • Performance bonus: +{bonus_data['bonus_xp']:<3} XP ({reasons})                    ║")
            
            if "engagement" in breakdown:
                print(f"║ • Daily engagement: {breakdown['engagement']:<3} XP                                       ║")
            
            print(f"║                                                                              ║")
            print(f"║ 🎯 TOTAL SESSION XP: {xp:<3} XP                                             ║")
        
        print("╚══════════════════════════════════════════════════════════════════════════════╝")


if __name__ == "__main__":
    import sys
    
    redesign = XPSystemRedesign()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "analysis":
            redesign.display_progression_analysis()
        elif command == "examples":
            redesign.demonstrate_xp_calculation()
        elif command == "all":
            redesign.display_progression_analysis()
            print("\n")
            redesign.demonstrate_xp_calculation()
        else:
            print("Usage:")
            print("  python xp_system_redesign.py [command]")
            print("Commands:")
            print("  analysis  - Show session-based progression analysis")
            print("  examples  - Show XP calculation examples")
            print("  all       - Show everything")
    else:
        # Default: show analysis
        redesign.display_progression_analysis()