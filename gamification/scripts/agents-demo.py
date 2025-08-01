#!/usr/bin/env python3
"""
SubAgents Interactive Demo
Shows the gamification system in action
"""

import time
import random
import os
import sys

# Add parent directory to path to import from core
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'core'))
from agents_tracker import AgentsTracker

class AgentsDemo:
    def __init__(self):
        self.tracker = AgentsTracker(".claude/demo-agents.json")
        self.clear_screen()
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
    def type_text(self, text, delay=0.03):
        """Simulate typing effect"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
        
    def show_mission_briefing(self, mission_name, agents):
        print("\n" + "━" * 60)
        print(f"🎯 MISSION BRIEFING: {mission_name}")
        print("━" * 60)
        print(f"\nDifficulty: {'⭐' * random.randint(3, 5)}")
        print(f"Required Squad: {', '.join(agents)}")
        print("\nObjectives:")
        print("□ Design system architecture")
        print("□ Implement core functionality") 
        print("□ Add security measures")
        print("□ Deploy to production")
        print("\n[DEPLOY SQUAD] [ABORT MISSION]")
        input("\nPress Enter to deploy squad...")
        
    def simulate_agent_work(self, agent_name, task, duration=3):
        """Simulate an agent working on a task"""
        print(f"\n🤖 {agent_name} is working on: {task}")
        
        # Progress bar
        for i in range(20):
            print(f"\rProgress: [{'█' * i}{'░' * (20-i)}] {i*5}%", end='', flush=True)
            time.sleep(duration/20)
        
        # Determine success (90% success rate for demo)
        success = random.random() < 0.9
        
        if success:
            print(f"\r✅ {agent_name} completed: {task}                    ")
            result = self.tracker.log_agent_call(agent_name, task, True, duration_seconds=duration)
            print(f"   +{result['xp_gained']} XP earned!")
            
            if result['level_up']:
                print(f"\n🎉 LEVEL UP! {agent_name} reached Level {result['new_level']}!")
                time.sleep(2)
        else:
            print(f"\r❌ {agent_name} encountered an error!")
            error_msg = "Type mismatch in API response"
            print(f"   Error: {error_msg}")
            time.sleep(1)
            
            # Simulate error resolution
            print(f"   🔧 {agent_name} is debugging...")
            time.sleep(2)
            print(f"   ✅ Error resolved!")
            result = self.tracker.log_agent_call(agent_name, task, False, 
                                               error_msg="Error resolved: " + error_msg,
                                               duration_seconds=duration+2)
            print(f"   +{result['xp_gained']} XP earned for learning from error!")
            
        return success
        
    def show_live_collaboration(self):
        """Show agents working together with visual flow"""
        print("\n" + "┌" + "─" * 57 + "┐")
        print("│          LIVE MISSION: Build User Authentication         │")
        print("├" + "─" * 57 + "┤")
        print("│                                                         │")
        print("│  [backend-architect] ═══► [security-auditor]          │")
        print("│         ║                        ║                      │")
        print("│         ╚════► [frontend-developer] ═══► [test-engineer]│")
        print("│                                                         │")
        print("├" + "─" * 57 + "┤")
        print("│ Status: ACTIVE | Squad Size: 4 | Mission XP: 0        │")
        print("└" + "─" * 57 + "┘")
        
    def run_demo(self):
        """Run the interactive demo"""
        self.type_text("\n🎮 Welcome to the SubAgents Demo!\n")
        time.sleep(1)
        
        # Mission 1: Simple task
        self.type_text("📋 New mission available: Optimize Database Queries")
        time.sleep(1)
        
        agents = ["database-optimizer", "performance-engineer"]
        self.show_mission_briefing("Database Optimization", agents)
        
        # Simulate work
        total_xp = 0
        for agent in agents:
            if agent == "database-optimizer":
                success = self.simulate_agent_work(agent, "Analyzing slow queries", 2)
                if success:
                    success = self.simulate_agent_work(agent, "Creating optimized indexes", 3)
            else:
                success = self.simulate_agent_work(agent, "Profiling application performance", 2)
                
        # Mission 2: Complex collaborative task
        print("\n" + "="*60)
        self.type_text("\n📋 New mission available: Build Real-Time Chat Feature")
        time.sleep(1)
        
        agents = ["backend-architect", "security-auditor", "frontend-developer", "test-engineer"]
        self.show_mission_briefing("Real-Time Chat Implementation", agents)
        
        # Show live collaboration
        self.show_live_collaboration()
        time.sleep(2)
        
        # Phase 1: Architecture
        print("\n🏗️ Phase 1: Architecture Design")
        self.simulate_agent_work("backend-architect", "Designing WebSocket architecture", 3)
        
        # Phase 2: Security  
        print("\n🔒 Phase 2: Security Implementation")
        self.simulate_agent_work("security-auditor", "Implementing authentication", 4)
        
        # Phase 3: Frontend
        print("\n💻 Phase 3: UI Development")  
        self.simulate_agent_work("frontend-developer", "Building chat components", 3)
        
        # Phase 4: Testing
        print("\n🧪 Phase 4: Testing")
        self.simulate_agent_work("test-engineer", "Writing integration tests", 2)
        
        # Show results
        print("\n" + "="*60)
        print("🎉 MISSION COMPLETE!")
        print("="*60)
        
        # Display leaderboard
        print("\n🏆 UPDATED LEADERBOARD:")
        leaders = self.tracker.get_leaderboard()
        for i, agent in enumerate(leaders[:5], 1):
            print(f"{i}. {agent['name']:<25} Lv.{agent['level']} - {agent['xp']} XP")
            
        # Show agent cards
        print("\n📇 AGENT TRADING CARDS:")
        if leaders:
            top_agent = leaders[0]['name']
            print(self.tracker.get_agent_card(top_agent))
            
        # Show mission report
        print(self.tracker.generate_mission_report())
        
        print("\n✨ Demo complete! This is how the SubAgents system tracks real usage.")
        print("\n📝 To integrate with your workflow:")
        print("  1. Use agents-monitor.sh to track Claude Code usage")
        print("  2. Check agents-tracker.py for XP and achievements")
        print("  3. View progress with leaderboards and reports")


if __name__ == "__main__":
    # Make scripts executable
    os.chmod("agents_tracker.py", 0o755)
    os.chmod("agents-monitor.sh", 0o755)
    
    demo = AgentsDemo()
    demo.run_demo()