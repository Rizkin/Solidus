"""Pytest configuration and shared fixtures."""

import pytest
import asyncio
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any, List

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tests.fixtures.mock_data import (
    SAMPLE_WORKFLOW, SAMPLE_BLOCKS, EXPECTED_STATE_STRUCTURE,
    TEMPLATE_TEST_DATA, generate_workflow_id, generate_sample_workflow,
    generate_sample_blocks
)
from tests.fixtures.mock_responses import (
    CLAUDE_SUCCESS_RESPONSES, CLAUDE_ERROR_RESPONSES,
    OPENAI_SUCCESS_RESPONSES, OPENAI_ERROR_RESPONSES,
    DATABASE_SUCCESS_RESPONSES, DATABASE_ERROR_RESPONSES,
    VALIDATION_RESULTS
)

# Configure asyncio for async tests
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Mock database service
@pytest.fixture
def mock_db_service():
    """Mock database service with common operations."""
    mock_db = AsyncMock()
    
    # Mock successful operations
    mock_db.get_workflow = AsyncMock(return_value=SAMPLE_WORKFLOW)
    mock_db.get_workflow_blocks = AsyncMock(return_value=SAMPLE_BLOCKS)
    mock_db.update_workflow_state = AsyncMock(return_value=True)
    mock_db.get_all_workflows = AsyncMock(return_value=[SAMPLE_WORKFLOW])
    
    # Mock database connection
    mock_db.is_connected = True
    mock_db.connection_status = "connected"
    
    return mock_db

# Mock Claude API client
@pytest.fixture
def mock_claude_client():
    """Mock Anthropic Claude API client."""
    mock_client = MagicMock()
    
    # Default successful response
    mock_client.messages.create = MagicMock(
        return_value=CLAUDE_SUCCESS_RESPONSES["generic"]
    )
    
    return mock_client

# Mock OpenAI client
@pytest.fixture
def mock_openai_client():
    """Mock OpenAI API client."""
    mock_client = MagicMock()
    
    # Default successful embedding response
    mock_client.embeddings.create = MagicMock(
        return_value=OPENAI_SUCCESS_RESPONSES["embedding"]
    )
    
    return mock_client

# Sample workflow fixtures
@pytest.fixture
def sample_workflow():
    """Sample workflow data."""
    return SAMPLE_WORKFLOW.copy()

@pytest.fixture
def sample_blocks():
    """Sample workflow blocks."""
    return [block.copy() for block in SAMPLE_BLOCKS]

@pytest.fixture
def expected_state():
    """Expected generated state structure."""
    return EXPECTED_STATE_STRUCTURE.copy()

# Template test fixtures
@pytest.fixture
def template_test_data():
    """Template test data for all templates."""
    return TEMPLATE_TEST_DATA.copy()

@pytest.fixture(params=[
    "lead_generation", "trading_bot", "multi_agent_research",
    "customer_support", "web3_automation", "data_pipeline",
    "content_generation", "notification_system",
    "social_media_automation", "ecommerce_automation",
    "hr_recruitment", "financial_analysis", "project_management"
])
def template_name(request):
    """Parameterized fixture for all 13 templates."""
    return request.param

# Validation test fixtures
@pytest.fixture
def valid_state():
    """Valid workflow state for validation testing."""
    return VALIDATION_RESULTS["all_pass"].copy()

