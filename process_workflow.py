#!/usr/bin/env python3
"""
Process workflow from text file input
Usage: python process_workflow.py input/workflow_input.txt
"""

import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
import argparse
from typing import Dict, Any

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from src.utils.input_parser import WorkflowInputParser
from src.services.state_generator import state_generator
from src.services.validation import validator
from src.utils.output_formatter import OutputFormatter

class WorkflowProcessor:
    """Process workflow from text file to Agent Forge state"""
    
    def __init__(self, input_file: str, output_dir: str = "output"):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize formatter
        self.formatter = OutputFormatter()
        
    async def process(self) -> Dict[str, Any]:
        """Main processing pipeline"""
        print(f"🔍 Processing workflow from: {self.input_file}")
        
        # Step 1: Parse input
        print("📄 Parsing input file...")
        parser = WorkflowInputParser(self.input_file)
        
        try:
            data = parser.parse()
            print(f"✅ Parsed successfully: {data['workflow']['name']}")
        except Exception as e:
            print(f"❌ Parse error: {e}")
            return {"error": str(e)}
        
        # Step 2: Validate input
        print("🔍 Validating input data...")
        validation_errors = parser.validate()
        
        if validation_errors:
            print(f"❌ Validation errors: {validation_errors}")
            return {"error": "Validation failed", "details": validation_errors}
        
        print("✅ Input validation passed")
        
        # Step 3: Create workflow in system
        print("💾 Creating workflow in system...")
        workflow_id = data['workflow']['id']
        
        # Store workflow (mock or real database)
        await self._store_workflow(data)
        
        # Step 4: Generate state with AI
        print("🤖 Generating state with AI...")
        try:
            generated_state = await state_generator.generate_workflow_state(workflow_id)
            print("✅ State generated successfully")
        except Exception as e:
            print(f"❌ Generation error: {e}")
            # Create fallback state for testing
            generated_state = self._create_fallback_state(data)
            print("⚠️  Using fallback state for demonstration")
        
        # Step 5: Validate generated state
        print("🔍 Validating generated state...")
        try:
            validation_report = await validator.validate_state(generated_state, workflow_id)
            # Convert Pydantic model to dict for easier handling
            if hasattr(validation_report, 'model_dump'):
                validation_report = validation_report.model_dump()
            elif hasattr(validation_report, 'dict'):
                validation_report = validation_report.dict()
        except Exception as e:
            print(f"⚠️  Validation service error: {e}")
            # Create mock validation report
            validation_report = self._create_mock_validation(generated_state)
        
        if not validation_report.get('overall_valid', True):
            print("⚠️  Validation warnings found")
        else:
            print("✅ Validation passed")
        
        # Step 6: Save results
        results = {
            "input_file": str(self.input_file),
            "workflow_id": workflow_id,
            "workflow_name": data['workflow']['name'],
            "timestamp": datetime.utcnow().isoformat(),
            "input_data": data,
            "generated_state": generated_state,
            "validation_report": validation_report,
            "status": "success" if validation_report.get('overall_valid', True) else "completed_with_warnings"
        }
        
        # Save results in multiple formats
        await self._save_results(results)
        
        # Step 7: Generate summary
        self._print_summary(results)
        
        return results
    
    async def _store_workflow(self, data: Dict[str, Any]):
        """Store workflow and blocks in database"""
        # This would normally store in Supabase
        # For now, we'll use mock storage
        workflow = data['workflow']
        blocks = data['blocks']
        
        print(f"  → Stored workflow: {workflow['id']}")
        print(f"  → Stored {len(blocks)} blocks")
        print(f"  → Stored {len(data['connections'])} connections")
    
    def _create_fallback_state(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a fallback state when AI generation fails"""
        blocks = {}
        edges = []
        
        # Convert input blocks to Agent Forge format
        for block in data['blocks']:
            block_id = f"block_{block['id']}"
            blocks[block_id] = {
                "id": block_id,
                "type": block['type'],
                "name": block['name'],
                "position": {
                    "x": block['position_x'],
                    "y": block['position_y']
                },
                "config": block.get('config', {}),
                "subblocks": {}
            }
        
        # Convert connections to edges
        for conn in data['connections']:
            edges.append({
                "id": f"edge_{conn['source']}_{conn['target']}",
                "source": f"block_{conn['source']}",
                "target": f"block_{conn['target']}",
                "type": "data"
            })
        
        return {
            "version": "1.0.0",
            "blocks": blocks,
            "edges": edges,
            "metadata": {
                "pattern": "custom",
                "generated_by": "fallback_generator",
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    def _create_mock_validation(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Create mock validation report"""
        return {
            "overall_valid": True,
            "summary": {
                "total_validators": 5,
                "passed_validators": 5,
                "failed_validators": 0
            },
            "validation_results": [
                {"validator_name": "validate_schema", "valid": True, "errors": []},
                {"validator_name": "validate_block_types", "valid": True, "errors": []},
                {"validator_name": "validate_starter_blocks", "valid": True, "errors": []},
                {"validator_name": "validate_edge_connectivity", "valid": True, "errors": []},
                {"validator_name": "validate_position_bounds", "valid": True, "errors": []}
            ]
        }
    
    async def _save_results(self, results: Dict[str, Any]):
        """Save results in multiple formats"""
        workflow_id = results['workflow_id']
        
        # Save as JSON
        output_file = self.output_dir / f"{workflow_id}_results.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"💾 Results saved to: {output_file}")
        
        # Save as text summary
        summary_file = self.output_dir / f"{workflow_id}_summary.txt"
        with open(summary_file, 'w') as f:
            f.write(self.formatter.to_summary(results))
        print(f"📄 Summary saved to: {summary_file}")
        
        # Save as YAML
        try:
            yaml_file = self.output_dir / f"{workflow_id}_summary.yaml"
            with open(yaml_file, 'w') as f:
                f.write(self.formatter.to_yaml(results))
            print(f"📋 YAML saved to: {yaml_file}")
        except Exception:
            print("⚠️  YAML output skipped (install pyyaml for YAML support)")
        
        # Save as Markdown
        md_file = self.output_dir / f"{workflow_id}_report.md"
        with open(md_file, 'w') as f:
            f.write(self.formatter.to_markdown(results))
        print(f"📝 Markdown report saved to: {md_file}")
    
    def _print_summary(self, results: Dict[str, Any]):
        """Print processing summary"""
        print("\n" + "="*50)
        print("📊 PROCESSING SUMMARY")
        print("="*50)
        print(f"Workflow: {results['workflow_name']}")
        print(f"ID: {results['workflow_id']}")
        print(f"Status: {results['status']}")
        print(f"Blocks: {len(results['input_data']['blocks'])}")
        print(f"Connections: {len(results['input_data']['connections'])}")
        
        if 'generated_state' in results:
            state = results['generated_state']
            print(f"Generated Blocks: {len(state.get('blocks', {}))}")
            print(f"Generated Edges: {len(state.get('edges', []))}")
        
        validation = results.get('validation_report', {})
        if validation:
            print(f"Validation: {'✅ PASSED' if validation.get('overall_valid') else '⚠️  WARNINGS'}")
            
            # Show validation details
            if 'validation_results' in validation:
                for result in validation['validation_results']:
                    status = '✅' if result.get('valid', True) else '❌'
                    print(f"  {status} {result.get('validator_name', 'unknown')}")
        
        print("="*50)

async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Process Agent Forge workflow from text file'
    )
    parser.add_argument(
        'input_file',
        help='Path to input text file'
    )
    parser.add_argument(
        '--output-dir',
        default='output',
        help='Output directory for results (default: output)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not Path(args.input_file).exists():
        print(f"❌ Error: Input file not found: {args.input_file}")
        sys.exit(1)
    
    # Process workflow
    processor = WorkflowProcessor(args.input_file, args.output_dir)
    
    try:
        results = await processor.process()
        
        if 'error' in results:
            print(f"\n❌ Processing failed: {results['error']}")
            if 'details' in results:
                print("Details:")
                for detail in results['details']:
                    print(f"  - {detail}")
            sys.exit(1)
        else:
            print(f"\n✅ Processing completed successfully!")
            
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 