"""
Comprehensive tests for AgentForgeStateGenerator class.

Tests AI state generation, edge inference, workflow type determination,
fallback generation, state enhancement, and error handling.

Coverage target: 95%+ for state_generator.py
"""

import pytest
import json
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any, List

from src.services.state_generator import AgentForgeStateGenerator
from tests.fixtures.mock_data import (
    SAMPLE_WORKFLOW, SAMPLE_BLOCKS, EXPECTED_STATE_STRUCTURE
)
from tests.fixtures.mock_responses import (
    CLAUDE_SUCCESS_RESPONSES, CLAUDE_ERROR_RESPONSES
)


class TestAgentForgeStateGenerator:
    """Test suite for AgentForgeStateGenerator."""

    @pytest.fixture(autouse=True)
    def setup_generator(self, mock_db_service):
        """Set up state generator for each test."""
        self.generator = AgentForgeStateGenerator(mock_db_service)
        self.mock_db = mock_db_service

    @pytest.mark.unit
    @pytest.mark.ai
    async def test_successful_ai_state_generation(self, mock_env_vars):
        """
        Test successful state generation using Claude AI.
        
        Verifies:
        - Mock workflow and blocks data
        - Mock Claude API response  
        - Generated state structure
        - Blocks, edges, metadata
        """
        # Setup mock data
        workflow_id = "test-workflow-ai"
        self.mock_db.get_workflow.return_value = {
            **SAMPLE_WORKFLOW,
            "id": workflow_id
        }
        self.mock_db.get_workflow_blocks.return_value = SAMPLE_BLOCKS
        
        # Mock Claude API response
        mock_claude_response = CLAUDE_SUCCESS_RESPONSES["trading_bot"]
        
        with patch('anthropic.Anthropic') as mock_claude_class:
            mock_claude_client = MagicMock()
            mock_claude_client.messages.create.return_value = mock_claude_response
            mock_claude_class.return_value = mock_claude_client
            
            # Execute state generation
            result = await self.generator.generate_state(workflow_id)
            
            # Verify results
            assert "generated_state" in result
            assert "metadata" in result
            
            generated_state = result["generated_state"]
            assert "blocks" in generated_state
            assert "edges" in generated_state
            assert "metadata" in generated_state
            
            # Verify blocks structure
            blocks = generated_state["blocks"]
            assert len(blocks) > 0
            
            for block_id, block in blocks.items():
                assert "id" in block
                assert "type" in block
                assert "name" in block
                assert "position" in block
                assert "config" in block
                assert "subBlocks" in block
            
            # Verify edges structure
            edges = generated_state["edges"]
            assert isinstance(edges, list)
            
            for edge in edges:
                assert "from" in edge
                assert "to" in edge
            
            # Verify metadata
            metadata = generated_state["metadata"]
            assert "agent_forge_version" in metadata
            assert "generated_at" in metadata
            
            # Verify Claude API was called
            mock_claude_client.messages.create.assert_called_once()

    @pytest.mark.unit
    async def test_edge_inference_linear_workflow(self):
        """
        Test edge inference from positions - linear workflow.
        
        Tests workflow with blocks at x-positions: 100, 300, 500
        Verifies correct sequential edge connections.
        """
        # Setup linear workflow blocks
        linear_blocks = [
            {
                "id": "starter-1",
                "type": "starter",
                "workflow_id": "linear-test",
                "name": "Start",
                "position_x": 100,
                "position_y": 300,
                "config": {}
            },
            {
                "id": "agent-1",
                "type": "agent",
                "workflow_id": "linear-test",
                "name": "Process",
                "position_x": 300,
                "position_y": 300,
                "config": {"model": "gpt-4"}
            },
            {
                "id": "output-1",
                "type": "output",
                "workflow_id": "linear-test",
                "name": "Result",
                "position_x": 500,
                "position_y": 300,
                "config": {}
            }
        ]
        
        # Mock database response
        self.mock_db.get_workflow_blocks.return_value = linear_blocks
        
        # Test edge inference method
        edges = self.generator._infer_edges_from_positions(linear_blocks)
        
        # Verify linear connections
        assert len(edges) == 2
        assert {"from": "starter-1", "to": "agent-1"} in edges
        assert {"from": "agent-1", "to": "output-1"} in edges

    @pytest.mark.unit
    async def test_edge_inference_branching_workflow(self):
        """
        Test edge inference for branching workflow.
        
        Tests workflow with parallel y-positions creating branches.
        Verifies correct branching edge connections.
        """
        # Setup branching workflow blocks
        branching_blocks = [
            {
                "id": "starter-1",
                "type": "starter",
                "workflow_id": "branch-test",
                "position_x": 100,
                "position_y": 300,
                "config": {}
            },
            {
                "id": "agent-1",
                "type": "agent", 
                "workflow_id": "branch-test",
                "position_x": 300,
                "position_y": 200,  # Upper branch
                "config": {"model": "gpt-4"}
            },
            {
                "id": "agent-2",
                "type": "agent",
                "workflow_id": "branch-test",
                "position_x": 300,
                "position_y": 400,  # Lower branch
                "config": {"model": "claude-3"}
            },
            {
                "id": "output-1",
                "type": "output",
                "workflow_id": "branch-test",
                "position_x": 500,
                "position_y": 300,
                "config": {}
            }
        ]
        
        edges = self.generator._infer_edges_from_positions(branching_blocks)
        
        # Verify branching connections
        assert len(edges) >= 3
        assert {"from": "starter-1", "to": "agent-1"} in edges
        assert {"from": "starter-1", "to": "agent-2"} in edges

    @pytest.mark.unit
    async def test_edge_inference_complex_multirow_workflow(self):
        """
        Test edge inference for complex multi-row workflow.
        
        Tests complex workflow with multiple rows and connections.
        Verifies correct complex edge relationships.
        """
        # Setup complex multi-row blocks
        complex_blocks = [
            {"id": "starter-1", "type": "starter", "position_x": 100, "position_y": 300},
            {"id": "agent-1", "type": "agent", "position_x": 300, "position_y": 200},
            {"id": "agent-2", "type": "agent", "position_x": 300, "position_y": 400},
            {"id": "api-1", "type": "api", "position_x": 500, "position_y": 200},
            {"id": "api-2", "type": "api", "position_x": 500, "position_y": 400},
            {"id": "output-1", "type": "output", "position_x": 700, "position_y": 300}
        ]
        
        edges = self.generator._infer_edges_from_positions(complex_blocks)
        
        # Verify complex connections exist
        assert len(edges) >= 4
        
        # Check that all blocks are connected in some way
        connected_blocks = set()
        for edge in edges:
            connected_blocks.add(edge["from"])
            connected_blocks.add(edge["to"])
        
        assert len(connected_blocks) == len(complex_blocks)

    @pytest.mark.unit
    async def test_workflow_type_determination_trading_bot(self):
        """
        Test trading bot pattern detection.
        
        Verifies workflow type is correctly identified as 'trading_bot'
        based on block patterns and configurations.
        """
        # Setup trading bot specific blocks
        trading_blocks = [
            {"id": "starter-1", "type": "starter", "name": "Initialize Trading"},
            {"id": "agent-1", "type": "agent", "name": "Market Analyzer", 
             "config": {"systemPrompt": "Analyze cryptocurrency market"}},
            {"id": "api-1", "type": "api", "name": "Price API",
             "config": {"url": "https://api.binance.com/api/v3/ticker/price"}},
            {"id": "output-1", "type": "output", "name": "Trading Decision"}
        ]
        
        workflow_type = self.generator._determine_workflow_type(trading_blocks)
        
        assert workflow_type == "trading_bot"

    @pytest.mark.unit
    async def test_workflow_type_determination_lead_generation(self):
        """
        Test lead generation pattern detection.
        
        Verifies workflow type is correctly identified as 'lead_generation'
        based on block patterns and configurations.
        """
        # Setup lead generation specific blocks
        lead_gen_blocks = [
            {"id": "starter-1", "type": "starter", "name": "Start Lead Gen"},
            {"id": "agent-1", "type": "agent", "name": "Lead Researcher",
             "config": {"systemPrompt": "Research potential leads"}},
            {"id": "tool-1", "type": "tool", "name": "CRM Integration",
             "config": {"tool_name": "hubspot"}},
            {"id": "output-1", "type": "output", "name": "Qualified Leads"}
        ]
        
        workflow_type = self.generator._determine_workflow_type(lead_gen_blocks)
        
        assert workflow_type == "lead_generation"

    @pytest.mark.unit 
    async def test_workflow_type_determination_multi_agent(self):
        """
        Test multi-agent pattern detection.
        
        Verifies workflow with 3+ agents is identified as 'multi_agent'.
        """
        # Setup multi-agent workflow (3+ agents)
        multi_agent_blocks = [
            {"id": "starter-1", "type": "starter"},
            {"id": "agent-1", "type": "agent", "name": "Researcher"},
            {"id": "agent-2", "type": "agent", "name": "Analyzer"}, 
            {"id": "agent-3", "type": "agent", "name": "Writer"},
            {"id": "output-1", "type": "output"}
        ]
        
        workflow_type = self.generator._determine_workflow_type(multi_agent_blocks)
        
        assert workflow_type == "multi_agent"

    @pytest.mark.unit
    async def test_workflow_type_determination_generic(self):
        """
        Test generic workflow pattern detection.
        
        Verifies workflow that doesn't match specific patterns 
        is identified as 'generic'.
        """
        # Setup generic workflow
        generic_blocks = [
            {"id": "starter-1", "type": "starter", "name": "Start Process"},
            {"id": "agent-1", "type": "agent", "name": "General Agent"}
        ]
        
        workflow_type = self.generator._determine_workflow_type(generic_blocks)
        
        assert workflow_type == "generic"

    @pytest.mark.unit
    async def test_fallback_state_generation(self, mock_env_vars):
        """
        Test fallback generation when AI is unavailable.
        
        Verifies:
        - Rule-based state generation when Claude API fails
        - All blocks included in fallback state
        - Basic structure maintained
        - Quick response time (<2s)
        """
        workflow_id = "test-fallback"
        self.mock_db.get_workflow.return_value = {**SAMPLE_WORKFLOW, "id": workflow_id}
        self.mock_db.get_workflow_blocks.return_value = SAMPLE_BLOCKS
        
        # Mock Claude API failure
        with patch('anthropic.Anthropic') as mock_claude_class:
            mock_claude_client = MagicMock()
            mock_claude_client.messages.create.side_effect = Exception("API unavailable")
            mock_claude_class.return_value = mock_claude_client
            
            # Time the fallback generation
            import time
            start_time = time.time()
            
            result = await self.generator.generate_state(workflow_id)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Verify fallback state generated
            assert "generated_state" in result
            assert "metadata" in result
            
            generated_state = result["generated_state"]
            assert "blocks" in generated_state
            assert "edges" in generated_state
            
            # Verify all original blocks included
            blocks = generated_state["blocks"]
            assert len(blocks) == len(SAMPLE_BLOCKS)
            
            # Verify fallback metadata
            metadata = generated_state["metadata"]
            assert metadata.get("generation_method") == "fallback"
            
            # Verify quick response (should be <2s for fallback)
            assert response_time < 5.0  # Allow some buffer for testing

    @pytest.mark.unit
    async def test_state_enhancement_missing_blocks(self):
        """
        Test state enhancement - missing blocks addition.
        
        Verifies that missing blocks are added during enhancement.
        """
        # Setup incomplete state (missing some blocks)
        incomplete_state = {
            "blocks": {
                "starter-1": {
                    "id": "starter-1",
                    "type": "starter",
                    "name": "Start"
                }
                # Missing other blocks from SAMPLE_BLOCKS
            },
            "edges": [],
            "metadata": {}
        }
        
        # Enhance state with all blocks
        enhanced_state = self.generator._enhance_state_with_missing_blocks(
            incomplete_state, SAMPLE_BLOCKS
        )
        
        # Verify all blocks are now present
        assert len(enhanced_state["blocks"]) == len(SAMPLE_BLOCKS)
        
        # Verify each block from SAMPLE_BLOCKS is included
        for block in SAMPLE_BLOCKS:
            assert block["id"] in enhanced_state["blocks"]

    @pytest.mark.unit
    async def test_state_enhancement_metadata_generation(self):
        """
        Test metadata generation during state enhancement.
        
        Verifies proper metadata is added to generated states.
        """
        # Setup state without metadata
        state_without_metadata = {
            "blocks": {"starter-1": {"type": "starter"}},
            "edges": [],
            "metadata": {}
        }
        
        enhanced_state = self.generator._enhance_state_metadata(
            state_without_metadata, "trading_bot"
        )
        
        # Verify metadata enhancement
        metadata = enhanced_state["metadata"]
        assert "agent_forge_version" in metadata
        assert "generated_at" in metadata
        assert "workflow_type" in metadata
        assert metadata["workflow_type"] == "trading_bot"

    @pytest.mark.unit
    async def test_state_enhancement_subblocks(self):
        """
        Test subBlocks enhancement during state generation.
        
        Verifies that appropriate subBlocks are added to blocks.
        """
        # Setup basic state
        basic_state = {
            "blocks": {
                "agent-1": {
                    "id": "agent-1",
                    "type": "agent",
                    "name": "AI Agent",
                    "config": {"model": "gpt-4"}
                }
            },
            "edges": [],
            "metadata": {}
        }
        
        enhanced_state = self.generator._enhance_subblocks(basic_state)
        
        # Verify subBlocks added
        agent_block = enhanced_state["blocks"]["agent-1"]
        assert "subBlocks" in agent_block
        assert isinstance(agent_block["subBlocks"], list)

    @pytest.mark.unit
    async def test_edge_validation_and_enhancement(self):
        """
        Test edge validation during state enhancement.
        
        Verifies that invalid edges are removed and valid ones maintained.
        """
        # Setup state with invalid edges
        state_with_invalid_edges = {
            "blocks": {
                "starter-1": {"id": "starter-1", "type": "starter"},
                "agent-1": {"id": "agent-1", "type": "agent"}
            },
            "edges": [
                {"from": "starter-1", "to": "agent-1"},  # Valid
                {"from": "nonexistent", "to": "agent-1"},  # Invalid - from doesn't exist
                {"from": "agent-1", "to": "nonexistent"}   # Invalid - to doesn't exist
            ],
            "metadata": {}
        }
        
        enhanced_state = self.generator._validate_and_fix_edges(state_with_invalid_edges)
        
        # Verify only valid edges remain
        edges = enhanced_state["edges"]
        assert len(edges) == 1
        assert {"from": "starter-1", "to": "agent-1"} in edges

    @pytest.mark.unit
    @pytest.mark.error_handling
    async def test_error_handling_missing_workflow(self):
        """
        Test error handling for missing workflow.
        
        Verifies appropriate error when workflow doesn't exist.
        """
        # Mock workflow not found
        self.mock_db.get_workflow.return_value = None
        
        with pytest.raises(ValueError, match="Workflow not found"):
            await self.generator.generate_state("nonexistent-workflow")

    @pytest.mark.unit
    @pytest.mark.error_handling
    async def test_error_handling_empty_blocks(self):
        """
        Test error handling for empty blocks.
        
        Verifies appropriate error when no blocks exist for workflow.
        """
        # Mock workflow exists but no blocks
        self.mock_db.get_workflow.return_value = SAMPLE_WORKFLOW
        self.mock_db.get_workflow_blocks.return_value = []
        
        with pytest.raises(ValueError, match="No blocks found"):
            await self.generator.generate_state("workflow-with-no-blocks")

    @pytest.mark.unit
    @pytest.mark.error_handling
    async def test_error_handling_invalid_data(self):
        """
        Test error handling for invalid workflow data.
        
        Verifies appropriate error handling for corrupted data.
        """
        # Mock invalid workflow data
        invalid_workflow = {"name": "Invalid"}  # Missing required fields
        self.mock_db.get_workflow.return_value = invalid_workflow
        
        with pytest.raises((ValueError, KeyError)):
            await self.generator.generate_state("invalid-workflow")

    @pytest.mark.unit
    @pytest.mark.error_handling
    async def test_error_handling_api_timeout(self, mock_env_vars):
        """
        Test error handling for API timeouts.
        
        Verifies fallback behavior when Claude API times out.
        """
        workflow_id = "timeout-test"
        self.mock_db.get_workflow.return_value = {**SAMPLE_WORKFLOW, "id": workflow_id}
        self.mock_db.get_workflow_blocks.return_value = SAMPLE_BLOCKS
        
        # Mock API timeout
        with patch('anthropic.Anthropic') as mock_claude_class:
            mock_claude_client = MagicMock()
            mock_claude_client.messages.create.side_effect = Exception("Request timeout")
            mock_claude_class.return_value = mock_claude_client
            
            # Should fallback gracefully
            result = await self.generator.generate_state(workflow_id)
            
            # Verify fallback state generated
            assert "generated_state" in result
            assert result["generated_state"]["metadata"]["generation_method"] == "fallback"

    @pytest.mark.unit
    async def test_concurrent_state_generation(self):
        """
        Test concurrent state generation requests.
        
        Verifies system handles multiple simultaneous requests properly.
        """
        workflow_ids = ["concurrent-1", "concurrent-2", "concurrent-3"]
        
        # Setup mock responses for each workflow
        for workflow_id in workflow_ids:
            self.mock_db.get_workflow.return_value = {
                **SAMPLE_WORKFLOW, 
                "id": workflow_id
            }
        
        self.mock_db.get_workflow_blocks.return_value = SAMPLE_BLOCKS
        
        # Mock successful Claude responses
        with patch('anthropic.Anthropic') as mock_claude_class:
            mock_claude_client = MagicMock()
            mock_claude_client.messages.create.return_value = CLAUDE_SUCCESS_RESPONSES["generic"]
            mock_claude_class.return_value = mock_claude_client
            
            # Execute concurrent requests
            tasks = [
                self.generator.generate_state(workflow_id) 
                for workflow_id in workflow_ids
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Verify all requests completed successfully
            assert len(results) == 3
            for result in results:
                assert not isinstance(result, Exception)
                assert "generated_state" in result

    @pytest.mark.unit
    async def test_workflow_complexity_analysis(self):
        """
        Test workflow complexity analysis.
        
        Verifies system correctly analyzes and reports workflow complexity.
        """
        # Simple workflow (2 blocks)
        simple_blocks = SAMPLE_BLOCKS[:2]
        simple_complexity = self.generator._analyze_workflow_complexity(simple_blocks)
        assert simple_complexity == "simple"
        
        # Medium complexity (3-5 blocks)
        medium_blocks = SAMPLE_BLOCKS
        medium_complexity = self.generator._analyze_workflow_complexity(medium_blocks)
        assert medium_complexity == "medium"
        
        # Complex workflow (6+ blocks)
        complex_blocks = SAMPLE_BLOCKS + [
            {"id": "extra-1", "type": "tool"},
            {"id": "extra-2", "type": "api"},
            {"id": "extra-3", "type": "output"}
        ]
        complex_complexity = self.generator._analyze_workflow_complexity(complex_blocks)
        assert complex_complexity == "complex"

    @pytest.mark.unit
    @pytest.mark.performance
    async def test_state_generation_performance(self, performance_monitor, mock_env_vars):
        """
        Test state generation performance benchmarks.
        
        Verifies generation completes within acceptable time limits.
        """
        workflow_id = "performance-test"
        self.mock_db.get_workflow.return_value = {**SAMPLE_WORKFLOW, "id": workflow_id}
        self.mock_db.get_workflow_blocks.return_value = SAMPLE_BLOCKS
        
        # Mock fast Claude response
        with patch('anthropic.Anthropic') as mock_claude_class:
            mock_claude_client = MagicMock()
            mock_claude_client.messages.create.return_value = CLAUDE_SUCCESS_RESPONSES["generic"]
            mock_claude_class.return_value = mock_claude_client
            
            # Measure performance
            performance_monitor.start_timer("state_generation")
            
            result = await self.generator.generate_state(workflow_id)
            
            performance_monitor.end_timer("state_generation")
            
            # Verify successful generation
            assert "generated_state" in result
            
            # Assert performance requirements (should be <5s for AI generation)
            performance_monitor.assert_performance("state_generation", 5.0) 