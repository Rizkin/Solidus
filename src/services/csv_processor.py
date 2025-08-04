"""
CSV Processor Service
Processes workflow_rows and workflow_blocks_rows data into proper Supabase tables
"""
import json
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from src.utils.database_hybrid import db_service

logger = logging.getLogger(__name__)

class CSVProcessor:
    """Process CSV data into proper workflow state format"""
    
    def __init__(self):
        self.db = db_service
    
    async def process_workflows_from_csv(self) -> List[Dict[str, Any]]:
        """
        Main processing function:
        1. Read from workflow_rows and workflow_blocks_rows
        2. Generate proper state JSON
        3. Store in public.workflow and public.workflow_blocks
        """
        try:
            # Get raw data from CSV tables
            workflow_rows = await self._get_workflow_rows()
            workflow_blocks_rows = await self._get_workflow_blocks_rows()
            
            processed_workflows = []
            
            for workflow_row in workflow_rows:
                # Get blocks for this workflow
                workflow_blocks = [
                    block for block in workflow_blocks_rows 
                    if block['workflow_id'] == workflow_row['id']
                ]
                
                # Generate state JSON from blocks
                state_json = self._generate_state_json(workflow_row, workflow_blocks)
                
                # Create final workflow data
                workflow_data = self._create_workflow_data(workflow_row, state_json)
                
                # Store in proper Supabase tables
                stored_workflow = await self._store_workflow(workflow_data, workflow_blocks)
                
                if stored_workflow:
                    processed_workflows.append(stored_workflow)
                    logger.info(f"✅ Processed workflow: {workflow_row['name']}")
                else:
                    logger.error(f"❌ Failed to store workflow: {workflow_row['name']}")
            
            return processed_workflows
            
        except Exception as e:
            logger.error(f"Error processing workflows from CSV: {e}")
            return []
    
    async def _get_workflow_rows(self) -> List[Dict[str, Any]]:
        """Get data from workflow_rows table (CSV source)"""
        if self.db.use_database:
            try:
                response = self.db.client.table("workflow_rows").select("*").execute()
                return response.data or []
            except Exception as e:
                logger.error(f"Database error reading workflow_rows: {e}")
                return self._get_mock_workflow_rows()
        else:
            return self._get_mock_workflow_rows()
    
    async def _get_workflow_blocks_rows(self) -> List[Dict[str, Any]]:
        """Get data from workflow_blocks_rows table (CSV source)"""
        if self.db.use_database:
            try:
                response = self.db.client.table("workflow_blocks_rows").select("*").execute()
                return response.data or []
            except Exception as e:
                logger.error(f"Database error reading workflow_blocks_rows: {e}")
                return self._get_mock_workflow_blocks_rows()
        else:
            return self._get_mock_workflow_blocks_rows()
    
    def _get_mock_workflow_rows(self) -> List[Dict[str, Any]]:
        """Mock workflow rows data for development"""
        return [
            {
                'id': 'wf_001',
                'user_id': 'user_123',
                'workspace_id': 'ws_456',
                'folder_id': None,
                'name': 'Trading Bot Workflow',
                'description': 'Automated cryptocurrency trading with risk management',
                'color': '#FF6B6B',
                'variables': {'TRADING_PAIR': 'BTC/USD', 'STOP_LOSS': -5, 'TAKE_PROFIT': 10},
                'is_published': False,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'id': 'wf_002',
                'user_id': 'user_123',
                'workspace_id': 'ws_456',
                'folder_id': None,
                'name': 'Lead Generation System',
                'description': 'Automated lead capture and qualification pipeline',
                'color': '#4ECDC4',
                'variables': {'LEAD_SOURCE': 'website', 'QUALIFICATION_THRESHOLD': 7},
                'is_published': False,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'id': 'wf_003',
                'user_id': 'user_789',
                'workspace_id': 'ws_789',
                'folder_id': None,
                'name': 'Multi-Agent Research Team',
                'description': 'Collaborative AI agents for comprehensive research tasks',
                'color': '#9B59B6',
                'variables': {'RESEARCH_TOPIC': 'Market Analysis', 'AGENT_COUNT': 4},
                'is_published': True,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
        ]
    
    def _get_mock_workflow_blocks_rows(self) -> List[Dict[str, Any]]:
        """Mock workflow blocks rows data for development"""
        return [
            # Trading Bot Workflow Blocks
            {
                'id': 'block_001',
                'workflow_id': 'wf_001',
                'type': 'starter',
                'name': 'Market Monitor',
                'position_x': 100,
                'position_y': 100,
                'enabled': True,
                'horizontal_handles': True,
                'is_wide': False,
                'advanced_mode': False,
                'height': 80,
                'sub_blocks': {'startWorkflow': 'schedule', 'scheduleType': 'interval', 'interval': '1m'},
                'outputs': {'success': 'block_002'},
                'data': {},
                'parent_id': None,
                'extent': None
            },
            {
                'id': 'block_002',
                'workflow_id': 'wf_001',
                'type': 'api',
                'name': 'Fetch Price Data',
                'position_x': 300,
                'position_y': 100,
                'enabled': True,
                'horizontal_handles': True,
                'is_wide': False,
                'advanced_mode': False,
                'height': 80,
                'sub_blocks': {
                    'url': 'https://api.binance.com/api/v3/ticker/price',
                    'method': 'GET',
                    'params': {'symbol': 'BTCUSDT'}
                },
                'outputs': {'success': 'block_003', 'error': 'block_006'},
                'data': {},
                'parent_id': None,
                'extent': None
            },
            {
                'id': 'block_003',
                'workflow_id': 'wf_001',
                'type': 'agent',
                'name': 'Trading Decision Agent',
                'position_x': 500,
                'position_y': 100,
                'enabled': True,
                'horizontal_handles': True,
                'is_wide': False,
                'advanced_mode': True,
                'height': 120,
                'sub_blocks': {
                    'model': 'gpt-4',
                    'systemPrompt': 'Analyze market data and make trading decisions based on technical indicators',
                    'temperature': 0.3
                },
                'outputs': {'buy': 'block_004', 'sell': 'block_005', 'hold': 'block_001'},
                'data': {},
                'parent_id': None,
                'extent': None
            },
            # Lead Generation Workflow Blocks
            {
                'id': 'block_101',
                'workflow_id': 'wf_002',
                'type': 'starter',
                'name': 'Lead Capture',
                'position_x': 100,
                'position_y': 100,
                'enabled': True,
                'horizontal_handles': True,
                'is_wide': False,
                'advanced_mode': False,
                'height': 80,
                'sub_blocks': {
                    'startWorkflow': 'webhook',
                    'webhookPath': '/lead-capture',
                    'method': 'POST'
                },
                'outputs': {'success': 'block_102'},
                'data': {},
                'parent_id': None,
                'extent': None
            },
            {
                'id': 'block_102',
                'workflow_id': 'wf_002',
                'type': 'agent',
                'name': 'Lead Qualifier Agent',
                'position_x': 300,
                'position_y': 100,
                'enabled': True,
                'horizontal_handles': True,
                'is_wide': False,
                'advanced_mode': True,
                'height': 120,
                'sub_blocks': {
                    'model': 'gpt-4',
                    'systemPrompt': 'Qualify leads based on company size, budget, and needs. Score from 1-10.',
                    'temperature': 0.5
                },
                'outputs': {'qualified': 'block_103', 'unqualified': 'block_105'},
                'data': {},
                'parent_id': None,
                'extent': None
            }
        ]
    
    def _generate_state_json(self, workflow_row: Dict[str, Any], workflow_blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate the state JSON object from workflow and blocks data"""
        
        # Create blocks dictionary
        blocks = {}
        edges = []
        
        for block in workflow_blocks:
            # Add block to blocks dictionary
            blocks[block['id']] = {
                'id': block['id'],
                'type': block['type'],
                'name': block['name'],
                'position_x': float(block['position_x']),
                'position_y': float(block['position_y']),
                'sub_blocks': block.get('sub_blocks', {}),
                'enabled': block.get('enabled', True),
                'horizontal_handles': block.get('horizontal_handles', True),
                'is_wide': block.get('is_wide', False),
                'advanced_mode': block.get('advanced_mode', False),
                'height': float(block.get('height', 80))
            }
            
            # Generate edges from outputs
            outputs = block.get('outputs', {})
            if isinstance(outputs, dict):
                for output_type, target_block in outputs.items():
                    if target_block and target_block != block['id']:  # Avoid self-loops
                        edges.append({
                            'from': block['id'],
                            'to': target_block,
                            'type': output_type
                        })
        
        # Create the complete state object
        state = {
            'blocks': blocks,
            'edges': edges,
            'subflows': {},
            'variables': workflow_row.get('variables', {}),
            'metadata': {
                'version': '1.0.0',
                'createdAt': datetime.utcnow().isoformat() + 'Z',
                'updatedAt': datetime.utcnow().isoformat() + 'Z',
                'processedFrom': 'csv_data',
                'blockCount': len(blocks),
                'edgeCount': len(edges)
            }
        }
        
        return state
    
    def _create_workflow_data(self, workflow_row: Dict[str, Any], state_json: Dict[str, Any]) -> Dict[str, Any]:
        """Create the final workflow data for storage in public.workflow table"""
        now = datetime.utcnow()
        
        return {
            'id': workflow_row['id'],
            'user_id': workflow_row['user_id'],
            'workspace_id': workflow_row.get('workspace_id'),
            'folder_id': workflow_row.get('folder_id'),
            'name': workflow_row['name'],
            'description': workflow_row.get('description'),
            'state': state_json,
            'color': workflow_row.get('color', '#3972F6'),
            'last_synced': now,
            'created_at': workflow_row.get('created_at', now),
            'updated_at': now,
            'is_deployed': False,
            'deployed_state': None,
            'deployed_at': None,
            'collaborators': [],
            'run_count': 0,
            'last_run_at': None,
            'variables': workflow_row.get('variables', {}),
            'is_published': workflow_row.get('is_published', False),
            'marketplace_data': None
        }
    
    async def _store_workflow(self, workflow_data: Dict[str, Any], workflow_blocks: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Store workflow and blocks in proper Supabase tables"""
        try:
            # Store workflow in public.workflow table
            if self.db.use_database:
                # Prepare workflow data for database
                db_workflow_data = workflow_data.copy()
                db_workflow_data['state'] = json.dumps(workflow_data['state'])
                db_workflow_data['variables'] = json.dumps(workflow_data['variables'])
                db_workflow_data['collaborators'] = json.dumps(workflow_data['collaborators'])
                
                # Convert datetime objects to ISO strings
                for field in ['last_synced', 'created_at', 'updated_at']:
                    if isinstance(db_workflow_data[field], datetime):
                        db_workflow_data[field] = db_workflow_data[field].isoformat()
                
                # Insert workflow
                workflow_response = self.db.client.table("workflow").upsert(db_workflow_data).execute()
                
                # Prepare and insert blocks
                db_blocks = []
                for block in workflow_blocks:
                    db_block = {
                        'id': block['id'],
                        'workflow_id': block['workflow_id'],
                        'type': block['type'],
                        'name': block['name'],
                        'position_x': float(block['position_x']),
                        'position_y': float(block['position_y']),
                        'enabled': block.get('enabled', True),
                        'horizontal_handles': block.get('horizontal_handles', True),
                        'is_wide': block.get('is_wide', False),
                        'advanced_mode': block.get('advanced_mode', False),
                        'height': float(block.get('height', 80)),
                        'sub_blocks': json.dumps(block.get('sub_blocks', {})),
                        'outputs': json.dumps(block.get('outputs', {})),
                        'data': json.dumps(block.get('data', {})),
                        'parent_id': block.get('parent_id'),
                        'extent': block.get('extent'),
                        'created_at': datetime.utcnow().isoformat(),
                        'updated_at': datetime.utcnow().isoformat()
                    }
                    db_blocks.append(db_block)
                
                if db_blocks:
                    blocks_response = self.db.client.table("workflow_blocks").upsert(db_blocks).execute()
                
                logger.info(f"✅ Stored workflow {workflow_data['id']} with {len(db_blocks)} blocks in database")
                return workflow_data
                
            else:
                # Store in mock data for development
                self.db.mock_workflows[workflow_data['id']] = workflow_data
                self.db.mock_blocks[workflow_data['id']] = workflow_blocks
                logger.info(f"✅ Stored workflow {workflow_data['id']} in mock data")
                return workflow_data
                
        except Exception as e:
            logger.error(f"Error storing workflow {workflow_data['id']}: {e}")
            return None
    
    async def get_processing_status(self) -> Dict[str, Any]:
        """Get status of CSV processing"""
        try:
            workflow_rows = await self._get_workflow_rows()
            workflow_blocks_rows = await self._get_workflow_blocks_rows()
            
            # Count processed workflows
            processed_count = 0
            if self.db.use_database:
                try:
                    response = self.db.client.table("workflow").select("id", count="exact").execute()
                    processed_count = response.count or 0
                except:
                    processed_count = len(self.db.mock_workflows)
            else:
                processed_count = len(self.db.mock_workflows)
            
            return {
                'csv_workflow_rows': len(workflow_rows),
                'csv_workflow_blocks_rows': len(workflow_blocks_rows),
                'processed_workflows': processed_count,
                'database_type': 'supabase' if self.db.use_database else 'mock',
                'processing_available': True
            }
            
        except Exception as e:
            logger.error(f"Error getting processing status: {e}")
            return {
                'error': str(e),
                'processing_available': False
            }

# Global instance
csv_processor = CSVProcessor() 