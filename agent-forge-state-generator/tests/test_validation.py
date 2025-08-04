# tests/test_validation.py
import pytest
import json
from src.services.validation import AgentForgeValidator
from src.models.schemas import ValidationResult, ValidationReport

class TestAgentForgeValidation:
    """Test Agent Forge-specific validation functionality"""
    
    @pytest.fixture
    def validator(self):
        """Create validator instance for testing"""
        return AgentForgeValidator()
    
    @pytest.fixture
    def valid_agent_forge_state(self):
        """Valid Agent Forge workflow state for testing"""
        return {
            "blocks": {
                "starter-1": {
                    "id": "starter-1",
                    "type": "starter",
                    "name": "Market Monitor",
                    "position": {"x": 100, "y": 200},
                    "subBlocks": {
                        "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"},
                        "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "minutes"}
                    },
                    "outputs": {"response": {"type": {"input": "any"}}},
                    "enabled": True,
                    "horizontalHandles": True,
                    "isWide": False,
                    "height": 95
                },
                "agent-1": {
                    "id": "agent-1", 
                    "type": "agent",
                    "name": "Trading Agent",
                    "position": {"x": 300, "y": 200},
                    "subBlocks": {
                        "model": {"id": "model", "type": "combobox", "value": "gpt-4"},
                        "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                                       "value": "You are a trading agent"},
                        "temperature": {"id": "temperature", "type": "slider", "value": 0.7}
                    },
                    "outputs": {"model": "string", "content": "string"},
                    "enabled": True,
                    "horizontalHandles": True,
                    "isWide": True,
                    "height": 120
                },
                "output-1": {
                    "id": "output-1",
                    "type": "output", 
                    "name": "Trade Alert",
                    "position": {"x": 500, "y": 200},
                    "subBlocks": {
                        "outputType": {"id": "outputType", "type": "dropdown", "value": "email"},
                        "channels": {"id": "channels", "type": "multi-select", "value": ["email", "slack"]}
                    },
                    "outputs": {"success": "boolean", "message": "string"},
                    "enabled": True,
                    "horizontalHandles": True,
                    "isWide": False,
                    "height": 95
                }
            },
            "edges": [
                {"source": "starter-1", "target": "agent-1", "sourceHandle": "output", "targetHandle": "input"},
                {"source": "agent-1", "target": "output-1", "sourceHandle": "output", "targetHandle": "input"}
            ],
            "subflows": {},
            "variables": {
                "STOP_LOSS": {"type": "number", "value": -5},
                "TAKE_PROFIT": {"type": "number", "value": 10}
            },
            "metadata": {
                "version": "1.0.0",
                "createdAt": "2024-01-01T00:00:00Z",
                "updatedAt": "2024-01-01T00:00:00Z"
            }
        }
    
    @pytest.mark.asyncio
    async def test_validate_marketplace_readiness(self, validator, valid_agent_forge_state):
        """Test validation for Agent Forge marketplace requirements"""
        
        report = await validator.validate_state(valid_agent_forge_state, "test-workflow-123")
        
        # Should pass all critical validations for marketplace
        assert report.overall_valid
        assert report.agent_forge_compliance
        
        # Check specific marketplace requirements
        schema_result = next(r for r in report.validation_results if r.validator_name == "validate_schema")
        assert schema_result.valid
        
        block_types_result = next(r for r in report.validation_results if r.validator_name == "validate_block_types")
        assert block_types_result.valid
        
        starter_result = next(r for r in report.validation_results if r.validator_name == "validate_starter_blocks")
        assert starter_result.valid
    
    @pytest.mark.asyncio
    async def test_detect_workflow_patterns(self, validator):
        """Test detection of common Agent Forge patterns"""
        
        # Test lead generation pattern
        lead_gen_state = {
            "blocks": {
                "1": {"type": "starter", "name": "Lead Form", "subBlocks": {"webhookPath": {"value": "leads"}}},
                "2": {"type": "agent", "name": "Lead Qualifier", "subBlocks": {"model": {"value": "gpt-4"}}},
                "3": {"type": "api", "name": "CRM Integration", "subBlocks": {"url": {"value": "https://api.hubspot.com"}}},
                "4": {"type": "output", "name": "Sales Alert"}
            },
            "edges": [{"source": "1", "target": "2"}, {"source": "2", "target": "3"}, {"source": "3", "target": "4"}],
            "metadata": {"version": "1.0.0"}
        }
        
        report = await validator.validate_state(lead_gen_state, "lead-gen-test")
        
        # Check pattern detection
        pattern_result = next(r for r in report.validation_results if r.validator_name == "validate_workflow_patterns")
        assert pattern_result.valid
        assert pattern_result.metadata is not None
        
        # Test multi-agent pattern detection
        multi_agent_state = {
            "blocks": {
                "1": {"type": "starter", "name": "Research Request"},
                "2": {"type": "agent", "name": "Coordinator", "subBlocks": {"model": {"value": "claude-3"}}},
                "3": {"type": "agent", "name": "Researcher 1", "subBlocks": {"model": {"value": "gpt-4"}}},
                "4": {"type": "agent", "name": "Researcher 2", "subBlocks": {"model": {"value": "gpt-4"}}},
                "5": {"type": "agent", "name": "Researcher 3", "subBlocks": {"model": {"value": "claude-3"}}},
                "6": {"type": "output", "name": "Research Report"}
            },
            "edges": [
                {"source": "1", "target": "2"},
                {"source": "2", "target": "3"}, {"source": "2", "target": "4"}, {"source": "2", "target": "5"},
                {"source": "3", "target": "6"}, {"source": "4", "target": "6"}, {"source": "5", "target": "6"}
            ],
            "metadata": {"version": "1.0.0"}
        }
        
        multi_report = await validator.validate_state(multi_agent_state, "multi-agent-test")
        pattern_result = next(r for r in multi_report.validation_results if r.validator_name == "validate_workflow_patterns")
        
        assert "multi_agent_team" in pattern_result.metadata.get("detected_patterns", [])
        assert pattern_result.metadata["agent_count"] == 4
    
    @pytest.mark.asyncio
    async def test_validate_agent_configurations(self, validator):
        """Test validation of AI agent configurations"""
        
        # Test with valid agent configuration
        valid_agent_state = {
            "blocks": {
                "1": {"type": "starter", "name": "Start"},
                "2": {
                    "type": "agent",
                    "name": "AI Agent",
                    "subBlocks": {
                        "model": {"id": "model", "type": "combobox", "value": "gpt-4"},
                        "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                                       "value": "You are a helpful assistant"},
                        "temperature": {"id": "temperature", "type": "slider", "value": 0.7}
                    }
                }
            },
            "edges": [{"source": "1", "target": "2"}],
            "metadata": {"version": "1.0.0"}
        }
        
        report = await validator.validate_state(valid_agent_state, "agent-test")
        agent_result = next(r for r in report.validation_results if r.validator_name == "validate_agent_configurations")
        assert agent_result.valid
        assert len(agent_result.errors) == 0
        
        # Test with invalid agent configuration (missing model)
        invalid_agent_state = {
            "blocks": {
                "1": {"type": "starter", "name": "Start"},
                "2": {
                    "type": "agent",
                    "name": "AI Agent", 
                    "subBlocks": {
                        "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "Test"}
                        # Missing model configuration
                    }
                }
            },
            "edges": [{"source": "1", "target": "2"}],
            "metadata": {"version": "1.0.0"}
        }
        
        invalid_report = await validator.validate_state(invalid_agent_state, "invalid-agent-test")
        agent_result = next(r for r in invalid_report.validation_results if r.validator_name == "validate_agent_configurations")
        assert not agent_result.valid
        assert len(agent_result.errors) > 0
        assert "missing model selection" in agent_result.errors[0].lower()
    
    @pytest.mark.asyncio
    async def test_validate_api_integrations(self, validator):
        """Test validation of API integration blocks"""
        
        # Test with valid API configuration
        valid_api_state = {
            "blocks": {
                "1": {"type": "starter", "name": "Start"},
                "2": {
                    "type": "api",
                    "name": "External API",
                    "subBlocks": {
                        "url": {"id": "url", "type": "short-input", "value": "https://api.example.com/data"},
                        "method": {"id": "method", "type": "dropdown", "value": "GET"}
                    }
                }
            },
            "edges": [{"source": "1", "target": "2"}],
            "metadata": {"version": "1.0.0"}
        }
        
        report = await validator.validate_state(valid_api_state, "api-test")
        api_result = next(r for r in report.validation_results if r.validator_name == "validate_api_integrations")
        assert api_result.valid
        
        # Test with invalid API configuration (missing URL)
        invalid_api_state = {
            "blocks": {
                "1": {"type": "starter", "name": "Start"},
                "2": {
                    "type": "api",
                    "name": "External API",
                    "subBlocks": {
                        "method": {"id": "method", "type": "dropdown", "value": "GET"}
                        # Missing URL
                    }
                }
            },
            "edges": [{"source": "1", "target": "2"}],
            "metadata": {"version": "1.0.0"}
        }
        
        invalid_report = await validator.validate_state(invalid_api_state, "invalid-api-test")
        api_result = next(r for r in invalid_report.validation_results if r.validator_name == "validate_api_integrations")
        assert not api_result.valid
        assert "missing URL" in api_result.errors[0]
    
    @pytest.mark.asyncio
    async def test_validate_edge_connectivity(self, validator):
        """Test validation of edge connectivity"""
        
        # Test with valid edges
        valid_edge_state = {
            "blocks": {
                "block-1": {"type": "starter", "name": "Start"},
                "block-2": {"type": "agent", "name": "Agent"},
                "block-3": {"type": "output", "name": "Output"}
            },
            "edges": [
                {"source": "block-1", "target": "block-2", "sourceHandle": "output", "targetHandle": "input"},
                {"source": "block-2", "target": "block-3", "sourceHandle": "output", "targetHandle": "input"}
            ],
            "metadata": {"version": "1.0.0"}
        }
        
        report = await validator.validate_state(valid_edge_state, "edge-test")
        edge_result = next(r for r in report.validation_results if r.validator_name == "validate_edge_connectivity")
        assert edge_result.valid
        
        # Test with invalid edges (non-existent block)
        invalid_edge_state = {
            "blocks": {
                "block-1": {"type": "starter", "name": "Start"},
                "block-2": {"type": "agent", "name": "Agent"}
            },
            "edges": [
                {"source": "block-1", "target": "non-existent-block"}
            ],
            "metadata": {"version": "1.0.0"}
        }
        
        invalid_report = await validator.validate_state(invalid_edge_state, "invalid-edge-test")
        edge_result = next(r for r in invalid_report.validation_results if r.validator_name == "validate_edge_connectivity")
        assert not edge_result.valid
        assert "not found in blocks" in edge_result.errors[0]
    
    @pytest.mark.asyncio
    async def test_validate_position_bounds(self, validator):
        """Test validation of block position bounds"""
        
        # Test with positions within bounds
        valid_position_state = {
            "blocks": {
                "1": {"type": "starter", "name": "Start", "position": {"x": 100, "y": 200}},
                "2": {"type": "agent", "name": "Agent", "position": {"x": 300, "y": 200}}
            },
            "edges": [{"source": "1", "target": "2"}],
            "metadata": {"version": "1.0.0"}
        }
        
        report = await validator.validate_state(valid_position_state, "position-test")
        position_result = next(r for r in report.validation_results if r.validator_name == "validate_position_bounds")
        assert position_result.valid
        
        # Test with positions out of bounds
        invalid_position_state = {
            "blocks": {
                "1": {"type": "starter", "name": "Start", "position": {"x": -500, "y": 2000}},
                "2": {"type": "agent", "name": "Agent", "position": {"x": 3000, "y": -300}}
            },
            "edges": [{"source": "1", "target": "2"}],
            "metadata": {"version": "1.0.0"}
        }
        
        invalid_report = await validator.validate_state(invalid_position_state, "invalid-position-test")
        position_result = next(r for r in invalid_report.validation_results if r.validator_name == "validate_position_bounds")
        assert not position_result.valid
        assert len(position_result.warnings) > 0
        assert "out of bounds" in position_result.warnings[0]
    
    @pytest.mark.asyncio
    async def test_generate_improvement_suggestions(self, validator):
        """Test generation of improvement suggestions"""
        
        # Test workflow that could benefit from improvements
        basic_workflow = {
            "blocks": {
                "1": {"type": "starter", "name": "Start"}
                # No agents, no outputs - very basic
            },
            "edges": [],
            "metadata": {"version": "1.0.0"}
        }
        
        report = await validator.validate_state(basic_workflow, "basic-test")
        
        # Should generate suggestions for improvement
        assert len(report.suggestions) > 0
        suggestions_text = " ".join(report.suggestions).lower()
        assert "agent" in suggestions_text or "automation" in suggestions_text
    
    def test_add_custom_validator(self, validator):
        """Test adding custom validators"""
        
        def custom_web3_validator(state, workflow_id):
            """Custom validator for Web3 workflows"""
            errors = []
            warnings = []
            
            # Check for Web3-specific elements
            has_web3_content = any("web3" in str(block).lower() or "defi" in str(block).lower() 
                                 for block in state.get("blocks", {}).values())
            
            if has_web3_content:
                # Check for gas limit variables
                variables = state.get("variables", {})
                if not any("gas" in str(var).lower() for var in variables.keys()):
                    warnings.append("Web3 workflow should include gas limit configuration")
            
            return ValidationResult(
                validator_name="custom_web3_validator",
                valid=len(errors) == 0,
                errors=errors,
                warnings=warnings
            )
        
        # Add custom validator
        initial_count = len(validator.validators)
        validator.add_custom_validator("custom_web3_validator", custom_web3_validator)
        
        assert len(validator.validators) == initial_count + 1
        assert validator.validators[-1].__name__ == "custom_web3_validator"
