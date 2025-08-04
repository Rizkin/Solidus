"""
Agent Forge Validation Service
Comprehensive 9-validator system for workflow compliance
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class ValidationResult(BaseModel):
    """Single validator result"""
    validator_name: str
    valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    metadata: Optional[Dict[str, Any]] = None

class ValidationReport(BaseModel):
    """Complete validation report"""
    workflow_id: str
    overall_valid: bool
    agent_forge_compliance: bool
    validation_results: List[ValidationResult]
    summary: Dict[str, Any]
    validated_at: str

class WorkflowValidator:
    """Comprehensive Agent Forge workflow validator"""
    
    def __init__(self):
        self.validators = [
            self._validate_schema,
            self._validate_block_types,
            self._validate_starter_blocks,
            self._validate_agent_configuration,
            self._validate_api_integration,
            self._validate_edge_connectivity,
            self._validate_workflow_patterns,
            self._validate_position_bounds,
            self._validate_subblock_structure
        ]
    
    async def validate_state(self, state: Dict[str, Any], workflow_id: str) -> ValidationReport:
        """Run all validators on workflow state"""
        validation_results = []
        
        for validator in self.validators:
            try:
                result = await validator(state, workflow_id)
                validation_results.append(result)
            except Exception as e:
                logger.error(f"Validator {validator.__name__} failed: {e}")
                validation_results.append(ValidationResult(
                    validator_name=validator.__name__,
                    valid=False,
                    errors=[f"Validator error: {str(e)}"]
                ))
        
        # Calculate overall validity
        overall_valid = all(result.valid for result in validation_results)
        
        # Check Agent Forge compliance (stricter requirements)
        agent_forge_compliance = self._check_agent_forge_compliance(validation_results)
        
        # Generate summary
        summary = self._generate_summary(validation_results, state)
        
        return ValidationReport(
            workflow_id=workflow_id,
            overall_valid=overall_valid,
            agent_forge_compliance=agent_forge_compliance,
            validation_results=validation_results,
            summary=summary,
            validated_at=datetime.utcnow().isoformat() + "Z"
        )
    
    async def _validate_schema(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate basic Agent Forge schema structure"""
        errors = []
        warnings = []
        
        # Required top-level fields
        required_fields = ["blocks", "edges", "subflows", "variables", "metadata"]
        
        for field in required_fields:
            if field not in state:
                errors.append(f"Missing required field: {field}")
        
        # Validate field types
        if "blocks" in state and not isinstance(state["blocks"], dict):
            errors.append("'blocks' must be a dictionary")
        
        if "edges" in state and not isinstance(state["edges"], list):
            errors.append("'edges' must be a list")
        
        if "variables" in state and not isinstance(state["variables"], dict):
            errors.append("'variables' must be a dictionary")
        
        if "metadata" in state and not isinstance(state["metadata"], dict):
            errors.append("'metadata' must be a dictionary")
        
        # Check metadata fields
        if "metadata" in state:
            metadata = state["metadata"]
            if "version" not in metadata:
                warnings.append("Missing version in metadata")
            if "createdAt" not in metadata:
                warnings.append("Missing createdAt timestamp")
        
        return ValidationResult(
            validator_name="validate_schema",
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    async def _validate_block_types(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate block types and configurations"""
        errors = []
        warnings = []
        
        valid_types = ["starter", "agent", "api", "output", "tool"]
        blocks = state.get("blocks", {})
        
        for block_id, block in blocks.items():
            # Check required fields
            if "type" not in block:
                errors.append(f"Block {block_id} missing 'type' field")
                continue
            
            if "id" not in block:
                errors.append(f"Block {block_id} missing 'id' field")
            
            if "name" not in block:
                warnings.append(f"Block {block_id} missing 'name' field")
            
            # Validate block type
            block_type = block["type"]
            if block_type not in valid_types:
                errors.append(f"Block {block_id} has invalid type: {block_type}")
            
            # Check position fields
            if "position_x" not in block:
                warnings.append(f"Block {block_id} missing position_x")
            if "position_y" not in block:
                warnings.append(f"Block {block_id} missing position_y")
            
            # Check sub_blocks
            if "sub_blocks" not in block:
                warnings.append(f"Block {block_id} missing sub_blocks configuration")
        
        return ValidationResult(
            validator_name="validate_block_types",
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metadata={"total_blocks": len(blocks), "block_types": list(set(b.get("type") for b in blocks.values()))}
        )
    
    async def _validate_starter_blocks(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate starter block requirements"""
        errors = []
        warnings = []
        
        blocks = state.get("blocks", {})
        starter_blocks = [b for b in blocks.values() if b.get("type") == "starter"]
        
        if not starter_blocks:
            errors.append("Workflow must have at least one starter block")
            return ValidationResult(
                validator_name="validate_starter_blocks",
                valid=False,
                errors=errors
            )
        
        for block in starter_blocks:
            sub_blocks = block.get("sub_blocks", {})
            
            if "startWorkflow" not in sub_blocks:
                errors.append(f"Starter block {block.get('id')} missing startWorkflow configuration")
            else:
                start_type = sub_blocks["startWorkflow"]
                valid_start_types = ["manual", "webhook", "schedule", "email"]
                
                if start_type not in valid_start_types:
                    errors.append(f"Invalid startWorkflow type: {start_type}")
                
                # Validate specific configurations
                if start_type == "webhook" and "webhookPath" not in sub_blocks:
                    warnings.append("Webhook starter missing webhookPath")
                
                if start_type == "schedule" and "scheduleType" not in sub_blocks:
                    warnings.append("Schedule starter missing scheduleType")
        
        return ValidationResult(
            validator_name="validate_starter_blocks",
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metadata={"starter_count": len(starter_blocks)}
        )
    
    async def _validate_agent_configuration(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate AI agent configurations"""
        errors = []
        warnings = []
        
        blocks = state.get("blocks", {})
        agent_blocks = [b for b in blocks.values() if b.get("type") == "agent"]
        
        valid_models = ["gpt-4", "gpt-3.5-turbo", "claude-3-opus", "claude-3-sonnet", "claude-3-haiku", "gemini-pro"]
        
        for block in agent_blocks:
            block_id = block.get("id", "unknown")
            sub_blocks = block.get("sub_blocks", {})
            
            # Check required fields
            if "model" not in sub_blocks:
                errors.append(f"Agent block {block_id} missing model configuration")
            else:
                model = sub_blocks["model"]
                if model not in valid_models:
                    warnings.append(f"Agent block {block_id} uses non-standard model: {model}")
            
            if "systemPrompt" not in sub_blocks:
                errors.append(f"Agent block {block_id} missing systemPrompt")
            else:
                prompt = sub_blocks["systemPrompt"]
                if len(prompt.strip()) < 10:
                    warnings.append(f"Agent block {block_id} has very short system prompt")
            
            # Check temperature
            if "temperature" in sub_blocks:
                temp = sub_blocks["temperature"]
                if not isinstance(temp, (int, float)) or temp < 0 or temp > 1:
                    warnings.append(f"Agent block {block_id} has invalid temperature: {temp}")
        
        return ValidationResult(
            validator_name="validate_agent_configuration",
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metadata={"agent_count": len(agent_blocks)}
        )
    
    async def _validate_api_integration(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate API integration blocks"""
        errors = []
        warnings = []
        
        blocks = state.get("blocks", {})
        api_blocks = [b for b in blocks.values() if b.get("type") == "api"]
        
        valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        
        for block in api_blocks:
            block_id = block.get("id", "unknown")
            sub_blocks = block.get("sub_blocks", {})
            
            # Check required fields
            if "url" not in sub_blocks:
                errors.append(f"API block {block_id} missing URL")
            else:
                url = sub_blocks["url"]
                if not url.startswith(("http://", "https://")):
                    warnings.append(f"API block {block_id} URL should use http/https protocol")
            
            if "method" not in sub_blocks:
                warnings.append(f"API block {block_id} missing HTTP method, defaulting to GET")
            else:
                method = sub_blocks["method"].upper()
                if method not in valid_methods:
                    errors.append(f"API block {block_id} has invalid HTTP method: {method}")
            
            # Check headers for authentication
            if "headers" in sub_blocks:
                headers = sub_blocks["headers"]
                if isinstance(headers, dict):
                    auth_headers = ["Authorization", "X-API-Key", "X-Auth-Token"]
                    has_auth = any(header in headers for header in auth_headers)
                    if not has_auth:
                        warnings.append(f"API block {block_id} may need authentication headers")
        
        return ValidationResult(
            validator_name="validate_api_integration",
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metadata={"api_count": len(api_blocks)}
        )
    
    async def _validate_edge_connectivity(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate block connections and workflow flow"""
        errors = []
        warnings = []
        
        blocks = state.get("blocks", {})
        edges = state.get("edges", [])
        
        if not edges and len(blocks) > 1:
            warnings.append("Workflow has multiple blocks but no connections")
        
        # Check edge validity
        block_ids = set(blocks.keys())
        
        for i, edge in enumerate(edges):
            if not isinstance(edge, dict):
                errors.append(f"Edge {i} is not a dictionary")
                continue
            
            if "from" not in edge or "to" not in edge:
                errors.append(f"Edge {i} missing 'from' or 'to' field")
                continue
            
            from_id = edge["from"]
            to_id = edge["to"]
            
            if from_id not in block_ids:
                errors.append(f"Edge {i} references non-existent block: {from_id}")
            
            if to_id not in block_ids:
                errors.append(f"Edge {i} references non-existent block: {to_id}")
        
        # Check for disconnected blocks
        connected_blocks = set()
        for edge in edges:
            if isinstance(edge, dict) and "from" in edge and "to" in edge:
                connected_blocks.add(edge["from"])
                connected_blocks.add(edge["to"])
        
        disconnected = block_ids - connected_blocks
        if disconnected and len(blocks) > 1:
            warnings.append(f"Disconnected blocks found: {list(disconnected)}")
        
        # Check for starter block connectivity
        starter_blocks = [b for b in blocks.values() if b.get("type") == "starter"]
        for starter in starter_blocks:
            starter_id = starter.get("id")
            has_outgoing = any(edge.get("from") == starter_id for edge in edges if isinstance(edge, dict))
            if not has_outgoing:
                warnings.append(f"Starter block {starter_id} has no outgoing connections")
        
        return ValidationResult(
            validator_name="validate_edge_connectivity",
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metadata={"edge_count": len(edges), "connected_blocks": len(connected_blocks)}
        )
    
    async def _validate_workflow_patterns(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate common workflow patterns"""
        errors = []
        warnings = []
        detected_patterns = []
        
        blocks = state.get("blocks", {})
        edges = state.get("edges", [])
        variables = state.get("variables", {})
        
        # Analyze block types
        block_types = [b.get("type") for b in blocks.values()]
        agent_count = block_types.count("agent")
        api_count = block_types.count("api")
        starter_count = block_types.count("starter")
        
        # Detect patterns
        if agent_count >= 3:
            detected_patterns.append("multi_agent_team")
        
        if api_count >= 2 and agent_count >= 1:
            detected_patterns.append("api_orchestration")
        
        # Check for trading bot pattern
        var_names = [k.lower() for k in variables.keys()]
        if any("trading" in name or "price" in name or "market" in name for name in var_names):
            detected_patterns.append("trading_bot")
        
        # Check for web3 pattern
        if any("web3" in str(b).lower() or "contract" in str(b).lower() for b in blocks.values()):
            detected_patterns.append("web3_automation")
        
        # Validate pattern-specific requirements
        if "multi_agent_team" in detected_patterns:
            if agent_count < 2:
                warnings.append("Multi-agent pattern detected but insufficient agents")
        
        if "trading_bot" in detected_patterns:
            required_vars = ["trading_pair", "stop_loss", "take_profit"]
            missing_vars = [var for var in required_vars if var not in [k.lower() for k in variables.keys()]]
            if missing_vars:
                warnings.append(f"Trading bot pattern missing variables: {missing_vars}")
        
        return ValidationResult(
            validator_name="validate_workflow_patterns",
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metadata={"detected_patterns": detected_patterns}
        )
    
    async def _validate_position_bounds(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate block positions are within reasonable bounds"""
        errors = []
        warnings = []
        
        blocks = state.get("blocks", {})
        
        # Canvas bounds (typical Agent Forge canvas)
        min_x, max_x = 0, 2000
        min_y, max_y = 0, 1500
        
        for block_id, block in blocks.items():
            x = block.get("position_x", 0)
            y = block.get("position_y", 0)
            
            if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                errors.append(f"Block {block_id} has invalid position coordinates")
                continue
            
            if x < min_x or x > max_x:
                warnings.append(f"Block {block_id} x-position ({x}) outside typical canvas bounds")
            
            if y < min_y or y > max_y:
                warnings.append(f"Block {block_id} y-position ({y}) outside typical canvas bounds")
        
        # Check for overlapping blocks
        positions = [(b.get("position_x", 0), b.get("position_y", 0)) for b in blocks.values()]
        if len(set(positions)) < len(positions):
            warnings.append("Some blocks have identical positions (may overlap)")
        
        return ValidationResult(
            validator_name="validate_position_bounds",
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    async def _validate_subblock_structure(self, state: Dict[str, Any], workflow_id: str) -> ValidationResult:
        """Validate sub-block configurations for each block type"""
        errors = []
        warnings = []
        
        blocks = state.get("blocks", {})
        
        for block_id, block in blocks.items():
            block_type = block.get("type")
            sub_blocks = block.get("sub_blocks", {})
            
            if block_type == "starter":
                required = ["startWorkflow"]
                for field in required:
                    if field not in sub_blocks:
                        errors.append(f"Starter block {block_id} missing required sub_block: {field}")
            
            elif block_type == "agent":
                required = ["model", "systemPrompt"]
                for field in required:
                    if field not in sub_blocks:
                        errors.append(f"Agent block {block_id} missing required sub_block: {field}")
            
            elif block_type == "api":
                required = ["url"]
                for field in required:
                    if field not in sub_blocks:
                        errors.append(f"API block {block_id} missing required sub_block: {field}")
            
            elif block_type == "output":
                required = ["outputType"]
                for field in required:
                    if field not in sub_blocks:
                        errors.append(f"Output block {block_id} missing required sub_block: {field}")
            
            elif block_type == "tool":
                required = ["toolType"]
                for field in required:
                    if field not in sub_blocks:
                        errors.append(f"Tool block {block_id} missing required sub_block: {field}")
        
        return ValidationResult(
            validator_name="validate_subblock_structure",
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def _check_agent_forge_compliance(self, validation_results: List[ValidationResult]) -> bool:
        """Check strict Agent Forge compliance"""
        # Must pass all critical validators
        critical_validators = [
            "validate_schema",
            "validate_block_types", 
            "validate_starter_blocks",
            "validate_edge_connectivity"
        ]
        
        for result in validation_results:
            if result.validator_name in critical_validators and not result.valid:
                return False
        
        return True
    
    def _generate_summary(self, validation_results: List[ValidationResult], state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate validation summary"""
        total_errors = sum(len(r.errors) for r in validation_results)
        total_warnings = sum(len(r.warnings) for r in validation_results)
        
        blocks = state.get("blocks", {})
        block_types = {}
        for block in blocks.values():
            block_type = block.get("type", "unknown")
            block_types[block_type] = block_types.get(block_type, 0) + 1
        
        return {
            "total_validators": len(validation_results),
            "passed_validators": sum(1 for r in validation_results if r.valid),
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "block_count": len(blocks),
            "block_types": block_types,
            "edge_count": len(state.get("edges", [])),
            "has_variables": bool(state.get("variables")),
            "has_metadata": bool(state.get("metadata"))
        }

# Global instance
validator = WorkflowValidator() 