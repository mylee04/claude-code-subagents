#!/usr/bin/env python3
"""
Agents Levels - Display agent levels in a format that matches /agents view
"""

import os
import json
from pathlib import Path
from agents_tracker import AgentsTracker

class AgentsLevels:
    def __init__(self):
        self.tracker = AgentsTracker()
        self.personal_agents_dir = Path.home() / ".claude" / "agents"
        self.project_agents_dir = Path(".claude") / "agents"
        
    def scan_available_agents(self):
        """Scan for all available agents in the system"""
        agents = {
            "personal": [],
            "project": [],
            "builtin": ["general-purpose"]
        }
        
        # Scan personal agents
        if self.personal_agents_dir.exists():
            for agent_file in self.personal_agents_dir.glob("**/*.md"):
                agent_name = agent_file.stem
                agents["personal"].append(agent_name)
                
        # Scan project agents  
        if self.project_agents_dir.exists():
            for agent_file in self.project_agents_dir.glob("**/*.md"):
                agent_name = agent_file.stem
                agents["project"].append(agent_name)
                
        return agents
        
    def get_level_thresholds(self):
        """Get realistic XP thresholds from redesigned system"""
        from xp_system_redesign import XPSystemRedesign
        redesign = XPSystemRedesign()
        return redesign.level_thresholds
    
    def get_tier_info(self, level):
        """Get tier name and visual representation for a level"""
        if level <= 10:
            return {"tier": "Novice", "color": "🟢", "stars": min(level, 5)}
        elif level <= 30:
            return {"tier": "Adept", "color": "🔵", "stars": min(5, 3 + (level - 10) // 5)}
        elif level <= 70:
            return {"tier": "Expert", "color": "🟡", "stars": 5}
        elif level <= 120:
            return {"tier": "Master", "color": "🟠", "stars": 5}
        elif level <= 200:
            return {"tier": "Grandmaster", "color": "🔴", "stars": 5}
        else:
            return {"tier": "Legend", "color": "💎", "stars": 5}
    
    def get_agent_level_display(self, agent_name):
        """Get level display for an agent with new tier system"""
        if agent_name in self.tracker.data["agents"]:
            agent = self.tracker.data["agents"][agent_name]
            level = agent["level"]
            xp = agent["xp"]
            
            # Get tier info
            tier_info = self.get_tier_info(level)
            
            # Level indicators with tier-based stars
            star_count = tier_info["stars"]
            level_stars = "★" * star_count + "☆" * (5 - star_count)
            level_name = f"{tier_info['tier']} {tier_info['color']}"
            
            # Progress to next level
            thresholds = self.get_level_thresholds()
            if level < len(thresholds) - 1:
                current_threshold = thresholds[level - 1] if level > 1 else 0
                next_threshold = thresholds[level] if level < len(thresholds) else thresholds[-1]
                progress = (xp - current_threshold) / max(next_threshold - current_threshold, 1)
                progress_bar = "█" * int(progress * 10) + "░" * (10 - int(progress * 10))
            else:
                progress_bar = "██████████"
                
            return {
                "stars": level_stars,
                "name": level_name,
                "tier": tier_info["tier"],
                "level": level,
                "xp": xp,
                "progress": progress_bar,
                "next_xp": thresholds[level] if level < len(thresholds) else "MAX"
            }
        else:
            return {
                "stars": "☆☆☆☆☆",
                "name": "Unranked 🔘",
                "tier": "Unranked",
                "level": 0,
                "xp": 0,
                "progress": "░░░░░░░░░░",
                "next_xp": self.get_level_thresholds()[1]  # XP needed for level 2
            }
            
    def display_agents_with_levels(self):
        """Display agents in a format similar to /agents with level info"""
        agents = self.scan_available_agents()
        
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║                      SUBAGENTS LEVELS                          ║")
        print("╠═══════════════════════════════════════════════════════════════╣")
        print(f"║ Total Agents: {len(agents['personal']) + len(agents['project'])}                                              ║")
        print("╠═══════════════════════════════════════════════════════════════╣")
        
        # Personal agents
        if agents["personal"]:
            print("║                                                               ║")
            print("║ 📁 Personal agents (~/.claude/agents)                         ║")
            print("║ ─────────────────────────────────────────────────────────── ║")
            
            for agent in sorted(agents["personal"]):
                level_info = self.get_agent_level_display(agent)
                # Format: agent-name · Lv.15 Adept 🔵 ★★★★★ [████░░░░░░]
                line = f"║ {agent:<20} Lv.{level_info['level']:<3} {level_info['name']:<15} {level_info['stars']} │"
                print(line.ljust(64) + "║")
                
        # Project agents
        if agents["project"]:
            print("║                                                               ║")
            print("║ 📁 Project agents (.claude/agents)                            ║")
            print("║ ─────────────────────────────────────────────────────────── ║")
            
            for agent in sorted(agents["project"]):
                level_info = self.get_agent_level_display(agent)
                line = f"║ {agent:<20} Lv.{level_info['level']:<3} {level_info['name']:<15} {level_info['stars']} │"
                print(line.ljust(64) + "║")
                
        print("╚═══════════════════════════════════════════════════════════════╝")
        
        # Show top performers
        leaders = self.tracker.get_leaderboard()
        if leaders:
            print("\n🏆 SubAgents Champions:")
            for i, agent in enumerate(leaders[:5], 1):
                level_info = self.get_agent_level_display(agent['name'])
                tier_display = level_info['tier']
                print(f"{i}. {agent['name']:<20} Lv.{agent['level']:<3} {tier_display:<12} - {agent['xp']:,} XP - {agent['achievements']} achievements")
                
    def generate_level_badge(self, agent_name):
        """Generate a visual level badge for an agent"""
        level_info = self.get_agent_level_display(agent_name)
        
        badge = f"""
╭─────────────────────────╮
│ {agent_name.upper():<23} │
├─────────────────────────┤
│ {level_info['stars']:<23} │
│ Level {level_info['level']:<3} {level_info['name']:<15} │
│ {level_info['xp']:,} XP [{level_info['progress']}] │
│ Next: {level_info['next_xp'] if isinstance(level_info['next_xp'], str) else f"{level_info['next_xp']:,}"} XP │
╰─────────────────────────╯
"""
        return badge
        
    def quick_level_check(self, agent_name):
        """Quick one-line level check"""
        level_info = self.get_agent_level_display(agent_name)
        return f"{agent_name}: Lv.{level_info['level']} {level_info['tier']} {level_info['stars']} ({level_info['xp']:,} XP)"


# CLI Interface
if __name__ == "__main__":
    import sys
    
    levels = AgentsLevels()
    
    if len(sys.argv) < 2:
        # Default: show all agents with levels
        levels.display_agents_with_levels()
    else:
        command = sys.argv[1]
        
        if command == "badge" and len(sys.argv) >= 3:
            # Show badge for specific agent
            agent_name = sys.argv[2]
            print(levels.generate_level_badge(agent_name))
            
        elif command == "check" and len(sys.argv) >= 3:
            # Quick level check
            agent_name = sys.argv[2]
            print(levels.quick_level_check(agent_name))
            
        elif command == "scan":
            # Just list available agents
            agents = levels.scan_available_agents()
            print(f"Found {len(agents['personal'])} personal agents")
            print(f"Found {len(agents['project'])} project agents")
            
        else:
            print("Usage:")
            print("  ./squad-levels.py         - Show all agents with levels")
            print("  ./squad-levels.py badge [agent]  - Show level badge") 
            print("  ./squad-levels.py check [agent]  - Quick level check")
            print("  ./squad-levels.py scan    - Scan for available agents")