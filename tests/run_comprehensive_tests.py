#!/usr/bin/env python3
"""
Comprehensive test runner for Agent Forge State Generator.

Executes all test suites with coverage reporting, performance benchmarks,
and detailed results analysis.
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Any


class ComprehensiveTestRunner:
    """Comprehensive test runner with reporting and analysis."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.test_results = {
            "start_time": time.time(),
            "phases": {},
            "summary": {},
            "coverage": {},
            "performance": {}
        }
    
    def run_all_tests(self):
        """Run all test phases in sequence."""
        print("🧪 Starting Comprehensive Test Suite for Agent Forge")
        print("=" * 70)
        
        # Phase 1: Unit Tests
        self.run_test_phase("unit", "Unit Tests - Core Functionality", [
            "tests/unit/test_state_generator.py",
            "tests/unit/test_validation.py", 
            "tests/unit/test_database_hybrid.py",
            "tests/unit/test_templates.py",
            "tests/unit/test_lookup_service.py"
        ])
        
        # Phase 2: Integration Tests
        self.run_test_phase("integration", "Integration Tests - System Integration", [
            "tests/integration/test_simple_integration.py"
        ])
        
        # Phase 3: Performance Tests (if available)
        self.run_test_phase("performance", "Performance Tests - Benchmarks", [
            "tests/performance/"
        ], optional=True)
        
        # Generate final report
        self.generate_final_report()
    
    def run_test_phase(self, phase_name: str, phase_title: str, test_paths: List[str], optional: bool = False):
        """Run a specific test phase."""
        print(f"\n🏃 {phase_title}")
        print("-" * 50)
        
        phase_start = time.time()
        phase_results = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": [],
            "duration": 0
        }
        
        for test_path in test_paths:
            full_path = self.project_root / test_path
            
            if not full_path.exists():
                if optional:
                    print(f"⚠️  Optional test path not found: {test_path}")
                    continue
                else:
                    print(f"❌ Test path not found: {test_path}")
                    phase_results["errors"].append(f"Missing test path: {test_path}")
                    continue
            
            result = self.run_pytest_command(test_path, phase_name)
            
            # Parse results
            if result["returncode"] == 0:
                print(f"✅ {test_path} - All tests passed")
                phase_results["passed"] += result.get("passed", 0)
            else:
                print(f"❌ {test_path} - Some tests failed")
                phase_results["failed"] += result.get("failed", 0)
                phase_results["errors"].extend(result.get("errors", []))
            
            phase_results["skipped"] += result.get("skipped", 0)
        
        phase_results["duration"] = time.time() - phase_start
        self.test_results["phases"][phase_name] = phase_results
        
        # Phase summary
        total_tests = phase_results["passed"] + phase_results["failed"] + phase_results["skipped"]
        if total_tests > 0:
            success_rate = (phase_results["passed"] / total_tests) * 100
            print(f"📊 Phase Summary: {phase_results['passed']}/{total_tests} passed ({success_rate:.1f}%)")
        
        print(f"⏱️  Phase Duration: {phase_results['duration']:.2f}s")
    
    def run_pytest_command(self, test_path: str, phase_name: str) -> Dict[str, Any]:
        """Run pytest for a specific test path."""
        cmd = [
            sys.executable, "-m", "pytest",
            test_path,
            "-v",
            "--tb=short",
            f"--junitxml=test_results_{phase_name}.xml",
            "--json-report",
            f"--json-report-file=test_results_{phase_name}.json"
        ]
        
        # Add coverage for unit tests
        if phase_name == "unit":
            cmd.extend([
                "--cov=src",
                "--cov-report=term-missing",
                f"--cov-report=json:coverage_{phase_name}.json"
            ])
        
        # Add performance benchmarking for performance tests
        if phase_name == "performance":
            cmd.append("--benchmark-only")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "passed": self.extract_test_count(result.stdout, "passed"),
                "failed": self.extract_test_count(result.stdout, "failed"),
                "skipped": self.extract_test_count(result.stdout, "skipped"),
                "errors": self.extract_errors(result.stderr)
            }
            
        except subprocess.TimeoutExpired:
            return {
                "returncode": -1,
                "errors": [f"Test timeout for {test_path}"],
                "passed": 0,
                "failed": 1,
                "skipped": 0
            }
        except Exception as e:
            return {
                "returncode": -1,
                "errors": [f"Test execution error: {str(e)}"],
                "passed": 0,
                "failed": 1,
                "skipped": 0
            }
    
    def extract_test_count(self, output: str, status: str) -> int:
        """Extract test count from pytest output."""
        # Simple parsing - in production, would use JSON report
        lines = output.split('\n')
        for line in lines:
            if "passed" in line and "failed" in line:
                # Parse summary line like "5 passed, 2 failed, 1 skipped"
                parts = line.split(',')
                for part in parts:
                    if status in part:
                        try:
                            return int(part.strip().split()[0])
                        except (ValueError, IndexError):
                            continue
        return 0
    
    def extract_errors(self, stderr: str) -> List[str]:
        """Extract error messages from stderr."""
        if not stderr:
            return []
        
        errors = []
        lines = stderr.split('\n')
        for line in lines:
            if "ERROR" in line or "FAILED" in line:
                errors.append(line.strip())
        
        return errors[:5]  # Limit to first 5 errors
    
    def generate_final_report(self):
        """Generate comprehensive final test report."""
        self.test_results["end_time"] = time.time()
        self.test_results["total_duration"] = self.test_results["end_time"] - self.test_results["start_time"]
        
        # Calculate overall statistics
        total_passed = sum(phase["passed"] for phase in self.test_results["phases"].values())
        total_failed = sum(phase["failed"] for phase in self.test_results["phases"].values())
        total_skipped = sum(phase["skipped"] for phase in self.test_results["phases"].values())
        total_tests = total_passed + total_failed + total_skipped
        
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        self.test_results["summary"] = {
            "total_tests": total_tests,
            "passed": total_passed,
            "failed": total_failed,
            "skipped": total_skipped,
            "success_rate": success_rate,
            "phases_run": len(self.test_results["phases"])
        }
        
        # Print final report
        print("\n" + "=" * 70)
        print("🎉 COMPREHENSIVE TEST SUITE COMPLETE!")
        print("=" * 70)
        
        print(f"\n📊 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {total_passed}")
        print(f"   ❌ Failed: {total_failed}")
        print(f"   ⚠️  Skipped: {total_skipped}")
        print(f"   📈 Success Rate: {success_rate:.1f}%")
        print(f"   ⏱️  Total Duration: {self.test_results['total_duration']:.2f}s")
        
        print(f"\n📋 PHASE BREAKDOWN:")
        for phase_name, phase_data in self.test_results["phases"].items():
            phase_total = phase_data["passed"] + phase_data["failed"] + phase_data["skipped"]
            phase_rate = (phase_data["passed"] / phase_total * 100) if phase_total > 0 else 0
            
            print(f"   {phase_name.upper():12} | {phase_data['passed']:3}/{phase_total:3} | {phase_rate:5.1f}% | {phase_data['duration']:5.2f}s")
        
        # Coverage report (if available)
        self.print_coverage_summary()
        
        # Performance summary (if available)
        self.print_performance_summary()
        
        # Recommendations
        self.print_recommendations()
        
        # Save detailed report
        self.save_detailed_report()
    
    def print_coverage_summary(self):
        """Print coverage summary if available."""
        coverage_file = self.project_root / "coverage_unit.json"
        if coverage_file.exists():
            try:
                with open(coverage_file) as f:
                    coverage_data = json.load(f)
                
                total_coverage = coverage_data.get("totals", {}).get("percent_covered", 0)
                
                print(f"\n📊 CODE COVERAGE:")
                print(f"   Overall Coverage: {total_coverage:.1f}%")
                
                # Top files by coverage
                files = coverage_data.get("files", {})
                if files:
                    print("   Top Coverage Files:")
                    sorted_files = sorted(
                        files.items(), 
                        key=lambda x: x[1].get("summary", {}).get("percent_covered", 0),
                        reverse=True
                    )[:3]
                    
                    for file_path, file_data in sorted_files:
                        file_coverage = file_data.get("summary", {}).get("percent_covered", 0)
                        file_name = Path(file_path).name
                        print(f"     {file_name:20} {file_coverage:5.1f}%")
                        
            except Exception as e:
                print(f"   ⚠️  Could not read coverage data: {e}")
    
    def print_performance_summary(self):
        """Print performance benchmark summary if available."""
        # This would integrate with pytest-benchmark results
        print(f"\n⚡ PERFORMANCE BENCHMARKS:")
        print("   Performance tests: Not yet implemented")
        print("   Target: <200ms API response time (P95)")
        print("   Target: >70% cache hit rate")
    
    def print_recommendations(self):
        """Print recommendations based on test results."""
        print(f"\n💡 RECOMMENDATIONS:")
        
        success_rate = self.test_results["summary"]["success_rate"]
        
        if success_rate >= 95:
            print("   🎯 Excellent! Test suite is comprehensive and passing.")
            print("   📈 Ready for production deployment.")
        elif success_rate >= 85:
            print("   ✅ Good test coverage with minor issues to address.")
            print("   🔧 Fix failing tests before deployment.")
        elif success_rate >= 70:
            print("   ⚠️  Moderate success rate - significant issues present.")
            print("   🛠️  Address failing tests and improve coverage.")
        else:
            print("   🚨 Low success rate - major issues need attention.")
            print("   🔥 Focus on core functionality fixes.")
        
        # Phase-specific recommendations
        for phase_name, phase_data in self.test_results["phases"].items():
            if phase_data["failed"] > 0:
                print(f"   🔍 {phase_name.upper()}: {phase_data['failed']} failing tests need attention")
            
            if phase_data["errors"]:
                print(f"   ⚠️  {phase_name.upper()}: Check error logs for details")
    
    def save_detailed_report(self):
        """Save detailed test report to file."""
        report_file = self.project_root / "test_report.json"
        
        try:
            with open(report_file, 'w') as f:
                json.dump(self.test_results, f, indent=2, default=str)
            
            print(f"\n💾 Detailed report saved: {report_file}")
            
        except Exception as e:
            print(f"   ⚠️  Could not save detailed report: {e}")


def main():
    """Main entry point for test runner."""
    if len(sys.argv) > 1:
        phase = sys.argv[1]
        if phase in ["unit", "integration", "performance", "all"]:
            runner = ComprehensiveTestRunner()
            
            if phase == "all":
                runner.run_all_tests()
            else:
                print(f"Running {phase} tests only...")
                if phase == "unit":
                    runner.run_test_phase("unit", "Unit Tests", [
                        "tests/unit/test_state_generator.py",
                        "tests/unit/test_validation.py",
                        "tests/unit/test_database_hybrid.py",
                        "tests/unit/test_templates.py",
                        "tests/unit/test_lookup_service.py"
                    ])
                elif phase == "integration":
                    runner.run_test_phase("integration", "Integration Tests", [
                        "tests/integration/test_simple_integration.py"
                    ])
                elif phase == "performance":
                    runner.run_test_phase("performance", "Performance Tests", [
                        "tests/performance/"
                    ], optional=True)
                
                runner.generate_final_report()
        else:
            print("Usage: python run_comprehensive_tests.py [unit|integration|performance|all]")
    else:
        # Run all tests by default
        runner = ComprehensiveTestRunner()
        runner.run_all_tests()


if __name__ == "__main__":
    main() 