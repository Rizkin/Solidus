"""
Agent Forge State Generator Service
AI-powered workflow state generation with intelligent caching and RAG
"""
import os
import json
import uuid
import logging
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
import asyncio

logger = logging.getLogger(__name__)

class StateGenerator:
    """AI-powered workflow state generator for Agent Forge platform with RAG"""
    
    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.use_ai = bool(self.anthropic_api_key)
        
        # Import here to avoid circular imports
        from src.utils.database_hybrid import db_service
        
        # Initialize enhanced lookup service with RAG capabilities
        from src.services.enhanced_lookup_service import EnhancedLookupService
        self.lookup_service = EnhancedLookupService(db_service, self.openai_api_key)
        
        self.db = db_service
        
        if self.use_ai:
            try:
                import anthropic
                self.client = anthropic.AsyncAnthropic(api_key=self.anthropic_api_key)
                logger.info("✅ Claude AI integration enabled with RAG caching")
            except ImportError:
                logger.warning("❌ Anthropic library not installed, using fallback generation")
                self.use_ai = False
        else:
            logger.info("🔄 Using rule-based state generation with RAG caching (no AI key)")
    
    async def generate_workflow_state(self, workflow_id: str, workflow_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate complete workflow state with intelligent RAG caching"""
        logger.info(f"🚀 Generating state for workflow: {workflow_id}")
        start_time = time.time()
        session_id = str(uuid.uuid4())
        
        try:
            # 1. Fetch workflow and blocks data
            if workflow_data:
                workflow = workflow_data
                blocks = workflow_data.get('blocks', [])
            else:
                workflow = await self.db.get_workflow(workflow_id)
                if not workflow:
                    raise ValueError(f"Workflow {workflow_id} not found")
                blocks = await self.db.get_workflow_blocks(workflow_id)
            
            logger.info(f"Found {len(blocks)} blocks for workflow")
            
            # 2. Prepare input data for caching system
            input_data = {
                'workflow_id': workflow_id,
                'workflow_type': self._determine_workflow_type(workflow, blocks),
                'name': workflow.get('name', ''),
                'description': workflow.get('description', ''),
                'blocks': blocks,
                'edges': self._infer_edges_from_positions(blocks),
                'variables': workflow.get('variables', {})
            }
            
            # 3. Create temp record for tracking
            temp_id = await self.lookup_service.create_temp_record(session_id, input_data)
            
            # 4. Check lookup table for similar workflows (hybrid search)
            logger.info("🔍 Checking cache for similar workflows (hybrid search)...")
            cached_result = await self.lookup_service.find_similar_workflows_hybrid(input_data)
            
            if cached_result:
                cached_state, similarity_score, match_type = cached_result
                logger.info(f"✅ Cache HIT! Using cached result with {similarity_score:.2%} similarity ({match_type} match)")
                
                # 5a. Adapt cached state for current requirements
                if similarity_score < 0.95:  # Not exact match
                    logger.info("🔧 Adapting cached state to current requirements...")
                    adapted_state = await self.lookup_service.adapt_cached_state(
                        cached_state,
                        input_data,
                        similarity_score
                    )
                    
                    # Optional: Use lighter AI model for fine-tuning
                    if self.use_ai and similarity_score < 0.85:
                        adapted_state = await self._ai_adapt_state(
                            adapted_state,
                            input_data,
                            similarity_score
                        )
                else:
                    adapted_state = cached_state
                    logger.info("🎯 Exact match found, using cached state as-is")
                
                # Update temp record
                await self.lookup_service.update_temp_record(
                    temp_id,
                    adapted_state,
                    similarity_score=similarity_score
                )
                
                generation_time = time.time() - start_time
                logger.info(f"⚡ State generated from cache in {generation_time:.2f}s (saved ~2-3s)")
                
                return adapted_state
            
            else:
                logger.info("❌ Cache MISS - No similar workflow found, generating new state")
                
                # 5b. Generate new state using AI or fallback
                if self.use_ai:
                    generated_state = await self._generate_ai_state(workflow_id, workflow_data)
                else:
                    generated_state = await self._generate_fallback_state(workflow_id, workflow_data)
                
                # 6. Enhance and validate the state
                final_state = self._enhance_generated_state(generated_state, workflow_id)
                
                # 7. Store in lookup table with embedding for future use
                generation_time = time.time() - start_time
                logger.info("💾 Storing new pattern in cache with embedding for future use...")
                await self.lookup_service.store_workflow_pattern_with_embedding(
                    input_data,
                    final_state,
                    generation_time
                )
                
                # Update temp record
                await self.lookup_service.update_temp_record(temp_id, final_state)
                
                logger.info(f"🆕 New state generated in {generation_time:.2f}s")
                
                return final_state
                
        except Exception as e:
            logger.error(f"Error in cached state generation: {e}")
            # Fallback to basic generation
            return await self._generate_fallback_state(workflow_id, workflow_data)
    
    def _determine_workflow_type(self, workflow: Dict[str, Any], blocks: List[Dict[str, Any]]) -> str:
        """Determine the type of workflow based on blocks and metadata"""
        name = workflow.get('name', '').lower()
        description = workflow.get('description', '').lower()
        block_types = [b.get('type') for b in blocks if b.get('type')]
        
        # Pattern matching
        combined_text = f"{name} {description}"
        
        if any(keyword in combined_text for keyword in ['trading', 'crypto', 'bot', 'exchange']):
            return 'trading_bot'
        elif any(keyword in combined_text for keyword in ['lead', 'marketing', 'crm', 'customer']):
            return 'lead_generation'
        elif block_types.count('agent') >= 3:
            return 'multi_agent'
        elif 'api' in block_types and 'agent' in block_types:
            return 'integration'
        elif any(keyword in combined_text for keyword in ['support', 'ticket', 'help']):
            return 'customer_support'
        elif any(keyword in combined_text for keyword in ['content', 'writing', 'publish']):
            return 'content_generation'
        elif any(keyword in combined_text for keyword in ['web3', 'defi', 'blockchain', 'smart contract']):
            return 'web3_automation'
        elif any(keyword in combined_text for keyword in ['data', 'etl', 'pipeline', 'transform']):
            return 'data_pipeline'
        elif any(keyword in combined_text for keyword in ['notification', 'alert', 'message']):
            return 'notification_system'
        else:
            return 'general'
    
    def _infer_edges_from_positions(self, blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Infer edges between blocks based on their positions and types"""
        edges = []
        
        if len(blocks) < 2:
            return edges
        
        # Sort blocks by position (left to right, top to bottom)
        sorted_blocks = sorted(blocks, key=lambda b: (b.get('position_y', 0), b.get('position_x', 0)))
        
        # Create simple sequential connections
        for i in range(len(sorted_blocks) - 1):
            current_block = sorted_blocks[i]
            next_block = sorted_blocks[i + 1]
            
            edges.append({
                'from': current_block.get('id'),
                'to': next_block.get('id'),
                'type': 'default'
            })
        
        return edges
    
    async def _ai_adapt_state(
        self,
        cached_state: Dict[str, Any],
        current_input: Dict[str, Any],
        similarity_score: float
    ) -> Dict[str, Any]:
        """Use lighter AI model to adapt cached state"""
        logger.info(f"🤖 Using AI to fine-tune cached state (similarity: {similarity_score:.2%})")
        
        try:
            adaptation_prompt = f"""
            Adapt this cached workflow state to match the current requirements.
            Similarity score: {similarity_score:.2%}
            Match type: semantic (RAG-based)
            
            Current requirements:
            - Workflow Name: {current_input.get('name', 'Unnamed')}
            - Workflow Type: {current_input.get('workflow_type')}
            - Block Count: {len(current_input.get('blocks', []))}
            - Block Types: {[b.get('type') for b in current_input.get('blocks', [])]}
            
            Cached state to adapt:
            {json.dumps(cached_state, indent=2)}
            
            Make minimal changes to adapt the cached state. Focus on:
            1. Updating block names/descriptions to match current context
            2. Adjusting variables if needed
            3. Preserving the overall structure
            4. Maintaining semantic meaning while adapting to new requirements
            
            Return only the adapted JSON state.
            """
            
            # Use a lighter model or shorter context for adaptation
            response = await self.client.messages.create(
                model="claude-3-haiku-20240307",  # Faster, cheaper model
                max_tokens=2000,  # Smaller response
                temperature=0.3,  # More deterministic
                messages=[{
                    "role": "user",
                    "content": adaptation_prompt
                }]
            )
            
            # Parse AI response
            ai_response = response.content[0].text
            
            # Extract JSON from response
            try:
                start = ai_response.find('{')
                end = ai_response.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = ai_response[start:end]
                    adapted_state = json.loads(json_str)
                    
                    # Add adaptation metadata
                    if 'metadata' not in adapted_state:
                        adapted_state['metadata'] = {}
                    adapted_state['metadata']['ai_adapted'] = True
                    adapted_state['metadata']['adaptation_method'] = 'rag_semantic'
                    
                    logger.info("✅ AI adaptation completed successfully")
                    return adapted_state
                else:
                    raise ValueError("No valid JSON found in AI response")
                    
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"Failed to parse AI adaptation: {e}")
                return cached_state  # Return original cached state
            
        except Exception as e:
            logger.error(f"AI adaptation failed: {e}")
            return cached_state  # Return original cached state
    
    async def _generate_ai_state(self, workflow_id: str, workflow_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate state using Claude AI (original method)"""
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
- starter: Workflow triggers (manual, schedule, webhook)
- agent: AI agents with specific roles
- api: External API integrations
- tool: Utility functions and transformations
- output: Data outputs and notifications

Generate a workflow that:
1. Has a logical flow from start to finish
2. Uses appropriate block types for the use case
3. Includes realistic configurations for each block
4. Has proper connections between blocks
5. Includes useful variables and metadata

Return only valid JSON.
"""
        
        if workflow_data:
            base_prompt += f"\n\nWorkflow context:\nName: {workflow_data.get('name', 'Unnamed')}\nDescription: {workflow_data.get('description', 'No description')}"
            base_prompt += f"\nBlocks: {len(workflow_data.get('blocks', []))} total"
            base_prompt += f"\nBlock types: {[b.get('type') for b in workflow_data.get('blocks', [])]}"
        
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
        """Analyze workflow pattern type"""
        try:
            if not workflow_data:
                workflow = await self.db.get_workflow(workflow_id)
                if not workflow:
                    return "unknown"
                blocks = await self.db.get_workflow_blocks(workflow_id)
            else:
                workflow = workflow_data
                blocks = workflow_data.get('blocks', [])
            
            return self._determine_workflow_type(workflow, blocks)
        except Exception as e:
            logger.error(f"Error analyzing workflow pattern: {e}")
            return "unknown"

# Global instance
state_generator = StateGenerator() 