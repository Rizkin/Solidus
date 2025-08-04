# tests/test_agent_forge_generation.py
import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
from src.services.state_generator import AgentForgeStateGenerator
from src.services.validation import AgentForgeValidator
from src.integrations.claude_client import ClaudeClient
from src.utils.database_hybrid import DatabaseHybridService

class TestAgentForgeGeneration:
    """Test Agent Forge-specific workflow state generation"""
    
    @pytest.fixture
    def mock_claude_client(self):
        """Mock Claude client for testing"""
        mock_client = Mock(spec=ClaudeClient)
        mock_client.generate_workflow_state = AsyncMock()
        mock_client.analyze_workflow_pattern = AsyncMock(return_value="trading_bot")
        return mock_client
    
    @pytest.fixture
    def mock_db_service(self):
        """Mock database service for testing"""
        mock_db = Mock(spec=DatabaseHybridService)
        mock_db.get_workflow = AsyncMock()
        mock_db.get_workflow_blocks = AsyncMock()
        mock_db.update_workflow_state = AsyncMock(return_value=True)
        return mock_db
    
    @pytest.fixture
    def sample_workflow(self):
        """Sample workflow data for testing"""
        return {
            "id": "test-workflow-123",
            "name": "Test Trading Bot",
            "description": "Automated crypto trading workflow",
            "user_id": "test-user",
            "workspace_id": "test-workspace"
        }
    
    @pytest.fixture
    def sample_blocks(self):
        """Sample workflow blocks for testing"""
        return [
            {
                "id": "starter-block-1",
                "workflow_id": "test-workflow-123",
                "type": "starter",
                "name": "Market Monitor",
                "position_x": 100,
                "position_y": 200,
                "sub_blocks": {
                    "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"},
                    "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "minutes"},
                    "minutesInterval": {"id": "minutesInterval", "type": "short-input", "value": "5"}
                },
                "outputs": {"response": {"type": {"input": "any"}}},
                "enabled": True,
                "horizontal_handles": True,
                "is_wide": False,
                "height": 95
            },
            {
                "id": "agent-block-1", 
                "workflow_id": "test-workflow-123",
                "type": "agent",
                "name": "Trading Agent",
                "position_x": 300,
                "position_y": 200,
                "sub_blocks": {
                    "model": {"id": "model", "type": "combobox", "value": "gpt-4"},
                    "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                                   "value": "You are a crypto trading agent with stop-loss at -5%"},
                    "temperature": {"id": "temperature", "type": "slider", "value": 0.3},
                    "tools": {"id": "tools", "type": "tool-input", "value": [
                        {"type": "market_analysis", "enabled": True}
                    ]}
                },
                "outputs": {"model": "string", "tokens": "any", "content": "string"},
                "enabled": True,
                "horizontal_handles": True,
                "is_wide": True,
                "height": 120
            },
            {
                "id": "api-block-1",
                "workflow_id": "test-workflow-123", 
                "type": "api",
                "name": "Execute Trade",
                "position_x": 500,
                "position_y": 200,
                "sub_blocks": {
                    "url": {"id": "url", "type": "short-input", "value": "https://api.binance.com/api/v3/order"},
                    "method": {"id": "method", "type": "dropdown", "value": "POST"}
                },
                "outputs": {"data": "any", "status": "number"},
                "enabled": True,
                "horizontal_handles": True,
                "is_wide": False,
                "height": 95
            }
        ]
    
    @pytest.mark.asyncio
    async def test_generate_trading_bot_state(self, mock_claude_client, mock_db_service, 
                                            sample_workflow, sample_blocks):
        """Test generating state for Agent Forge trading bot pattern"""
        
        # Setup mocks
        mock_db_service.get_workflow.return_value = sample_workflow
        mock_db_service.get_workflow_blocks.return_value = sample_blocks
        
        # Mock Claude response with Agent Forge format
        mock_claude_response = {
            "blocks": {
                "starter-block-1": {
                    "id": "starter-block-1",
                    "type": "starter",
                    "name": "Market Monitor",
                    "position": {"x": 100, "y": 200},
                    "subBlocks": {
                        "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"},
                        "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "minutes"},
                        "minutesInterval": {"id": "minutesInterval", "type": "short-input", "value": "5"}
                    },
                    "outputs": {"response": {"type": {"input": "any"}}},
                    "enabled": True,
                    "horizontalHandles": True,
                    "isWide": False,
                    "height": 95
                },
                "agent-block-1": {
                    "id": "agent-block-1",
                    "type": "agent", 
                    "name": "Trading Agent",
                    "position": {"x": 300, "y": 200},
                    "subBlocks": {
                        "model": {"id": "model", "type": "combobox", "value": "gpt-4"},
                        "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                                       "value": "You are a crypto trading agent with stop-loss at -5%"},
                        "temperature": {"id": "temperature", "type": "slider", "value": 0.3},
                        "tools": {"id": "tools", "type": "tool-input", "value": [
                            {"type": "market_analysis", "enabled": True}
                        ]}
                    },
                    "outputs": {"model": "string", "tokens": "any", "content": "string"},
                    "enabled": True,
                    "horizontalHandles": True,
                    "isWide": True,
                    "height": 120
                }
            },
            "edges": [
                {"source": "starter-block-1", "target": "agent-block-1", 
                 "sourceHandle": "output", "targetHandle": "input"}
            ],
            "subflows": {},
            "variables": {
                "STOP_LOSS_PCT": {"type": "number", "value": -5},
                "TAKE_PROFIT_PCT": {"type": "number", "value": 10}
            },
            "metadata": {
                "version": "1.0.0",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        mock_claude_client.generate_workflow_state.return_value = mock_claude_response
        
        # Create generator with mocked dependencies
        generator = AgentForgeStateGenerator()
        generator.claude = mock_claude_client
        generator.db = mock_db_service
        
        # Generate state
        state = await generator.generate_workflow_state("test-workflow-123")
        
        # Verify Agent Forge structure
        assert "blocks" in state
        assert "edges" in state  
        assert "metadata" in state
        assert "variables" in state
        assert state["metadata"]["version"] == "1.0.0"
        
        # Verify agent configuration
        agent_block = state["blocks"]["agent-block-1"]
        assert agent_block["type"] == "agent"
        assert agent_block["subBlocks"]["model"]["value"] in ["gpt-4", "claude-3", "gemini-pro"]
        assert "systemPrompt" in agent_block["subBlocks"]
        assert "tools" in agent_block["subBlocks"]
        
        # Verify trading-specific variables
        assert "STOP_LOSS_PCT" in state["variables"]
        assert "TAKE_PROFIT_PCT" in state["variables"]
        
        # Verify edges connect properly
        edge = state["edges"][0]
        assert edge["source"] == "starter-block-1"
        assert edge["target"] == "agent-block-1"
    
    @pytest.mark.asyncio
    async def test_multi_agent_team_generation(self, mock_claude_client, mock_db_service):
        """Test generating multi-agent collaboration workflows"""
        
        # Setup multi-agent workflow
        multi_agent_workflow = {
            "id": "multi-agent-123",
            "name": "Research Team",
            "description": "Multi-agent research collaboration"
        }
        
        multi_agent_blocks = [
            {
                "id": "coordinator-1", "type": "agent", "name": "Research Coordinator",
                "position_x": 200, "position_y": 300,
                "sub_blocks": {"model": {"value": "claude-3"}}
            },
            {
                "id": "researcher-1", "type": "agent", "name": "Market Researcher", 
                "position_x": 400, "position_y": 200,
                "sub_blocks": {"model": {"value": "gpt-4"}}
            },
            {
                "id": "researcher-2", "type": "agent", "name": "Technical Researcher",
                "position_x": 400, "position_y": 300, 
                "sub_blocks": {"model": {"value": "gpt-4"}}
            },
            {
                "id": "researcher-3", "type": "agent", "name": "Competitive Researcher",
                "position_x": 400, "position_y": 400,
                "sub_blocks": {"model": {"value": "claude-3"}}
            },
            {
                "id": "synthesizer-1", "type": "agent", "name": "Research Synthesizer",
                "position_x": 600, "position_y": 300,
                "sub_blocks": {"model": {"value": "claude-3"}}
            }
        ]
        
        mock_db_service.get_workflow.return_value = multi_agent_workflow
        mock_db_service.get_workflow_blocks.return_value = multi_agent_blocks
        mock_claude_client.generate_workflow_state.return_value = {
            "blocks": {block["id"]: block for block in multi_agent_blocks},
            "edges": [
                {"source": "coordinator-1", "target": "researcher-1"},
                {"source": "coordinator-1", "target": "researcher-2"}, 
                {"source": "coordinator-1", "target": "researcher-3"},
                {"source": "researcher-1", "target": "synthesizer-1"},
                {"source": "researcher-2", "target": "synthesizer-1"},
                {"source": "researcher-3", "target": "synthesizer-1"}
            ],
            "metadata": {"version": "1.0.0"}
        }
        
        generator = AgentForgeStateGenerator()
        generator.claude = mock_claude_client
        generator.db = mock_db_service
        
        state = await generator.generate_workflow_state("multi-agent-123")
        
        # Verify multi-agent structure
        agent_blocks = [b for b in state["blocks"].values() if b.get("type") == "agent"]
        assert len(agent_blocks) >= 3, "Should have at least 3 agents for multi-agent team"
        
        # Verify proper coordination setup (coordinator connects to multiple agents)
        coordinator_edges = [e for e in state["edges"] if e["source"] == "coordinator-1"]
        assert len(coordinator_edges) >= 2, "Coordinator should connect to multiple agents"
        
        # Verify synthesis pattern (multiple agents connect to synthesizer)
        synthesizer_edges = [e for e in state["edges"] if e["target"] == "synthesizer-1"]
        assert len(synthesizer_edges) >= 2, "Multiple agents should connect to synthesizer"
    
    @pytest.mark.asyncio
    async def test_web3_automation_generation(self, mock_claude_client, mock_db_service):
        """Test Web3-specific workflow generation"""
        
        web3_workflow = {
            "id": "web3-defi-123",
            "name": "DeFi Yield Optimizer", 
            "description": "Multi-protocol DeFi yield farming"
        }
        
        web3_blocks = [
            {
                "id": "blockchain-monitor", "type": "starter", "name": "Blockchain Monitor",
                "sub_blocks": {"startWorkflow": {"value": "schedule"}}
            },
            {
                "id": "uniswap-api", "type": "api", "name": "Uniswap Data",
                "sub_blocks": {"url": {"value": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"}}
            },
            {
                "id": "defi-agent", "type": "agent", "name": "DeFi Strategy Agent",
                "sub_blocks": {
                    "model": {"value": "gpt-4"},
                    "systemPrompt": {"value": "DeFi yield optimization strategy"}
                }
            },
            {
                "id": "contract-execution", "type": "api", "name": "Smart Contract Execution",
                "sub_blocks": {"url": {"value": "https://mainnet.infura.io/v3/YOUR-PROJECT-ID"}}
            }
        ]
        
        mock_db_service.get_workflow.return_value = web3_workflow
        mock_db_service.get_workflow_blocks.return_value = web3_blocks
        mock_claude_client.generate_workflow_state.return_value = {
            "blocks": {block["id"]: block for block in web3_blocks},
            "edges": [
                {"source": "blockchain-monitor", "target": "uniswap-api"},
                {"source": "uniswap-api", "target": "defi-agent"},
                {"source": "defi-agent", "target": "contract-execution"}
            ],
            "variables": {
                "GAS_LIMIT": {"type": "number", "value": 200000},
                "SLIPPAGE_TOLERANCE": {"type": "number", "value": 0.5}
            },
            "metadata": {"version": "1.0.0"}
        }
        
        generator = AgentForgeStateGenerator()
        generator.claude = mock_claude_client
        generator.db = mock_db_service
        
        state = await generator.generate_workflow_state("web3-defi-123")
        
        # Verify Web3-specific elements
        assert "variables" in state
        web3_vars = state["variables"]
        assert any("gas" in str(var).lower() for var in web3_vars.keys()), "Should have gas-related variables"
        
        # Verify blockchain monitoring trigger
        starter_blocks = [b for b in state["blocks"].values() if b.get("type") == "starter"]
        assert len(starter_blocks) >= 1, "Should have blockchain monitoring trigger"
        
        # Verify smart contract integration
        api_blocks = [b for b in state["blocks"].values() if b.get("type") == "api"]
        contract_apis = [b for b in api_blocks if "contract" in b.get("name", "").lower() or 
                        "infura" in str(b.get("sub_blocks", {})).lower()]
        assert len(contract_apis) >= 1, "Should have smart contract API integration"
    
    @pytest.mark.asyncio
    async def test_fallback_generation_when_claude_fails(self, mock_claude_client, mock_db_service,
                                                       sample_workflow, sample_blocks):
        """Test fallback generation when Claude API fails"""
        
        # Setup mocks
        mock_db_service.get_workflow.return_value = sample_workflow
        mock_db_service.get_workflow_blocks.return_value = sample_blocks
        mock_claude_client.generate_workflow_state.return_value = None  # Simulate Claude failure
        
        generator = AgentForgeStateGenerator()
        generator.claude = mock_claude_client
        generator.db = mock_db_service
        
        # Generate state (should use fallback)
        state = await generator.generate_workflow_state("test-workflow-123")
        
        # Verify fallback state is valid
        assert "blocks" in state
        assert "edges" in state
        assert "metadata" in state
        assert state["metadata"]["version"] == "1.0.0"
        
        # Verify all original blocks are preserved
        assert len(state["blocks"]) == len(sample_blocks)
        for block in sample_blocks:
            assert block["id"] in state["blocks"]
    
    @pytest.mark.asyncio
    async def test_edge_inference_from_positions(self, mock_claude_client, mock_db_service):
        """Test automatic edge inference based on block positions"""
        
        # Create blocks in a clear left-to-right flow
        positioned_blocks = [
            {"id": "block-1", "type": "starter", "position_x": 100, "position_y": 200},
            {"id": "block-2", "type": "agent", "position_x": 300, "position_y": 200}, 
            {"id": "block-3", "type": "api", "position_x": 500, "position_y": 200},
            {"id": "block-4", "type": "output", "position_x": 700, "position_y": 200}
        ]
        
        mock_db_service.get_workflow.return_value = {"id": "test", "name": "Test"}
        mock_db_service.get_workflow_blocks.return_value = positioned_blocks
        mock_claude_client.generate_workflow_state.return_value = None  # Force fallback
        
        generator = AgentForgeStateGenerator()
        generator.claude = mock_claude_client
        generator.db = mock_db_service
        
        # Test edge inference
        edges = generator._infer_edges_from_positions(positioned_blocks)
        
        # Should create left-to-right flow
        assert len(edges) == 3  # 4 blocks = 3 edges
        assert edges[0]["source"] == "block-1" and edges[0]["target"] == "block-2"
        assert edges[1]["source"] == "block-2" and edges[1]["target"] == "block-3"
        assert edges[2]["source"] == "block-3" and edges[2]["target"] == "block-4"

class TestAgentForgePromptGeneration:
    """Test Agent Forge-specific prompt generation"""
    
    def test_create_agent_forge_prompt(self):
        """Test generation of Agent Forge-specific prompts for Claude"""
        generator = AgentForgeStateGenerator()
        
        workflow = {"id": "test", "name": "Trading Bot", "description": "Crypto trading"}
        blocks = [
            {"id": "1", "type": "starter", "name": "Start", "position_x": 100, "position_y": 200},
            {"id": "2", "type": "agent", "name": "Agent", "position_x": 300, "position_y": 200}
        ]
        edges = [{"source": "1", "target": "2"}]
        
        prompt = generator._create_agent_forge_prompt(workflow, blocks, edges)
        
        # Verify Agent Forge-specific elements in prompt
        assert "Agent Forge" in prompt
        assert "drag-and-drop" in prompt
        assert "24/7 autonomous operation" in prompt
        assert "multi-agent collaboration" in prompt
        assert "Web2 and Web3 services" in prompt
        assert "gpt-4, claude-3, gemini-pro" in prompt
        assert "starter: webhookPath, scheduleType" in prompt
        assert "agent: model, systemPrompt, temperature" in prompt
