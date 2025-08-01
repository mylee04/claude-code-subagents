#!/usr/bin/env python3
"""
Comprehensive Integration Testing Script
Tests feature-planner integration, XP tracking, caching behavior, and system integration
"""

import os
import sys
import time
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agent_registry import AgentRegistry
from feature_coordinator import FeatureCoordinator
from squad_tracker import SquadTracker

class IntegrationTester:
    """Comprehensive testing suite for system integration"""
    
    def __init__(self):
        self.test_results = []
        self.temp_files = []
        
    def log_test_result(self, test_name: str, passed: bool, message: str = "", details: Dict = None):
        """Log test result for reporting"""
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "message": message,
            "details": details or {}
        })
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details:
            for key, value in details.items():
                print(f"    {key}: {value}")
        print()
        
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        for temp_file in self.temp_files:
            if temp_file.exists():
                temp_file.unlink()
        self.temp_files.clear()
        
    def test_registry_coordinator_integration(self):
        """Test integration between AgentRegistry and FeatureCoordinator"""
        print("🔍 Testing Registry-Coordinator Integration...")
        
        coordinator = FeatureCoordinator()
        registry = coordinator.registry
        
        # Test that coordinator can access registry data
        agents = registry.discover_agents()
        
        if len(agents) == 0:
            self.log_test_result(
                "Registry-Coordinator Integration",
                False,
                "No agents found - cannot test integration"
            )
            return
            
        # Test that coordinator uses registry for recommendations
        analysis = coordinator.analyze_feature_request(
            "Build a Python web application with authentication",
            tech_stack=["python", "javascript"]
        )
        
        # Verify that recommended agents exist in registry
        recommended_agents = analysis["recommended_squad"]
        agents_exist_in_registry = all(
            registry.get_agent_by_name(agent_name) is not None 
            for agent_name in recommended_agents
        )
        
        if agents_exist_in_registry and len(recommended_agents) > 0:
            self.log_test_result(
                "Registry-Coordinator Integration",
                True,
                "Coordinator successfully integrates with registry",
                {
                    "total_agents_in_registry": len(agents),
                    "recommended_agents": len(recommended_agents),
                    "all_recommendations_valid": agents_exist_in_registry
                }
            )
        else:
            self.log_test_result(
                "Registry-Coordinator Integration",
                False,
                "Coordinator-registry integration issues",
                {
                    "recommended_agents": recommended_agents,
                    "agents_exist": agents_exist_in_registry
                }
            )
            
    def test_xp_tracking_integration(self):
        """Test XP tracking integration with coordinator"""
        print("🔍 Testing XP Tracking Integration...")
        
        coordinator = FeatureCoordinator()
        tracker = coordinator.tracker
        
        # Create a test plan
        plan = coordinator.create_feature_plan(
            "XP Integration Test",
            "Test XP tracking integration",
            tech_stack=["python"]
        )
        
        if not plan:
            self.log_test_result(
                "XP Tracking Integration",
                False,
                "Could not create plan for XP testing"
            )
            return
            
        # Get and assign a task
        next_task = coordinator.get_next_task(plan.id)
        if not next_task:
            self.log_test_result(
                "XP Tracking Integration",
                False,
                "No task available for XP testing"
            )
            return
            
        recommended_agents = coordinator.recommend_agent_for_task(next_task)
        if not recommended_agents:
            self.log_test_result(
                "XP Tracking Integration",
                False,
                "No agents recommended for XP testing"
            )
            return
            
        test_agent = recommended_agents[0]
        
        # Get initial XP
        initial_stats = coordinator.registry.get_agent_stats(test_agent)
        initial_xp = initial_stats.xp
        
        # Assign and complete task
        coordinator.assign_task(plan.id, next_task.id, test_agent)
        coordinator.complete_task(
            plan.id,
            next_task.id,
            success=True,
            duration_minutes=15
        )
        
        # Check if XP was updated
        final_stats = coordinator.registry.get_agent_stats(test_agent)
        final_xp = final_stats.xp
        
        xp_gained = final_xp - initial_xp
        
        if xp_gained > 0:
            self.log_test_result(
                "XP Tracking Integration",
                True,
                f"XP tracking working correctly - {xp_gained} XP gained",
                {
                    "agent": test_agent,
                    "initial_xp": initial_xp,
                    "final_xp": final_xp,
                    "xp_gained": xp_gained,
                    "task_complexity": next_task.complexity.value
                }
            )
        else:
            self.log_test_result(
                "XP Tracking Integration",
                False,
                "XP tracking not working - no XP gained",
                {
                    "agent": test_agent,
                    "initial_xp": initial_xp,
                    "final_xp": final_xp
                }
            )
            
    def test_cache_effectiveness(self):
        """Test caching behavior and effectiveness"""
        print("🔍 Testing Cache Effectiveness...")
        
        # Test registry caching
        registry = AgentRegistry(cache_timeout=5)  # 5 second timeout
        
        # First discovery (cold cache)
        start_time = time.time()
        agents1 = registry.discover_agents(force_refresh=True)
        cold_cache_time = time.time() - start_time
        
        # Second discovery (warm cache)
        start_time = time.time()
        agents2 = registry.discover_agents()
        warm_cache_time = time.time() - start_time
        
        # Third discovery (still warm cache)
        start_time = time.time()
        agents3 = registry.discover_agents()
        still_warm_time = time.time() - start_time
        
        # Calculate speedup
        if warm_cache_time > 0:
            speedup = cold_cache_time / warm_cache_time
        else:
            speedup = float('inf')
            
        cache_consistent = (
            len(agents1) == len(agents2) == len(agents3) and
            list(agents1.keys()) == list(agents2.keys()) == list(agents3.keys())
        )
        
        cache_effective = speedup > 5 and warm_cache_time < 0.01  # Should be very fast
        
        if cache_effective and cache_consistent:
            self.log_test_result(
                "Cache Effectiveness",
                True,
                f"Cache working effectively - {speedup:.1f}x speedup",
                {
                    "cold_cache_ms": int(cold_cache_time * 1000),
                    "warm_cache_ms": int(warm_cache_time * 1000),
                    "speedup_factor": f"{speedup:.1f}x",
                    "data_consistency": cache_consistent
                }
            )
        else:
            self.log_test_result(
                "Cache Effectiveness",
                False,
                f"Cache not effective - speedup: {speedup:.1f}x",
                {
                    "cold_cache_ms": int(cold_cache_time * 1000),
                    "warm_cache_ms": int(warm_cache_time * 1000),
                    "data_consistency": cache_consistent
                }
            )
            
    def test_cache_expiration(self):
        """Test cache expiration behavior"""
        print("🔍 Testing Cache Expiration...")
        
        registry = AgentRegistry(cache_timeout=1)  # 1 second timeout
        
        # First discovery
        agents1 = registry.discover_agents(force_refresh=True)
        
        # Wait for cache to expire
        time.sleep(1.5)
        
        # Discovery after expiration (should re-scan)
        start_time = time.time()
        agents2 = registry.discover_agents()
        post_expiry_time = time.time() - start_time
        
        # Should take longer than cached access but find same agents
        cache_expired_correctly = (
            post_expiry_time > 0.001 and  # Took some time (not instant cache hit)
            len(agents1) == len(agents2) and
            list(agents1.keys()) == list(agents2.keys())
        )
        
        if cache_expired_correctly:
            self.log_test_result(
                "Cache Expiration",
                True,
                "Cache expiration working correctly",
                {
                    "post_expiry_time_ms": int(post_expiry_time * 1000),
                    "agents_consistent": len(agents1) == len(agents2)
                }
            )
        else:
            self.log_test_result(
                "Cache Expiration",
                False,
                "Cache expiration not working correctly",
                {
                    "post_expiry_time_ms": int(post_expiry_time * 1000),
                    "agents_count_1": len(agents1),
                    "agents_count_2": len(agents2)
                }
            )
            
    def test_disk_persistence_integration(self):
        """Test disk persistence across system components"""
        print("🔍 Testing Disk Persistence Integration...")
        
        # Test registry cache persistence
        registry1 = AgentRegistry()
        agents = registry1.discover_agents(force_refresh=True)
        
        # Create new registry instance
        registry2 = AgentRegistry()
        # Should load from disk cache if recent enough
        agents2 = registry2.discover_agents()
        
        registry_persistence = len(agents) == len(agents2)
        
        # Test coordinator plan persistence
        coordinator1 = FeatureCoordinator()
        plan = coordinator1.create_feature_plan(
            "Persistence Test",
            "Test cross-instance persistence",
            tech_stack=["python"]
        )
        
        if plan:
            # Create new coordinator instance
            coordinator2 = FeatureCoordinator()
            loaded_plan = coordinator2.get_plan_status(plan.id)
            coordinator_persistence = loaded_plan is not None
        else:
            coordinator_persistence = False
            
        # Test squad tracker persistence
        tracker1 = SquadTracker()
        tracker1.log_agent_call("test-agent", "test task", True)
        
        tracker2 = SquadTracker()
        agent_data = tracker2.data.get("agents", {}).get("test-agent")
        tracker_persistence = agent_data is not None
        
        all_persistence_working = (
            registry_persistence and 
            coordinator_persistence and 
            tracker_persistence
        )
        
        if all_persistence_working:
            self.log_test_result(
                "Disk Persistence Integration",
                True,
                "All components persist data correctly",
                {
                    "registry_persistence": registry_persistence,
                    "coordinator_persistence": coordinator_persistence,
                    "tracker_persistence": tracker_persistence
                }
            )
        else:
            self.log_test_result(
                "Disk Persistence Integration",
                False,
                "Some components not persisting data",
                {
                    "registry_persistence": registry_persistence,
                    "coordinator_persistence": coordinator_persistence,
                    "tracker_persistence": tracker_persistence
                }
            )
            
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        print("🔍 Testing End-to-End Workflow...")
        
        try:
            # Step 1: Initialize systems
            coordinator = FeatureCoordinator()
            registry = coordinator.registry
            
            # Step 2: Discover agents
            agents = registry.discover_agents()
            if len(agents) == 0:
                self.log_test_result(
                    "End-to-End Workflow",
                    False,
                    "No agents available for workflow test"
                )
                return
                
            # Step 3: Analyze feature request
            analysis = coordinator.analyze_feature_request(
                "Build a secure user authentication API with rate limiting",
                tech_stack=["python", "sql"]
            )
            
            # Step 4: Create feature plan
            plan = coordinator.create_feature_plan(
                "E2E Test Feature",
                "End-to-end workflow test",
                tech_stack=analysis["tech_stack"],
                project_type=analysis["project_type"]
            )
            
            # Step 5: Process first task
            next_task = coordinator.get_next_task(plan.id)
            if not next_task:
                raise Exception("No next task available")
                
            # Step 6: Get agent recommendations
            recommended_agents = coordinator.recommend_agent_for_task(next_task)
            if not recommended_agents:
                raise Exception("No agent recommendations")
                
            # Step 7: Assign task
            assignment_success = coordinator.assign_task(
                plan.id, 
                next_task.id, 
                recommended_agents[0]
            )
            if not assignment_success:
                raise Exception("Task assignment failed")
                
            # Step 8: Complete task
            completion_success = coordinator.complete_task(
                plan.id,
                next_task.id,
                success=True,
                result={"status": "completed"},
                duration_minutes=20
            )
            if not completion_success:
                raise Exception("Task completion failed")
                
            # Step 9: Verify state
            final_status = coordinator.get_plan_status(plan.id)
            agent_stats = registry.get_agent_stats(recommended_agents[0])
            
            workflow_success = (
                final_status["progress"]["completed"] == 1 and
                agent_stats.xp > 0 and
                agent_stats.successful_tasks > 0
            )
            
            if workflow_success:
                self.log_test_result(
                    "End-to-End Workflow",
                    True,
                    "Complete workflow executed successfully",
                    {
                        "project_type": analysis["project_type"],
                        "complexity": analysis["complexity_score"],
                        "assigned_agent": recommended_agents[0],
                        "completed_tasks": final_status["progress"]["completed"],
                        "agent_xp_gained": agent_stats.xp,
                        "plan_status": final_status["status"]
                    }
                )
            else:
                self.log_test_result(
                    "End-to-End Workflow",
                    False,
                    "Workflow completed but state inconsistent",
                    {
                        "final_status": final_status,
                        "agent_stats": {"xp": agent_stats.xp, "successful_tasks": agent_stats.successful_tasks}
                    }
                )
                
        except Exception as e:
            self.log_test_result(
                "End-to-End Workflow",
                False,
                f"Workflow failed: {str(e)}"
            )
            
    def test_concurrent_access_simulation(self):
        """Test concurrent access simulation"""
        print("🔍 Testing Concurrent Access Simulation...")
        
        # Simulate multiple coordinators accessing the same data
        coordinators = [FeatureCoordinator() for _ in range(3)]
        
        # Each coordinator creates a plan
        plans = []
        for i, coordinator in enumerate(coordinators):
            plan = coordinator.create_feature_plan(
                f"Concurrent Test {i+1}",
                f"Concurrent access test plan {i+1}",
                tech_stack=["python"]
            )
            if plan:
                plans.append(plan)
                
        # Verify all plans were created and are accessible by all coordinators
        all_plans_accessible = True
        for coordinator in coordinators:
            for plan in plans:
                status = coordinator.get_plan_status(plan.id)
                if not status:
                    all_plans_accessible = False
                    break
            if not all_plans_accessible:
                break
                
        if all_plans_accessible and len(plans) == 3:
            self.log_test_result(
                "Concurrent Access Simulation",
                True,
                "Concurrent access handled correctly",
                {
                    "coordinators_tested": len(coordinators),
                    "plans_created": len(plans),
                    "all_plans_accessible": all_plans_accessible
                }
            )
        else:
            self.log_test_result(
                "Concurrent Access Simulation",
                False,
                "Concurrent access issues detected",
                {
                    "plans_created": len(plans),
                    "all_accessible": all_plans_accessible
                }
            )
            
    def test_error_recovery_integration(self):
        """Test error recovery across integrated systems"""
        print("🔍 Testing Error Recovery Integration...")
        
        coordinator = FeatureCoordinator()
        
        # Test with invalid agent assignment
        plan = coordinator.create_feature_plan(
            "Error Recovery Test",
            "Test error recovery",
            tech_stack=["python"]
        )
        
        if not plan:
            self.log_test_result(
                "Error Recovery Integration",
                False,
                "Could not create plan for error recovery test"
            )
            return
            
        next_task = coordinator.get_next_task(plan.id)
        if not next_task:
            self.log_test_result(
                "Error Recovery Integration",
                False,
                "No task available for error recovery test"
            )
            return
            
        # Try to assign to non-existent agent
        invalid_assignment = coordinator.assign_task(
            plan.id,
            next_task.id,
            "non-existent-agent"
        )
        
        # Should fail gracefully
        if not invalid_assignment:
            # Try with valid agent
            recommended_agents = coordinator.recommend_agent_for_task(next_task)
            if recommended_agents:
                valid_assignment = coordinator.assign_task(
                    plan.id,
                    next_task.id,
                    recommended_agents[0]
                )
                
                if valid_assignment:
                    self.log_test_result(
                        "Error Recovery Integration",
                        True,
                        "System recovered from invalid assignment",
                        {
                            "invalid_assignment_rejected": not invalid_assignment,
                            "valid_assignment_succeeded": valid_assignment
                        }
                    )
                else:
                    self.log_test_result(
                        "Error Recovery Integration",
                        False,
                        "Could not recover with valid assignment"
                    )
            else:
                self.log_test_result(
                    "Error Recovery Integration",
                    False,
                    "No valid agents available for recovery test"
                )
        else:
            self.log_test_result(
                "Error Recovery Integration",
                False,
                "System did not reject invalid assignment"
            )
            
    def run_all_tests(self) -> Dict:
        """Run all integration tests"""
        print("🎯 Running Comprehensive Integration Tests")
        print("=" * 80)
        
        try:
            self.test_registry_coordinator_integration()
            self.test_xp_tracking_integration()
            self.test_cache_effectiveness()
            self.test_cache_expiration()
            self.test_disk_persistence_integration()
            self.test_end_to_end_workflow()
            self.test_concurrent_access_simulation()
            self.test_error_recovery_integration()
            
        except Exception as e:
            print(f"❌ Test suite failed with error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup_temp_files()
            
        # Generate summary
        passed_tests = sum(1 for result in self.test_results if result["passed"])
        total_tests = len(self.test_results)
        
        print("\n" + "=" * 80)
        print("📊 INTEGRATION TEST SUMMARY")
        print("=" * 80)
        print(f"Tests Passed: {passed_tests}/{total_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("🎉 ALL INTEGRATION TESTS PASSED!")
        else:
            print("⚠️  Some tests failed. Check output above for details.")
            
        print("\n📋 Detailed Results:")
        for result in self.test_results:
            status = "✅" if result["passed"] else "❌"
            print(f"  {status} {result['test']}: {result['message']}")
            
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "success_rate": (passed_tests/total_tests)*100,
            "results": self.test_results
        }

if __name__ == "__main__":
    tester = IntegrationTester()
    results = tester.run_all_tests()
    
    # Exit with error code if tests failed
    sys.exit(0 if results["passed_tests"] == results["total_tests"] else 1)