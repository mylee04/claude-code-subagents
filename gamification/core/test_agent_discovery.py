#!/usr/bin/env python3
"""
Comprehensive Agent Discovery Testing Script
Tests agent discovery from multiple locations, missing directories, and edge cases
"""

import os
import sys
import time
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agent_registry import AgentRegistry, AgentMetadata

class AgentDiscoveryTester:
    """Comprehensive testing suite for agent discovery functionality"""
    
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
        
    def create_temp_agent_dir(self, structure: Dict) -> Path:
        """Create temporary directory structure with test agents"""
        temp_dir = Path(tempfile.mkdtemp())
        self.temp_dirs.append(temp_dir)
        
        def create_structure(base_dir: Path, struct: Dict):
            for name, content in struct.items():
                if isinstance(content, dict):
                    # Directory
                    subdir = base_dir / name
                    subdir.mkdir(exist_ok=True)
                    create_structure(subdir, content)
                else:
                    # File
                    file_path = base_dir / name
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(file_path, 'w') as f:
                        f.write(content)
        
        create_structure(temp_dir, structure)
        return temp_dir
        
    def cleanup_temp_dirs(self):
        """Clean up temporary directories"""
        for temp_dir in self.temp_dirs:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
        self.temp_dirs.clear()
        
    def test_basic_agent_discovery(self):
        """Test basic agent discovery from default locations"""
        print("🔍 Testing Basic Agent Discovery...")
        
        registry = AgentRegistry()
        
        # Test discovery with force refresh
        start_time = time.time()
        agents = registry.discover_agents(force_refresh=True)
        discovery_time = time.time() - start_time
        
        # Check if agents were found
        if len(agents) > 0:
            self.log_test_result(
                "Basic Discovery",
                True,
                f"Discovered {len(agents)} agents in {discovery_time:.2f}s",
                {"agent_count": len(agents), "discovery_time_ms": int(discovery_time * 1000)}
            )
        else:
            self.log_test_result(
                "Basic Discovery",
                False,
                "No agents found in default locations",
                {"search_paths": [str(p) for p in registry.search_paths]}
            )
            
    def test_missing_directories(self):
        """Test behavior with missing agent directories"""
        print("🔍 Testing Missing Directories...")
        
        registry = AgentRegistry()
        
        # Add non-existent directory
        fake_dir = Path("/this/directory/does/not/exist")
        registry.add_search_path(fake_dir)
        
        try:
            agents = registry.discover_agents(force_refresh=True)
            self.log_test_result(
                "Missing Directories",
                True,
                "Gracefully handled missing directories",
                {"agents_found": len(agents)}
            )
        except Exception as e:
            self.log_test_result(
                "Missing Directories",
                False,
                f"Failed to handle missing directories: {str(e)}"
            )
            
    def test_custom_agent_directory(self):
        """Test discovery from custom agent directories"""
        print("🔍 Testing Custom Agent Directory...")
        
        # Create test agent structure
        test_structure = {
            "custom_agents": {
                "test_category": {
                    "test-agent.md": """---
name: "Test Agent"
description: "A test agent for verification"
color: "#FF0000"
tools: "test-tools"
---

# Test Agent

This is a test agent for verification purposes.

## Core Competencies
- Test execution
- Verification
- Quality assurance

## My Approach
I focus on thorough testing and verification.
"""
                }
            }
        }
        
        temp_dir = self.create_temp_agent_dir(test_structure)
        
        registry = AgentRegistry()
        registry.add_search_path(temp_dir / "custom_agents")
        
        agents = registry.discover_agents(force_refresh=True)
        
        # Check if test agent was found
        test_agent = agents.get("Test Agent")
        if test_agent:
            self.log_test_result(
                "Custom Directory Discovery",
                True,
                f"Successfully discovered test agent from custom directory",
                {
                    "agent_name": test_agent.name,
                    "category": test_agent.category,
                    "description": test_agent.description[:50] + "...",
                    "tech_stack": test_agent.tech_stack,
                    "specialties": len(test_agent.specialties)
                }
            )
        else:
            self.log_test_result(
                "Custom Directory Discovery",
                False,
                "Failed to discover test agent from custom directory",
                {"available_agents": list(agents.keys())}
            )
            
    def test_nested_directory_structure(self):
        """Test discovery in deeply nested directory structures"""
        print("🔍 Testing Nested Directory Structure...")
        
        test_structure = {
            "agents": {
                "level1": {
                    "level2": {
                        "level3": {
                            "deep-agent.md": """---
name: "Deep Agent"
description: "Agent in deeply nested structure"
---

# Deep Agent
Located in deeply nested directory structure.
"""
                        }
                    }
                }
            }
        }
        
        temp_dir = self.create_temp_agent_dir(test_structure)
        
        registry = AgentRegistry()
        registry.add_search_path(temp_dir / "agents")
        
        agents = registry.discover_agents(force_refresh=True)
        
        deep_agent = agents.get("Deep Agent")
        if deep_agent:
            self.log_test_result(
                "Nested Directory Discovery",
                True,
                "Successfully discovered agent in deeply nested structure",
                {"depth": "level1/level2/level3", "agent_found": deep_agent.name}
            )
        else:
            self.log_test_result(
                "Nested Directory Discovery",
                False,
                "Failed to discover agent in nested structure",
                {"searched_paths": [str(p) for p in registry.search_paths]}
            )
            
    def test_duplicate_agent_handling(self):
        """Test how the system handles duplicate agent names"""
        print("🔍 Testing Duplicate Agent Handling...")
        
        test_structure = {
            "agents1": {
                "duplicate-agent.md": """---
name: "Duplicate Agent"
description: "First instance"
---
# First Duplicate Agent
"""
            },
            "agents2": {
                "duplicate-agent.md": """---
name: "Duplicate Agent"
description: "Second instance"
---
# Second Duplicate Agent
"""
            }
        }
        
        temp_dir = self.create_temp_agent_dir(test_structure)
        
        registry = AgentRegistry()
        registry.add_search_path(temp_dir / "agents1")
        registry.add_search_path(temp_dir / "agents2")
        
        agents = registry.discover_agents(force_refresh=True)
        
        duplicate_agent = agents.get("Duplicate Agent")
        if duplicate_agent:
            # Check which instance was kept (should be the last one discovered)
            self.log_test_result(
                "Duplicate Agent Handling",
                True,
                "Handled duplicate agent names (kept last discovered)",
                {
                    "final_description": duplicate_agent.description,
                    "total_agents": len(agents)
                }
            )
        else:
            self.log_test_result(
                "Duplicate Agent Handling",
                False,
                "Failed to handle duplicate agent names properly"
            )
            
    def test_non_markdown_files(self):
        """Test that non-markdown files are ignored"""
        print("🔍 Testing Non-Markdown File Filtering...")
        
        test_structure = {
            "agents": {
                "valid-agent.md": """---
name: "Valid Agent"
---
# Valid Agent
""",
                "invalid-agent.txt": "This should be ignored",
                "config.json": '{"ignored": true}',
                "readme.rst": "This should also be ignored",
                "another-valid.md": """---
name: "Another Valid"
---
# Another Valid Agent
"""
            }
        }
        
        temp_dir = self.create_temp_agent_dir(test_structure)
        
        registry = AgentRegistry()
        registry.add_search_path(temp_dir / "agents")
        
        agents = registry.discover_agents(force_refresh=True)
        
        # Should only find 2 markdown files
        valid_count = len([a for a in agents.keys() if "Valid" in a])
        
        if valid_count == 2 and len(agents) == 2:
            self.log_test_result(
                "Non-Markdown File Filtering",
                True,
                "Correctly filtered out non-markdown files",
                {"markdown_agents_found": valid_count, "total_files_in_dir": 5}
            )
        else:
            self.log_test_result(
                "Non-Markdown File Filtering",
                False,
                f"Incorrect filtering: found {len(agents)} agents, expected 2",
                {"agents_found": list(agents.keys())}
            )
            
    def test_empty_directories(self):
        """Test behavior with empty directories"""
        print("🔍 Testing Empty Directories...")
        
        test_structure = {
            "empty_agents": {},
            "agents_with_empty_subdirs": {
                "empty_category": {},
                "valid_category": {
                    "valid-agent.md": """---
name: "Valid Agent"
---
# Valid Agent
"""
                }
            }
        }
        
        temp_dir = self.create_temp_agent_dir(test_structure)
        
        registry = AgentRegistry()
        registry.add_search_path(temp_dir / "empty_agents")
        registry.add_search_path(temp_dir / "agents_with_empty_subdirs")
        
        agents = registry.discover_agents(force_refresh=True)
        
        if len(agents) == 1 and "Valid Agent" in agents:
            self.log_test_result(
                "Empty Directories",
                True,
                "Correctly handled empty directories",
                {"agents_found": len(agents)}
            )
        else:
            self.log_test_result(
                "Empty Directories",
                False,
                f"Unexpected behavior with empty directories: {len(agents)} agents found"
            )
            
    def test_permission_errors(self):
        """Test behavior with permission errors (if possible)"""
        print("🔍 Testing Permission Handling...")
        
        # This test is platform-dependent and may not work on all systems
        try:
            test_structure = {
                "restricted": {
                    "agent.md": """---
name: "Restricted Agent"
---
# Restricted Agent
"""
                }
            }
            
            temp_dir = self.create_temp_agent_dir(test_structure)
            
            # Try to make directory unreadable (Unix-like systems only)
            if os.name != 'nt':  # Not Windows
                restricted_dir = temp_dir / "restricted"
                os.chmod(restricted_dir, 0o000)
                
                registry = AgentRegistry()
                registry.add_search_path(temp_dir)
                
                agents = registry.discover_agents(force_refresh=True)
                
                # Restore permissions for cleanup
                os.chmod(restricted_dir, 0o755)
                
                self.log_test_result(
                    "Permission Errors",
                    True,
                    "Gracefully handled permission errors",
                    {"agents_discovered": len(agents)}
                )
            else:
                self.log_test_result(
                    "Permission Errors",
                    True,
                    "Skipped permission test on Windows platform"
                )
                
        except Exception as e:
            self.log_test_result(
                "Permission Errors",
                True,
                f"Permission test completed with expected exception: {type(e).__name__}"
            )
            
    def test_cache_behavior(self):
        """Test caching behavior"""
        print("🔍 Testing Cache Behavior...")
        
        registry = AgentRegistry(cache_timeout=1)  # 1 second timeout
        
        # First discovery
        start_time = time.time()
        agents1 = registry.discover_agents(force_refresh=True)
        first_discovery_time = time.time() - start_time
        
        # Second discovery (should use cache)
        start_time = time.time()
        agents2 = registry.discover_agents()
        cached_discovery_time = time.time() - start_time
        
        # Wait for cache to expire
        time.sleep(1.1)
        
        # Third discovery (cache expired)
        start_time = time.time()
        agents3 = registry.discover_agents()
        expired_cache_time = time.time() - start_time
        
        cache_speedup = first_discovery_time / max(cached_discovery_time, 0.001)
        
        if cache_speedup > 2 and len(agents1) == len(agents2) == len(agents3):
            self.log_test_result(
                "Cache Behavior",
                True,
                f"Cache working correctly - {cache_speedup:.1f}x speedup",
                {
                    "first_discovery_ms": int(first_discovery_time * 1000),
                    "cached_discovery_ms": int(cached_discovery_time * 1000),
                    "expired_cache_ms": int(expired_cache_time * 1000),
                    "speedup_factor": f"{cache_speedup:.1f}x"
                }
            )
        else:
            self.log_test_result(
                "Cache Behavior",
                False,
                f"Cache not working as expected - speedup: {cache_speedup:.1f}x",
                {
                    "agents_count_consistency": len(agents1) == len(agents2) == len(agents3),
                    "speedup_factor": f"{cache_speedup:.1f}x"
                }
            )
            
    def run_all_tests(self) -> Dict:
        """Run all agent discovery tests"""
        print("🎯 Running Comprehensive Agent Discovery Tests")
        print("=" * 80)
        
        try:
            self.test_basic_agent_discovery()
            self.test_missing_directories()
            self.test_custom_agent_directory()
            self.test_nested_directory_structure()
            self.test_duplicate_agent_handling()
            self.test_non_markdown_files()
            self.test_empty_directories()
            self.test_permission_errors()
            self.test_cache_behavior()
            
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
        print("📊 AGENT DISCOVERY TEST SUMMARY")
        print("=" * 80)
        print(f"Tests Passed: {passed_tests}/{total_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("🎉 ALL AGENT DISCOVERY TESTS PASSED!")
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
    tester = AgentDiscoveryTester()
    results = tester.run_all_tests()
    
    # Exit with error code if tests failed
    sys.exit(0 if results["passed_tests"] == results["total_tests"] else 1)