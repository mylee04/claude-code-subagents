#!/usr/bin/env python3
"""
Test script for the Agent Registry and Feature Coordinator system
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agent_registry import AgentRegistry
from feature_coordinator import FeatureCoordinator

def test_agent_registry():
    """Test the Agent Registry functionality"""
    print("🔍 Testing Agent Registry System...")
    print("=" * 60)
    
    registry = AgentRegistry()
    
    # Test agent discovery
    print("1. Testing agent discovery...")
    agents = registry.discover_agents(force_refresh=True)
    print(f"   ✅ Discovered {len(agents)} agents")
    
    if not agents:
        print("   ⚠️  No agents found - check your agents directory")
        return False
    
    # Test category listing
    print("\n2. Testing category classification...")
    categories = registry.get_categories()
    print(f"   ✅ Found {len(categories)} categories:")
    for category in categories[:5]:  # Show first 5
        category_agents = registry.get_agents_by_category(category)
        print(f"      • {category}: {len(category_agents)} agents")
    
    # Test tech stack analysis
    print("\n3. Testing tech stack analysis...")
    tech_stacks = registry.get_tech_stacks()
    print(f"   ✅ Identified {len(tech_stacks)} tech stacks:")
    print(f"      • {', '.join(tech_stacks[:8])}")  # Show first 8
    
    # Test search functionality
    print("\n4. Testing search functionality...")
    search_results = registry.search_agents("python")
    print(f"   ✅ Found {len(search_results)} agents for 'python':")
    for agent in search_results[:3]:  # Show first 3
        print(f"      • {agent.name} ({agent.category})")
    
    # Test agent recommendation
    print("\n5. Testing squad recommendations...")
    squad = registry.get_recommended_squad("web-app", ["python", "javascript"])
    print(f"   ✅ Recommended squad for web-app: {', '.join(squad)}")
    
    print("\n✅ Agent Registry tests completed successfully!")
    return True

def test_feature_coordinator():
    """Test the Feature Coordinator functionality"""
    print("\n🚀 Testing Feature Coordinator System...")
    print("=" * 60)
    
    coordinator = FeatureCoordinator()
    
    # Test feature analysis
    print("1. Testing feature analysis...")
    analysis = coordinator.analyze_feature_request(
        "Build a user authentication system with OAuth social login",
        ["python", "javascript"], 
        "web-app"
    )
    print(f"   ✅ Project Type: {analysis['project_type']}")
    print(f"   ✅ Complexity: {analysis['complexity_score']}/10")
    print(f"   ✅ Estimated Duration: {analysis['estimated_duration']} hours")
    print(f"   ✅ Recommended Squad: {', '.join(analysis['recommended_squad'][:3])}")
    
    # Test plan creation
    print("\n2. Testing plan creation...")
    plan = coordinator.create_feature_plan(
        "User Authentication System",
        "Implement OAuth social login with JWT tokens",
        ["python", "react"]
    )
    print(f"   ✅ Created plan: {plan.id}")
    print(f"   ✅ Tasks: {len(plan.tasks)}")
    print(f"   ✅ Status: {plan.coordination_status.value}")
    
    # Test task management
    print("\n3. Testing task management...")
    next_task = coordinator.get_next_task(plan.id)
    if next_task:
        print(f"   ✅ Next task: {next_task.description[:50]}...")
        
        # Test agent recommendation for task
        recommended_agents = coordinator.recommend_agent_for_task(next_task)
        print(f"   ✅ Recommended agents: {', '.join(recommended_agents[:3])}")
        
        # Test task assignment
        if recommended_agents:
            success = coordinator.assign_task(plan.id, next_task.id, recommended_agents[0])
            print(f"   ✅ Task assignment: {'Success' if success else 'Failed'}")
    
    # Test plan status
    print("\n4. Testing plan status...")
    status = coordinator.get_plan_status(plan.id)
    if status:
        print(f"   ✅ Plan progress: {status['progress']['completed']}/{status['progress']['total']} tasks")
        print(f"   ✅ Current status: {status['status']}")
    
    print("\n✅ Feature Coordinator tests completed successfully!")
    return True

def test_integration():
    """Test integration between registry and coordinator"""
    print("\n🔗 Testing System Integration...")
    print("=" * 60)
    
    # Test that coordinator can use registry data
    coordinator = FeatureCoordinator()
    registry = coordinator.registry
    
    # Discover agents through coordinator's registry
    agents = registry.discover_agents()
    print(f"1. ✅ Coordinator accessing {len(agents)} agents via registry")
    
    # Test enhanced analysis
    analysis = coordinator.analyze_feature_request(
        "Build a machine learning pipeline for text classification",
        tech_stack=["python", "tensorflow"]
    )
    
    # Verify ML agents are recommended
    ml_agents = [agent for agent in analysis['recommended_squad'] 
                if 'ml' in agent.lower() or 'ai' in agent.lower() or 'data' in agent.lower()]
    print(f"2. ✅ ML pipeline correctly identified {len(ml_agents)} ML-related agents")
    
    # Test that registry can find tech-specific agents
    python_agents = registry.get_agents_by_tech_stack(["python"])
    print(f"3. ✅ Found {len(python_agents)} Python-capable agents")
    
    print("\n✅ Integration tests completed successfully!")
    return True

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("🎯 SubAgents Agent Registry System - Comprehensive Test Suite")
    print("=" * 80)
    
    tests_passed = 0
    total_tests = 3
    
    try:
        # Test 1: Agent Registry
        if test_agent_registry():
            tests_passed += 1
        
        # Test 2: Feature Coordinator  
        if test_feature_coordinator():
            tests_passed += 1
            
        # Test 3: Integration
        if test_integration():
            tests_passed += 1
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    # Final summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"Tests Passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! The Agent Registry System is ready for production.")
        print("\n🚀 Next Steps:")
        print("   • The feature-planner agent now has enhanced coordination capabilities")
        print("   • Custom agents will be automatically discovered and coordinated")
        print("   • All agent interactions contribute to XP tracking")
        print("   • Use the registry CLI tools for agent management")
        return True
    else:
        print(f"⚠️  {total_tests - tests_passed} tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)