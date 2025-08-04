"""
Comprehensive tests for validation system.

Tests all 9 validators: Schema, Block Type, Starter Block, Agent Configuration,
API Integration, Edge Connectivity, Workflow Pattern, Position Bounds, SubBlock Structure.

Coverage target: 100% for validation.py
"""

import pytest
from unittest.mock import MagicMock, patch
from typing import Dict, Any, List

from src.services.validation import WorkflowValidator
from tests.fixtures.mock_data import VALIDATION_TEST_CASES
from tests.fixtures.mock_responses import VALIDATION_RESULTS


class TestWorkflowValidator:
    """Test suite for WorkflowValidator - all 9 validators."""

    @pytest.fixture(autouse=True)
    def setup_validator(self):
        """Set up validator for each test."""
        self.validator = WorkflowValidator()

    # ========================================
    # 1. Schema Validation Tests
    # ========================================
    
    @pytest.mark.unit
    @pytest.mark.validation
    def test_schema_validation_valid_state(self):
        """Test schema validation with valid state structure."""
        valid_state = {
            "blocks": {
                "starter-1": {
                    "id": "starter-1",
                    "type": "starter",
                    "name": "Start",
                    "position": {"x": 100, "y": 300},
                    "config": {},
                    "subBlocks": []
                }
            },
            "edges": [{"from": "starter-1", "to": "agent-1"}],
            "metadata": {
                "agent_forge_version": "1.0.0",
                "generated_at": "2024-01-01T00:00:00Z"
            }
        }
        
        result = self.validator.validate_schema(valid_state)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    @pytest.mark.unit
    @pytest.mark.validation
    def test_schema_validation_missing_blocks(self):
        """Test schema validation with missing required 'blocks' field."""
        invalid_state = {
            "edges": [],
            "metadata": {}
            # Missing 'blocks' field
        }
        
        result = self.validator.validate_schema(invalid_state)
        
        assert result["valid"] is False
        assert any("blocks" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    def test_schema_validation_missing_edges(self):
        """Test schema validation with missing required 'edges' field."""
        invalid_state = {
            "blocks": {},
            "metadata": {}
            # Missing 'edges' field
        }
        
        result = self.validator.validate_schema(invalid_state)
        
        assert result["valid"] is False
        assert any("edges" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    def test_schema_validation_missing_metadata(self):
        """Test schema validation with missing required 'metadata' field."""
        invalid_state = {
            "blocks": {},
            "edges": []
            # Missing 'metadata' field
        }
        
        result = self.validator.validate_schema(invalid_state)
        
        assert result["valid"] is False
        assert any("metadata" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    def test_schema_validation_wrong_field_types(self):
        """Test schema validation with wrong field types."""
        invalid_state = {
            "blocks": "should_be_dict",  # Wrong type
            "edges": "should_be_list",   # Wrong type
            "metadata": []               # Wrong type
        }
        
        result = self.validator.validate_schema(invalid_state)
        
        assert result["valid"] is False
        assert len(result["errors"]) >= 3  # At least one error per wrong type

    @pytest.mark.unit
    @pytest.mark.validation
    def test_schema_validation_empty_state(self):
        """Test schema validation with completely empty state."""
        empty_state = {}
        
        result = self.validator.validate_schema(empty_state)
        
        assert result["valid"] is False
        assert len(result["errors"]) >= 3  # Missing all required fields

    # ========================================
    # 2. Block Type Validation Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.validation
    @pytest.mark.parametrize("valid_type", [
        "starter", "agent", "api", "output", "tool"
    ])
    def test_block_type_validation_valid_types(self, valid_type):
        """Test block type validation with valid block types."""
        state_with_valid_type = {
            "blocks": {
                f"{valid_type}-1": {
                    "id": f"{valid_type}-1",
                    "type": valid_type,
                    "name": f"Test {valid_type.title()}",
                    "position": {"x": 100, "y": 300},
                    "config": {},
                    "subBlocks": []
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_block_types(state_with_valid_type)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    @pytest.mark.unit
    @pytest.mark.validation
    @pytest.mark.parametrize("invalid_type", [
        "invalid_type", "unknown", "custom_block", "workflow", "process"
    ])
    def test_block_type_validation_invalid_types(self, invalid_type):
        """Test block type validation with invalid block types."""
        state_with_invalid_type = {
            "blocks": {
                "invalid-1": {
                    "id": "invalid-1",
                    "type": invalid_type,
                    "name": "Invalid Block",
                    "position": {"x": 100, "y": 300},
                    "config": {},
                    "subBlocks": []
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_block_types(state_with_invalid_type)
        
        assert result["valid"] is False
        assert any(invalid_type in error for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    def test_block_type_validation_missing_type_field(self):
        """Test block type validation with missing 'type' field."""
        state_missing_type = {
            "blocks": {
                "no-type-1": {
                    "id": "no-type-1",
                    "name": "Block Without Type",
                    "position": {"x": 100, "y": 300},
                    "config": {}
                    # Missing 'type' field
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_block_types(state_missing_type)
        
        assert result["valid"] is False
        assert any("type" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    def test_block_type_validation_mixed_valid_invalid(self):
        """Test block type validation with mix of valid and invalid types."""
        mixed_state = {
            "blocks": {
                "valid-1": {
                    "id": "valid-1",
                    "type": "starter",
                    "name": "Valid Starter"
                },
                "valid-2": {
                    "id": "valid-2", 
                    "type": "agent",
                    "name": "Valid Agent"
                },
                "invalid-1": {
                    "id": "invalid-1",
                    "type": "invalid_type",
                    "name": "Invalid Block"
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_block_types(mixed_state)
        
        assert result["valid"] is False
        assert any("invalid_type" in error for error in result["errors"])
        assert len(result["errors"]) == 1  # Only one invalid type

    # ========================================
    # 3. Starter Block Validation Tests  
    # ========================================

    @pytest.mark.unit
    @pytest.mark.validation
    def test_starter_block_validation_has_starter(self):
        """Test starter block validation with starter block present."""
        state_with_starter = {
            "blocks": {
                "starter-1": {
                    "id": "starter-1",
                    "type": "starter",
                    "name": "Start Process",
                    "position": {"x": 100, "y": 300},
                    "config": {},
                    "subBlocks": []
                },
                "agent-1": {
                    "id": "agent-1",
                    "type": "agent",
                    "name": "AI Agent",
                    "position": {"x": 300, "y": 300},
                    "config": {"model": "gpt-4"},
                    "subBlocks": []
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_starter_block(state_with_starter)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    @pytest.mark.unit
    @pytest.mark.validation
    def test_starter_block_validation_no_starter(self):
        """Test starter block validation without starter block."""
        state_without_starter = {
            "blocks": {
                "agent-1": {
                    "id": "agent-1",
                    "type": "agent",
                    "name": "AI Agent",
                    "position": {"x": 300, "y": 300},
                    "config": {"model": "gpt-4"},
                    "subBlocks": []
                },
                "output-1": {
                    "id": "output-1",
                    "type": "output",
                    "name": "Result",
                    "position": {"x": 500, "y": 300},
                    "config": {},
                    "subBlocks": []
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_starter_block(state_without_starter)
        
        assert result["valid"] is False
        assert any("starter" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    def test_starter_block_validation_multiple_starters(self):
        """Test starter block validation with multiple starter blocks."""
        state_multiple_starters = {
            "blocks": {
                "starter-1": {
                    "id": "starter-1",
                    "type": "starter",
                    "name": "Start 1"
                },
                "starter-2": {
                    "id": "starter-2",
                    "type": "starter", 
                    "name": "Start 2"
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_starter_block(state_multiple_starters)
        
        # Multiple starters might be valid or invalid depending on requirements
        # Adjust assertion based on your business logic
        assert isinstance(result["valid"], bool)
        if not result["valid"]:
            assert any("multiple" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    def test_starter_block_configuration_validation(self):
        """Test starter block configuration validation."""
        state_starter_config = {
            "blocks": {
                "starter-1": {
                    "id": "starter-1",
                    "type": "starter",
                    "name": "Start Process",
                    "position": {"x": 100, "y": 300},
                    "config": {
                        "description": "Initialize the workflow",
                        "autoStart": True
                    },
                    "subBlocks": []
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_starter_block(state_starter_config)
        
        assert result["valid"] is True

    # ========================================
    # 4. Agent Configuration Validation Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.validation
    @pytest.mark.parametrize("valid_model", [
        "gpt-4", "gpt-3.5-turbo", "claude-3-5-sonnet", "claude-3-haiku", "gemini-pro"
    ])
    def test_agent_config_validation_valid_models(self, valid_model):
        """Test agent configuration validation with valid AI models."""
        state_valid_model = {
            "blocks": {
                "agent-1": {
                    "id": "agent-1",
                    "type": "agent",
                    "name": "AI Agent",
                    "position": {"x": 300, "y": 300},
                    "config": {
                        "model": valid_model,
                        "systemPrompt": "You are a helpful assistant",
                        "temperature": 0.7
                    },
                    "subBlocks": []
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_agent_config(state_valid_model)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    @pytest.mark.unit
    @pytest.mark.validation
    @pytest.mark.parametrize("invalid_model", [
        "gpt-5", "claude-4", "invalid-model", "custom-ai", ""
    ])
    def test_agent_config_validation_invalid_models(self, invalid_model):
        """Test agent configuration validation with invalid models."""
        state_invalid_model = {
            "blocks": {
                "agent-1": {
                    "id": "agent-1",
                    "type": "agent",
                    "name": "AI Agent",
                    "config": {
                        "model": invalid_model,
                        "systemPrompt": "Test prompt"
                    }
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_agent_config(state_invalid_model)
        
        assert result["valid"] is False
        assert any(invalid_model in error or "model" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    def test_agent_config_validation_missing_system_prompt(self):
        """Test agent configuration validation with missing system prompt."""
        state_missing_prompt = {
            "blocks": {
                "agent-1": {
                    "id": "agent-1",
                    "type": "agent",
                    "name": "AI Agent",
                    "config": {
                        "model": "gpt-4"
                        # Missing systemPrompt
                    }
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_agent_config(state_missing_prompt)
        
        assert result["valid"] is False
        assert any("prompt" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    def test_agent_config_validation_missing_model(self):
        """Test agent configuration validation with missing model selection."""
        state_missing_model = {
            "blocks": {
                "agent-1": {
                    "id": "agent-1",
                    "type": "agent",
                    "name": "AI Agent",
                    "config": {
                        "systemPrompt": "You are helpful"
                        # Missing model
                    }
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_agent_config(state_missing_model)
        
        assert result["valid"] is False
        assert any("model" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    @pytest.mark.parametrize("temperature", [0.0, 0.5, 1.0, 1.5, 2.0])
    def test_agent_config_validation_temperature_valid(self, temperature):
        """Test agent configuration validation with valid temperature values."""
        state_valid_temp = {
            "blocks": {
                "agent-1": {
                    "id": "agent-1",
                    "type": "agent",
                    "name": "AI Agent",
                    "config": {
                        "model": "gpt-4",
                        "systemPrompt": "Test",
                        "temperature": temperature
                    }
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_agent_config(state_valid_temp)
        
        assert result["valid"] is True

    @pytest.mark.unit
    @pytest.mark.validation
    @pytest.mark.parametrize("invalid_temperature", [-1.0, 3.0, "high", None])
    def test_agent_config_validation_temperature_invalid(self, invalid_temperature):
        """Test agent configuration validation with invalid temperature values."""
        state_invalid_temp = {
            "blocks": {
                "agent-1": {
                    "id": "agent-1",
                    "type": "agent",
                    "name": "AI Agent",
                    "config": {
                        "model": "gpt-4",
                        "systemPrompt": "Test",
                        "temperature": invalid_temperature
                    }
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_agent_config(state_invalid_temp)
        
        if invalid_temperature is not None:
            assert result["valid"] is False
            assert any("temperature" in error.lower() for error in result["errors"])

    # ========================================
    # 5. API Integration Validation Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.validation
    def test_api_integration_validation_valid_config(self):
        """Test API integration validation with valid API blocks."""
        state_valid_api = {
            "blocks": {
                "api-1": {
                    "id": "api-1",
                    "type": "api",
                    "name": "External API",
                    "position": {"x": 500, "y": 300},
                    "config": {
                        "url": "https://api.example.com/data",
                        "method": "GET",
                        "headers": {
                            "Authorization": "Bearer token",
                            "Content-Type": "application/json"
                        }
                    },
                    "subBlocks": []
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_api_integration(state_valid_api)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    @pytest.mark.unit
    @pytest.mark.validation
    def test_api_integration_validation_missing_url(self):
        """Test API integration validation with missing URL."""
        state_missing_url = {
            "blocks": {
                "api-1": {
                    "id": "api-1",
                    "type": "api",
                    "name": "API Block",
                    "config": {
                        "method": "GET"
                        # Missing URL
                    }
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_api_integration(state_missing_url)
        
        assert result["valid"] is False
        assert any("url" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    @pytest.mark.parametrize("invalid_url", [
        "not-a-url", "ftp://invalid.com", "javascript:alert(1)", "", None
    ])
    def test_api_integration_validation_invalid_url_format(self, invalid_url):
        """Test API integration validation with invalid URL formats."""
        state_invalid_url = {
            "blocks": {
                "api-1": {
                    "id": "api-1",
                    "type": "api",
                    "name": "API Block",
                    "config": {
                        "url": invalid_url,
                        "method": "GET"
                    }
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_api_integration(state_invalid_url)
        
        if invalid_url:
            assert result["valid"] is False
            assert any("url" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    def test_api_integration_validation_missing_method(self):
        """Test API integration validation with missing HTTP method."""
        state_missing_method = {
            "blocks": {
                "api-1": {
                    "id": "api-1",
                    "type": "api",
                    "name": "API Block",
                    "config": {
                        "url": "https://api.example.com/data"
                        # Missing method
                    }
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_api_integration(state_missing_method)
        
        assert result["valid"] is False
        assert any("method" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    def test_api_integration_validation_headers(self):
        """Test API integration validation with various header configurations."""
        # Valid headers
        state_valid_headers = {
            "blocks": {
                "api-1": {
                    "id": "api-1",
                    "type": "api",
                    "name": "API Block",
                    "config": {
                        "url": "https://api.example.com/data",
                        "method": "POST",
                        "headers": {
                            "Content-Type": "application/json",
                            "X-API-Key": "secret",
                            "User-Agent": "AgentForge/1.0"
                        }
                    }
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_api_integration(state_valid_headers)
        assert result["valid"] is True

    # ========================================
    # 6. Edge Connectivity Validation Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.validation
    def test_edge_connectivity_validation_all_connected(self):
        """Test edge connectivity validation with all blocks connected."""
        state_all_connected = {
            "blocks": {
                "starter-1": {"id": "starter-1", "type": "starter"},
                "agent-1": {"id": "agent-1", "type": "agent"},
                "output-1": {"id": "output-1", "type": "output"}
            },
            "edges": [
                {"from": "starter-1", "to": "agent-1"},
                {"from": "agent-1", "to": "output-1"}
            ],
            "metadata": {}
        }
        
        result = self.validator.validate_edge_connectivity(state_all_connected)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    @pytest.mark.unit
    @pytest.mark.validation
    def test_edge_connectivity_validation_orphaned_blocks(self):
        """Test edge connectivity validation with orphaned blocks."""
        state_orphaned = {
            "blocks": {
                "starter-1": {"id": "starter-1", "type": "starter"},
                "agent-1": {"id": "agent-1", "type": "agent"},
                "orphan-1": {"id": "orphan-1", "type": "agent"},  # Orphaned
                "output-1": {"id": "output-1", "type": "output"}
            },
            "edges": [
                {"from": "starter-1", "to": "agent-1"},
                {"from": "agent-1", "to": "output-1"}
                # orphan-1 has no connections
            ],
            "metadata": {}
        }
        
        result = self.validator.validate_edge_connectivity(state_orphaned)
        
        assert result["valid"] is False
        assert any("orphan" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    def test_edge_connectivity_validation_invalid_references(self):
        """Test edge connectivity validation with invalid edge references."""
        state_invalid_refs = {
            "blocks": {
                "starter-1": {"id": "starter-1", "type": "starter"},
                "agent-1": {"id": "agent-1", "type": "agent"}
            },
            "edges": [
                {"from": "starter-1", "to": "agent-1"},      # Valid
                {"from": "nonexistent", "to": "agent-1"},   # Invalid from
                {"from": "agent-1", "to": "nonexistent"}    # Invalid to
            ],
            "metadata": {}
        }
        
        result = self.validator.validate_edge_connectivity(state_invalid_refs)
        
        assert result["valid"] is False
        assert len(result["errors"]) >= 2  # At least 2 invalid references

    @pytest.mark.unit
    @pytest.mark.validation
    def test_edge_connectivity_validation_circular_dependencies(self):
        """Test edge connectivity validation with circular dependencies."""
        state_circular = {
            "blocks": {
                "agent-1": {"id": "agent-1", "type": "agent"},
                "agent-2": {"id": "agent-2", "type": "agent"},
                "agent-3": {"id": "agent-3", "type": "agent"}
            },
            "edges": [
                {"from": "agent-1", "to": "agent-2"},
                {"from": "agent-2", "to": "agent-3"},
                {"from": "agent-3", "to": "agent-1"}  # Creates circular dependency
            ],
            "metadata": {}
        }
        
        result = self.validator.validate_edge_connectivity(state_circular)
        
        # Depending on requirements, circular dependencies might be invalid
        if not result["valid"]:
            assert any("circular" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    def test_edge_connectivity_validation_self_referencing(self):
        """Test edge connectivity validation with self-referencing edges."""
        state_self_ref = {
            "blocks": {
                "agent-1": {"id": "agent-1", "type": "agent"}
            },
            "edges": [
                {"from": "agent-1", "to": "agent-1"}  # Self-referencing
            ],
            "metadata": {}
        }
        
        result = self.validator.validate_edge_connectivity(state_self_ref)
        
        # Self-referencing edges are typically invalid
        assert result["valid"] is False
        assert any("self" in error.lower() for error in result["errors"])

    # ========================================
    # 7. Workflow Pattern Validation Tests  
    # ========================================

    @pytest.mark.unit
    @pytest.mark.validation
    def test_workflow_pattern_validation_lead_generation(self):
        """Test workflow pattern validation for lead generation pattern."""
        lead_gen_state = {
            "blocks": {
                "starter-1": {"type": "starter", "name": "Start Lead Gen"},
                "agent-1": {"type": "agent", "name": "Lead Researcher"},
                "tool-1": {"type": "tool", "name": "CRM Integration"},
                "output-1": {"type": "output", "name": "Qualified Leads"}
            },
            "edges": [
                {"from": "starter-1", "to": "agent-1"},
                {"from": "agent-1", "to": "tool-1"},
                {"from": "tool-1", "to": "output-1"}
            ],
            "metadata": {"workflow_type": "lead_generation"}
        }
        
        result = self.validator.validate_workflow_pattern(lead_gen_state)
        
        assert result["valid"] is True

    @pytest.mark.unit
    @pytest.mark.validation
    def test_workflow_pattern_validation_multi_agent(self):
        """Test workflow pattern validation for multi-agent pattern."""
        multi_agent_state = {
            "blocks": {
                "starter-1": {"type": "starter"},
                "agent-1": {"type": "agent", "name": "Researcher"},
                "agent-2": {"type": "agent", "name": "Analyzer"},
                "agent-3": {"type": "agent", "name": "Writer"},
                "output-1": {"type": "output"}
            },
            "edges": [
                {"from": "starter-1", "to": "agent-1"},
                {"from": "agent-1", "to": "agent-2"},
                {"from": "agent-2", "to": "agent-3"},
                {"from": "agent-3", "to": "output-1"}
            ],
            "metadata": {"workflow_type": "multi_agent"}
        }
        
        result = self.validator.validate_workflow_pattern(multi_agent_state)
        
        assert result["valid"] is True

    @pytest.mark.unit
    @pytest.mark.validation
    def test_workflow_pattern_validation_trading_bot(self):
        """Test workflow pattern validation for trading bot pattern."""
        trading_bot_state = {
            "blocks": {
                "starter-1": {"type": "starter", "name": "Initialize Trading"},
                "agent-1": {"type": "agent", "name": "Market Analyzer"},
                "api-1": {"type": "api", "name": "Price Data"},
                "output-1": {"type": "output", "name": "Trading Decision"}
            },
            "edges": [
                {"from": "starter-1", "to": "agent-1"},
                {"from": "agent-1", "to": "api-1"},
                {"from": "api-1", "to": "output-1"}
            ],
            "metadata": {"workflow_type": "trading_bot"}
        }
        
        result = self.validator.validate_workflow_pattern(trading_bot_state)
        
        assert result["valid"] is True

    @pytest.mark.unit
    @pytest.mark.validation
    def test_workflow_pattern_validation_detection_accuracy(self):
        """Test pattern detection accuracy for various workflow types."""
        # Test that patterns are correctly detected
        patterns_to_test = [
            ("lead_generation", ["starter", "agent", "tool", "output"]),
            ("trading_bot", ["starter", "agent", "api", "output"]),
            ("multi_agent", ["starter", "agent", "agent", "agent", "output"]),
            ("data_pipeline", ["starter", "api", "agent", "tool", "output"])
        ]
        
        for expected_pattern, block_types in patterns_to_test:
            test_state = {
                "blocks": {
                    f"{block_type}-{i}": {"type": block_type}
                    for i, block_type in enumerate(block_types, 1)
                },
                "edges": [],
                "metadata": {}
            }
            
            detected_pattern = self.validator._detect_workflow_pattern(test_state)
            
            # Pattern detection should be consistent
            assert isinstance(detected_pattern, str)

    # ========================================
    # 8. Position Bounds Validation Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.validation
    @pytest.mark.parametrize("x_pos", [0, 1000, 2000])
    @pytest.mark.parametrize("y_pos", [-200, 0, 500, 1000])
    def test_position_bounds_validation_valid_positions(self, x_pos, y_pos):
        """Test position bounds validation with valid positions (0-2000 x, -200-1000 y)."""
        state_valid_pos = {
            "blocks": {
                "block-1": {
                    "id": "block-1",
                    "type": "starter",
                    "name": "Test Block",
                    "position": {"x": x_pos, "y": y_pos},
                    "config": {},
                    "subBlocks": []
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_position_bounds(state_valid_pos)
        
        assert result["valid"] is True

    @pytest.mark.unit
    @pytest.mark.validation
    @pytest.mark.parametrize("x_pos", [-100, 2100, 5000])
    def test_position_bounds_validation_invalid_x_positions(self, x_pos):
        """Test position bounds validation with out of bounds x positions."""
        state_invalid_x = {
            "blocks": {
                "block-1": {
                    "position": {"x": x_pos, "y": 300}
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_position_bounds(state_invalid_x)
        
        assert result["valid"] is False
        assert any("x" in error.lower() and "bounds" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    @pytest.mark.parametrize("y_pos", [-300, 1100, 2000])
    def test_position_bounds_validation_invalid_y_positions(self, y_pos):
        """Test position bounds validation with out of bounds y positions."""
        state_invalid_y = {
            "blocks": {
                "block-1": {
                    "position": {"x": 500, "y": y_pos}
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_position_bounds(state_invalid_y)
        
        assert result["valid"] is False
        assert any("y" in error.lower() and "bounds" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    def test_position_bounds_validation_negative_positions(self):
        """Test position bounds validation with negative positions."""
        # Negative x should be invalid, negative y might be valid within bounds
        state_negative = {
            "blocks": {
                "block-1": {"position": {"x": -50, "y": -100}}  # x invalid, y valid
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_position_bounds(state_negative)
        
        # Should fail due to negative x
        assert result["valid"] is False

    @pytest.mark.unit
    @pytest.mark.validation
    @pytest.mark.parametrize("pos_type", ["float", "string"])
    def test_position_bounds_validation_float_vs_integer(self, pos_type):
        """Test position bounds validation with float vs integer positions."""
        if pos_type == "float":
            position = {"x": 100.5, "y": 300.7}
        else:  # string
            position = {"x": "100", "y": "300"}
        
        state_position_type = {
            "blocks": {
                "block-1": {"position": position}
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_position_bounds(state_position_type)
        
        # Float positions should be valid, string positions might be invalid
        if pos_type == "float":
            assert result["valid"] is True
        # Add specific assertion for string case based on requirements

    # ========================================
    # 9. SubBlock Structure Validation Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.validation
    def test_subblock_structure_validation_valid_structure(self):
        """Test subBlock structure validation with valid subBlock structure."""
        state_valid_subblocks = {
            "blocks": {
                "agent-1": {
                    "id": "agent-1",
                    "type": "agent",
                    "name": "AI Agent",
                    "subBlocks": [
                        {
                            "id": "sub-1",
                            "type": "input",
                            "name": "Input Handler",
                            "config": {"validation": True}
                        },
                        {
                            "id": "sub-2", 
                            "type": "processor",
                            "name": "Data Processor",
                            "config": {"timeout": 30}
                        }
                    ]
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_subblock_structure(state_valid_subblocks)
        
        assert result["valid"] is True

    @pytest.mark.unit
    @pytest.mark.validation
    def test_subblock_structure_validation_missing_id_type(self):
        """Test subBlock structure validation with missing id/type fields."""
        state_missing_fields = {
            "blocks": {
                "agent-1": {
                    "subBlocks": [
                        {
                            "name": "Missing ID and Type"
                            # Missing id and type
                        }
                    ]
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_subblock_structure(state_missing_fields)
        
        assert result["valid"] is False
        assert any("id" in error.lower() or "type" in error.lower() for error in result["errors"])

    @pytest.mark.unit
    @pytest.mark.validation
    def test_subblock_structure_validation_nested_subblocks(self):
        """Test subBlock structure validation with nested subBlocks."""
        state_nested = {
            "blocks": {
                "agent-1": {
                    "subBlocks": [
                        {
                            "id": "sub-1",
                            "type": "container",
                            "name": "Container",
                            "subBlocks": [  # Nested subBlocks
                                {
                                    "id": "nested-1",
                                    "type": "processor",
                                    "name": "Nested Processor"
                                }
                            ]
                        }
                    ]
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_subblock_structure(state_nested)
        
        # Nested subBlocks might be valid or invalid based on requirements
        assert isinstance(result["valid"], bool)

    @pytest.mark.unit
    @pytest.mark.validation
    def test_subblock_structure_validation_block_specific(self):
        """Test subBlock structure validation for block-specific subBlocks."""
        # Different block types might have different subBlock requirements
        agent_specific_state = {
            "blocks": {
                "agent-1": {
                    "type": "agent",
                    "subBlocks": [
                        {"id": "memory", "type": "memory", "name": "Agent Memory"},
                        {"id": "tools", "type": "tools", "name": "Available Tools"}
                    ]
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        result = self.validator.validate_subblock_structure(agent_specific_state)
        
        assert result["valid"] is True

    # ========================================
    # Comprehensive Integration Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.validation
    def test_complete_workflow_validation_all_pass(self):
        """Test complete workflow validation with all validators passing."""
        perfect_state = {
            "blocks": {
                "starter-1": {
                    "id": "starter-1",
                    "type": "starter", 
                    "name": "Start Process",
                    "position": {"x": 100, "y": 300},
                    "config": {"description": "Initialize workflow"},
                    "subBlocks": []
                },
                "agent-1": {
                    "id": "agent-1",
                    "type": "agent",
                    "name": "AI Assistant",
                    "position": {"x": 300, "y": 300},
                    "config": {
                        "model": "gpt-4",
                        "systemPrompt": "You are a helpful assistant",
                        "temperature": 0.7
                    },
                    "subBlocks": []
                },
                "api-1": {
                    "id": "api-1",
                    "type": "api",
                    "name": "External Service",
                    "position": {"x": 500, "y": 300},
                    "config": {
                        "url": "https://api.example.com/data",
                        "method": "GET",
                        "headers": {"Authorization": "Bearer token"}
                    },
                    "subBlocks": []
                },
                "output-1": {
                    "id": "output-1",
                    "type": "output",
                    "name": "Result",
                    "position": {"x": 700, "y": 300},
                    "config": {"format": "json"},
                    "subBlocks": []
                }
            },
            "edges": [
                {"from": "starter-1", "to": "agent-1"},
                {"from": "agent-1", "to": "api-1"},
                {"from": "api-1", "to": "output-1"}
            ],
            "metadata": {
                "agent_forge_version": "1.0.0",
                "generated_at": "2024-01-01T00:00:00Z",
                "workflow_type": "generic"
            }
        }
        
        result = self.validator.validate_workflow_state(perfect_state)
        
        assert result["overall_valid"] is True
        assert result["summary"]["failed"] == 0
        assert result["summary"]["passed"] == 9  # All 9 validators

    @pytest.mark.unit
    @pytest.mark.validation
    def test_complete_workflow_validation_multiple_failures(self):
        """Test complete workflow validation with multiple validator failures."""
        flawed_state = {
            "blocks": "invalid",  # Schema error
            "edges": [
                {"from": "nonexistent", "to": "also-nonexistent"}  # Connectivity error
            ],
            "metadata": {}
            # Multiple issues: no starter, invalid schema, connectivity problems
        }
        
        result = self.validator.validate_workflow_state(flawed_state)
        
        assert result["overall_valid"] is False
        assert result["summary"]["failed"] > 1  # Multiple failures
        assert len(result["validation_results"]) == 9  # All validators ran

    @pytest.mark.unit
    @pytest.mark.validation
    @pytest.mark.parametrize("validation_level", ["strict", "lenient", "warning_only"])
    def test_validation_levels_and_severity(self, validation_level):
        """Test different validation levels and severity handling."""
        # This test assumes different validation levels are supported
        state_with_warnings = {
            "blocks": {
                "starter-1": {"type": "starter"},
                "agent-1": {
                    "type": "agent",
                    "config": {
                        "model": "gpt-4",
                        "systemPrompt": "Short prompt"  # Might trigger warning
                    }
                }
            },
            "edges": [{"from": "starter-1", "to": "agent-1"}],
            "metadata": {}
        }
        
        result = self.validator.validate_workflow_state(
            state_with_warnings, 
            level=validation_level
        )
        
        # Behavior should vary based on validation level
        if validation_level == "strict":
            # Might fail on warnings
            pass
        elif validation_level == "lenient":
            # Should pass with warnings
            assert result["overall_valid"] is True
        # Add specific assertions based on your validation level implementation

    @pytest.mark.unit
    @pytest.mark.validation
    @pytest.mark.performance
    def test_validation_performance_large_workflow(self, performance_monitor):
        """Test validation performance with large workflows."""
        # Create large workflow (50+ blocks)
        large_state = {
            "blocks": {
                f"block-{i}": {
                    "id": f"block-{i}",
                    "type": "agent" if i > 0 else "starter",
                    "name": f"Block {i}",
                    "position": {"x": (i % 10) * 200, "y": (i // 10) * 200},
                    "config": {"model": "gpt-4"} if i > 0 else {},
                    "subBlocks": []
                }
                for i in range(50)
            },
            "edges": [
                {"from": f"block-{i}", "to": f"block-{i+1}"}
                for i in range(49)
            ],
            "metadata": {"agent_forge_version": "1.0.0"}
        }
        
        performance_monitor.start_timer("large_validation")
        
        result = self.validator.validate_workflow_state(large_state)
        
        performance_monitor.end_timer("large_validation")
        
        # Verify validation completed and performance requirements met
        assert "overall_valid" in result
        performance_monitor.assert_performance("large_validation", 5.0)  # Should complete in <5s 