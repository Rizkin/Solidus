# src/services/state_generator.py
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import json
import logging
from src.integrations.claude_client import claude_client
from src.utils.database_hybrid import db_service
from src.models.schemas import WorkflowState, Position

logger = logging.getLogger(__name__)

class AgentForgeStateGenerator:
    """Generate Agent Forge-compatible workflow states using AI"""
    
    def __init__(self):
        self.claude = claude_client
        self.db = db_service
        
    async def generate_workflow_state(self, workflow_id: str) -> Dict[str, Any]:
        """Main method to generate workflow state"""
        logger.info(f"Generating state for workflow: {workflow_id}")
        
        # 1. Fetch workflow and blocks data
        workflow = await self.db.get_workflow(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        blocks = await self.db.get_workflow_blocks(workflow_id)
        logger.info(f"Found {len(blocks)} blocks for workflow")
        
        # 2. Analyze block relationships based on positions
        edges = self._infer_edges_from_positions(blocks)
        
        # 3. Create enhanced prompt for Claude
        prompt = self._create_agent_forge_prompt(workflow, blocks, edges)
        
        # 4. Generate state using Claude
        generated_state = await self.claude.generate_workflow_state(prompt)
        
        if not generated_state:
            # Fallback to rule-based generation
            logger.warning("Claude generation failed, using fallback")
            generated_state = self._generate_fallback_state(workflow, blocks, edges)
        
        # 5. Enhance and validate the state
        final_state = self._enhance_state(generated_state, blocks)
        
        return final_state
    
    def _infer_edges_from_positions(self, blocks: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Infer edges based on block positions (left-to-right flow)"""
        edges = []
        
        # Sort blocks by x position
        sorted_blocks = sorted(blocks, key=lambda b: float(b['position_x']))
        
        # Group blocks by approximate y position (same row)
        rows = {}
        for block in sorted_blocks:
            y = float(block['position_y'])
            # Group blocks within 50 pixels of each other
            row_key = round(y / 50) * 50
            
            if row_key not in rows:
                rows[row_key] = []
            rows[row_key].append(block)
        
        # Create edges within each row
        for row_blocks in rows.values():
            for i in range(len(row_blocks) - 1):
                source = row_blocks[i]['id']
                target = row_blocks[i + 1]['id']
                edges.append({
                    "source": source,
                    "target": target,
                    "sourceHandle": "output",
                    "targetHandle": "input"
                })
        
        logger.info(f"Inferred {len(edges)} edges from positions")
        return edges
    
    def _create_agent_forge_prompt(self, workflow: Dict[str, Any], 
                                  blocks: List[Dict[str, Any]], 
                                  edges: List[Dict[str, str]]) -> str:
        """Create a detailed prompt for Claude"""
        
        # Format blocks for the prompt
        blocks_info = []
        for block in blocks:
            block_info = f"""
            Block ID: {block['id']}
            Type: {block['type']}
            Name: {block['name']}
            Position: ({block['position_x']}, {block['position_y']})
            Sub-blocks: {json.dumps(block.get('sub_blocks', {}), indent=2)}
            Outputs: {json.dumps(block.get('outputs', {}), indent=2)}
            """
            blocks_info.append(block_info)
        
        prompt = f"""
        Generate an Agent Forge workflow state for the following workflow:
        
        WORKFLOW INFORMATION:
        - ID: {workflow['id']}
        - Name: {workflow['name']}
        - Description: {workflow.get('description', 'No description')}
        
        BLOCKS INFORMATION:
        {chr(10).join(blocks_info)}
        
        INFERRED EDGES:
        {json.dumps(edges, indent=2)}
        
        REQUIREMENTS:
        1. Generate a complete Agent Forge state structure with:
           - blocks: Dictionary of all blocks with proper formatting
           - edges: Array of connections between blocks
           - subflows: Empty object {{}}
           - variables: Any workflow variables needed
           - metadata: Version "1.0.0" and timestamps
        
        2. For each block, ensure:
           - Proper position format: {{"x": number, "y": number}}
           - subBlocks match the block type:
             * starter: webhookPath, scheduleType, startWorkflow, etc.
             * agent: model, systemPrompt, temperature, tools
             * api: url, method, headers, params
             * output: outputType, channels, configuration
           - All boolean fields (enabled, horizontalHandles, isWide)
           - Proper height values (95 for most, 120 for agent blocks)
        
        3. Block-specific rules:
           - Starter blocks must have startWorkflow configuration
           - Agent blocks need valid AI model (gpt-4, claude-3, gemini-pro)
           - API blocks require URL and method
           - Output blocks need channel configuration
        
        4. Edge rules:
           - Each edge needs source, target, sourceHandle, targetHandle
           - Edges should follow logical flow (left to right based on positions)
           - No orphaned blocks (except starters)
        
        5. This is for Agent Forge - a no-code platform for building AI agents that:
           - Supports 24/7 autonomous operation
           - Enables multi-agent collaboration
           - Integrates with Web2 and Web3 services
           - Uses drag-and-drop interface
        
        IMPORTANT: Return ONLY valid JSON. No explanations, no markdown, just the state object.
        
        Generate the complete state JSON:
        """
        
        return prompt
    
    def _generate_fallback_state(self, workflow: Dict[str, Any], 
                                blocks: List[Dict[str, Any]], 
                                edges: List[Dict[str, str]]) -> Dict[str, Any]:
        """Fallback state generation if Claude fails"""
        logger.info("Using fallback state generation")
        
        state = {
            "blocks": {},
            "edges": edges,
            "subflows": {},
            "variables": {},
            "metadata": {
                "version": "1.0.0",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        # Process each block
        for block in blocks:
            block_state = {
                "id": block['id'],
                "type": block['type'],
                "name": block['name'],
                "position": {
                    "x": float(block['position_x']),
                    "y": float(block['position_y'])
                },
                "subBlocks": block.get('sub_blocks', {}),
                "outputs": block.get('outputs', {}),
                "enabled": block.get('enabled', True),
                "horizontalHandles": block.get('horizontal_handles', True),
                "isWide": block.get('is_wide', False),
                "height": float(block.get('height', 95))
            }
            
            # Enhance subBlocks based on type
            if block['type'] == 'starter' and not block_state['subBlocks']:
                block_state['subBlocks'] = {
                    "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"},
                    "webhookPath": {"id": "webhookPath", "type": "short-input", "value": ""},
                    "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "daily"}
                }
            elif block['type'] == 'agent' and not block_state['subBlocks']:
                block_state['subBlocks'] = {
                    "model": {"id": "model", "type": "combobox", "value": "gpt-4"},
                    "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                                   "value": "You are a helpful AI assistant."},
                    "temperature": {"id": "temperature", "type": "slider", "value": 0.7}
                }
            
            state["blocks"][block['id']] = block_state
        
        return state
    
    def _enhance_state(self, state: Dict[str, Any], blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Enhance and fix the generated state"""
        # Ensure all required fields are present
        if "metadata" not in state:
            state["metadata"] = {
                "version": "1.0.0",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z"
            }
        
        # Ensure all blocks from database are in the state
        state_block_ids = set(state.get("blocks", {}).keys())
        db_block_ids = set(block['id'] for block in blocks)
        
        # Add any missing blocks
        for block in blocks:
            if block['id'] not in state_block_ids:
                logger.warning(f"Adding missing block {block['id']} to state")
                # Add block using fallback logic
                fallback = self._generate_fallback_state(None, [block], [])
                state["blocks"][block['id']] = fallback["blocks"][block['id']]
        
        # Ensure edges array exists
        if "edges" not in state:
            state["edges"] = []
        
        # Ensure other required fields
        if "subflows" not in state:
            state["subflows"] = {}
        if "variables" not in state:
            state["variables"] = {}
        
        return state
    
    async def analyze_workflow_pattern(self, workflow_id: str) -> str:
        """Identify the Agent Forge pattern of a workflow"""
        workflow = await self.db.get_workflow(workflow_id)
        blocks = await self.db.get_workflow_blocks(workflow_id)
        
        workflow_data = {
            "name": workflow['name'],
            "blocks": [{"type": b['type'], "name": b['name']} for b in blocks]
        }
        
        pattern = await self.claude.analyze_workflow_pattern(workflow_data)
        return pattern

# Create singleton instance
state_generator = AgentForgeStateGenerator()
