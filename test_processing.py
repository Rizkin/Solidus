#!/usr/bin/env python3
"""
Test the workflow processing system with various inputs
"""

import asyncio
import json
from pathlib import Path
import sys
from typing import List, Dict, Any
from datetime import datetime

sys.path.append(str(Path(__file__).parent))
from process_workflow import WorkflowProcessor

class WorkflowTestRunner:
    """Run tests on workflow processing system"""
    
    def __init__(self):
        self.test_files = [
            ("input/simple_workflow.txt", True),  # Should succeed
            ("input/trading_bot.txt", True),      # Should succeed
            ("input/workflow_input.txt", True),   # Should succeed
            ("input/invalid_workflow.txt", False) # Should fail
        ]
        self.results = []
        
    async def run_all_tests(self):
        """Run all test cases"""
        print("🧪 WORKFLOW PROCESSING TEST SUITE")
        print("="*50)
        
        for test_file, should_succeed in self.test_files:
            print(f"\n📁 Testing: {test_file}")
            print("-"*30)
            
            result = await self._run_single_test(test_file, should_succeed)
            self.results.append(result)
            
        # Print summary
        self._print_test_summary()
    
    async def _run_single_test(self, file_path: str, should_succeed: bool) -> Dict[str, Any]:
        """Run a single test case"""
        if not Path(file_path).exists():
            print(f"⚠️  Test file not found: {file_path}")
            return {
                "file": file_path,
                "expected": should_succeed,
                "actual": False,
                "passed": not should_succeed,  # If file doesn't exist and we expect failure, that's correct
                "error": "File not found"
            }
        
        processor = WorkflowProcessor(file_path, "test_output")
        
        try:
            result = await processor.process()
            
            success = 'error' not in result
            passed = success == should_succeed
            
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"Test Result: {status}")
            
            if not passed:
                print(f"  Expected: {'success' if should_succeed else 'failure'}")
                print(f"  Actual: {'success' if success else 'failure'}")
            
            return {
                "file": file_path,
                "expected": should_succeed,
                "actual": success,
                "passed": passed,
                "result": result
            }
            
        except Exception as e:
            passed = not should_succeed  # Exception expected for invalid files
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"Test Result: {status} (Exception: {e})")
            
            return {
                "file": file_path,
                "expected": should_succeed,
                "actual": False,
                "passed": passed,
                "error": str(e)
            }
    
    def _print_test_summary(self):
        """Print test summary"""
        print("\n" + "="*50)
        print("📊 TEST SUMMARY")
        print("="*50)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r['passed'])
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        print("\nDetailed Results:")
        for result in self.results:
            status = "✅" if result['passed'] else "❌"
            print(f"{status} {result['file']}")
            
            if not result['passed']:
                print(f"   Expected: {'success' if result['expected'] else 'failure'}")
                print(f"   Actual: {'success' if result['actual'] else 'failure'}")
                if 'error' in result:
                    print(f"   Error: {result['error']}")

class InputValidator:
    """Validate input file format"""
    
    @staticmethod
    def validate_file_structure(file_path: str) -> List[str]:
        """Validate the structure of input file"""
        errors = []
        
        if not Path(file_path).exists():
            return [f"File does not exist: {file_path}"]
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check required sections
        required_sections = ['@WORKFLOW', '@BLOCKS']
        for section in required_sections:
            if section not in content:
                errors.append(f"Missing required section: {section}")
        
        # Check block format
        if '@BLOCKS' in content:
            blocks_section = content.split('@BLOCKS')[1].split('@')[0]
            for line in blocks_section.strip().split('\n'):
                if line.strip() and not line.startswith('#'):
                    parts = line.split('|')
                    if len(parts) < 5:
                        errors.append(f"Invalid block format: {line}")
        
        return errors

def generate_test_report(output_dir: str = "test_output"):
    """Generate HTML test report"""
    report_path = Path(output_dir) / "test_report.html"
    
    # Collect all result files
    results = []
    output_path = Path(output_dir)
    if output_path.exists():
        for json_file in output_path.glob("*_results.json"):
            try:
                with open(json_file, 'r') as f:
                    results.append(json.load(f))
            except Exception as e:
                print(f"⚠️  Could not read {json_file}: {e}")
    
    if not results:
        print("⚠️  No result files found for report generation")
        return
    
    # Generate HTML
    html = f"""
    <html>
    <head>
        <title>Workflow Processing Test Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .success {{ color: green; }}
            .warning {{ color: orange; }}
            .error {{ color: red; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .summary {{ background-color: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h1>Workflow Processing Test Report</h1>
        <p>Generated: {datetime.utcnow().isoformat()}</p>
        
        <div class="summary">
            <h2>Summary</h2>
            <p>Total workflows processed: {len(results)}</p>
            <p>Successful: {len([r for r in results if r['status'] == 'success'])}</p>
            <p>With warnings: {len([r for r in results if r['status'] == 'completed_with_warnings'])}</p>
        </div>
        
        <h2>Results Summary</h2>
        <table>
            <tr>
                <th>Workflow</th>
                <th>Status</th>
                <th>Input Blocks</th>
                <th>Generated Blocks</th>
                <th>Edges</th>
                <th>Validation</th>
            </tr>
    """
    
    for result in results:
        status_class = "success" if result['status'] == 'success' else "warning"
        validation = "✅" if result['validation_report'].get('overall_valid', False) else "⚠️"
        
        html += f"""
            <tr>
                <td>{result['workflow_name']}</td>
                <td class="{status_class}">{result['status']}</td>
                <td>{len(result['input_data']['blocks'])}</td>
                <td>{len(result['generated_state'].get('blocks', {}))}</td>
                <td>{len(result['generated_state'].get('edges', []))}</td>
                <td>{validation}</td>
            </tr>
        """
    
    html += """
        </table>
        
        <h2>Detailed Results</h2>
    """
    
    for result in results:
        html += f"""
        <div class="summary">
            <h3>{result['workflow_name']} ({result['workflow_id']})</h3>
            <p><strong>Input File:</strong> {result['input_file']}</p>
            <p><strong>Status:</strong> {result['status']}</p>
            <p><strong>Processed:</strong> {result['timestamp']}</p>
            
            <h4>Validation Details</h4>
        """
        
        for val_result in result['validation_report'].get('validation_results', []):
            status_icon = '✅' if val_result.get('valid', True) else '❌'
            html += f"<p>{status_icon} {val_result.get('validator_name', 'unknown')}</p>"
        
        html += "</div>"
    
    html += """
    </body>
    </html>
    """
    
    with open(report_path, 'w') as f:
        f.write(html)
    
    print(f"📄 Test report generated: {report_path}")

async def run_validation_tests():
    """Run input validation tests"""
    print("\n🔍 RUNNING INPUT VALIDATION TESTS")
    print("-"*50)
    
    validator = InputValidator()
    test_files = [
        "input/simple_workflow.txt",
        "input/trading_bot.txt", 
        "input/workflow_input.txt",
        "input/invalid_workflow.txt"
    ]
    
    for file_path in test_files:
        print(f"\n📋 Validating: {file_path}")
        errors = validator.validate_file_structure(file_path)
        
        if errors:
            print("❌ Validation errors found:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("✅ File structure is valid")

async def main():
    """Run all tests"""
    # Run input validation tests first
    await run_validation_tests()
    
    # Run main processing tests
    print("\n")
    runner = WorkflowTestRunner()
    await runner.run_all_tests()
    
    # Generate report
    print(f"\n📈 Generating test report...")
    generate_test_report()
    
    print(f"\n🎯 All tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 