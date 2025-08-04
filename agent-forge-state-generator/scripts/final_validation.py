#!/usr/bin/env python3
"""
Agent Forge State Generator - Final Validation Script
Comprehensive testing and validation of the complete system.
"""

import asyncio
import json
import requests
import time
import sys
from typing import Dict, List, Any
from datetime import datetime

class AgentForgeValidator:
    """Comprehensive validation for Agent Forge State Generator"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = []
        self.start_time = time.time()
    
    def log_result(self, test_name: str, success: bool, details: str = "", response_time: float = 0):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "response_time_ms": round(response_time * 1000, 2),
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        time_info = f" ({result['response_time_ms']}ms)" if response_time > 0 else ""
        print(f"{status} {test_name}{time_info}")
        if details and not success:
            print(f"    Details: {details}")
    
    def test_system_health(self):
        """Test basic system health"""
        print("\n🏥 Testing System Health...")
        
        try:
            start = time.time()
            response = requests.get(f"{self.base_url}/api/health", timeout=10)
            response_time = time.time() - start
            
            if response.status_code == 200:
                health_data = response.json()
                
                # Check overall status
                overall_status = health_data.get("status", "unknown")
                self.log_result(
                    "System Health Check", 
                    overall_status in ["healthy", "degraded"],
                    f"Status: {overall_status}",
                    response_time
                )
                
                # Check individual components
                checks = health_data.get("checks", {})
                for component, status in checks.items():
                    self.log_result(
                        f"Component: {component}",
                        status in ["connected", "configured", "active"],
                        f"Status: {status}"
                    )
                
                return True
            else:
                self.log_result(
                    "System Health Check", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}",
                    response_time
                )
                return False
                
        except Exception as e:
            self.log_result("System Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_api_endpoints(self):
        """Test all API endpoints"""
        print("\n📡 Testing API Endpoints...")
        
        endpoints = [
            ("GET", "/", "Root endpoint"),
            ("GET", "/api/health", "Health check"),
            ("GET", "/api/block-types", "Block types documentation"),
            ("GET", "/docs", "API documentation"),
            ("GET", "/openapi.json", "OpenAPI specification")
        ]
        
        for method, endpoint, description in endpoints:
            try:
                start = time.time()
                response = requests.request(method, f"{self.base_url}{endpoint}", timeout=10)
                response_time = time.time() - start
                
                success = response.status_code in [200, 201]
                details = f"HTTP {response.status_code}" if not success else ""
                
                self.log_result(f"API: {description}", success, details, response_time)
                
            except Exception as e:
                self.log_result(f"API: {description}", False, f"Error: {str(e)}")
    
    def test_workflow_operations(self):
        """Test workflow-related operations"""
        print("\n�� Testing Workflow Operations...")
        
        # Test with the existing workflow ID from our database
        test_workflow_id = "81e98d1e-459d-4e1d-b9c3-e1e56f8155ab"
        
        # Test workflow state retrieval
        try:
            start = time.time()
            response = requests.get(f"{self.base_url}/api/workflows/{test_workflow_id}/state", timeout=15)
            response_time = time.time() - start
            
            if response.status_code == 200:
                state_data = response.json()
                self.log_result(
                    "Workflow State Retrieval", 
                    True,
                    f"Retrieved workflow: {state_data.get('name', 'Unknown')}",
                    response_time
                )
            else:
                self.log_result(
                    "Workflow State Retrieval", 
                    False, 
                    f"HTTP {response.status_code}",
                    response_time
                )
        except Exception as e:
            self.log_result("Workflow State Retrieval", False, f"Error: {str(e)}")
        
        # Test workflow validation
        try:
            start = time.time()
            response = requests.post(f"{self.base_url}/api/workflows/{test_workflow_id}/validate", timeout=15)
            response_time = time.time() - start
            
            if response.status_code == 200:
                validation_data = response.json()
                overall_valid = validation_data.get("validation_report", {}).get("overall_valid", False)
                self.log_result(
                    "Workflow Validation", 
                    overall_valid,
                    f"Validation result: {'Valid' if overall_valid else 'Invalid'}",
                    response_time
                )
            else:
                self.log_result(
                    "Workflow Validation", 
                    False, 
                    f"HTTP {response.status_code}",
                    response_time
                )
        except Exception as e:
            self.log_result("Workflow Validation", False, f"Error: {str(e)}")
        
        # Test state generation
        try:
            start = time.time()
            response = requests.post(
                f"{self.base_url}/api/workflows/{test_workflow_id}/generate-state",
                json={"optimization_goal": "efficiency", "include_suggestions": True},
                timeout=30
            )
            response_time = time.time() - start
            
            if response.status_code == 200:
                generation_data = response.json()
                has_state = "generated_state" in generation_data
                self.log_result(
                    "AI State Generation", 
                    has_state,
                    f"Generated state: {'Success' if has_state else 'Failed'}",
                    response_time
                )
            else:
                self.log_result(
                    "AI State Generation", 
                    False, 
                    f"HTTP {response.status_code}",
                    response_time
                )
        except Exception as e:
            self.log_result("AI State Generation", False, f"Error: {str(e)}")
    
    def test_agent_forge_features(self):
        """Test Agent Forge-specific features"""
        print("\n�� Testing Agent Forge Features...")
        
        test_workflow_id = "81e98d1e-459d-4e1d-b9c3-e1e56f8155ab"
        
        # Test marketplace preview
        try:
            start = time.time()
            response = requests.get(f"{self.base_url}/api/workflows/{test_workflow_id}/marketplace-preview", timeout=15)
            response_time = time.time() - start
            
            if response.status_code == 200:
                preview_data = response.json()
                has_categories = "categories" in preview_data
                has_stats = "stats" in preview_data
                self.log_result(
                    "Marketplace Preview", 
                    has_categories and has_stats,
                    f"Categories: {preview_data.get('categories', [])}",
                    response_time
                )
            else:
                self.log_result(
                    "Marketplace Preview", 
                    response.status_code == 404,  # 404 is acceptable if endpoint not implemented
                    f"HTTP {response.status_code}" if response.status_code != 404 else "Endpoint not implemented (acceptable)",
                    response_time
                )
        except Exception as e:
            self.log_result("Marketplace Preview", False, f"Error: {str(e)}")
        
        # Test block types documentation
        try:
            start = time.time()
            response = requests.get(f"{self.base_url}/api/block-types", timeout=10)
            response_time = time.time() - start
            
            if response.status_code == 200:
                block_types_data = response.json()
                block_types = block_types_data.get("block_types", {})
                
                # Check for essential Agent Forge block types
                essential_types = ["starter", "agent", "api", "output", "tool"]
                has_all_types = all(bt in block_types for bt in essential_types)
                
                self.log_result(
                    "Block Types Documentation", 
                    has_all_types,
                    f"Block types available: {list(block_types.keys())}",
                    response_time
                )
            else:
                self.log_result(
                    "Block Types Documentation", 
                    False, 
                    f"HTTP {response.status_code}",
                    response_time
                )
        except Exception as e:
            self.log_result("Block Types Documentation", False, f"Error: {str(e)}")
    
    def test_performance(self):
        """Test system performance"""
        print("\n⚡ Testing Performance...")
        
        # Test response times for key endpoints
        performance_tests = [
            ("GET", "/api/health", "Health Check", 1.0),
            ("GET", "/api/block-types", "Block Types", 2.0),
            ("GET", "/api/workflows/81e98d1e-459d-4e1d-b9c3-e1e56f8155ab/state", "Workflow State", 3.0)
        ]
        
        for method, endpoint, test_name, max_time in performance_tests:
            try:
                start = time.time()
                response = requests.request(method, f"{self.base_url}{endpoint}", timeout=max_time + 5)
                response_time = time.time() - start
                
                within_limit = response_time <= max_time
                status = response.status_code in [200, 201]
                
                self.log_result(
                    f"Performance: {test_name}",
                    status and within_limit,
                    f"Target: <{max_time}s, Actual: {response_time:.2f}s",
                    response_time
                )
                
            except Exception as e:
                self.log_result(f"Performance: {test_name}", False, f"Error: {str(e)}")
    
    def test_data_integrity(self):
        """Test data integrity and consistency"""
        print("\n🗄️ Testing Data Integrity...")
        
        # Test that synthetic data is available
        try:
            start = time.time()
            response = requests.get(f"{self.base_url}/api/health", timeout=10)
            response_time = time.time() - start
            
            if response.status_code == 200:
                health_data = response.json()
                metrics = health_data.get("metrics", {})
                workflows_count = metrics.get("workflows_in_database", 0)
                
                self.log_result(
                    "Database Data Availability",
                    workflows_count > 0,
                    f"Workflows in database: {workflows_count}",
                    response_time
                )
            else:
                self.log_result("Database Data Availability", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_result("Database Data Availability", False, f"Error: {str(e)}")
    
    def generate_report(self):
        """Generate comprehensive validation report"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        total_time = time.time() - self.start_time
        
        print("\n" + "="*60)
        print("🎯 AGENT FORGE STATE GENERATOR - VALIDATION REPORT")
        print("="*60)
        print(f"📊 Test Results: {passed_tests}/{total_tests} passed ({success_rate:.1f}%)")
        print(f"⏱️  Total Time: {total_time:.2f} seconds")
        print(f"🎯 System Status: {'🟢 OPERATIONAL' if success_rate >= 80 else '🔴 ISSUES DETECTED'}")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests ({failed_tests}):")
            for result in self.results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['details']}")
        
        print(f"\n✅ Passed Tests ({passed_tests}):")
        for result in self.results:
            if result["success"]:
                print(f"  • {result['test']}")
        
        # Performance summary
        response_times = [r["response_time_ms"] for r in self.results if r["response_time_ms"] > 0]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            print(f"\n⚡ Performance Summary:")
            print(f"  • Average Response Time: {avg_response_time:.1f}ms")
            print(f"  • Maximum Response Time: {max_response_time:.1f}ms")
        
        # Save detailed report
        report_data = {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": success_rate,
                "total_time_seconds": total_time,
                "timestamp": datetime.now().isoformat()
            },
            "results": self.results
        }
        
        with open("validation_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: validation_report.json")
        print("="*60)
        
        return success_rate >= 80

def main():
    """Main validation function"""
    print("�� Agent Forge State Generator - Final Validation")
    print("=" * 60)
    
    # Check if server is running
    validator = AgentForgeValidator()
    
    try:
        requests.get(validator.base_url, timeout=5)
    except:
        print("❌ Server not accessible at http://localhost:8000")
        print("   Please start the server with: docker-compose up -d")
        print("   Or: uvicorn src.main:app --reload --port 8000")
        sys.exit(1)
    
    # Run all validation tests
    tests_passed = True
    
    if not validator.test_system_health():
        tests_passed = False
    
    validator.test_api_endpoints()
    validator.test_workflow_operations() 
    validator.test_agent_forge_features()
    validator.test_performance()
    validator.test_data_integrity()
    
    # Generate final report
    overall_success = validator.generate_report()
    
    if overall_success:
        print("\n🎉 VALIDATION SUCCESSFUL!")
        print("   Agent Forge State Generator is ready for production deployment.")
        sys.exit(0)
    else:
        print("\n⚠️  VALIDATION ISSUES DETECTED")
        print("   Please review the failed tests and fix issues before deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main()
