# tests/conftest.py - Shared test configuration for Agent Forge
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def client():
    """FastAPI test client for integration tests"""
    return TestClient(app)

@pytest.fixture
def mock_claude_client():
    """Mock Claude client for testing without API calls"""
    mock_client = Mock()
    mock_client.generate_workflow_state = AsyncMock()
    mock_client.analyze_workflow_pattern = AsyncMock(return_value="unknown")
    return mock_client

@pytest.fixture
def mock_db_service():
    """Mock database service for testing without database"""
    mock_db = Mock()
    mock_db.get_workflow = AsyncMock()
    mock_db.get_workflow_blocks = AsyncMock()
    mock_db.update_workflow_state = AsyncMock(return_value=True)
    mock_db.create_workflow = AsyncMock()
    return mock_db

@pytest.fixture
def sample_agent_forge_workflow():
    """Sample Agent Forge workflow for testing"""
    return {
        "id": "test-workflow-123",
        "name": "Test Agent Forge Workflow",
        "description": "A test workflow for Agent Forge",
        "user_id": "test-user",
        "workspace_id": "test-workspace",
        "state": {
            "blocks": {
                "starter-1": {
                    "id": "starter-1",
                    "type": "starter",
                    "name": "Start",
                    "position": {"x": 100, "y": 200},
                    "subBlocks": {
                        "startWorkflow": {"value": "manual"}
                    }
                }
            },
            "edges": [],
            "metadata": {"version": "1.0.0"}
        }
    }

@pytest.fixture
def agent_forge_block_types():
    """Agent Forge block types for testing"""
    return ["starter", "agent", "api", "output", "tool"]

# Test markers for different test categories
pytest.mark.agent_forge = pytest.mark.agent_forge
pytest.mark.claude = pytest.mark.claude
pytest.mark.database = pytest.mark.database
