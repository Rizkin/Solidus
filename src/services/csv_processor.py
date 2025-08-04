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
        """Mock workflow rows data matching ACTUAL CSV structure"""
        return [
            {
                'id': '79e8076f-0ae0-4b6f-9d14-65364ddae6d2',
                'user_id': 'sEfcNW1TZedrJ8mDW81UFVtZpZXVd3Mf',
                'workspace_id': 'f639bbc2-cbda-49c3-9301-9c632c8e86e2',
                'folder_id': None,
                'name': 'default-agent',
                'description': 'Your first workflow - start building here!',
                'color': '#3972F6',
                'variables': {},
                'is_published': False,
                'created_at': datetime(2025, 7, 22, 7, 10, 51, 778000),
                'updated_at': datetime(2025, 7, 22, 7, 10, 51, 778000)
            },
            {
                'id': '81e98d1e-459d-4e1d-b9c3-e1e56f8155ab',
                'user_id': 'H2sjCYSjVkkhay0GpyXM53XmEWwDVgjc',
                'workspace_id': 'd8b61a6b-d682-4d70-8f39-1261eb4d880b',
                'folder_id': None,
                'name': 'workflow-test',
                'description': 'Your first workflow - start building here!',
                'color': '#3972F6',
                'variables': {},
                'is_published': False,
                'created_at': datetime(2025, 7, 21, 14, 25, 55, 945000),
                'updated_at': datetime(2025, 7, 22, 7, 38, 15, 676000)
            },
            {
                'id': 'af18372b-03e8-45fd-9be5-3ac559c88f57',
                'user_id': 'H2sjCYSjVkkhay0GpyXM53XmEWwDVgjc',
                'workspace_id': 'd8b61a6b-d682-4d70-8f39-1261eb4d880b',
                'folder_id': None,
                'name': 'arctic-constellation',
                'description': 'New workflow',
                'color': '#15803D',
                'variables': {},
                'is_published': False,
                'created_at': datetime(2025, 7, 21, 14, 26, 24, 553000),
                'updated_at': datetime(2025, 7, 21, 14, 26, 24, 553000)
            }
        ]
    
    def _get_mock_workflow_blocks_rows(self) -> List[Dict[str, Any]]:
        """Mock workflow blocks rows data matching ACTUAL CSV structure"""
        return [
            # Agent Block from workflow-test
            {
                'id': '135552e8-592e-4567-bf09-156b0a5e28f0',
                'workflow_id': '81e98d1e-459d-4e1d-b9c3-e1e56f8155ab',
                'type': 'agent',
                'name': 'Agent 1',
                'position_x': 556.9230769230769,
                'position_y': -119.80769230769232,
                'enabled': True,
                'horizontal_handles': True,
                'is_wide': False,
                'advanced_mode': False,
                'height': 0,
                'sub_blocks': {
                    "model": {"id": "model", "type": "combobox", "value": "gemini-2.5-pro"},
                    "tools": {"id": "tools", "type": "tool-input", "value": [{"type": "elevenlabs", "title": "ElevenLabs", "params": {"apiKey": "sk_539725a6d8b99b16a11467e7b1cb7d514233f90a58dc4823", "voiceId": "Xb7hH8MSUJpSbSDYk0k2"}, "isExpanded": True, "usageControl": "auto"}]},
                    "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "You are an assistant that transitions what the user says into text to speech using elevenlabs and sends them the URL to the output."},
                    "userPrompt": {"id": "userPrompt", "type": "long-input", "value": "<start>"},
                    "temperature": {"id": "temperature", "type": "slider", "value": None}
                },
                'outputs': {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"},
                'data': {},
                'parent_id': None,
                'extent': None
            },
            # API Block from workflow-test
            {
                'id': 'a091ef02-b50b-425f-b5cf-f3a936281c32',
                'workflow_id': '81e98d1e-459d-4e1d-b9c3-e1e56f8155ab',
                'type': 'api',
                'name': 'API 1',
                'position_x': 959.7926327015055,
                'position_y': 129.0738138570569,
                'enabled': True,
                'horizontal_handles': True,
                'is_wide': False,
                'advanced_mode': False,
                'height': 0,
                'sub_blocks': {
                    "url": {"id": "url", "type": "short-input", "value": "https://api.coingecko.com/api/v3/search/trending"},
                    "method": {"id": "method", "type": "dropdown", "value": "GET"},
                    "headers": {"id": "headers", "type": "table", "value": [{"id": "58f892db-c69b-49d0-a803-33e9ed4c25e1", "cells": {"Key": "Accept", "Value": "application/json"}}]}
                },
                'outputs': {"data": "any", "status": "number", "headers": "json"},
                'data': {},
                'parent_id': None,
                'extent': None
            },
            # Starter Block from default-agent
            {
                'id': 'cb7ebf84-9d43-45bf-a327-cca64d30d602',
                'workflow_id': '79e8076f-0ae0-4b6f-9d14-65364ddae6d2',
                'type': 'starter',
                'name': 'Start',
                'position_x': 100,
                'position_y': 100,
                'enabled': True,
                'horizontal_handles': True,
                'is_wide': False,
                'advanced_mode': False,
                'height': 95,
                'sub_blocks': {
                    "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"},
                    "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "daily"},
                    "webhookPath": {"id": "webhookPath", "type": "short-input", "value": ""}
                },
                'outputs': {"response": {"type": {"input": "any"}}},
                'data': {},
                'parent_id': None,
                'extent': None
            },
            # Starter Block from workflow-test
            {
                'id': 'f668ee62-8abb-49df-9b4e-b7d5e18f11df',
                'workflow_id': '81e98d1e-459d-4e1d-b9c3-e1e56f8155ab',
                'type': 'starter',
                'name': 'Start',
                'position_x': 100,
                'position_y': 100,
                'enabled': True,
                'horizontal_handles': True,
                'is_wide': False,
                'advanced_mode': False,
                'height': 95,
                'sub_blocks': {
                    "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"},
                    "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "daily"},
                    "webhookPath": {"id": "webhookPath", "type": "short-input", "value": "732a975e-4a63-4c5c-bee4-d8061444ae24"},
                    "webhookProvider": {"id": "webhookProvider", "type": "unknown", "value": "generic"}
                },
                'outputs': {"response": {"type": {"input": "any"}}},
                'data': {},
                'parent_id': None,
                'extent': None
            },
            # Starter Block from arctic-constellation
            {
                'id': '1814dd59-5ded-43ed-9b90-549861b8bbde',
                'workflow_id': 'af18372b-03e8-45fd-9be5-3ac559c88f57',
                'type': 'starter',
                'name': 'Start',
                'position_x': 100,
                'position_y': 100,
                'enabled': True,
                'horizontal_handles': True,
                'is_wide': False,
                'advanced_mode': False,
                'height': 95,
                'sub_blocks': {
                    "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"},
                    "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "daily"},
                    "timezone": {"id": "timezone", "type": "dropdown", "value": "UTC"}
                },
                'outputs': {"response": {"type": {"input": "any"}}},
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