"""
Agent Forge State Generator Service
AI-powered workflow state generation with fallback systems
"""
import os
import json
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import asyncio

logger = logging.getLogger(__name__)

class StateGenerator:
    """AI-powered workflow state generator for Agent Forge platform"""
    
    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.use_ai = bool(self.anthropic_api_key)
        
        if self.use_ai:
            try:
                import anthropic
                self.client = anthropic.AsyncAnthropic(api_key=self.anthropic_api_key)
                logger.info("✅ Claude AI integration enabled")
            except ImportError:
                logger.warning("❌ Anthropic library not installed, using fallback generation")
                self.use_ai = False
        else:
            logger.info("🔄 Using rule-based state generation (no AI key)")
    
    async def generate_workflow_state(self, workflow_id: str, workflow_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate complete workflow state for Agent Forge"""
        try:
            if self.use_ai:
                return await self._generate_ai_state(workflow_id, workflow_data)
            else:
                return await self._generate_fallback_state(workflow_id, workflow_data)
        except Exception as e:
            logger.error(f"State generation failed: {e}")
            return await self._generate_fallback_state(workflow_id, workflow_data)
    
    async def _generate_ai_state(self, workflow_id: str, workflow_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate state using Claude AI"""
        try:
            # Create prompt for Claude
            prompt = self._create_ai_prompt(workflow_id, workflow_data)
            
            response = await self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Parse AI response
            ai_response = response.content[0].text
            
            # Extract JSON from response
            try:
                # Find JSON in response
                start = ai_response.find('{')
                end = ai_response.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = ai_response[start:end]
                    generated_state = json.loads(json_str)
                else:
                    raise ValueError("No valid JSON found in AI response")
                    
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"Failed to parse AI response: {e}")
                return await self._generate_fallback_state(workflow_id, workflow_data)
            
            # Validate and enhance the generated state
            enhanced_state = self._enhance_generated_state(generated_state, workflow_id)
            
            logger.info(f"✅ AI-generated state for workflow {workflow_id}")
            return enhanced_state
            
        except Exception as e:
            logger.error(f"AI state generation failed: {e}")
            return await self._generate_fallback_state(workflow_id, workflow_data)
    
    def _create_ai_prompt(self, workflow_id: str, workflow_data: Optional[Dict] = None) -> str:
        """Create prompt for AI state generation"""
        base_prompt = f"""
Generate a complete Agent Forge workflow state for workflow ID: {workflow_id}

Create a realistic, functional workflow with the following structure:
- blocks: Dictionary of block IDs to block configurations
- edges: Array of connections between blocks
- subflows: Dictionary for nested workflows (can be empty)
- variables: Dictionary of workflow variables
- metadata: Version, timestamps, and other metadata

Block types available:
- starter: Entry points (webhook, schedule, manual)
- agent: AI agents with models and prompts
- api: External API integrations
- output: Results destinations (email, webhook, etc.)
- tool: Specialized tools

Each block should have:
- id: Unique identifier
- type: Block type
- name: Human-readable name
- position_x, position_y: Canvas coordinates
- sub_blocks: Configuration specific to block type

Make the workflow practical and realistic for Agent Forge platform.
"""
        
        if workflow_data:
            base_prompt += f"\nWorkflow context: {json.dumps(workflow_data, indent=2)}"
        
        base_prompt += "\n\nReturn ONLY valid JSON in this exact format:"
        
        example_state = {
            "blocks": {
                "starter_1": {
                    "id": "starter_1",
                    "type": "starter",
                    "name": "Workflow Trigger",
                    "position_x": 100,
                    "position_y": 100,
                    "sub_blocks": {
                        "startWorkflow": "webhook",
                        "webhookPath": "/start",
                        "scheduleType": "manual"
                    }
                },
                "agent_1": {
                    "id": "agent_1", 
                    "type": "agent",
                    "name": "Processing Agent",
                    "position_x": 300,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are a helpful assistant",
                        "temperature": 0.7
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "agent_1"}
            ],
            "subflows": {},
            "variables": {
                "API_KEY": "{{env.API_KEY}}",
                "WORKFLOW_NAME": "Generated Workflow"
            },
            "metadata": {
                "version": "1.0.0",
                "createdAt": "2024-01-04T10:00:00Z",
                "updatedAt": "2024-01-04T10:00:00Z"
            }
        }
        
        base_prompt += f"\n\n{json.dumps(example_state, indent=2)}"
        
        return base_prompt
    
    async def _generate_fallback_state(self, workflow_id: str, workflow_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate state using rule-based fallback"""
        
        # Determine workflow pattern
        pattern = await self.analyze_workflow_pattern(workflow_id, workflow_data)
        
        if pattern == "trading_bot":
            return self._create_trading_bot_state()
        elif pattern == "lead_generation":
            return self._create_lead_gen_state()
        elif pattern == "multi_agent":
            return self._create_multi_agent_state()
        elif pattern == "web3_automation":
            return self._create_web3_state()
        else:
            return self._create_basic_state()
    
    def _create_trading_bot_state(self) -> Dict[str, Any]:
        """Create trading bot workflow state"""
        return {
            "blocks": {
                "starter_1": {
                    "id": "starter_1",
                    "type": "starter", 
                    "name": "Market Monitor",
                    "position_x": 100,
                    "position_y": 100,
                    "sub_blocks": {
                        "startWorkflow": "schedule",
                        "scheduleType": "interval",
                        "interval": "1m"
                    }
                },
                "api_1": {
                    "id": "api_1",
                    "type": "api",
                    "name": "Fetch Market Data",
                    "position_x": 300,
                    "position_y": 100,
                    "sub_blocks": {
                        "url": "https://api.binance.com/api/v3/ticker/price",
                        "method": "GET",
                        "params": {"symbol": "BTCUSDT"}
                    }
                },
                "agent_1": {
                    "id": "agent_1",
                    "type": "agent",
                    "name": "Trading Decision Agent",
                    "position_x": 500,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "Analyze market data and make trading decisions based on technical indicators",
                        "temperature": 0.3
                    }
                },
                "api_2": {
                    "id": "api_2",
                    "type": "api", 
                    "name": "Execute Trade",
                    "position_x": 700,
                    "position_y": 100,
                    "sub_blocks": {
                        "url": "https://api.binance.com/api/v3/order",
                        "method": "POST",
                        "headers": {"X-MBX-APIKEY": "{{env.BINANCE_API_KEY}}"}
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "api_1"},
                {"from": "api_1", "to": "agent_1"},
                {"from": "agent_1", "to": "api_2"}
            ],
            "subflows": {},
            "variables": {
                "TRADING_PAIR": "BTC/USDT",
                "STOP_LOSS": -5,
                "TAKE_PROFIT": 10,
                "POSITION_SIZE": 0.01
            },
            "metadata": {
                "version": "1.0.0",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z",
                "pattern": "trading_bot"
            }
        }
    
    def _create_lead_gen_state(self) -> Dict[str, Any]:
        """Create lead generation workflow state"""
        return {
            "blocks": {
                "starter_1": {
                    "id": "starter_1",
                    "type": "starter",
                    "name": "Lead Capture",
                    "position_x": 100,
                    "position_y": 100,
                    "sub_blocks": {
                        "startWorkflow": "webhook",
                        "webhookPath": "/lead-capture",
                        "method": "POST"
                    }
                },
                "agent_1": {
                    "id": "agent_1",
                    "type": "agent",
                    "name": "Lead Qualifier",
                    "position_x": 300,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "Qualify leads based on company size, budget, and needs",
                        "temperature": 0.5
                    }
                },
                "api_1": {
                    "id": "api_1",
                    "type": "api",
                    "name": "Save to CRM",
                    "position_x": 500,
                    "position_y": 100,
                    "sub_blocks": {
                        "url": "https://api.hubspot.com/contacts/v1/contact",
                        "method": "POST",
                        "headers": {"Authorization": "Bearer {{env.HUBSPOT_TOKEN}}"}
                    }
                },
                "output_1": {
                    "id": "output_1",
                    "type": "output",
                    "name": "Notify Sales Team",
                    "position_x": 700,
                    "position_y": 100,
                    "sub_blocks": {
                        "outputType": "email",
                        "channels": ["sales@company.com"],
                        "template": "new_qualified_lead"
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "agent_1"},
                {"from": "agent_1", "to": "api_1"},
                {"from": "api_1", "to": "output_1"}
            ],
            "subflows": {},
            "variables": {
                "QUALIFICATION_SCORE_THRESHOLD": 7,
                "CRM_PIPELINE": "sales",
                "NOTIFICATION_EMAIL": "sales@company.com"
            },
            "metadata": {
                "version": "1.0.0",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z",
                "pattern": "lead_generation"
            }
        }
    
    def _create_multi_agent_state(self) -> Dict[str, Any]:
        """Create multi-agent research workflow state"""
        return {
            "blocks": {
                "starter_1": {
                    "id": "starter_1",
                    "type": "starter",
                    "name": "Research Request",
                    "position_x": 100,
                    "position_y": 200,
                    "sub_blocks": {
                        "startWorkflow": "manual",
                        "inputFields": ["research_topic", "depth_level"]
                    }
                },
                "agent_1": {
                    "id": "agent_1",
                    "type": "agent",
                    "name": "Research Coordinator",
                    "position_x": 300,
                    "position_y": 200,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "Break down research topics into subtasks for specialized agents",
                        "temperature": 0.6
                    }
                },
                "agent_2": {
                    "id": "agent_2",
                    "type": "agent",
                    "name": "Data Researcher",
                    "position_x": 500,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "claude-3-sonnet",
                        "systemPrompt": "Gather and analyze quantitative data and statistics",
                        "temperature": 0.4
                    }
                },
                "agent_3": {
                    "id": "agent_3",
                    "type": "agent",
                    "name": "Trend Analyst",
                    "position_x": 500,
                    "position_y": 300,
                    "sub_blocks": {
                        "model": "gemini-pro",
                        "systemPrompt": "Identify trends and patterns in the research domain",
                        "temperature": 0.5
                    }
                },
                "agent_4": {
                    "id": "agent_4",
                    "type": "agent",
                    "name": "Report Synthesizer",
                    "position_x": 700,
                    "position_y": 200,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "Synthesize research findings into comprehensive report",
                        "temperature": 0.3
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "agent_1"},
                {"from": "agent_1", "to": "agent_2"},
                {"from": "agent_1", "to": "agent_3"},
                {"from": "agent_2", "to": "agent_4"},
                {"from": "agent_3", "to": "agent_4"}
            ],
            "subflows": {},
            "variables": {
                "RESEARCH_DEPTH": "comprehensive",
                "OUTPUT_FORMAT": "markdown",
                "MAX_AGENTS": 4
            },
            "metadata": {
                "version": "1.0.0",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z",
                "pattern": "multi_agent_research"
            }
        }
    
    def _create_web3_state(self) -> Dict[str, Any]:
        """Create Web3 automation workflow state"""
        return {
            "blocks": {
                "starter_1": {
                    "id": "starter_1",
                    "type": "starter",
                    "name": "Blockchain Monitor",
                    "position_x": 100,
                    "position_y": 100,
                    "sub_blocks": {
                        "startWorkflow": "schedule",
                        "scheduleType": "interval",
                        "interval": "5m"
                    }
                },
                "api_1": {
                    "id": "api_1",
                    "type": "api",
                    "name": "Check Contract Events",
                    "position_x": 300,
                    "position_y": 100,
                    "sub_blocks": {
                        "url": "https://api.etherscan.io/api",
                        "method": "GET",
                        "params": {
                            "module": "logs",
                            "action": "getLogs",
                            "address": "{{env.CONTRACT_ADDRESS}}"
                        }
                    }
                },
                "agent_1": {
                    "id": "agent_1",
                    "type": "agent",
                    "name": "Event Analyzer",
                    "position_x": 500,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "Analyze blockchain events and determine if action is needed",
                        "temperature": 0.2
                    }
                },
                "tool_1": {
                    "id": "tool_1",
                    "type": "tool",
                    "name": "Web3 Transaction",
                    "position_x": 700,
                    "position_y": 100,
                    "sub_blocks": {
                        "toolType": "web3",
                        "network": "ethereum",
                        "gasLimit": 21000
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "api_1"},
                {"from": "api_1", "to": "agent_1"},
                {"from": "agent_1", "to": "tool_1"}
            ],
            "subflows": {},
            "variables": {
                "CONTRACT_ADDRESS": "0x...",
                "NETWORK": "ethereum",
                "GAS_PRICE": "20",
                "WALLET_ADDRESS": "{{env.WALLET_ADDRESS}}"
            },
            "metadata": {
                "version": "1.0.0",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z",
                "pattern": "web3_automation"
            }
        }
    
    def _create_basic_state(self) -> Dict[str, Any]:
        """Create basic workflow state"""
        return {
            "blocks": {
                "starter_1": {
                    "id": "starter_1",
                    "type": "starter",
                    "name": "Start Workflow",
                    "position_x": 100,
                    "position_y": 100,
                    "sub_blocks": {
                        "startWorkflow": "manual"
                    }
                },
                "agent_1": {
                    "id": "agent_1",
                    "type": "agent",
                    "name": "Processing Agent",
                    "position_x": 300,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "Process the input and provide helpful output",
                        "temperature": 0.7
                    }
                },
                "output_1": {
                    "id": "output_1",
                    "type": "output",
                    "name": "Result Output",
                    "position_x": 500,
                    "position_y": 100,
                    "sub_blocks": {
                        "outputType": "webhook",
                        "url": "{{env.WEBHOOK_URL}}"
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "agent_1"},
                {"from": "agent_1", "to": "output_1"}
            ],
            "subflows": {},
            "variables": {
                "WORKFLOW_NAME": "Basic Workflow"
            },
            "metadata": {
                "version": "1.0.0",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z",
                "pattern": "basic"
            }
        }
    
    def _enhance_generated_state(self, state: Dict[str, Any], workflow_id: str) -> Dict[str, Any]:
        """Enhance and validate generated state"""
        # Ensure required fields exist
        if "blocks" not in state:
            state["blocks"] = {}
        if "edges" not in state:
            state["edges"] = []
        if "subflows" not in state:
            state["subflows"] = {}
        if "variables" not in state:
            state["variables"] = {}
        if "metadata" not in state:
            state["metadata"] = {}
        
        # Add timestamps
        now = datetime.utcnow().isoformat() + "Z"
        state["metadata"].update({
            "version": state["metadata"].get("version", "1.0.0"),
            "createdAt": state["metadata"].get("createdAt", now),
            "updatedAt": now,
            "generatedBy": "claude-ai",
            "workflowId": workflow_id
        })
        
        # Ensure all blocks have required fields
        for block_id, block in state["blocks"].items():
            if "id" not in block:
                block["id"] = block_id
            if "position_x" not in block:
                block["position_x"] = 100
            if "position_y" not in block:
                block["position_y"] = 100
            if "sub_blocks" not in block:
                block["sub_blocks"] = {}
        
        return state
    
    async def analyze_workflow_pattern(self, workflow_id: str, workflow_data: Optional[Dict] = None) -> str:
        """Analyze workflow to determine its pattern/type"""
        if not workflow_data:
            # Analyze based on workflow_id or other available data
            workflow_id_lower = workflow_id.lower()
            
            if any(term in workflow_id_lower for term in ["trade", "trading", "bot", "crypto", "btc", "eth"]):
                return "trading_bot"
            elif any(term in workflow_id_lower for term in ["lead", "sales", "crm", "marketing"]):
                return "lead_generation"
            elif any(term in workflow_id_lower for term in ["research", "multi", "team", "agent"]):
                return "multi_agent"
            elif any(term in workflow_id_lower for term in ["web3", "blockchain", "defi", "smart"]):
                return "web3_automation"
            else:
                return "basic"
        
        # Analyze workflow data content
        content = str(workflow_data).lower()
        
        if any(term in content for term in ["trading", "market", "price", "crypto"]):
            return "trading_bot"
        elif any(term in content for term in ["lead", "sales", "qualification"]):
            return "lead_generation"
        elif any(term in content for term in ["research", "analysis", "multi-agent"]):
            return "multi_agent"
        elif any(term in content for term in ["web3", "blockchain", "contract"]):
            return "web3_automation"
        else:
            return "basic"

# Global instance
state_generator = StateGenerator() 