#!/usr/bin/env python3
"""
Master Test Runner for AgentRegistry System
Runs all test suites and generates comprehensive report
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Any

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def run_test_module(module_name: str) -> Dict[str, Any]:
    """Run a test module and return results"""
    print(f"\n{'='*80}")
    print(f"🏃‍♂️ RUNNING {module_name.upper()} TESTS")
    print(f"{'='*80}")
    
    try:
        # Import and run the test module
        if module_name == "agent_discovery":
            from test_agent_discovery import AgentDiscoveryTester
            tester = AgentDiscoveryTester()
            return tester.run_all_tests()
            
        elif module_name == "yaml_parsing":
            from test_yaml_parsing import YAMLParsingTester
            tester = YAMLParsingTester()
            return tester.run_all_tests()
            
        elif module_name == "feature_coordinator":
            from test_feature_coordinator import FeatureCoordinatorTester
            tester = FeatureCoordinatorTester()
            return tester.run_all_tests()
            
        elif module_name == "integration":
            from test_integration import IntegrationTester
            tester = IntegrationTester()
            return tester.run_all_tests()
            
        elif module_name == "performance":
            from test_performance import PerformanceTester
            tester = PerformanceTester()
            return tester.run_all_tests()
            
        else:
            return {
                "total_tests": 0,
                "passed_tests": 0,
                "success_rate": 0,
                "results": [],
                "error": f"Unknown test module: {module_name}"
            }
            
    except Exception as e:
        print(f"❌ Failed to run {module_name} tests: {e}")
        import traceback
        traceback.print_exc()
        return {
            "total_tests": 0,
            "passed_tests": 0,
            "success_rate": 0,
            "results": [],
            "error": str(e)
        }

def generate_comprehensive_report(all_results: Dict[str, Dict]) -> str:
    """Generate comprehensive test report"""
    
    # Calculate overall statistics
    total_tests = sum(results.get("total_tests", 0) for results in all_results.values())
    total_passed = sum(results.get("passed_tests", 0) for results in all_results.values())
    overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    # Count modules with issues
    failed_modules = [name for name, results in all_results.items() 
                     if results.get("success_rate", 0) < 100]
    
    report = []
    report.append("╔════════════════════════════════════════════════════════════════════════════════╗")
    report.append("║                      AGENTREGISTRY SYSTEM TEST REPORT                         ║")
    report.append("╠════════════════════════════════════════════════════════════════════════════════╣")
    report.append("║                                                                                ║")
    report.append(f"║  Test Execution Date: {time.strftime('%Y-%m-%d %H:%M:%S')}                               ║")
    report.append("║                                                                                ║")
    report.append("║  📊 OVERALL SUMMARY                                                           ║")
    report.append("║  ─────────────────────────────────────────────────────────────────────────  ║")
    report.append(f"║  Total Tests: {total_tests:<4}                                                      ║")
    report.append(f"║  Tests Passed: {total_passed:<4}                                                     ║")
    report.append(f"║  Success Rate: {overall_success_rate:.1f}%                                                    ║")
    report.append(f"║  Failed Modules: {len(failed_modules):<4}                                                   ║")
    report.append("║                                                                                ║")
    
    # Module breakdown
    report.append("║  📋 MODULE BREAKDOWN                                                          ║")
    report.append("║  ─────────────────────────────────────────────────────────────────────────  ║")
    
    for module_name, results in all_results.items():
        status_icon = "✅" if results.get("success_rate", 0) == 100 else "❌"
        passed = results.get("passed_tests", 0)
        total = results.get("total_tests", 0)
        rate = results.get("success_rate", 0)
        
        module_display = module_name.replace("_", " ").title()
        report.append(f"║  {status_icon} {module_display:<20}: {passed:>2}/{total:<2} tests ({rate:>5.1f}%)                ║")
    
    report.append("║                                                                                ║")
    
    # Issues section
    if failed_modules:
        report.append("║  ⚠️  ISSUES DETECTED                                                         ║")
        report.append("║  ─────────────────────────────────────────────────────────────────────────  ║")
        
        for module_name in failed_modules:
            results = all_results[module_name]
            failed_tests = [result for result in results.get("results", []) 
                          if not result.get("passed", True)]
            
            module_display = module_name.replace("_", " ").title()
            report.append(f"║  • {module_display}: {len(failed_tests)} failed test(s)                                      ║")
            
            for failed_test in failed_tests[:3]:  # Show first 3 failed tests
                test_name = failed_test.get("test", "Unknown")[:35]
                report.append(f"║    - {test_name:<35}                                   ║")
        
        report.append("║                                                                                ║")
    
    # Recommendations
    report.append("║  💡 RECOMMENDATIONS                                                           ║")
    report.append("║  ─────────────────────────────────────────────────────────────────────────  ║")
    
    if overall_success_rate >= 95:
        report.append("║  🎉 Excellent! System is ready for production deployment.                  ║")
        report.append("║  • All critical functionality working correctly                            ║")
        report.append("║  • Performance characteristics are acceptable                              ║")
        report.append("║  • Integration between components is solid                                 ║")
    elif overall_success_rate >= 80:
        report.append("║  ✅ Good! System is mostly ready with minor issues to address.           ║")
        report.append("║  • Core functionality working well                                         ║")
        report.append("║  • Address failing tests before production deployment                      ║")
        report.append("║  • Consider performance optimizations                                      ║")
    elif overall_success_rate >= 60:
        report.append("║  ⚠️  Moderate issues detected. System needs work before deployment.       ║")
        report.append("║  • Critical functionality may be impaired                                  ║")
        report.append("║  • Focus on fixing integration and core feature tests                      ║")
        report.append("║  • Performance testing should be addressed                                 ║")
    else:
        report.append("║  ❌ Significant issues detected. System not ready for deployment.         ║")
        report.append("║  • Core functionality is broken or unreliable                              ║")
        report.append("║  • Extensive debugging and fixes required                                  ║")
        report.append("║  • Consider architectural review                                            ║")
    
    report.append("║                                                                                ║")
    
    # Next steps
    report.append("║  🚀 NEXT STEPS                                                               ║")
    report.append("║  ─────────────────────────────────────────────────────────────────────────  ║")
    
    if "agent_discovery" in failed_modules:
        report.append("║  1. Fix agent discovery issues - critical for system operation            ║")
    if "yaml_parsing" in failed_modules:
        report.append("║  2. Resolve YAML parsing problems - affects agent metadata                ║")
    if "feature_coordinator" in failed_modules:
        report.append("║  3. Address coordinator issues - impacts task management                  ║")
    if "integration" in failed_modules:
        report.append("║  4. Fix integration problems - prevents proper system operation           ║")
    if "performance" in failed_modules:
        report.append("║  5. Optimize performance issues - affects user experience                 ║")
    
    if not failed_modules:
        report.append("║  1. Deploy to production environment                                       ║")
        report.append("║  2. Monitor system performance and usage                                   ║")
        report.append("║  3. Set up continuous integration testing                                  ║")
        report.append("║  4. Create user documentation and training materials                       ║")
    
    report.append("║                                                                                ║")
    report.append("╚════════════════════════════════════════════════════════════════════════════════╝")
    
    return "\n".join(report)

def save_detailed_results(all_results: Dict[str, Dict], report: str):
    """Save detailed test results to file"""
    output_dir = Path.home() / ".claude"
    output_dir.mkdir(exist_ok=True)
    
    # Save JSON results
    json_file = output_dir / "agentregistry_test_results.json"
    with open(json_file, 'w') as f:
        json.dump({
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "overall_stats": {
                "total_tests": sum(r.get("total_tests", 0) for r in all_results.values()),
                "passed_tests": sum(r.get("passed_tests", 0) for r in all_results.values()),
                "success_rate": sum(r.get("passed_tests", 0) for r in all_results.values()) / 
                               max(sum(r.get("total_tests", 0) for r in all_results.values()), 1) * 100
            },
            "module_results": all_results
        }, f, indent=2)
    
    # Save text report
    report_file = output_dir / "agentregistry_test_report.txt"
    with open(report_file, 'w') as f:
        f.write(report)
        f.write("\n\n" + "="*80 + "\n")
        f.write("DETAILED TEST RESULTS\n")
        f.write("="*80 + "\n\n")
        
        for module_name, results in all_results.items():
            f.write(f"{module_name.upper()} TESTS:\n")
            f.write("-" * 40 + "\n")
            for result in results.get("results", []):
                status = "PASS" if result.get("passed", False) else "FAIL"
                f.write(f"[{status}] {result.get('test', 'Unknown')}: {result.get('message', '')}\n")
                if result.get("details"):
                    for key, value in result["details"].items():
                        f.write(f"    {key}: {value}\n")
            f.write("\n")
    
    print(f"\n📄 Detailed results saved to:")
    print(f"  JSON: {json_file}")
    print(f"  Report: {report_file}")

def main():
    """Main test runner"""
    print("🎯 AgentRegistry System - Comprehensive Test Suite")
    print("=" * 80)
    
    start_time = time.time()
    
    # Test modules to run
    test_modules = [
        "agent_discovery",
        "yaml_parsing", 
        "feature_coordinator",
        "integration",
        "performance"
    ]
    
    all_results = {}
    
    # Run each test module
    for module in test_modules:
        results = run_test_module(module)
        all_results[module] = results
        
    total_time = time.time() - start_time
    
    # Generate and display comprehensive report
    print(f"\n\n⏱️  Total execution time: {total_time:.2f} seconds")
    
    report = generate_comprehensive_report(all_results)
    print(f"\n{report}")
    
    # Save detailed results
    save_detailed_results(all_results, report)
    
    # Exit with appropriate code
    overall_success = all(results.get("success_rate", 0) == 100 
                         for results in all_results.values())
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED! AgentRegistry system is ready for deployment!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Review the report above and fix issues before deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main()