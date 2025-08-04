"""Mock data fixtures for comprehensive testing."""

import uuid
from datetime import datetime
from typing import Dict, List, Any

# Sample Workflow Data
SAMPLE_WORKFLOW = {
    "id": "test-workflow-123",
    "name": "Test Trading Bot",
    "description": "A test trading bot workflow",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}

SAMPLE_BLOCKS = [
    {
        "id": "starter-1",
        "type": "starter",
        "workflow_id": "test-workflow-123",
        "name": "Start Trading",
        "position_x": 100,
        "position_y": 300,
        "config": {
            "description": "Initialize trading bot"
        }
    },
    {
        "id": "agent-1", 
        "type": "agent",
        "workflow_id": "test-workflow-123",
        "name": "Market Analyzer",
        "position_x": 300,
        "position_y": 300,
        "config": {
            "model": "gpt-4",
            "systemPrompt": "Analyze market conditions",
            "temperature": 0.7
        }
    },
    {
        "id": "api-1",
        "type": "api",
        "workflow_id": "test-workflow-123", 
        "name": "Get Price Data",
        "position_x": 500,
        "position_y": 300,
        "config": {
            "url": "https://api.example.com/price",
            "method": "GET",
            "headers": {"API-Key": "test"}
        }
    }
]

# Expected Generated State Structure
EXPECTED_STATE_STRUCTURE = {
    "blocks": {
        "starter-1": {
            "id": "starter-1",
            "type": "starter",
            "name": "Start Trading",
            "position": {"x": 100, "y": 300},
            "config": {"description": "Initialize trading bot"},
            "subBlocks": []
        },
        "agent-1": {
            "id": "agent-1", 
            "type": "agent",
            "name": "Market Analyzer",
            "position": {"x": 300, "y": 300},
            "config": {
                "model": "gpt-4",
                "systemPrompt": "Analyze market conditions",
                "temperature": 0.7
            },
            "subBlocks": []
        },
        "api-1": {
            "id": "api-1",
            "type": "api", 
            "name": "Get Price Data",
            "position": {"x": 500, "y": 300},
            "config": {
                "url": "https://api.example.com/price",
                "method": "GET",
                "headers": {"API-Key": "test"}
            },
            "subBlocks": []
        }
    },
    "edges": [
        {"from": "starter-1", "to": "agent-1"},
        {"from": "agent-1", "to": "api-1"}
    ],
    "metadata": {
        "agent_forge_version": "1.0.0",
        "generated_at": "2024-01-01T00:00:00Z",
        "workflow_type": "trading_bot"
    }
}

# Template Test Data
TEMPLATE_TEST_DATA = {
    "trading_bot": {
        "customization": {"trading_pair": "BTC/USD", "stop_loss": -5},
        "expected_blocks": ["starter", "agent", "api", "output"],
        "expected_connections": 3
    },
    "lead_generation": {
        "customization": {"lead_source": "LinkedIn", "crm": "HubSpot"},
        "expected_blocks": ["starter", "agent", "tool", "output"],
        "expected_connections": 3
    },
    "multi_agent_research": {
        "customization": {"research_topic": "AI Trends", "num_agents": 3},
        "expected_blocks": ["starter", "agent", "agent", "agent", "output"],
        "expected_connections": 4
    }
}

# Mock Claude API Responses
MOCK_CLAUDE_RESPONSES = {
    "successful_generation": {
        "content": [
            {
                "text": """
                {
                    "blocks": {
                        "starter-1": {
                            "id": "starter-1",
                            "type": "starter",
                            "name": "Initialize Process",
                            "position": {"x": 100, "y": 300},
                            "config": {"description": "Start the workflow"},
                            "subBlocks": []
                        },
                        "agent-1": {
                            "id": "agent-1",
                            "type": "agent", 
                            "name": "AI Assistant",
                            "position": {"x": 300, "y": 300},
                            "config": {
                                "model": "claude-3-5-sonnet",
                                "systemPrompt": "You are a helpful assistant",
                                "temperature": 0.7
                            },
                            "subBlocks": []
                        }
                    },
                    "edges": [
                        {"from": "starter-1", "to": "agent-1"}
                    ],
                    "metadata": {
                        "agent_forge_version": "1.0.0",
                        "generated_at": "2024-01-01T00:00:00Z",
                        "workflow_type": "generic"
                    }
                }
                """
            }
        ],
        "usage": {
            "input_tokens": 150,
            "output_tokens": 300
        }
    },
    "error_response": {
        "error": {
            "type": "rate_limit_error",
            "message": "Rate limit exceeded"
        }
    }
}

