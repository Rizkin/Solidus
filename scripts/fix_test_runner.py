#!/usr/bin/env python3
"""
Improved Test Runner for Agent Forge State Generator
Fixes environment setup and handles pytest configuration properly
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class ImprovedTestRunner:
    """Improved test runner with proper environment setup"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.results = {
            "start_time": time.time(),
            "environment_setup": {},
            "test_phases": {},
            "summary": {}
        }
        
    def setup_environment(self) -> Dict[str, Any]:
        """Set up the test environment properly"""
        print("🔧 Setting up test environment...")
        
        setup_result = {
            "python_path": None,
            "pytest_available": False,
            "dependencies_checked": False,
            "environment_vars": {},
            "issues": []
        }
        
        # Set PYTHONPATH
        python_path = str(self.project_root.absolute())
        os.environ['PYTHONPATH'] = python_path
        setup_result["python_path"] = python_path
        print(f"✅ PYTHONPATH set to: {python_path}")
        
        # Check Python and pytest
        try:
            result = subprocess.run([sys.executable, "-m", "pytest", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                setup_result["pytest_available"] = True
                print(f"✅ pytest available: {result.stdout.strip()}")
            else:
                setup_result["issues"].append(f"pytest check failed: {result.stderr}")
                print(f"❌ pytest check failed: {result.stderr}")
        except Exception as e:
            setup_result["issues"].append(f"pytest check error: {e}")
            print(f"❌ pytest check error: {e}")
        
        # Check key dependencies
        key_deps = ["anthropic", "supabase", "pytest-asyncio", "pytest-cov"]
        missing_deps = []
        
        for dep in key_deps:
            try:
                result = subprocess.run([sys.executable, "-c", f"import {dep}; print('OK')"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ {dep} available")
                else:
                    missing_deps.append(dep)
                    print(f"❌ {dep} not available")
            except Exception as e:
                missing_deps.append(dep)
                print(f"❌ {dep} check failed: {e}")
        
        if not missing_deps:
            setup_result["dependencies_checked"] = True
        else:
            setup_result["issues"].append(f"Missing dependencies: {missing_deps}")
        
        # Check environment variables
        env_vars = {
            "SUPABASE_URL": os.getenv("SUPABASE_URL"),
            "SUPABASE_SERVICE_KEY": os.getenv("SUPABASE_SERVICE_KEY"),
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY")
        }
        
        for var, value in env_vars.items():
            if value:
                setup_result["environment_vars"][var] = f"SET ({len(value)} chars)"
            else:
                setup_result["environment_vars"][var] = "NOT_SET"
        
        self.results["environment_setup"] = setup_result
        return setup_result
    
    def run_pytest_command(self, test_paths: List[str], phase_name: str, 
                          additional_args: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run a pytest command with proper error handling"""
        
        phase_result = {
            "phase": phase_name,
            "start_time": time.time(),
            "command": [],
            "return_code": None,
            "stdout": "",
            "stderr": "",
            "tests_collected": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "tests_skipped": 0,
            "duration": 0,
            "success": False
        }
        
        # Build pytest command
        cmd = [
            sys.executable, "-m", "pytest",
            "--tb=short",
            "-v",
            "--no-cov",  # Disable coverage for faster testing
            "--disable-warnings"  # Reduce warning noise
        ]
        
        if additional_args:
            cmd.extend(additional_args)
        
        cmd.extend(test_paths)
        phase_result["command"] = cmd
        
        print(f"\n🧪 Running {phase_name}...")
        print(f"Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            phase_result["return_code"] = result.returncode
            phase_result["stdout"] = result.stdout
            phase_result["stderr"] = result.stderr
            phase_result["duration"] = time.time() - phase_result["start_time"]
            
            # Parse pytest output for test counts
            output = result.stdout + result.stderr
            
            # Look for collection info
            if "collected" in output:
                for line in output.split('\n'):
                    if "collected" in line and "items" in line:
                        try:
                            # Extract number before "items"
                            parts = line.split()
                            for i, part in enumerate(parts):
                                if part == "items" and i > 0:
                                    phase_result["tests_collected"] = int(parts[i-1])
                                    break
                        except (ValueError, IndexError):
                            pass
            
            # Look for test results
            if "passed" in output or "failed" in output:
                for line in output.split('\n'):
                    if "passed" in line and "failed" in line:
                        # Parse line like "2 passed, 1 failed in 1.23s"
                        try:
                            parts = line.split()
                            for i, part in enumerate(parts):
                                if part == "passed" and i > 0:
                                    phase_result["tests_passed"] = int(parts[i-1])
                                elif part == "failed" and i > 0:
                                    phase_result["tests_failed"] = int(parts[i-1])
                                elif part == "skipped" and i > 0:
                                    phase_result["tests_skipped"] = int(parts[i-1])
                        except (ValueError, IndexError):
                            pass
            
            # Determine success
            if result.returncode == 0:
                phase_result["success"] = True
                print(f"✅ {phase_name} completed successfully")
            else:
                phase_result["success"] = False
                print(f"❌ {phase_name} failed with return code {result.returncode}")
                
                # Print error details
                if result.stderr:
                    print(f"STDERR: {result.stderr[:500]}...")
                if result.stdout and "ERROR" in result.stdout:
                    print(f"STDOUT errors: {result.stdout[:500]}...")
            
        except subprocess.TimeoutExpired:
            phase_result["duration"] = time.time() - phase_result["start_time"]
            phase_result["stderr"] = "Command timed out after 5 minutes"
            print(f"❌ {phase_name} timed out")
        except Exception as e:
            phase_result["duration"] = time.time() - phase_result["start_time"]
            phase_result["stderr"] = str(e)
            print(f"❌ {phase_name} failed with exception: {e}")
        
        return phase_result
    
    def run_collection_test(self) -> Dict[str, Any]:
        """Test that tests can be collected without errors"""
        print("\n📋 Testing test collection...")
        
        test_dirs = [
            "tests/unit/",
            "tests/integration/",
        ]
        
        collection_results = {}
        
        for test_dir in test_dirs:
            test_path = self.project_root / test_dir
            if test_path.exists():
                result = self.run_pytest_command(
                    [str(test_path)], 
                    f"Collection Test - {test_dir}",
                    ["--collect-only"]
                )
                collection_results[test_dir] = result
            else:
                print(f"⚠️  Test directory not found: {test_dir}")
        
        return collection_results
    
    def run_unit_tests(self) -> Dict[str, Any]:
        """Run unit tests"""
        test_files = [
            "tests/unit/test_database_hybrid.py",
            "tests/unit/test_state_generator.py",
            "tests/unit/test_validation.py",
            "tests/unit/test_templates.py",
            "tests/unit/test_lookup_service.py"
        ]
        
        # Filter to only existing files
        existing_files = []
        for test_file in test_files:
            test_path = self.project_root / test_file
            if test_path.exists():
                existing_files.append(str(test_path))
            else:
                print(f"⚠️  Test file not found: {test_file}")
        
        if existing_files:
            return self.run_pytest_command(existing_files, "Unit Tests")
        else:
            return {"success": False, "error": "No unit test files found"}
    
    def run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests"""
        integration_path = self.project_root / "tests/integration/"
        
        if integration_path.exists():
            return self.run_pytest_command([str(integration_path)], "Integration Tests")
        else:
            return {"success": False, "error": "Integration test directory not found"}
    
    def generate_report(self):
        """Generate a comprehensive test report"""
        
        total_duration = time.time() - self.results["start_time"]
        
        # Calculate summary
        total_collected = 0
        total_passed = 0
        total_failed = 0
        total_skipped = 0
        phases_run = 0
        successful_phases = 0
        
        for phase_name, phase_result in self.results["test_phases"].items():
            if isinstance(phase_result, dict):
                phases_run += 1
                if phase_result.get("success", False):
                    successful_phases += 1
                
                total_collected += phase_result.get("tests_collected", 0)
                total_passed += phase_result.get("tests_passed", 0)
                total_failed += phase_result.get("tests_failed", 0)
                total_skipped += phase_result.get("tests_skipped", 0)
        
        self.results["summary"] = {
            "total_duration": total_duration,
            "phases_run": phases_run,
            "successful_phases": successful_phases,
            "total_collected": total_collected,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_skipped": total_skipped,
            "success_rate": (successful_phases / phases_run * 100) if phases_run > 0 else 0
        }
        
        # Save detailed report
        report_file = self.project_root / "improved_test_report.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 TEST EXECUTION SUMMARY")
        print("="*60)
        print(f"Total Duration: {total_duration:.2f}s")
        print(f"Phases Run: {successful_phases}/{phases_run}")
        print(f"Tests Collected: {total_collected}")
        print(f"Tests Passed: {total_passed}")
        print(f"Tests Failed: {total_failed}")
        print(f"Tests Skipped: {total_skipped}")
        print(f"Success Rate: {self.results['summary']['success_rate']:.1f}%")
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        # Print environment issues if any
        env_issues = self.results["environment_setup"].get("issues", [])
        if env_issues:
            print("\n⚠️  Environment Issues:")
            for issue in env_issues:
                print(f"   - {issue}")
    
    def run_all_tests(self):
        """Run the complete test suite"""
        print("🚀 Agent Forge Improved Test Runner")
        print("="*60)
        
        # Setup environment
        env_setup = self.setup_environment()
        
        if not env_setup["pytest_available"]:
            print("❌ Cannot proceed without pytest")
            return
        
        # Run test collection first
        collection_results = self.run_collection_test()
        self.results["test_phases"]["collection"] = collection_results
        
        # Run unit tests
        unit_results = self.run_unit_tests()
        self.results["test_phases"]["unit_tests"] = unit_results
        
        # Run integration tests
        integration_results = self.run_integration_tests()
        self.results["test_phases"]["integration_tests"] = integration_results
        
        # Generate report
        self.generate_report()

def main():
    """Main entry point"""
    runner = ImprovedTestRunner()
    runner.run_all_tests()

if __name__ == "__main__":
    main() 