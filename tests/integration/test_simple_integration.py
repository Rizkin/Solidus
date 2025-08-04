"""
Simple integration test to demonstrate comprehensive testing system.
"""

import pytest
from tests.fixtures.mock_data import SAMPLE_WORKFLOW, SAMPLE_BLOCKS


class TestSimpleIntegration:
    """Simple integration tests to verify testing infrastructure."""

    @pytest.mark.integration
    def test_mock_data_availability(self):
        """Test that mock data fixtures are available."""
        assert SAMPLE_WORKFLOW is not None
        assert "id" in SAMPLE_WORKFLOW
        assert "name" in SAMPLE_WORKFLOW
        
        assert SAMPLE_BLOCKS is not None
        assert len(SAMPLE_BLOCKS) > 0
        assert all("id" in block for block in SAMPLE_BLOCKS)

    @pytest.mark.integration
    def test_fixture_structure(self, sample_workflow, sample_blocks):
        """Test that pytest fixtures work properly."""
        assert sample_workflow is not None
        assert sample_blocks is not None
        assert len(sample_blocks) > 0

    @pytest.mark.integration
    @pytest.mark.parametrize("template_name", [
        "trading_bot", "lead_generation", "social_media_automation"
    ])
    def test_template_names_parameterized(self, template_name):
        """Test parameterized testing works."""
        assert isinstance(template_name, str)
        assert len(template_name) > 0
        assert "_" in template_name or template_name.isalpha()

    @pytest.mark.integration
    def test_mock_responses_structure(self):
        """Test that mock responses are properly structured."""
        from tests.fixtures.mock_responses import (
            CLAUDE_SUCCESS_RESPONSES, OPENAI_SUCCESS_RESPONSES
        )
        
        assert "trading_bot" in CLAUDE_SUCCESS_RESPONSES
        assert "embedding" in OPENAI_SUCCESS_RESPONSES
        
        # Verify Claude response structure
        trading_response = CLAUDE_SUCCESS_RESPONSES["trading_bot"]
        assert hasattr(trading_response, 'content')
        assert hasattr(trading_response, 'usage')

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_async_test_support(self):
        """Test that async tests work properly."""
        # Simple async operation
        import asyncio
        await asyncio.sleep(0.01)
        
        result = await self._mock_async_operation()
        assert result == "async_success"

    async def _mock_async_operation(self):
        """Mock async operation for testing."""
        return "async_success"

    @pytest.mark.integration
    def test_environment_setup(self, mock_env_vars):
        """Test that environment variable mocking works."""
        assert "ANTHROPIC_API_KEY" in mock_env_vars
        assert "OPENAI_API_KEY" in mock_env_vars
        assert mock_env_vars["ANTHROPIC_API_KEY"] == "test-anthropic-key"

    @pytest.mark.integration
    def test_performance_monitoring(self, performance_monitor):
        """Test that performance monitoring works."""
        performance_monitor.start_timer("test_operation")
        
        # Simulate some work
        sum(range(1000))
        
        performance_monitor.end_timer("test_operation")
        
        duration = performance_monitor.get_duration("test_operation")
        assert duration > 0
        assert duration < 1.0  # Should be very fast

    @pytest.mark.integration
    def test_error_scenarios_fixture(self, error_scenarios):
        """Test that error scenarios fixture works."""
        assert "database_connection_failed" in error_scenarios
        assert "api_timeout" in error_scenarios
        
        # Verify error types
        assert isinstance(error_scenarios["database_connection_failed"], Exception)
        assert isinstance(error_scenarios["api_timeout"], Exception) 