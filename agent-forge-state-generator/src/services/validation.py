# src/services/validation.py
from typing import Dict, Any, List, Callable
from datetime import datetime
import logging
from src.models.schemas import ValidationResult, ValidationReport

logger = logging.getLogger(__name__)

class AgentForgeValidator:
    """Validate workflow states for Agent Forge compliance"""
    
    def __init__(self):
        self.validators = []
        self._register_default_validators()
    
    def _register_default_validators(self):
        """Register all default validators"""
        self.validators = [
            self.validate_schema,
            self.validate_block_types,
            self.validate_starter_blocks,
            self.validate_agent_configurations,
            self.validate_api_integrations,
            self.validate_edge_connectivity,
            self.validate_workflow_patterns,
            self.validate_position_bounds,
            self.validate_subblock_structure
        ]
    
    async def validate_state(self, state: Dict[str, Any], workflow_id: str) -> ValidationReport:
        """Run all validators on the state"""
        results = []
        
        for validator in self.validators:
            try:
                result = await validator(state, workflow_id)
                results.append(result)
            except Exception as e:
                logger.error(f"Validator {validator.__name__} failed: {e}")
                results.append(ValidationResult(
                    validator_name=validator.__name__,
                    valid=False,
                    errors=[f"Validator error: {str(e)}"]
                ))
        
        # Calculate overall validity
        overall_valid = all(r.valid for r in results)
        
        # Check Agent Forge compliance
        critical_validators = ['validate_schema', 'validate_block_types', 'validate_starter_blocks']
        agent_forge_compliance = all(
            r.valid for r in results 
            if r.validator_name in critical_validators
        )
        
        # Generate suggestions
        suggestions = self._generate_suggestions(results)
        
        return ValidationReport(
            overall_valid=overall_valid,
            validation_results=results,
            agent_forge_compliance=agent_forge_compliance,
            suggestions=suggestions
        )
    
    async def validate_schema(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate state matches Agent Forge schema"""
        errors = []
        
        # Check required top-level fields
        required_fields = ['blocks', 'edges', 'metadata']
        for field in required_fields:
            if field not in state:
                errors.append(f"Missing required field: {field}")
        
        # Check blocks structure
        if 'blocks' in state and not isinstance(state['blocks'], dict):
            errors.append("'blocks' must be a dictionary")
        
        # Check edges structure
        if 'edges' in state and not isinstance(state['edges'], list):
            errors.append("'edges' must be an array")
        
        # Check metadata
        if 'metadata' in state:
            metadata = state['metadata']
            if not isinstance(metadata, dict):
                errors.append("'metadata' must be a dictionary")
            elif 'version' not in metadata:
                errors.append("'metadata' must contain 'version'")
        
        return ValidationResult(
            validator_name="validate_schema",
            valid=len(errors) == 0,
            errors=errors
        )
    
    async def validate_block_types(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate all blocks have valid Agent Forge types"""
        errors = []
        warnings = []
        
        valid_types = ['starter', 'agent', 'api', 'output', 'tool']
        
        blocks = state.get('blocks', {})
        for block_id, block in blocks.items():
            if 'type' not in block:
                errors.append(f"Block {block_id} missing 'type'")
            elif block['type'] not in valid_types:
                errors.append(f"Block {block_id} has invalid type: {block['type']}")
            
            # Check required block fields
            required_fields = ['name', 'position', 'subBlocks', 'outputs']
            for field in required_fields:
                if field not in block:
                    errors.append(f"Block {block_id} missing required field: {field}")
        
        return ValidationResult(
            validator_name="validate_block_types",
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    async def validate_starter_blocks(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate workflow has at least one starter block"""
        errors = []
        warnings = []
        
        blocks = state.get('blocks', {})
        starter_blocks = [b for b in blocks.values() if b.get('type') == 'starter']
        
        if not starter_blocks:
            errors.append("Workflow must have at least one starter block")
        else:
            # Validate starter configurations
            for starter in starter_blocks:
                sub_blocks = starter.get('subBlocks', {})
                if 'startWorkflow' not in sub_blocks:
                    warnings.append(f"Starter block {starter.get('name')} missing startWorkflow configuration")
        
        return ValidationResult(
            validator_name="validate_starter_blocks",
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    async def validate_agent_configurations(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate agent blocks have proper AI configurations"""
        errors = []
        warnings = []
        
        valid_models = ['gpt-4', 'claude-3', 'gemini-pro', 'custom-byoi', 'gpt-3.5-turbo']
        
        blocks = state.get('blocks', {})
        agent_blocks = [b for b in blocks.values() if b.get('type') == 'agent']
        
        for agent in agent_blocks:
            sub_blocks = agent.get('subBlocks', {})
            
            # Check model configuration
            model_config = sub_blocks.get('model', {})
            if not model_config.get('value'):
                errors.append(f"Agent {agent.get('name')} missing model selection")
            elif model_config.get('value') not in valid_models:
                warnings.append(f"Agent {agent.get('name')} using non-standard model: {model_config.get('value')}")
            
            # Check system prompt
            if not sub_blocks.get('systemPrompt', {}).get('value'):
                warnings.append(f"Agent {agent.get('name')} missing system prompt")
        
        return ValidationResult(
            validator_name="validate_agent_configurations",
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    async def validate_api_integrations(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate API blocks have proper configuration"""
        errors = []
        warnings = []
        
        blocks = state.get('blocks', {})
        api_blocks = [b for b in blocks.values() if b.get('type') == 'api']
        
        for api in api_blocks:
            sub_blocks = api.get('subBlocks', {})
            
            # Check URL
            if not sub_blocks.get('url', {}).get('value'):
                errors.append(f"API block {api.get('name')} missing URL")
            
            # Check method (optional but recommended)
            if not sub_blocks.get('method', {}).get('value'):
                warnings.append(f"API block {api.get('name')} missing HTTP method")
        
        return ValidationResult(
            validator_name="validate_api_integrations",
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    async def validate_edge_connectivity(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate all edges connect existing blocks"""
        errors = []
        warnings = []
        
        blocks = state.get('blocks', {})
        edges = state.get('edges', [])
        
        block_ids = set(blocks.keys())
        
        for edge in edges:
            if 'source' not in edge or 'target' not in edge:
                errors.append("Edge missing source or target")
                continue
            
            if edge['source'] not in block_ids:
                errors.append(f"Edge source '{edge['source']}' not found in blocks")
            if edge['target'] not in block_ids:
                errors.append(f"Edge target '{edge['target']}' not found in blocks")
        
        # Check for orphaned blocks (except starters)
        connected_blocks = set()
        for edge in edges:
            connected_blocks.add(edge.get('source'))
            connected_blocks.add(edge.get('target'))
        
        for block_id, block in blocks.items():
            if block_id not in connected_blocks and block.get('type') != 'starter':
                warnings.append(f"Block {block.get('name')} is not connected to any other blocks")
        
        return ValidationResult(
            validator_name="validate_edge_connectivity",
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    async def validate_workflow_patterns(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate common Agent Forge workflow patterns"""
        errors = []
        warnings = []
        metadata = {}
        
        blocks = state.get('blocks', {})
        
        # Detect patterns
        patterns = []
        
        # Check for multi-agent pattern
        agent_count = sum(1 for b in blocks.values() if b.get('type') == 'agent')
        if agent_count >= 3:
            patterns.append("multi_agent_team")
        
        # Check for API integration pattern
        api_count = sum(1 for b in blocks.values() if b.get('type') == 'api')
        if api_count > 0:
            patterns.append("api_integration")
        
        # Check for output pattern
        output_blocks = [b for b in blocks.values() if b.get('type') == 'output']
        if not output_blocks:
            warnings.append("Consider adding output blocks for results delivery")
        
        metadata['detected_patterns'] = patterns
        metadata['agent_count'] = agent_count
        
        return ValidationResult(
            validator_name="validate_workflow_patterns",
            valid=True,  # Pattern detection doesn't fail
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )
    
    async def validate_position_bounds(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate block positions are within reasonable bounds"""
        errors = []
        warnings = []
        
        blocks = state.get('blocks', {})
        
        for block_id, block in blocks.items():
            position = block.get('position', {})
            x = position.get('x', 0)
            y = position.get('y', 0)
            
            # Check reasonable bounds (Agent Forge canvas is typically 2000x1000)
            if x < 0 or x > 2000:
                warnings.append(f"Block {block.get('name')} X position {x} may be out of bounds")
            if y < -200 or y > 1000:
                warnings.append(f"Block {block.get('name')} Y position {y} may be out of bounds")
        
        return ValidationResult(
            validator_name="validate_position_bounds",
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    async def validate_subblock_structure(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate subBlocks have proper structure"""
        errors = []
        warnings = []
        
        blocks = state.get('blocks', {})
        
        for block_id, block in blocks.items():
            sub_blocks = block.get('subBlocks', {})
            
            # Check each subBlock has required fields
            for sub_id, sub_block in sub_blocks.items():
                if not isinstance(sub_block, dict):
                    errors.append(f"Block {block.get('name')} subBlock {sub_id} must be a dictionary")
                    continue
                
                # Check for id and type (common fields)
                if 'id' not in sub_block:
                    warnings.append(f"Block {block.get('name')} subBlock {sub_id} missing 'id' field")
                if 'type' not in sub_block:
                    warnings.append(f"Block {block.get('name')} subBlock {sub_id} missing 'type' field")
        
        return ValidationResult(
            validator_name="validate_subblock_structure",
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def _generate_suggestions(self, results: List[ValidationResult]) -> List[str]:
        """Generate improvement suggestions based on validation results"""
        suggestions = []
        
        # Analyze patterns
        for result in results:
            if result.validator_name == "validate_workflow_patterns" and result.metadata:
                patterns = result.metadata.get('detected_patterns', [])
                if 'multi_agent_team' in patterns:
                    suggestions.append("Consider adding a coordinator agent for better multi-agent orchestration")
                if not patterns:
                    suggestions.append("This workflow could benefit from agent blocks for automation")
        
        # Check for warnings
        total_warnings = sum(len(r.warnings) for r in results)
        if total_warnings > 5:
            suggestions.append("Review warnings to improve workflow quality")
        
        # Agent count suggestions
        for result in results:
            if result.metadata and 'agent_count' in result.metadata:
                if result.metadata['agent_count'] == 0:
                    suggestions.append("Add AI agent blocks to leverage Agent Forge's capabilities")
                elif result.metadata['agent_count'] > 5:
                    suggestions.append("Consider breaking complex workflows into sub-workflows")
        
        return suggestions
    
    def add_custom_validator(self, name: str, validator_func: Callable):
        """Add a custom validator"""
        validator_func.__name__ = name
        self.validators.append(validator_func)

# Create singleton instance
validator = AgentForgeValidator()
