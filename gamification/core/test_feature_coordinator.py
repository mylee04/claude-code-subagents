#!/usr/bin/env python3
"""
Comprehensive Feature Coordinator Testing Script
Tests squad formation, task breakdown, dependencies, and agent recommendations
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

from feature_coordinator import FeatureCoordinator, TaskComplexity, CoordinationStatus, Task, FeaturePlan
from agent_registry import AgentRegistry

class FeatureCoordinatorTester:
    """Comprehensive testing suite for FeatureCoordinator functionality"""
    
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
        
    def test_feature_analysis_basic(self):
        """Test basic feature analysis functionality"""
        print("🔍 Testing Basic Feature Analysis...")
        
        coordinator = FeatureCoordinator()
        
        # Test web app analysis
        analysis = coordinator.analyze_feature_request(
            "Build a user authentication system with social login",
            tech_stack=["python", "react"],
            project_type="web-app"
        )
        
        expected_fields = ["project_type", "tech_stack", "recommended_squad", 
                          "complexity_score", "estimated_duration", "task_breakdown"]
        
        all_fields_present = all(field in analysis for field in expected_fields)
        
        if (all_fields_present and 
            analysis["project_type"] == "web-app" and
            len(analysis["recommended_squad"]) > 0):
            self.log_test_result(
                "Basic Feature Analysis",
                True,
                "Successfully analyzed feature request",
                {
                    "project_type": analysis["project_type"],
                    "complexity_score": analysis["complexity_score"],
                    "squad_size": len(analysis["recommended_squad"]),
                    "estimated_hours": analysis["estimated_duration"],
                    "task_count": len(analysis["task_breakdown"])
                }
            )
        else:
            self.log_test_result(
                "Basic Feature Analysis",
                False,
                "Feature analysis incomplete or incorrect",
                {"analysis_keys": list(analysis.keys())}
            )
            
    def test_project_type_inference(self):
        """Test automatic project type inference"""
        print("🔍 Testing Project Type Inference...")
        
        coordinator = FeatureCoordinator()
        
        test_cases = [
            ("Build a REST API for user management", "api"),
            ("Create a machine learning model for text classification", "ai-ml"),
            ("Set up a data pipeline for analytics", "data-pipeline"),
            ("Build a web dashboard for monitoring", "web-app"),
            ("Deploy application to AWS with CI/CD", "devops")
        ]
        
        passed_inferences = 0
        for description, expected_type in test_cases:
            analysis = coordinator.analyze_feature_request(description)
            if analysis["project_type"] == expected_type:
                passed_inferences += 1
                
        success_rate = (passed_inferences / len(test_cases)) * 100
        
        if success_rate >= 80:
            self.log_test_result(
                "Project Type Inference",
                True,
                f"Successfully inferred {success_rate:.0f}% of project types",
                {
                    "correct_inferences": passed_inferences,
                    "total_tests": len(test_cases),
                    "success_rate": f"{success_rate:.0f}%"
                }
            )
        else:
            self.log_test_result(
                "Project Type Inference",
                False,
                f"Low project type inference success rate: {success_rate:.0f}%",
                {"correct_inferences": passed_inferences, "total_tests": len(test_cases)}
            )
            
    def test_tech_stack_inference(self):
        """Test automatic tech stack inference"""
        print("🔍 Testing Tech Stack Inference...")
        
        coordinator = FeatureCoordinator()
        
        test_cases = [
            ("Build a Python FastAPI service with PostgreSQL", ["python", "sql", "backend"]),
            ("Create a React frontend with TypeScript", ["javascript", "typescript", "frontend"]),
            ("Deploy using Docker and Kubernetes on AWS", ["cloud", "devops"]),
            ("Build a Go microservice with Redis", ["golang", "backend"])
        ]
        
        passed_inferences = 0
        inference_details = []
        
        for description, expected_techs in test_cases:
            analysis = coordinator.analyze_feature_request(description)
            inferred_tech = analysis["tech_stack"]
            
            # Check if at least half of expected technologies were inferred
            matches = sum(1 for tech in expected_techs if tech in inferred_tech)
            if matches >= len(expected_techs) / 2:
                passed_inferences += 1
                
            inference_details.append({
                "description": description[:50] + "...",
                "expected": expected_techs,
                "inferred": inferred_tech,
                "match_rate": f"{matches}/{len(expected_techs)}"
            })
        
        success_rate = (passed_inferences / len(test_cases)) * 100
        
        if success_rate >= 75:
            self.log_test_result(
                "Tech Stack Inference",
                True,
                f"Successfully inferred {success_rate:.0f}% of tech stacks",
                {
                    "success_rate": f"{success_rate:.0f}%",
                    "details": inference_details
                }
            )
        else:
            self.log_test_result(
                "Tech Stack Inference",
                False,
                f"Low tech stack inference success rate: {success_rate:.0f}%",
                {"details": inference_details}
            )
            
    def test_complexity_analysis(self):
        """Test complexity scoring algorithm"""
        print("🔍 Testing Complexity Analysis...")
        
        coordinator = FeatureCoordinator()
        
        test_cases = [
            ("Add a simple contact form", 1, 3),
            ("Build a user authentication system", 4, 7),
            ("Create a distributed microservices architecture", 7, 10),
            ("Implement real-time analytics with machine learning", 8, 10)
        ]
        
        passed_complexity = 0
        complexity_details = []
        
        for description, min_expected, max_expected in test_cases:
            analysis = coordinator.analyze_feature_request(description)
            complexity = analysis["complexity_score"]
            
            if min_expected <= complexity <= max_expected:
                passed_complexity += 1
                
            complexity_details.append({
                "description": description[:50] + "...",
                "expected_range": f"{min_expected}-{max_expected}",
                "actual": complexity,
                "in_range": min_expected <= complexity <= max_expected
            })
        
        success_rate = (passed_complexity / len(test_cases)) * 100
        
        if success_rate >= 75:
            self.log_test_result(
                "Complexity Analysis",
                True,
                f"Complexity scoring {success_rate:.0f}% accurate",
                {"details": complexity_details}
            )
        else:
            self.log_test_result(
                "Complexity Analysis",
                False,
                f"Complexity scoring only {success_rate:.0f}% accurate",
                {"details": complexity_details}
            )
            
    def test_plan_creation(self):
        """Test feature plan creation"""
        print("🔍 Testing Plan Creation...")
        
        coordinator = FeatureCoordinator()
        
        plan = coordinator.create_feature_plan(
            "Test Feature",
            "Build a test feature for validation",
            tech_stack=["python", "react"],
            project_type="web-app"
        )
        
        # Verify plan structure
        plan_valid = (
            isinstance(plan, FeaturePlan) and
            plan.name == "Test Feature" and
            len(plan.tasks) > 0 and
            len(plan.recommended_squad) > 0 and
            plan.coordination_status == CoordinationStatus.PLANNING
        )
        
        if plan_valid:
            self.log_test_result(
                "Plan Creation",
                True,
                "Successfully created feature plan",
                {
                    "plan_id": plan.id,
                    "task_count": len(plan.tasks),
                    "squad_size": len(plan.recommended_squad),
                    "estimated_duration": plan.estimated_total_duration,
                    "status": plan.coordination_status.value
                }
            )
        else:
            self.log_test_result(
                "Plan Creation",
                False,
                "Failed to create valid feature plan",
                {"plan": str(plan) if plan else None}
            )
            
        return plan if plan_valid else None
        
    def test_task_dependency_management(self):
        """Test task dependency management"""
        print("🔍 Testing Task Dependency Management...")
        
        coordinator = FeatureCoordinator()
        
        plan = coordinator.create_feature_plan(
            "Dependency Test",
            "Test task dependencies",
            tech_stack=["python"],
            project_type="web-app"
        )
        
        if not plan:
            self.log_test_result(
                "Task Dependency Management",
                False,
                "Could not create plan for dependency testing"
            )
            return
            
        # Check that tasks have dependencies (except the first one)
        first_task = plan.tasks[0]
        later_tasks = plan.tasks[1:]
        
        first_has_no_deps = len(first_task.dependencies) == 0
        later_have_deps = all(len(task.dependencies) > 0 for task in later_tasks)
        
        # Test getting next task
        next_task = coordinator.get_next_task(plan.id)
        next_task_is_first = next_task and next_task.id == first_task.id
        
        if first_has_no_deps and later_have_deps and next_task_is_first:
            self.log_test_result(
                "Task Dependency Management",
                True,
                "Task dependencies properly configured",
                {
                    "first_task_deps": len(first_task.dependencies),
                    "later_tasks_with_deps": sum(1 for t in later_tasks if len(t.dependencies) > 0),
                    "next_task_correct": next_task_is_first
                }
            )
        else:
            self.log_test_result(
                "Task Dependency Management",
                False,
                "Task dependencies not properly configured",
                {
                    "first_task_deps": len(first_task.dependencies),
                    "later_tasks_with_deps": sum(1 for t in later_tasks if len(t.dependencies) > 0),
                    "next_task_id": next_task.id if next_task else None
                }
            )
            
    def test_agent_recommendation(self):
        """Test agent recommendation for tasks"""
        print("🔍 Testing Agent Recommendation...")
        
        coordinator = FeatureCoordinator()
        
        # Create test task
        test_task = Task(
            id="test_task_1",
            description="Implement user authentication with OAuth",
            complexity=TaskComplexity.COMPLEX,
            required_agent_categories=["Development", "Security"],
            preferred_agents=["backend-architect", "security-auditor"]
        )
        
        recommendations = coordinator.recommend_agent_for_task(test_task)
        
        if len(recommendations) > 0:
            # Check if preferred agents are prioritized
            preferred_found = any(agent in recommendations for agent in test_task.preferred_agents)
            
            self.log_test_result(
                "Agent Recommendation",
                True,
                f"Generated {len(recommendations)} agent recommendations",
                {
                    "recommendation_count": len(recommendations),
                    "recommended_agents": recommendations[:3],
                    "preferred_agents_included": preferred_found
                }
            )
        else:
            self.log_test_result(
                "Agent Recommendation",
                False,
                "No agent recommendations generated"
            )
            
    def test_task_assignment_and_completion(self):
        """Test task assignment and completion workflow"""
        print("🔍 Testing Task Assignment and Completion...")
        
        coordinator = FeatureCoordinator()
        
        plan = coordinator.create_feature_plan(
            "Assignment Test",
            "Test task assignment workflow",
            tech_stack=["python"],
            project_type="api"
        )
        
        if not plan:
            self.log_test_result(
                "Task Assignment and Completion",
                False,
                "Could not create plan for assignment testing"
            )
            return
            
        # Get first task and assign it
        next_task = coordinator.get_next_task(plan.id)
        if not next_task:
            self.log_test_result(
                "Task Assignment and Completion",
                False,
                "No next task available"
            )
            return
            
        # Get agent recommendations
        recommended_agents = coordinator.recommend_agent_for_task(next_task)
        if not recommended_agents:
            self.log_test_result(
                "Task Assignment and Completion",
                False,
                "No agents recommended for task"
            )
            return
            
        # Assign task
        assignment_success = coordinator.assign_task(
            plan.id, 
            next_task.id, 
            recommended_agents[0]
        )
        
        if not assignment_success:
            self.log_test_result(
                "Task Assignment and Completion",
                False,
                "Failed to assign task to agent"
            )
            return
            
        # Complete task
        completion_success = coordinator.complete_task(
            plan.id,
            next_task.id,
            success=True,
            result={"test": "completed"},
            duration_minutes=30
        )
        
        # Check plan status
        plan_status = coordinator.get_plan_status(plan.id)
        
        if (assignment_success and completion_success and plan_status and
            plan_status["progress"]["completed"] == 1):
            self.log_test_result(
                "Task Assignment and Completion",
                True,
                "Successfully completed task assignment workflow",
                {
                    "assigned_agent": recommended_agents[0],
                    "completed_tasks": plan_status["progress"]["completed"],
                    "plan_status": plan_status["status"]
                }
            )
        else:
            self.log_test_result(
                "Task Assignment and Completion",
                False,
                "Task assignment workflow failed",
                {
                    "assignment_success": assignment_success,
                    "completion_success": completion_success,
                    "plan_status": plan_status
                }
            )
            
    def test_squad_formation_different_project_types(self):
        """Test squad formation for different project types"""
        print("🔍 Testing Squad Formation for Different Project Types...")
        
        coordinator = FeatureCoordinator()
        
        project_types = ["web-app", "api", "data-pipeline", "ai-ml", "devops"]
        squad_results = {}
        
        for project_type in project_types:
            analysis = coordinator.analyze_feature_request(
                f"Build a {project_type} project",
                project_type=project_type
            )
            squad_results[project_type] = analysis["recommended_squad"]
            
        # Verify each project type gets a different squad composition
        all_squads_different = len(set(str(sorted(squad)) for squad in squad_results.values())) == len(project_types)
        all_squads_have_agents = all(len(squad) > 0 for squad in squad_results.values())
        
        if all_squads_different and all_squads_have_agents:
            self.log_test_result(
                "Squad Formation for Different Project Types",
                True,
                "Each project type gets appropriate squad composition",
                {
                    "project_types_tested": len(project_types),
                    "unique_squad_compositions": len(set(str(sorted(squad)) for squad in squad_results.values())),
                    "sample_squads": {pt: squad[:3] for pt, squad in squad_results.items()}
                }
            )
        else:
            self.log_test_result(
                "Squad Formation for Different Project Types",
                False,
                "Squad formation not appropriately differentiated",
                {"squad_results": squad_results}
            )
            
    def test_plan_persistence(self):
        """Test plan persistence to disk"""
        print("🔍 Testing Plan Persistence...")
        
        coordinator1 = FeatureCoordinator()
        
        # Create a plan
        plan = coordinator1.create_feature_plan(
            "Persistence Test",
            "Test plan persistence",
            tech_stack=["python"]
        )
        
        if not plan:
            self.log_test_result(
                "Plan Persistence",
                False,
                "Could not create plan for persistence testing"
            )
            return
            
        # Create new coordinator instance (should load from disk)
        coordinator2 = FeatureCoordinator()
        
        # Check if plan exists in new instance
        loaded_plan_status = coordinator2.get_plan_status(plan.id)
        
        if loaded_plan_status and loaded_plan_status["name"] == "Persistence Test":
            self.log_test_result(
                "Plan Persistence",
                True,
                "Plans successfully persisted and loaded",
                {
                    "plan_id": plan.id,
                    "loaded_name": loaded_plan_status["name"],
                    "task_count": loaded_plan_status["progress"]["total"]
                }
            )
        else:
            self.log_test_result(
                "Plan Persistence",
                False,
                "Plan persistence failed",
                {"loaded_status": loaded_plan_status}
            )
            
    def test_coordination_status_transitions(self):
        """Test coordination status transitions"""
        print("🔍 Testing Coordination Status Transitions...")
        
        coordinator = FeatureCoordinator()
        
        plan = coordinator.create_feature_plan(
            "Status Test",
            "Test status transitions",
            tech_stack=["python"]
        )
        
        if not plan:
            self.log_test_result(
                "Coordination Status Transitions",
                False,
                "Could not create plan for status testing"
            )
            return
            
        # Initial status should be PLANNING
        initial_status = coordinator.get_plan_status(plan.id)["status"]
        
        # Assign a task (should change to COORDINATING)
        next_task = coordinator.get_next_task(plan.id)
        if next_task:
            recommended_agents = coordinator.recommend_agent_for_task(next_task)
            if recommended_agents:
                coordinator.assign_task(plan.id, next_task.id, recommended_agents[0])
                
        coordinating_status = coordinator.get_plan_status(plan.id)["status"]
        
        status_transitions_correct = (
            initial_status == "planning" and
            coordinating_status == "coordinating"
        )
        
        if status_transitions_correct:
            self.log_test_result(
                "Coordination Status Transitions",
                True,
                "Status transitions working correctly",
                {
                    "initial_status": initial_status,
                    "after_assignment": coordinating_status
                }
            )
        else:
            self.log_test_result(
                "Coordination Status Transitions",
                False,
                "Status transitions not working correctly",
                {
                    "initial_status": initial_status,
                    "after_assignment": coordinating_status
                }
            )
            
    def run_all_tests(self) -> Dict:
        """Run all FeatureCoordinator tests"""
        print("🎯 Running Comprehensive FeatureCoordinator Tests")
        print("=" * 80)
        
        try:
            self.test_feature_analysis_basic()
            self.test_project_type_inference()
            self.test_tech_stack_inference()
            self.test_complexity_analysis()
            self.test_plan_creation()
            self.test_task_dependency_management()
            self.test_agent_recommendation()
            self.test_task_assignment_and_completion()
            self.test_squad_formation_different_project_types()
            self.test_plan_persistence()
            self.test_coordination_status_transitions()
            
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
        print("📊 FEATURE COORDINATOR TEST SUMMARY")
        print("=" * 80)
        print(f"Tests Passed: {passed_tests}/{total_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("🎉 ALL FEATURE COORDINATOR TESTS PASSED!")
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
    tester = FeatureCoordinatorTester()
    results = tester.run_all_tests()
    
    # Exit with error code if tests failed
    sys.exit(0 if results["passed_tests"] == results["total_tests"] else 1)