# Mock OpenAI Responses
MOCK_OPENAI_RESPONSES = {
    "embedding_success": {
        "data": [
            {
                "embedding": [0.1] * 1536,  # 1536-dimension vector
                "index": 0
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "total_tokens": 10
        }
    },
    "embedding_error": {
        "error": {
            "message": "Invalid API key",
            "type": "invalid_request_error"
        }
    }
}

# Validation Test Cases
VALIDATION_TEST_CASES = {
    "valid_state": {
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
        "edges": [],
        "metadata": {
            "agent_forge_version": "1.0.0",
            "generated_at": "2024-01-01T00:00:00Z"
        }
    },
    "invalid_schema": {
        "blocks": "invalid",  # Should be dict
        "edges": [],
        "metadata": {}
    },
    "missing_starter": {
        "blocks": {
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
    },
    "invalid_block_type": {
        "blocks": {
            "invalid-1": {
                "id": "invalid-1",
                "type": "invalid_type",
                "name": "Invalid Block",
                "position": {"x": 100, "y": 300},
                "config": {},
                "subBlocks": []
            }
        },
        "edges": [],
        "metadata": {}
    },
    "orphaned_block": {
        "blocks": {
            "starter-1": {
                "id": "starter-1",
                "type": "starter", 
                "name": "Start",
                "position": {"x": 100, "y": 300},
                "config": {},
                "subBlocks": []
            },
            "orphan-1": {
                "id": "orphan-1",
                "type": "agent",
                "name": "Orphaned Agent",
                "position": {"x": 500, "y": 300},
                "config": {"model": "gpt-4"},
                "subBlocks": []
            }
        },
        "edges": [],  # No edges connecting orphan
        "metadata": {}
    }
}

# Database Mock Data
MOCK_DATABASE_RESPONSES = {
    "workflow_exists": SAMPLE_WORKFLOW,
    "workflow_not_found": None,
    "blocks_for_workflow": SAMPLE_BLOCKS,
    "empty_blocks": [],
    "database_error": Exception("Database connection failed")
}

# Performance Test Data
PERFORMANCE_TEST_WORKFLOWS = [
    {
        "id": f"perf-workflow-{i}",
        "name": f"Performance Test Workflow {i}",
        "blocks": [
            {
                "id": f"starter-{i}",
                "type": "starter",
                "workflow_id": f"perf-workflow-{i}",
                "position_x": 100,
                "position_y": 300
            },
            {
                "id": f"agent-{i}",
                "type": "agent", 
                "workflow_id": f"perf-workflow-{i}",
                "position_x": 300,
                "position_y": 300,
                "config": {"model": "gpt-4"}
            }
        ]
    }
    for i in range(100)  # 100 test workflows
]

# Cache Test Data
CACHE_TEST_PATTERNS = [
    {
        "pattern_key": "trading_3_blocks",
        "block_types": ["starter", "agent", "api"],
        "connection_count": 2,
        "usage_count": 5,
        "similarity_threshold": 0.85
    },
    {
        "pattern_key": "lead_gen_4_blocks", 
        "block_types": ["starter", "agent", "tool", "output"],
        "connection_count": 3,
        "usage_count": 3,
        "similarity_threshold": 0.80
    }
]

def generate_workflow_id() -> str:
    """Generate unique workflow ID for testing."""
    return f"test-{uuid.uuid4()}"

def generate_sample_workflow(workflow_type: str = "generic") -> Dict[str, Any]:
    """Generate a sample workflow for testing."""
    workflow_id = generate_workflow_id()
    
    return {
        "id": workflow_id,
        "name": f"Test {workflow_type.title()} Workflow",
        "description": f"A test {workflow_type} workflow",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }

def generate_sample_blocks(workflow_id: str, count: int = 3) -> List[Dict[str, Any]]:
    """Generate sample blocks for a workflow."""
    block_types = ["starter", "agent", "api", "tool", "output"]
    blocks = []
    
    for i in range(count):
        block_type = block_types[i % len(block_types)]
        blocks.append({
            "id": f"{block_type}-{i+1}",
            "type": block_type,
            "workflow_id": workflow_id,
            "name": f"Test {block_type.title()} {i+1}",
            "position_x": 100 + (i * 200),
            "position_y": 300,
            "config": get_block_config(block_type)
        })
    
    return blocks

def get_block_config(block_type: str) -> Dict[str, Any]:
    """Get appropriate config for block type."""
    configs = {
        "starter": {"description": "Start the process"},
        "agent": {
            "model": "gpt-4",
            "systemPrompt": "You are a helpful assistant",
            "temperature": 0.7
        },
        "api": {
            "url": "https://api.example.com/data",
            "method": "GET",
            "headers": {"Authorization": "Bearer test"}
        },
        "tool": {
            "tool_name": "calculator",
            "parameters": {"precision": 2}
        },
        "output": {
            "format": "json",
            "destination": "console"
        }
    }
    return configs.get(block_type, {}) 