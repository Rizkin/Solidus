"""Mock responses for AI services and external APIs."""

from typing import Any, Dict, List
import json

class MockAnthropicResponse:
    """Mock Anthropic Claude API response."""
    
    def __init__(self, content: str, usage: Dict[str, int] = None):
        self.content = [type('Content', (), {'text': content})()]
        self.usage = usage or {"input_tokens": 100, "output_tokens": 200}
        
    def json(self):
        return {
            "content": [{"text": self.content[0].text}],
            "usage": self.usage
        }

class MockOpenAIResponse:
    """Mock OpenAI API response."""
    
    def __init__(self, data: List[Dict[str, Any]], usage: Dict[str, int] = None):
        self.data = data
        self.usage = usage or {"prompt_tokens": 10, "total_tokens": 10}
    
    def json(self):
        return {
            "data": self.data,
            "usage": self.usage
        }

# Successful Claude responses for different workflow types
CLAUDE_SUCCESS_RESPONSES = {
    "trading_bot": MockAnthropicResponse(
        json.dumps({
            "blocks": {
                "starter-1": {
                    "id": "starter-1",
                    "type": "starter",
                    "name": "Initialize Trading Bot",
                    "position": {"x": 100, "y": 300},
                    "config": {"description": "Start the crypto trading process"},
                    "subBlocks": []
                },
                "agent-1": {
                    "id": "agent-1",
                    "type": "agent",
                    "name": "Market Analyzer",
                    "position": {"x": 300, "y": 300},
                    "config": {
                        "model": "gpt-4",
                        "systemPrompt": "Analyze cryptocurrency market conditions and trends",
                        "temperature": 0.3
                    },
                    "subBlocks": []
                },
                "api-1": {
                    "id": "api-1",
                    "type": "api",
                    "name": "Price Data API",
                    "position": {"x": 500, "y": 300},
                    "config": {
                        "url": "https://api.binance.com/api/v3/ticker/price",
                        "method": "GET",
                        "headers": {"Content-Type": "application/json"}
                    },
                    "subBlocks": []
                },
                "output-1": {
                    "id": "output-1",
                    "type": "output",
                    "name": "Trading Decision",
                    "position": {"x": 700, "y": 300},
                    "config": {"format": "json", "destination": "trading_system"},
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
                "workflow_type": "trading_bot",
                "complexity": "medium"
            }
        }),
        {"input_tokens": 250, "output_tokens": 500}
    ),
    
    "lead_generation": MockAnthropicResponse(
        json.dumps({
            "blocks": {
                "starter-1": {
                    "id": "starter-1",
                    "type": "starter",
                    "name": "Start Lead Generation",
                    "position": {"x": 100, "y": 300},
                    "config": {"description": "Initialize lead generation process"},
                    "subBlocks": []
                },
                "agent-1": {
                    "id": "agent-1",
                    "type": "agent",
                    "name": "Lead Researcher",
                    "position": {"x": 300, "y": 300},
                    "config": {
                        "model": "claude-3-5-sonnet",
                        "systemPrompt": "Research and identify potential leads",
                        "temperature": 0.5
                    },
                    "subBlocks": []
                },
                "tool-1": {
                    "id": "tool-1",
                    "type": "tool",
                    "name": "CRM Integration",
                    "position": {"x": 500, "y": 300},
                    "config": {
                        "tool_name": "hubspot_crm",
                        "parameters": {"pipeline": "sales"}
                    },
                    "subBlocks": []
                }
            },
            "edges": [
                {"from": "starter-1", "to": "agent-1"},
                {"from": "agent-1", "to": "tool-1"}
            ],
            "metadata": {
                "agent_forge_version": "1.0.0",
                "generated_at": "2024-01-01T00:00:00Z",
                "workflow_type": "lead_generation"
            }
        })
    ),
    
    "generic": MockAnthropicResponse(
        json.dumps({
            "blocks": {
                "starter-1": {
                    "id": "starter-1",
                    "type": "starter",
                    "name": "Start Process",
                    "position": {"x": 100, "y": 300},
                    "config": {"description": "Initialize the workflow"},
                    "subBlocks": []
                },
                "agent-1": {
                    "id": "agent-1",
                    "type": "agent",
                    "name": "AI Assistant",
                    "position": {"x": 300, "y": 300},
                    "config": {
                        "model": "gpt-4",
                        "systemPrompt": "You are a helpful AI assistant",
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
        })
    )
}

# Error responses
CLAUDE_ERROR_RESPONSES = {
    "rate_limit": Exception("Rate limit exceeded. Please try again later."),
    "invalid_key": Exception("Invalid API key provided"),
    "timeout": Exception("Request timed out"),
    "malformed_response": MockAnthropicResponse("Invalid JSON response"),
    "empty_response": MockAnthropicResponse("")
}

# OpenAI embedding responses
OPENAI_SUCCESS_RESPONSES = {
    "embedding": MockOpenAIResponse(
        [{"embedding": [round(0.1 + i * 0.001, 6) for i in range(1536)], "index": 0}],
        {"prompt_tokens": 5, "total_tokens": 5}
    ),
    "multiple_embeddings": MockOpenAIResponse(
        [
            {"embedding": [0.1] * 1536, "index": 0},
            {"embedding": [0.2] * 1536, "index": 1}
        ],
        {"prompt_tokens": 10, "total_tokens": 10}
    )
}

OPENAI_ERROR_RESPONSES = {
    "invalid_key": Exception("Invalid API key"),
    "rate_limit": Exception("Rate limit exceeded"),
    "quota_exceeded": Exception("You exceeded your quota"),
    "timeout": Exception("Request timeout")
}

# Database mock responses
class MockDatabaseResponse:
    """Mock database query response."""
    
    def __init__(self, data: Any = None, error: Exception = None):
        self.data = data
        self.error = error
    
    async def execute(self):
        if self.error:
            raise self.error
        return self.data
    
    async def fetchone(self):
        if self.error:
            raise self.error
        return self.data
    
    async def fetchall(self):
        if self.error:
            raise self.error
        return self.data if isinstance(self.data, list) else [self.data]

DATABASE_SUCCESS_RESPONSES = {
    "workflow_found": MockDatabaseResponse({
        "id": "test-workflow-123",
        "name": "Test Workflow",
        "description": "A test workflow"
    }),
    "blocks_found": MockDatabaseResponse([
        {
            "id": "starter-1",
            "type": "starter",
            "workflow_id": "test-workflow-123",
            "name": "Start",
            "position_x": 100,
            "position_y": 300
        },
        {
            "id": "agent-1",
            "type": "agent",
            "workflow_id": "test-workflow-123",
            "name": "AI Agent",
            "position_x": 300,
            "position_y": 300
        }
    ]),
    "empty_result": MockDatabaseResponse([]),
    "insert_success": MockDatabaseResponse({"id": "new-workflow-456"})
}

DATABASE_ERROR_RESPONSES = {
    "connection_failed": MockDatabaseResponse(error=Exception("Database connection failed")),
    "query_timeout": MockDatabaseResponse(error=Exception("Query timeout")),
    "constraint_violation": MockDatabaseResponse(error=Exception("Foreign key constraint violation")),
    "table_not_found": MockDatabaseResponse(error=Exception("Table 'workflow' doesn't exist"))
}

# HTTP response mocks
class MockHTTPResponse:
    """Mock HTTP response for API testing."""
    
    def __init__(self, status_code: int, json_data: Dict[str, Any] = None, text: str = ""):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = text
        self.headers = {"Content-Type": "application/json"}
    
    def json(self):
        return self._json_data
    
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code} Error")

API_SUCCESS_RESPONSES = {
    "templates_list": MockHTTPResponse(200, {
        "total_count": 13,
        "categories": ["Finance", "Marketing", "AI"],
        "templates": {
            "trading_bot": {"category": "Finance", "description": "Crypto trading bot"},
            "lead_generation": {"category": "Marketing", "description": "Lead generation workflow"}
        }
    }),
    "workflow_created": MockHTTPResponse(200, {
        "workflow_id": "new-workflow-789",
        "message": "Workflow created successfully"
    }),
    "state_generated": MockHTTPResponse(200, {
        "workflow_id": "test-workflow-123",
        "generated_state": {"blocks": {}, "edges": [], "metadata": {}},
        "validation_report": {"overall_valid": True}
    }),
    "cache_stats": MockHTTPResponse(200, {
        "cache_statistics": {
            "total_requests": 100,
            "cache_hits": 75,
            "cache_misses": 25,
            "hit_rate": 0.75
        }
    })
}

API_ERROR_RESPONSES = {
    "not_found": MockHTTPResponse(404, {"detail": "Not found"}),
    "bad_request": MockHTTPResponse(400, {"detail": "Bad request"}),
    "internal_error": MockHTTPResponse(500, {"detail": "Internal server error"}),
    "rate_limit": MockHTTPResponse(429, {"detail": "Rate limit exceeded"})
}

# Validation result mocks
VALIDATION_RESULTS = {
    "all_pass": {
        "overall_valid": True,
        "validation_results": {
            "schema_validation": {"valid": True, "errors": []},
            "block_type_validation": {"valid": True, "errors": []},
            "starter_block_validation": {"valid": True, "errors": []},
            "agent_config_validation": {"valid": True, "errors": []},
            "api_integration_validation": {"valid": True, "errors": []},
            "edge_connectivity_validation": {"valid": True, "errors": []},
            "workflow_pattern_validation": {"valid": True, "errors": []},
            "position_bounds_validation": {"valid": True, "errors": []},
            "subblock_structure_validation": {"valid": True, "errors": []}
        },
        "summary": {
            "total_validators": 9,
            "passed": 9,
            "failed": 0,
            "warnings": 0
        }
    },
    
    "schema_fail": {
        "overall_valid": False,
        "validation_results": {
            "schema_validation": {
                "valid": False,
                "errors": ["Missing required field: blocks", "Invalid type for edges"]
            }
        },
        "summary": {
            "total_validators": 9,
            "passed": 8,
            "failed": 1,
            "warnings": 0
        }
    },
    
    "multiple_failures": {
        "overall_valid": False,
        "validation_results": {
            "schema_validation": {"valid": True, "errors": []},
            "block_type_validation": {
                "valid": False,
                "errors": ["Invalid block type: invalid_type"]
            },
            "starter_block_validation": {
                "valid": False,
                "errors": ["No starter block found"]
            },
            "edge_connectivity_validation": {
                "valid": False,
                "errors": ["Orphaned block: orphan-1"]
            }
        },
        "summary": {
            "total_validators": 9,
            "passed": 6,
            "failed": 3,
            "warnings": 0
        }
    }
}

# Cache operation results
CACHE_OPERATION_RESULTS = {
    "cache_hit": {
        "found": True,
        "pattern": "trading_3_blocks",
        "similarity": 0.92,
        "cached_state": {"blocks": {}, "edges": [], "metadata": {}},
        "adaptation_needed": False
    },
    
    "cache_miss": {
        "found": False,
        "searched_patterns": ["trading_3_blocks", "generic_3_blocks"],
        "best_match": None,
        "similarity": 0.0
    },
    
    "cache_adaptation": {
        "found": True,
        "pattern": "trading_3_blocks",
        "similarity": 0.85,
        "adaptation_needed": True,
        "adaptations": ["Update trading pair", "Adjust stop loss"]
    }
} 