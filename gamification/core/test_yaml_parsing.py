#!/usr/bin/env python3
"""
Comprehensive YAML Frontmatter Parsing Testing Script
Tests YAML parsing with valid/invalid frontmatter, missing metadata, and error handling
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agent_registry import AgentRegistry, AgentMetadata

class YAMLParsingTester:
    """Comprehensive testing suite for YAML frontmatter parsing"""
    
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
        
    def create_test_agent_file(self, content: str) -> Path:
        """Create a temporary agent file with given content"""
        temp_dir = Path(tempfile.mkdtemp())
        self.temp_dirs.append(temp_dir)
        
        agent_file = temp_dir / "test-agent.md"
        with open(agent_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return agent_file
        
    def cleanup_temp_dirs(self):
        """Clean up temporary directories"""
        for temp_dir in self.temp_dirs:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
        self.temp_dirs.clear()
        
    def test_valid_complete_yaml(self):
        """Test parsing of valid, complete YAML frontmatter"""
        print("🔍 Testing Valid Complete YAML...")
        
        content = """---
name: "Complete Agent"
description: "An agent with complete YAML frontmatter"
color: "#FF5733"
tools: "advanced-tools,testing-suite"
---

# Complete Agent

This agent has all the YAML fields properly defined.

## Core Competencies
- YAML parsing
- Metadata extraction
- Configuration management

## My Approach
I ensure all metadata is properly structured.
"""
        
        agent_file = self.create_test_agent_file(content)
        
        registry = AgentRegistry()
        agent_metadata = registry._analyze_agent_file(agent_file)
        
        if agent_metadata and agent_metadata.name == "Complete Agent":
            self.log_test_result(
                "Valid Complete YAML",
                True,
                "Successfully parsed complete YAML frontmatter",
                {
                    "name": agent_metadata.name,
                    "description": agent_metadata.description[:50] + "...",
                    "color": agent_metadata.color,
                    "tools": agent_metadata.tools,
                    "tech_stack": agent_metadata.tech_stack,
                    "specialties_count": len(agent_metadata.specialties)
                }
            )
        else:
            self.log_test_result(
                "Valid Complete YAML",
                False,
                "Failed to parse valid YAML frontmatter",
                {"agent_metadata": agent_metadata}
            )
            
    def test_minimal_yaml(self):
        """Test parsing of minimal YAML frontmatter"""
        print("🔍 Testing Minimal YAML...")
        
        content = """---
name: "Minimal Agent"
---

# Minimal Agent

This agent has minimal YAML frontmatter.
"""
        
        agent_file = self.create_test_agent_file(content)
        
        registry = AgentRegistry()
        agent_metadata = registry._analyze_agent_file(agent_file)
        
        if (agent_metadata and 
            agent_metadata.name == "Minimal Agent" and
            agent_metadata.description == "No description available"):
            self.log_test_result(
                "Minimal YAML",
                True,
                "Successfully parsed minimal YAML with defaults",
                {
                    "name": agent_metadata.name,
                    "description": agent_metadata.description,
                    "has_defaults": True
                }
            )
        else:
            self.log_test_result(
                "Minimal YAML",
                False,
                "Failed to handle minimal YAML properly"
            )
            
    def test_no_yaml_frontmatter(self):
        """Test parsing of file without YAML frontmatter"""
        print("🔍 Testing No YAML Frontmatter...")
        
        content = """# Agent Without YAML

This agent has no YAML frontmatter at all.

## Specialties
- Basic operations
- Simple tasks
"""
        
        agent_file = self.create_test_agent_file(content)
        
        registry = AgentRegistry()
        agent_metadata = registry._analyze_agent_file(agent_file)
        
        if (agent_metadata and 
            agent_metadata.name == "test-agent" and  # Should use filename
            agent_metadata.description == "No description available"):
            self.log_test_result(
                "No YAML Frontmatter",
                True,
                "Successfully handled missing YAML frontmatter",
                {
                    "name": agent_metadata.name,
                    "description": agent_metadata.description,
                    "specialties_extracted": len(agent_metadata.specialties) > 0
                }
            )
        else:
            self.log_test_result(
                "No YAML Frontmatter",
                False,
                "Failed to handle missing YAML frontmatter"
            )
            
    def test_invalid_yaml_syntax(self):
        """Test parsing of invalid YAML syntax"""
        print("🔍 Testing Invalid YAML Syntax...")
        
        content = """---
