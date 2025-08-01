#!/usr/bin/env python3
"""
Example script showing how to track XP for agents
Demonstrates the Claude Arena XP tracking API
"""

import asyncio
import httpx
from datetime import datetime
from uuid import uuid4


# API Configuration
API_BASE = "http://localhost:8000/api/v1"
WS_BASE = "ws://localhost:8000/ws"

# Mock authentication token (for development)
AUTH_TOKEN = "dev-user-1"  # This gets a developer user

# Headers for API requests
HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}


async def track_agent_xp_example():
    """Example: Track XP for different agents"""
    
    async with httpx.AsyncClient() as client:
        print("🎮 Claude Arena XP Tracking Example")
        print("=" * 40)
        
        # Example 1: Simple task completion
        print("\n1. Simple Task Completion")
        simple_task = {
            "user_id": "12345678-1234-5678-9012-123456789012",  # Mock user ID
            "agent_name": "python-pro",
            "action_type": "task_completion",
            "task_description": "Created a simple Python function",
            "task_complexity": "simple",
            "task_duration": 45.0,  # 45 seconds
            "success": True,
            "base_points": 10,
            "response_quality": 0.85,
            "user_satisfaction": 0.9,
            "code_quality": 0.8
        }
        
        response = await client.post(
            f"{API_BASE}/agents/python-pro/xp",
            headers=HEADERS,
            json=simple_task
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ XP Gained: {result['xp_gained']}")
            print(f"📊 Total XP: {result['total_xp']}")
            print(f"🆙 Level Up: {result['level_up']}")
            if result["achievements_unlocked"]:
                print(f"🏆 Achievements: {', '.join(result['achievements_unlocked'])}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
        
        # Example 2: Complex task with bonuses
        print("\n2. Complex Task with Bonuses")
        complex_task = {
            "user_id": "12345678-1234-5678-9012-123456789012",
            "agent_name": "backend-architect",
            "action_type": "task_completion",
            "task_description": "Designed scalable microservices architecture",
            "task_complexity": "expert",
            "task_duration": 300.0,  # 5 minutes
            "success": True,
            "base_points": 25,
            "multipliers": [
                {"type": "architecture_bonus", "value": 1.5, "reason": "Complex architecture design"},
                {"type": "innovation_bonus", "value": 1.2, "reason": "Novel approach used"}
            ],
            "bonus_points": 50,
            "response_quality": 0.95,
            "user_satisfaction": 1.0,
            "code_quality": 0.9,
            "evidence_type": "complexity_handling",
            "evidence_data": {
                "improvement_factor": 1.8,
                "complexity_score": 0.95
            }
        }
        
        response = await client.post(
            f"{API_BASE}/agents/backend-architect/xp",
            headers=HEADERS,
            json=complex_task
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ XP Gained: {result['xp_gained']}")
            print(f"📊 Total XP: {result['total_xp']}")
            print(f"🆙 Level Up: {result['level_up']}")
            if result["achievements_unlocked"]:
                print(f"🏆 Achievements: {', '.join(result['achievements_unlocked'])}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
        
        # Example 3: Error resolution
        print("\n3. Error Resolution")
        error_task = {
            "user_id": "12345678-1234-5678-9012-123456789012",
            "agent_name": "devops-troubleshooter",
            "action_type": "error_resolution",
            "task_description": "Fixed critical production deployment issue",
            "task_complexity": "complex",
            "task_duration": 120.0,  # 2 minutes
            "success": True,
            "base_points": 20,
            "bonus_points": 30,
            "response_quality": 0.9,
            "evidence_type": "bug_resolution",
            "evidence_data": {
                "severity": "critical",
                "time_to_resolution": 120,
                "improvement_factor": 2.0
            }
        }
        
        response = await client.post(
            f"{API_BASE}/agents/devops-troubleshooter/xp",
            headers=HEADERS,
            json=error_task
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ XP Gained: {result['xp_gained']}")
            print(f"📊 Total XP: {result['total_xp']}")
            print(f"🆙 Level Up: {result['level_up']}")
            if result["achievements_unlocked"]:
                print(f"🏆 Achievements: {', '.join(result['achievements_unlocked'])}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")


async def get_agent_stats_example():
    """Example: Get agent statistics"""
    
    async with httpx.AsyncClient() as client:
        print("\n" + "=" * 40)
        print("📊 Agent Statistics Examples")
        print("=" * 40)
        
        agents = ["python-pro", "backend-architect", "devops-troubleshooter"]
        
        for agent in agents:
            print(f"\n🤖 {agent.replace('-', ' ').title()} Stats:")
            
            response = await client.get(
                f"{API_BASE}/agents/{agent}/stats",
                headers=HEADERS
            )
            
            if response.status_code == 200:
                stats = response.json()
                print(f"  Level: {stats['level']}")
                print(f"  XP: {stats['xp']}")
                print(f"  Total Calls: {stats['total_calls']}")
                print(f"  Success Rate: {stats['success_rate']:.1f}%")
                print(f"  Avg Task Time: {stats['avg_task_time']:.1f}s")
                print(f"  Last Used: {stats['last_used']}")
            else:
                print(f"  ❌ Error: {response.status_code}")


async def get_leaderboard_example():
    """Example: Get personal leaderboard"""
    
    async with httpx.AsyncClient() as client:
        print("\n" + "=" * 40)
        print("🏆 Personal Leaderboard")
        print("=" * 40)
        
        response = await client.get(
            f"{API_BASE}/agents/leaderboard/personal?sort_by=xp&limit=10",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            leaderboard = response.json()
            
            print("\n🥇 Top Agents by XP:")
            for i, agent in enumerate(leaderboard, 1):
                stars = "★" * agent['level'] + "☆" * (5 - agent['level'])
                print(f"{i:2}. {agent['agent_name']:<20} Lv.{agent['level']} {stars} - {agent['xp']} XP")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")


async def get_performance_summary_example():
    """Example: Get overall performance summary"""
    
    async with httpx.AsyncClient() as client:
        print("\n" + "=" * 40)
        print("📈 Performance Summary")
        print("=" * 40)
        
        response = await client.get(
            f"{API_BASE}/agents/performance/summary",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            summary = response.json()
            
            print("\n📊 Overall Stats:")
            print(f"  Unique Agents Used: {summary['summary']['unique_agents']}")
            print(f"  Total XP: {summary['summary']['total_xp']}")
            print(f"  Current Level: {summary['summary']['current_level']}")
            print(f"  Total Tasks: {summary['summary']['total_tasks']}")
            print(f"  Errors Resolved: {summary['summary']['errors_resolved']}")
            
            print("\n📅 Recent Activity (Last 7 Days):")
            print(f"  Tasks: {summary['recent_activity']['tasks_last_7_days']}")
            print(f"  XP Gained: {summary['recent_activity']['xp_last_7_days']}")
            
            print("\n🔥 Top Agents:")
            for agent in summary['top_agents']:
                print(f"  {agent['name']:<20} Lv.{agent['level']} - {agent['xp']} XP")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")


async def integration_with_existing_tracker():
    """Example: Integration with existing squad tracker"""
    
    print("\n" + "=" * 40)
    print("🔗 Integration with Existing Squad Tracker")
    print("=" * 40)
    
    # This shows how to integrate with the existing gamification/core/squad_tracker.py
    from gamification.core.squad_tracker import SquadTracker
    
    # Initialize the existing tracker
    tracker = SquadTracker()
    
    # Simulate some activity in the existing system
    print("\n1. Logging activity in existing system...")
    result = tracker.log_agent_call(
        "fastapi-arena-backend", 
        "Implemented XP tracking system with real-time notifications", 
        True,
        duration_seconds=1800  # 30 minutes
    )
    
    print(f"✅ Existing system logged: +{result['xp_gained']} XP")
    
    # Now track the same activity in the new API system
    print("\n2. Tracking same activity in new API system...")
    
    async with httpx.AsyncClient() as client:
        api_task = {
            "user_id": "12345678-1234-5678-9012-123456789012",
            "agent_name": "fastapi-arena-backend",
            "action_type": "task_completion",
            "task_description": "Implemented XP tracking system with real-time notifications",
            "task_complexity": "expert",
            "task_duration": 1800.0,
            "success": True,
            "base_points": 100,  # Higher base for system implementation
            "multipliers": [
                {"type": "system_implementation", "value": 2.0}
            ],
            "response_quality": 0.95,
            "evidence_type": "innovation",
            "evidence_data": {
                "lines_of_code": 2000,
                "features_implemented": 5,
                "improvement_factor": 3.0
            }
        }
        
        response = await client.post(
            f"{API_BASE}/agents/fastapi-arena-backend/xp",
            headers=HEADERS,
            json=api_task
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ New system tracked: +{result['xp_gained']} XP")
            print(f"🆙 Level up: {result['level_up']}")
            
            # Show agent signature
            print(f"\n🏷️  Agent Signature:")
            print(f"FastAPI Arena Backend Agent")
            print(f"Level: {result['level_after']} ⭐ | XP: {result['total_xp']} | Specialty: Gamification Backend Systems")
            
            if result["achievements_unlocked"]:
                print(f"🏆 New Achievements: {', '.join(result['achievements_unlocked'])}")


async def main():
    """Run all examples"""
    try:
        await track_agent_xp_example()
        await get_agent_stats_example()
        await get_leaderboard_example()
        await get_performance_summary_example()
        await integration_with_existing_tracker()
        
        print("\n" + "=" * 40)
        print("✅ All examples completed successfully!")
        print("🚀 Check out the API docs at: http://localhost:8000/docs")
        print("🎮 Claude Arena Backend is ready for integration!")
        
    except Exception as e:
        print(f"\n❌ Example failed: {e}")
        print("Make sure the server is running: python start_server.py")


if __name__ == "__main__":
    asyncio.run(main())