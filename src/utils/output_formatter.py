import json
from typing import Dict, Any
from datetime import datetime

class OutputFormatter:
    """Format processing results in various formats"""
    
    @staticmethod
    def to_summary(results: Dict[str, Any]) -> str:
        """Generate human-readable summary"""
        summary = []
        summary.append("WORKFLOW PROCESSING RESULTS")
        summary.append("=" * 50)
        summary.append(f"Workflow: {results['workflow_name']}")
        summary.append(f"ID: {results['workflow_id']}")
        summary.append(f"Processed: {results['timestamp']}")
        summary.append(f"Status: {results['status']}")
        summary.append("")
        
        # Input summary
        summary.append("INPUT SUMMARY:")
        summary.append(f"  Blocks: {len(results['input_data']['blocks'])}")
        summary.append(f"  Connections: {len(results['input_data']['connections'])}")
        
        # Output summary
        state = results['generated_state']
        summary.append("")
        summary.append("GENERATED STATE:")
        summary.append(f"  Blocks: {len(state.get('blocks', {}))}")
        summary.append(f"  Edges: {len(state.get('edges', []))}")
        summary.append(f"  Pattern: {state.get('metadata', {}).get('pattern', 'unknown')}")
        
        # Validation summary
        validation = results['validation_report']
        summary.append("")
        summary.append("VALIDATION:")
        summary.append(f"  Overall: {'✅ PASSED' if validation.get('overall_valid', False) else '⚠️  WARNINGS'}")
        summary.append(f"  Checks Passed: {validation.get('summary', {}).get('passed_validators', 0)}/{validation.get('summary', {}).get('total_validators', 0)}")
        
        if not validation.get('overall_valid', True):
            summary.append("  Issues:")
            for result in validation.get('validation_results', []):
                if not result.get('valid', True):
                    summary.append(f"    - {result.get('validator_name', 'unknown')}: {', '.join(result.get('errors', []))}")
        
        return "\n".join(summary)
    
    @staticmethod
    def to_yaml(results: Dict[str, Any]) -> str:
        """Convert results to YAML format"""
        try:
            import yaml
        except ImportError:
            return "# YAML output requires PyYAML package\n# pip install pyyaml"
        
        # Simplify for YAML
        simplified = {
            'workflow': {
                'id': results['workflow_id'],
                'name': results['workflow_name'],
                'status': results['status']
            },
            'statistics': {
                'input_blocks': len(results['input_data']['blocks']),
                'generated_blocks': len(results['generated_state'].get('blocks', {})),
                'edges': len(results['generated_state'].get('edges', []))
            },
            'validation': {
                'passed': results['validation_report'].get('overall_valid', False),
                'checks': results['validation_report'].get('summary', {})
            }
        }
        
        return yaml.dump(simplified, default_flow_style=False)
    
    @staticmethod
    def to_markdown(results: Dict[str, Any]) -> str:
        """Generate Markdown report"""
        md = []
        md.append(f"# Workflow Processing Report: {results['workflow_name']}")
        md.append("")
        md.append(f"**Generated**: {results['timestamp']}")
        md.append("")
        
        md.append("## Summary")
        md.append(f"- **ID**: `{results['workflow_id']}`")
        md.append(f"- **Status**: {results['status']}")
        md.append("")
        
        md.append("## Input Analysis")
        md.append(f"- Blocks: {len(results['input_data']['blocks'])}")
        md.append(f"- Connections: {len(results['input_data']['connections'])}")
        md.append("")
        
        md.append("## Generated State")
        state = results['generated_state']
        md.append(f"- Blocks: {len(state.get('blocks', {}))}")
        md.append(f"- Edges: {len(state.get('edges', []))}")
        md.append(f"- Pattern: `{state.get('metadata', {}).get('pattern', 'unknown')}`")
        md.append("")
        
        md.append("## Validation Results")
        validation = results['validation_report']
        md.append(f"- Overall: {'✅ Passed' if validation.get('overall_valid', False) else '⚠️ Warnings'}")
        md.append(f"- Checks: {validation.get('summary', {}).get('passed_validators', 0)}/{validation.get('summary', {}).get('total_validators', 0)}")
        
        if validation.get('validation_results'):
            md.append("")
            md.append("### Validation Details")
            for result in validation['validation_results']:
                status = '✅' if result.get('valid', True) else '❌'
                md.append(f"- {status} {result.get('validator_name', 'unknown')}")
        
        return "\n".join(md)
    
    @staticmethod
    def to_json_pretty(results: Dict[str, Any]) -> str:
        """Convert results to pretty-printed JSON"""
        return json.dumps(results, indent=2, default=str) 