name: "Invalid YAML Agent"
description: This is missing quotes and has: invalid: nested: colons
color: #FF5733
tools: [unclosed bracket
---

# Invalid YAML Agent

This agent has malformed YAML frontmatter.
"""
        
        agent_file = self.create_test_agent_file(content)
        
        registry = AgentRegistry()
        agent_metadata = registry._analyze_agent_file(agent_file)
        
        # Should fallback gracefully
        if agent_metadata and agent_metadata.name == "test-agent":
            self.log_test_result(
                "Invalid YAML Syntax",
                True,
                "Gracefully handled invalid YAML syntax",
                {
                    "fallback_name": agent_metadata.name,
                    "fallback_description": agent_metadata.description
                }
            )
        else:
            self.log_test_result(
                "Invalid YAML Syntax",
                False,
                "Failed to handle invalid YAML syntax gracefully"
            )
            
    def test_incomplete_yaml_delimiters(self):
        """Test parsing with incomplete YAML delimiters"""
        print("🔍 Testing Incomplete YAML Delimiters...")
        
        content = """---
name: "Incomplete Delimiter Agent"
description: "This YAML is missing the closing delimiter"

# Agent Content

This should be treated as content, not YAML.
"""
        
        agent_file = self.create_test_agent_file(content)
        
        registry = AgentRegistry()
        agent_metadata = registry._analyze_agent_file(agent_file)
        
        # Should treat as no YAML frontmatter
        if agent_metadata and agent_metadata.name == "test-agent":
            self.log_test_result(
                "Incomplete YAML Delimiters",
                True,
                "Correctly handled incomplete YAML delimiters",
                {
                    "name": agent_metadata.name,
                    "treated_as_no_yaml": True
                }
            )
        else:
            self.log_test_result(
                "Incomplete YAML Delimiters",
                False,
                "Failed to handle incomplete YAML delimiters"
            )
            
    def test_yaml_with_special_characters(self):
        """Test YAML parsing with special characters"""
        print("🔍 Testing YAML with Special Characters...")
        
        content = """---
name: "Special Chars: Agent 🤖"
description: "Agent with émojis, accénts, and speciàl chars: @#$%^&*()"
color: "#FF5733"
tools: "spéciål-tøøls,unicode-support"
---

# Special Characters Agent

This agent tests unicode and special character handling.
"""
        
        agent_file = self.create_test_agent_file(content)
        
        registry = AgentRegistry()
        agent_metadata = registry._analyze_agent_file(agent_file)
        
        if (agent_metadata and 
            "🤖" in agent_metadata.name and
            "émojis" in agent_metadata.description):
            self.log_test_result(
                "YAML with Special Characters",
                True,
                "Successfully handled special characters and Unicode",
                {
                    "name": agent_metadata.name,
                    "unicode_preserved": True,
                    "special_chars_preserved": True
                }
            )
        else:
            self.log_test_result(
                "YAML with Special Characters",
                False,
                "Failed to handle special characters properly"
            )
            
    def test_yaml_with_multiline_values(self):
        """Test YAML parsing with multiline values"""
        print("🔍 Testing YAML with Multiline Values...")
        
        content = """---
name: "Multiline Agent"
description: |
  This is a multiline description
  that spans multiple lines
  and should be preserved properly
color: "#FF5733"
tools: >
  multiline-tool,
  another-tool,
  third-tool
---

# Multiline Agent

This agent tests multiline YAML values.
"""
        
        agent_file = self.create_test_agent_file(content)
        
        registry = AgentRegistry()
        agent_metadata = registry._analyze_agent_file(agent_file)
        
        if (agent_metadata and 
            "multiline description" in agent_metadata.description and
            "spans multiple lines" in agent_metadata.description):
            self.log_test_result(
                "YAML with Multiline Values",
                True,
                "Successfully parsed multiline YAML values",
                {
                    "name": agent_metadata.name,
                    "multiline_description": True,
                    "description_length": len(agent_metadata.description)
                }
            )
        else:
            self.log_test_result(
                "YAML with Multiline Values",
                False,
                "Failed to parse multiline YAML values"
            )
            
    def test_yaml_with_arrays_and_objects(self):
        """Test YAML parsing with arrays and nested objects"""
        print("🔍 Testing YAML with Arrays and Objects...")
        
        content = """---
name: "Complex YAML Agent"
description: "Agent with complex YAML structures"
tags:
  - testing
  - yaml
  - complex
config:
  level: advanced
  features:
    - feature1
    - feature2
  settings:
    debug: true
    timeout: 30
---

# Complex YAML Agent

This agent tests complex YAML structures.
"""
        
        agent_file = self.create_test_agent_file(content)
        
        registry = AgentRegistry()
        frontmatter, body = registry._parse_yaml_frontmatter(
            open(agent_file, 'r', encoding='utf-8').read()
        )
        
        if (frontmatter and 
            isinstance(frontmatter.get('tags'), list) and
            isinstance(frontmatter.get('config'), dict)):
            self.log_test_result(
                "YAML with Arrays and Objects",
                True,
                "Successfully parsed complex YAML structures",
                {
                    "has_arrays": isinstance(frontmatter.get('tags'), list),
                    "has_objects": isinstance(frontmatter.get('config'), dict),
                    "tags_count": len(frontmatter.get('tags', [])),
                    "config_keys": list(frontmatter.get('config', {}).keys())
                }
            )
        else:
            self.log_test_result(
                "YAML with Arrays and Objects",
                False,
                "Failed to parse complex YAML structures",
                {"frontmatter": frontmatter}
            )
            
    def test_yaml_type_coercion(self):
        """Test YAML type coercion (strings, numbers, booleans)"""
        print("🔍 Testing YAML Type Coercion...")
        
        content = """---
name: "Type Test Agent"
description: "Testing type coercion"
version: 1.5
enabled: true
count: 42
disabled: false
level: "3"
---

# Type Test Agent

Testing various YAML data types.
"""
        
        agent_file = self.create_test_agent_file(content)
        
        registry = AgentRegistry()
        frontmatter, body = registry._parse_yaml_frontmatter(
            open(agent_file, 'r', encoding='utf-8').read()
        )
        
        type_checks = {
            "version_is_float": isinstance(frontmatter.get('version'), float),
            "enabled_is_bool": isinstance(frontmatter.get('enabled'), bool),
            "count_is_int": isinstance(frontmatter.get('count'), int),
            "disabled_is_bool": isinstance(frontmatter.get('disabled'), bool),
            "level_is_string": isinstance(frontmatter.get('level'), str)
        }
        
        all_types_correct = all(type_checks.values())
        
        if all_types_correct:
            self.log_test_result(
                "YAML Type Coercion",
                True,
                "All YAML types coerced correctly",
                type_checks
            )
        else:
            self.log_test_result(
                "YAML Type Coercion",
                False,
                "Some YAML types not coerced correctly",
                type_checks
            )
            
    def test_empty_yaml_frontmatter(self):
        """Test parsing with empty YAML frontmatter"""
        print("🔍 Testing Empty YAML Frontmatter...")
        
        content = """---
---

# Empty YAML Agent

This agent has empty YAML frontmatter.
"""
        
        agent_file = self.create_test_agent_file(content)
        
        registry = AgentRegistry()
        agent_metadata = registry._analyze_agent_file(agent_file)
        
        if (agent_metadata and 
            agent_metadata.name == "test-agent" and
            agent_metadata.description == "No description available"):
            self.log_test_result(
                "Empty YAML Frontmatter",
                True,
                "Successfully handled empty YAML frontmatter",
                {
                    "name": agent_metadata.name,
                    "uses_defaults": True
                }
            )
        else:
            self.log_test_result(
                "Empty YAML Frontmatter",
                False,
                "Failed to handle empty YAML frontmatter"
            )
            
    def test_yaml_with_comments(self):
        """Test YAML parsing with comments"""
        print("🔍 Testing YAML with Comments...")
        
        content = """---
# This is a comment
name: "Commented Agent"  # Inline comment
description: "Agent with YAML comments"
# Another comment
color: "#FF5733"
# tools: "disabled-tool"  # Commented out field
tools: "active-tool"
---

# Commented Agent

This agent tests YAML comments.
"""
        
        agent_file = self.create_test_agent_file(content)
        
        registry = AgentRegistry()
        agent_metadata = registry._analyze_agent_file(agent_file)
        
        if (agent_metadata and 
            agent_metadata.name == "Commented Agent" and
            agent_metadata.tools == "active-tool"):
            self.log_test_result(
                "YAML with Comments",
                True,
                "Successfully parsed YAML with comments",
                {
                    "name": agent_metadata.name,
                    "tools": agent_metadata.tools,
                    "comments_ignored": True
                }
            )
        else:
            self.log_test_result(
                "YAML with Comments",
                False,
                "Failed to parse YAML with comments properly"
            )
            
    def run_all_tests(self) -> Dict:
        """Run all YAML parsing tests"""
        print("🎯 Running Comprehensive YAML Parsing Tests")
        print("=" * 80)
        
        try:
            self.test_valid_complete_yaml()
            self.test_minimal_yaml()
            self.test_no_yaml_frontmatter()
            self.test_invalid_yaml_syntax()
            self.test_incomplete_yaml_delimiters()
            self.test_yaml_with_special_characters()
            self.test_yaml_with_multiline_values()
            self.test_yaml_with_arrays_and_objects()
            self.test_yaml_type_coercion()
            self.test_empty_yaml_frontmatter()
            self.test_yaml_with_comments()
            
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
        print("📊 YAML PARSING TEST SUMMARY")
        print("=" * 80)
        print(f"Tests Passed: {passed_tests}/{total_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("🎉 ALL YAML PARSING TESTS PASSED!")
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
    tester = YAMLParsingTester()
    results = tester.run_all_tests()
    
    # Exit with error code if tests failed
    sys.exit(0 if results["passed_tests"] == results["total_tests"] else 1)