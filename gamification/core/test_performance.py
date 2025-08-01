#!/usr/bin/env python3
"""
Comprehensive Performance Testing Script
Tests discovery time, cache effectiveness, memory usage, and scalability
"""

import os
import sys
import time
import gc
import psutil
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any
import tracemalloc

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agent_registry import AgentRegistry
from feature_coordinator import FeatureCoordinator

class PerformanceTester:
    """Comprehensive testing suite for performance characteristics"""
    
    def __init__(self):
        self.test_results = []
        self.temp_dirs = []
        
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
        
    def get_memory_usage(self):
        """Get current memory usage in MB"""
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024
        
    def create_large_agent_directory(self, agent_count: int) -> Path:
        """Create directory with many test agents for scalability testing"""
        temp_dir = Path(tempfile.mkdtemp())
        self.temp_dirs.append(temp_dir)
        
        agents_dir = temp_dir / "agents"
        agents_dir.mkdir()
        
        # Create agents in different categories
        categories = ["dev", "ops", "security", "data", "product"]
        
        for i in range(agent_count):
            category = categories[i % len(categories)]
            category_dir = agents_dir / category
            category_dir.mkdir(exist_ok=True)
            
            agent_file = category_dir / f"agent-{i:04d}.md"
            content = f"""---
name: "Performance Test Agent {i}"
description: "Agent {i} for performance testing"
color: "#FF{i:04X}"
tools: "performance-tool-{i}"
---

# Performance Test Agent {i}

This is performance test agent number {i}.

## Core Competencies
- Performance testing capability {i}
- Scalability validation {i}
- Load testing for scenario {i}

## My Approach
I handle performance test case {i} with efficiency and precision.
"""
            
            with open(agent_file, 'w') as f:
                f.write(content)
                
        return temp_dir
        
    def cleanup_temp_dirs(self):
        """Clean up temporary directories"""
        for temp_dir in self.temp_dirs:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
        self.temp_dirs.clear()
        
    def test_discovery_performance_baseline(self):
        """Test baseline discovery performance"""
        print("🔍 Testing Discovery Performance Baseline...")
        
        registry = AgentRegistry()
        
        # Warm up (ensure any lazy loading is done)
        registry.discover_agents(force_refresh=True)
        
        # Measure discovery time
        times = []
        for i in range(5):
            start_time = time.perf_counter()
            agents = registry.discover_agents(force_refresh=True)
            end_time = time.perf_counter()
            times.append(end_time - start_time)
            
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        # Performance criteria
        performance_acceptable = avg_time < 1.0  # Should complete in under 1 second
        consistency_good = (max_time - min_time) < avg_time * 0.5  # Variation < 50%
        
        if performance_acceptable and len(agents) > 0:
            self.log_test_result(
                "Discovery Performance Baseline",
                True,
                f"Discovery completed in {avg_time:.3f}s average",
                {
                    "agents_discovered": len(agents),
                    "avg_time_ms": int(avg_time * 1000),
                    "min_time_ms": int(min_time * 1000),
                    "max_time_ms": int(max_time * 1000),
                    "consistency_good": consistency_good,
                    "agents_per_second": len(agents) / avg_time
                }
            )
        else:
            self.log_test_result(
                "Discovery Performance Baseline",
                False,
                f"Discovery too slow: {avg_time:.3f}s average" if performance_acceptable else "No agents found",
                {
                    "avg_time_ms": int(avg_time * 1000),
                    "agents_discovered": len(agents)
                }
            )
            
    def test_scalability_with_many_agents(self):
        """Test scalability with increasing numbers of agents"""
        print("🔍 Testing Scalability with Many Agents...")
        
        agent_counts = [10, 50, 100, 200]
        scalability_results = []
        
        for count in agent_counts:
            print(f"  Testing with {count} agents...")
            
            # Create test directory with many agents
            test_dir = self.create_large_agent_directory(count)
            
            registry = AgentRegistry()
            registry.add_search_path(test_dir / "agents")
            
            # Measure discovery time
            start_time = time.perf_counter()
            start_memory = self.get_memory_usage()
            
            agents = registry.discover_agents(force_refresh=True)
            
            end_time = time.perf_counter()
            end_memory = self.get_memory_usage()
            
            discovery_time = end_time - start_time
            memory_used = end_memory - start_memory
            
            scalability_results.append({
                "agent_count": count,
                "discovery_time": discovery_time,
                "memory_used_mb": memory_used,
                "agents_per_second": len(agents) / discovery_time,
                "kb_per_agent": (memory_used * 1024) / len(agents) if len(agents) > 0 else 0
            })
            
        # Analyze scalability
        time_grows_linearly = True
        memory_grows_linearly = True
        
        for i in range(1, len(scalability_results)):
            prev = scalability_results[i-1]
            curr = scalability_results[i]
            
            # Time should grow roughly linearly (within 2x factor)
            expected_time = prev["discovery_time"] * (curr["agent_count"] / prev["agent_count"])
            if curr["discovery_time"] > expected_time * 2:
                time_grows_linearly = False
                
            # Memory should grow roughly linearly (within 2x factor)
            expected_memory = prev["memory_used_mb"] * (curr["agent_count"] / prev["agent_count"])
            if curr["memory_used_mb"] > expected_memory * 2:
                memory_grows_linearly = False
                
        scalability_good = time_grows_linearly and memory_grows_linearly
        
        if scalability_good:
            self.log_test_result(
                "Scalability with Many Agents",
                True,
                "System scales well with increasing agent count",
                {
                    "max_agents_tested": max(agent_counts),
                    "time_scalability": "Linear" if time_grows_linearly else "Poor",
                    "memory_scalability": "Linear" if memory_grows_linearly else "Poor",
                    "results": scalability_results
                }
            )
        else:
            self.log_test_result(
                "Scalability with Many Agents",
                False,
                "System does not scale well",
                {
                    "time_scalability": "Linear" if time_grows_linearly else "Poor",
                    "memory_scalability": "Linear" if memory_grows_linearly else "Poor",
                    "results": scalability_results
                }
            )
            
    def test_cache_performance_impact(self):
        """Test performance impact of caching"""
        print("🔍 Testing Cache Performance Impact...")
        
        registry = AgentRegistry(cache_timeout=10)
        
        # Cold cache (first discovery)
        start_time = time.perf_counter()
        agents_cold = registry.discover_agents(force_refresh=True)
        cold_time = time.perf_counter() - start_time
        
        # Warm cache (multiple subsequent discoveries)
        warm_times = []
        for _ in range(10):
            start_time = time.perf_counter()
            agents_warm = registry.discover_agents()
            warm_time = time.perf_counter() - start_time
            warm_times.append(warm_time)
            
        avg_warm_time = sum(warm_times) / len(warm_times)
        
        # Calculate performance metrics
        if avg_warm_time > 0:
            speedup = cold_time / avg_warm_time
        else:
            speedup = float('inf')
            
        cache_effective = speedup > 10 and avg_warm_time < 0.01
        data_consistent = len(agents_cold) == len(agents_warm)
        
        if cache_effective and data_consistent:
            self.log_test_result(
                "Cache Performance Impact",
                True,
                f"Cache provides {speedup:.1f}x speedup",
                {
                    "cold_cache_ms": int(cold_time * 1000),
                    "avg_warm_cache_ms": int(avg_warm_time * 1000),
                    "speedup_factor": f"{speedup:.1f}x",
                    "data_consistent": data_consistent,
                    "cache_hit_time_us": int(avg_warm_time * 1000000)
                }
            )
        else:
            self.log_test_result(
                "Cache Performance Impact",
                False,
                f"Cache not effective - speedup: {speedup:.1f}x",
                {
                    "cold_cache_ms": int(cold_time * 1000),
                    "avg_warm_cache_ms": int(avg_warm_time * 1000),
                    "data_consistent": data_consistent
                }
            )
            
    def test_memory_usage_and_leaks(self):
        """Test memory usage and potential leaks"""
        print("🔍 Testing Memory Usage and Leaks...")
        
        # Start memory tracing
        tracemalloc.start()
        
        initial_memory = self.get_memory_usage()
        
        # Create many registries and coordinators
        registries = []
        coordinators = []
        
        for i in range(20):
            registry = AgentRegistry()
            coordinator = FeatureCoordinator()
            
            # Use them briefly
            agents = registry.discover_agents()
            if len(agents) > 0:
                analysis = coordinator.analyze_feature_request(f"Test request {i}")
                
            registries.append(registry)
            coordinators.append(coordinator)
            
        peak_memory = self.get_memory_usage()
        memory_used = peak_memory - initial_memory
        
        # Clean up references
        registries.clear()
        coordinators.clear()
        
        # Force garbage collection
        gc.collect()
        
        final_memory = self.get_memory_usage()
        memory_freed = peak_memory - final_memory
        
        # Get tracemalloc stats
        current_trace, peak_trace = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Memory criteria
        reasonable_usage = memory_used < 100  # Less than 100MB for 20 instances
        good_cleanup = memory_freed > memory_used * 0.7  # At least 70% cleaned up
        
        if reasonable_usage and good_cleanup:
            self.log_test_result(
                "Memory Usage and Leaks",
                True,
                f"Memory usage reasonable: {memory_used:.1f}MB used, {memory_freed:.1f}MB freed",
                {
                    "peak_memory_mb": peak_memory,
                    "memory_used_mb": memory_used,
                    "memory_freed_mb": memory_freed,
                    "cleanup_percentage": int((memory_freed / memory_used) * 100) if memory_used > 0 else 0,
                    "tracemalloc_peak_mb": peak_trace / 1024 / 1024
                }
            )
        else:
            self.log_test_result(
                "Memory Usage and Leaks",
                False,
                f"Memory issues detected: {memory_used:.1f}MB used, {memory_freed:.1f}MB freed",
                {
                    "memory_used_mb": memory_used,
                    "memory_freed_mb": memory_freed,
                    "reasonable_usage": reasonable_usage,
                    "good_cleanup": good_cleanup
                }
            )
            
    def test_concurrent_discovery_performance(self):
        """Test performance under simulated concurrent access"""
        print("🔍 Testing Concurrent Discovery Performance...")
        
        import threading
        import queue
        
        result_queue = queue.Queue()
        
        def discovery_worker(worker_id, results_queue):
            """Worker function for concurrent discovery"""
            registry = AgentRegistry()
            
            start_time = time.perf_counter()
            agents = registry.discover_agents()
            end_time = time.perf_counter()
            
            results_queue.put({
                "worker_id": worker_id,
                "discovery_time": end_time - start_time,
                "agents_count": len(agents),
                "success": len(agents) > 0
            })
            
        # Launch concurrent workers
        threads = []
        worker_count = 10
        
        start_time = time.perf_counter()
        
        for i in range(worker_count):
            thread = threading.Thread(target=discovery_worker, args=(i, result_queue))
            threads.append(thread)
            thread.start()
            
        # Wait for all workers to complete
        for thread in threads:
            thread.join()
            
        total_time = time.perf_counter() - start_time
        
        # Collect results
        results = []
        while not result_queue.empty():
            results.append(result_queue.get())
            
        # Analyze results
        all_successful = all(result["success"] for result in results)
        avg_individual_time = sum(result["discovery_time"] for result in results) / len(results)
        consistent_results = len(set(result["agents_count"] for result in results)) == 1
        
        concurrent_efficient = total_time < avg_individual_time * 2  # Should be much faster than sequential
        
        if all_successful and consistent_results and concurrent_efficient:
            self.log_test_result(
                "Concurrent Discovery Performance",
                True,
                f"Concurrent access handled efficiently: {worker_count} workers in {total_time:.3f}s",
                {
                    "worker_count": worker_count,
                    "total_time_ms": int(total_time * 1000),
                    "avg_individual_time_ms": int(avg_individual_time * 1000),
                    "all_successful": all_successful,
                    "results_consistent": consistent_results,
                    "efficiency_gain": f"{(avg_individual_time * worker_count / total_time):.1f}x"
                }
            )
        else:
            self.log_test_result(
                "Concurrent Discovery Performance",
                False,
                "Concurrent access issues detected",
                {
                    "all_successful": all_successful,
                    "results_consistent": consistent_results,
                    "concurrent_efficient": concurrent_efficient,
                    "total_time_ms": int(total_time * 1000)
                }
            )
            
    def test_feature_coordinator_performance(self):
        """Test FeatureCoordinator performance characteristics"""
        print("🔍 Testing FeatureCoordinator Performance...")
        
        coordinator = FeatureCoordinator()
        
        # Test analysis performance
        analysis_times = []
        for i in range(10):
            start_time = time.perf_counter()
            analysis = coordinator.analyze_feature_request(
                f"Build a complex web application with authentication, payments, and analytics {i}",
                tech_stack=["python", "javascript", "sql"]
            )
            end_time = time.perf_counter()
            analysis_times.append(end_time - start_time)
            
        avg_analysis_time = sum(analysis_times) / len(analysis_times)
        
        # Test plan creation performance
        plan_times = []
        for i in range(5):
            start_time = time.perf_counter()
            plan = coordinator.create_feature_plan(
                f"Performance Test Plan {i}",
                f"Performance test plan {i}",
                tech_stack=["python", "react"]
            )
            end_time = time.perf_counter()
            plan_times.append(end_time - start_time)
            
        avg_plan_time = sum(plan_times) / len(plan_times)
        
        # Performance criteria
        analysis_fast = avg_analysis_time < 0.1  # Under 100ms
        plan_creation_fast = avg_plan_time < 0.5  # Under 500ms
        
        if analysis_fast and plan_creation_fast:
            self.log_test_result(
                "FeatureCoordinator Performance",
                True,
                f"Coordinator performs well: {avg_analysis_time:.3f}s analysis, {avg_plan_time:.3f}s plan creation",
                {
                    "avg_analysis_time_ms": int(avg_analysis_time * 1000),
                    "avg_plan_creation_time_ms": int(avg_plan_time * 1000),
                    "analysis_samples": len(analysis_times),
                    "plan_samples": len(plan_times)
                }
            )
        else:
            self.log_test_result(
                "FeatureCoordinator Performance",
                False,
                f"Coordinator performance issues: {avg_analysis_time:.3f}s analysis, {avg_plan_time:.3f}s plan creation",
                {
                    "avg_analysis_time_ms": int(avg_analysis_time * 1000),
                    "avg_plan_creation_time_ms": int(avg_plan_time * 1000),
                    "analysis_fast": analysis_fast,
                    "plan_creation_fast": plan_creation_fast
                }
            )
            
    def test_disk_io_performance(self):
        """Test disk I/O performance for persistence"""
        print("🔍 Testing Disk I/O Performance...")
        
        coordinator = FeatureCoordinator()
        
        # Test plan persistence performance
        persist_times = []
        for i in range(20):
            plan = coordinator.create_feature_plan(
                f"IO Test Plan {i}",
                f"Testing disk I/O performance {i}",
                tech_stack=["python"]
            )
            
            if plan:
                start_time = time.perf_counter()
                # Trigger explicit save by modifying plan
                coordinator._save_plans()
                end_time = time.perf_counter()
                persist_times.append(end_time - start_time)
                
        if persist_times:
            avg_persist_time = sum(persist_times) / len(persist_times)
            max_persist_time = max(persist_times)
            
            # Test load performance
            load_times = []
            for i in range(10):
                start_time = time.perf_counter()
                new_coordinator = FeatureCoordinator()
                end_time = time.perf_counter()
                load_times.append(end_time - start_time)
                
            avg_load_time = sum(load_times) / len(load_times)
            
            # Performance criteria
            persist_fast = avg_persist_time < 0.1  # Under 100ms
            load_fast = avg_load_time < 0.5  # Under 500ms
            
            if persist_fast and load_fast:
                self.log_test_result(
                    "Disk I/O Performance",
                    True,
                    f"Disk I/O performs well: {avg_persist_time:.3f}s persist, {avg_load_time:.3f}s load",
                    {
                        "avg_persist_time_ms": int(avg_persist_time * 1000),
                        "max_persist_time_ms": int(max_persist_time * 1000),
                        "avg_load_time_ms": int(avg_load_time * 1000),
                        "persist_samples": len(persist_times),
                        "load_samples": len(load_times)
                    }
                )
            else:
                self.log_test_result(
                    "Disk I/O Performance",
                    False,
                    f"Disk I/O performance issues: {avg_persist_time:.3f}s persist, {avg_load_time:.3f}s load",
                    {
                        "avg_persist_time_ms": int(avg_persist_time * 1000),
                        "avg_load_time_ms": int(avg_load_time * 1000),
                        "persist_fast": persist_fast,
                        "load_fast": load_fast
                    }
                )
        else:
            self.log_test_result(
                "Disk I/O Performance",
                False,
                "Could not test disk I/O - no plans created"
            )
            
    def run_all_tests(self) -> Dict:
        """Run all performance tests"""
        print("🎯 Running Comprehensive Performance Tests")
        print("=" * 80)
        
        try:
            self.test_discovery_performance_baseline()
            self.test_scalability_with_many_agents()
            self.test_cache_performance_impact()
            self.test_memory_usage_and_leaks()
            self.test_concurrent_discovery_performance()
            self.test_feature_coordinator_performance()
            self.test_disk_io_performance()
            
        except Exception as e:
            print(f"❌ Test suite failed with error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup_temp_dirs()
            
        # Generate summary
        passed_tests = sum(1 for result in self.test_results if result["passed"])
        total_tests = len(self.test_results)
        
        print("\n" + "=" * 80)
        print("📊 PERFORMANCE TEST SUMMARY")
        print("=" * 80)
        print(f"Tests Passed: {passed_tests}/{total_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("🎉 ALL PERFORMANCE TESTS PASSED!")
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
    tester = PerformanceTester()
    results = tester.run_all_tests()
    
    # Exit with error code if tests failed
    sys.exit(0 if results["passed_tests"] == results["total_tests"] else 1)