@pytest.fixture
def invalid_states():
    """Various invalid states for testing."""
    return {
        "schema_invalid": {"blocks": "invalid", "edges": [], "metadata": {}},
        "missing_starter": {
            "blocks": {
                "agent-1": {
                    "id": "agent-1",
                    "type": "agent",
                    "name": "Test Agent",
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
            "edges": [],  # No edges, so orphan-1 is disconnected
            "metadata": {}
        }
    }

# Performance test fixtures
@pytest.fixture
def performance_workflow_data():
    """Generate multiple workflows for performance testing."""
    workflows = []
    for i in range(10):
        workflow_id = f"perf-test-{i}"
        workflow = generate_sample_workflow("performance")
        workflow["id"] = workflow_id
        blocks = generate_sample_blocks(workflow_id, count=3 + i)  # Varying complexity
        workflows.append({"workflow": workflow, "blocks": blocks})
    return workflows

# Mock external API responses
@pytest.fixture
def mock_api_responses():
    """Mock responses for external API calls."""
    return {
        "successful_state_generation": {
            "status_code": 200,
            "json": {
                "workflow_id": "test-123",
                "generated_state": EXPECTED_STATE_STRUCTURE,
                "validation_report": VALIDATION_RESULTS["all_pass"]
            }
        },
        "api_error": {
            "status_code": 500,
            "json": {"detail": "Internal server error"}
        },
        "not_found": {
            "status_code": 404,
            "json": {"detail": "Not found"}
        }
    }

# Environment variable fixtures
@pytest.fixture
def mock_env_vars():
    """Mock environment variables."""
    env_vars = {
        "ANTHROPIC_API_KEY": "test-anthropic-key",
        "OPENAI_API_KEY": "test-openai-key",
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_ANON_KEY": "test-supabase-key"
    }
    
    with patch.dict(os.environ, env_vars):
        yield env_vars

# Mock services fixtures
@pytest.fixture
def mock_state_generator():
    """Mock state generator service."""
    from src.services.state_generator import AgentForgeStateGenerator
    
    mock_generator = MagicMock(spec=AgentForgeStateGenerator)
    
    # Mock successful generation
    mock_generator.generate_state = AsyncMock(
        return_value={
            "generated_state": EXPECTED_STATE_STRUCTURE,
            "metadata": {"generation_method": "ai", "model": "claude-3-5-sonnet"}
        }
    )
    
    # Mock fallback generation
    mock_generator._generate_fallback_state = MagicMock(
        return_value={
            "blocks": {"starter-1": {"type": "starter"}},
            "edges": [],
            "metadata": {"generation_method": "fallback"}
        }
    )
    
    return mock_generator

@pytest.fixture
def mock_validation_service():
    """Mock validation service."""
    mock_validator = MagicMock()
    
    # Mock successful validation
    mock_validator.validate_workflow_state = MagicMock(
        return_value=VALIDATION_RESULTS["all_pass"]
    )
    
    # Mock individual validators
    mock_validator.validate_schema = MagicMock(return_value={"valid": True, "errors": []})
    mock_validator.validate_block_types = MagicMock(return_value={"valid": True, "errors": []})
    mock_validator.validate_starter_block = MagicMock(return_value={"valid": True, "errors": []})
    
    return mock_validator

@pytest.fixture
def mock_lookup_service():
    """Mock enhanced lookup service."""
    mock_lookup = AsyncMock()
    
    # Mock cache operations
    mock_lookup.find_similar_workflows_hybrid = AsyncMock(
        return_value={"found": False, "patterns": []}
    )
    mock_lookup.store_workflow_pattern = AsyncMock(return_value=True)
    mock_lookup.get_cache_statistics = AsyncMock(
        return_value={
            "total_requests": 100,
            "cache_hits": 75,
            "cache_misses": 25,
            "hit_rate": 0.75
        }
    )
    
    # Mock embedding generation
    mock_lookup.generate_embedding = AsyncMock(
        return_value=[0.1] * 1536
    )
    
    return mock_lookup

# Database transaction fixtures
@pytest.fixture
def mock_database_transaction():
    """Mock database transaction context manager."""
    mock_transaction = AsyncMock()
    mock_transaction.__aenter__ = AsyncMock(return_value=mock_transaction)
    mock_transaction.__aexit__ = AsyncMock(return_value=None)
    mock_transaction.commit = AsyncMock()
    mock_transaction.rollback = AsyncMock()
    return mock_transaction

# Error simulation fixtures
@pytest.fixture
def error_scenarios():
    """Various error scenarios for testing."""
    return {
        "database_connection_failed": Exception("Database connection failed"),
        "api_timeout": Exception("Request timeout"),
        "invalid_json": ValueError("Invalid JSON format"),
        "rate_limit_exceeded": Exception("Rate limit exceeded"),
        "authentication_failed": Exception("Invalid API key")
    }

# Test data generators
@pytest.fixture
def workflow_generator():
    """Generator function for creating test workflows."""
    def _generate_workflow(workflow_type="generic", blocks_count=3):
        workflow_id = generate_workflow_id()
        workflow = generate_sample_workflow(workflow_type)
        workflow["id"] = workflow_id
        blocks = generate_sample_blocks(workflow_id, blocks_count)
        return {"workflow": workflow, "blocks": blocks}
    
    return _generate_workflow

# API client fixtures
@pytest.fixture
def mock_http_client():
    """Mock HTTP client for API testing."""
    mock_client = MagicMock()
    
    # Mock successful responses
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}
    mock_response.raise_for_status = MagicMock()
    
    mock_client.get = MagicMock(return_value=mock_response)
    mock_client.post = MagicMock(return_value=mock_response)
    mock_client.put = MagicMock(return_value=mock_response)
    mock_client.delete = MagicMock(return_value=mock_response)
    
    return mock_client

# Performance measurement fixtures
@pytest.fixture
def performance_monitor():
    """Performance monitoring utilities."""
    import time
    
    class PerformanceMonitor:
        def __init__(self):
            self.measurements = {}
        
        def start_timer(self, name: str):
            self.measurements[name] = {"start": time.time()}
        
        def end_timer(self, name: str):
            if name in self.measurements:
                self.measurements[name]["end"] = time.time()
                self.measurements[name]["duration"] = (
                    self.measurements[name]["end"] - self.measurements[name]["start"]
                )
        
        def get_duration(self, name: str) -> float:
            return self.measurements.get(name, {}).get("duration", 0.0)
        
        def assert_performance(self, name: str, max_duration: float):
            duration = self.get_duration(name)
            assert duration <= max_duration, f"Performance test failed: {name} took {duration}s, expected <{max_duration}s"
    
    return PerformanceMonitor()

# Cleanup fixtures
@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Automatically cleanup test data after each test."""
    # Setup
    yield
    
    # Cleanup - can be extended to clean up test files, database records, etc.
    pass

# Logging fixtures
@pytest.fixture
def capture_logs(caplog):
    """Capture and provide access to logs during testing."""
    import logging
    caplog.set_level(logging.DEBUG)
    return caplog
