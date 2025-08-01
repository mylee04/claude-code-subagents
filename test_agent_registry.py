#!/usr/bin/env python3
"""Quick test of AgentRegistry system"""

import sys
sys.path.append('gamification/core')

from agent_registry import AgentRegistry
from feature_coordinator import FeatureCoordinator

def test_agent_discovery():
    print("🔍 Testing Agent Discovery...")
    registry = AgentRegistry()
    
    # Discover all agents
    agents = registry.discover_agents()
    print(f"✅ Found {len(agents)} total agents")
    
    # Show categories (extract from agents)
    categories = set()
    for agent in agents.values():
        if hasattr(agent, 'category'):
            categories.add(agent.category)
    print(f"📁 Categories: {sorted(categories)}")
    
    # Test filtering (note: categories are capitalized)
    dev_agents = [a for a in agents.values() if getattr(a, 'category', '') == 'Development']
    print(f"💻 Development agents: {len(dev_agents)}")
    
    # Show some agent names
    if agents:
        print("\n📋 Sample agents:")
        for agent in list(agents.values())[:5]:
            print(f"  - {agent.name}: {agent.description[:50]}...")

def test_feature_coordination():
    print("\n🎯 Testing Feature Coordination...")
    coordinator = FeatureCoordinator()
    
    # Create a feature plan
    plan = coordinator.create_feature_plan(
        name="Test Feature",
        description="Build a real-time chat system with React frontend and FastAPI backend",
        tech_stack=["react", "typescript", "fastapi"],
        project_type="web-app"
    )
    
    print(f"✅ Created feature plan with {len(plan.tasks)} tasks")
    print(f"📋 Recommended squad: {plan.recommended_squad[:3]}...")  # Show first 3
    
    # Test agent recommendation for first task
    if plan.tasks:
        task = plan.tasks[0]
        recommended = coordinator.recommend_agent_for_task(task)
        print(f"🎯 For task '{task.description[:50]}...'")
        print(f"   Recommended agents: {recommended[:3]}")

if __name__ == "__main__":
    try:
        test_agent_discovery()
        test_feature_coordination()
        print("\n✅ All tests passed!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()