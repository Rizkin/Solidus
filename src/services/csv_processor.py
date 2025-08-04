"""
CSV Processor Service - One-Time Migration
Processes workflow_rows and workflow_blocks_rows (CSV INPUT) into proper Supabase tables (OUTPUT)
WITH DUPLICATE PREVENTION
"""
import json
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Set
from src.utils.database_hybrid import db_service

logger = logging.getLogger(__name__)

class CSVProcessor:
    """One-time CSV migration processor with duplicate prevention"""
    
    def __init__(self):
        self.db = db_service
        self.processed_workflow_ids: Set[str] = set()
        self.processed_block_ids: Set[str] = set()
    
    async def process_workflows_from_csv(self, force_reprocess: bool = False) -> List[Dict[str, Any]]:
        """
        ONE-TIME MIGRATION: Process CSV input → Supabase output tables
        
        Args:
            force_reprocess: If True, will reprocess even if already exists (for testing)
        
        Returns:
            List of successfully processed workflows
        """
        try:
            logger.info("🚀 Starting ONE-TIME CSV migration process...")
            
            # Check if migration already completed
            if not force_reprocess and await self._is_migration_completed():
                return {
                    "message": "CSV migration already completed",
                    "status": "already_processed",
                    "suggestion": "Use force_reprocess=true to rerun migration",
                    "existing_workflows": await self._get_existing_workflow_count()
                }
            
            # Get CSV input data
            workflow_rows = await self._get_workflow_rows()
            workflow_blocks_rows = await self._get_workflow_blocks_rows()
            
            if not workflow_rows:
                return {
                    "message": "No CSV input data found",
                    "status": "no_input_data",
                    "suggestion": "Ensure workflow_rows table contains data"
                }
            
            # Load existing data to prevent duplicates
            await self._load_existing_ids()
            
            processed_workflows = []
            skipped_workflows = []
            
            for workflow_row in workflow_rows:
                workflow_id = workflow_row['id']
                
                # Skip if already processed (duplicate prevention)
                if workflow_id in self.processed_workflow_ids and not force_reprocess:
                    skipped_workflows.append({
                        "id": workflow_id,
                        "name": workflow_row['name'],
                        "reason": "already_exists"
                    })
                    logger.info(f"⏭️  Skipping duplicate workflow: {workflow_row['name']}")
                    continue
                
                # Get blocks for this workflow
                workflow_blocks = [
                    block for block in workflow_blocks_rows 
                    if block['workflow_id'] == workflow_id
                ]
                
                # Generate state JSON from blocks
                state_json = self._generate_state_json(workflow_row, workflow_blocks)
                
                # Create final workflow data
                workflow_data = self._create_workflow_data(workflow_row, state_json)
                
                # Store in output tables with duplicate prevention
                stored_workflow = await self._store_workflow_with_duplicate_check(
                    workflow_data, workflow_blocks, force_reprocess
                )
                
                if stored_workflow:
                    processed_workflows.append(stored_workflow)
                    self.processed_workflow_ids.add(workflow_id)
                    logger.info(f"✅ Migrated workflow: {workflow_row['name']}")
                else:
                    logger.error(f"❌ Failed to migrate workflow: {workflow_row['name']}")
            
            # Create migration summary
            migration_result = {
                "message": f"CSV migration completed",
                "status": "success",
                "processed_count": len(processed_workflows),
                "skipped_count": len(skipped_workflows),
                "total_input_workflows": len(workflow_rows),
                "processed_workflows": [
                    {
                        "id": w["id"],
                        "name": w["name"],
                        "description": w.get("description"),
                        "block_count": len(w["state"]["blocks"]),
                        "edge_count": len(w["state"]["edges"])
                    }
                    for w in processed_workflows
                ],
                "skipped_workflows": skipped_workflows,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "migration_type": "one_time_csv_to_supabase"
            }
            
            # Mark migration as completed
            await self._mark_migration_completed(migration_result)
            
            return migration_result
            
        except Exception as e:
            logger.error(f"Error in CSV migration process: {e}")
            return {
                "message": "CSV migration failed",
                "status": "error",
                "error": str(e),
                "processed_count": len(getattr(self, 'processed_workflows', [])),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
    
    async def _is_migration_completed(self) -> bool:
        """Check if CSV migration was already completed"""
        try:
            if self.db.use_database:
                # Check for migration marker in database
                response = self.db.client.table("workflow").select("id", count="exact").execute()
                existing_count = response.count or 0
                
                # If we have workflows in output table, migration likely completed
                if existing_count > 0:
                    logger.info(f"Found {existing_count} existing workflows in output table")
                    return True
                    
            else:
                # Check mock data
                if len(self.db.mock_workflows) > 0:
                    logger.info(f"Found {len(self.db.mock_workflows)} existing workflows in mock data")
                    return True
                    
            return False
            
        except Exception as e:
            logger.warning(f"Could not check migration status: {e}")
            return False
    
    async def _load_existing_ids(self) -> None:
        """Load existing workflow and block IDs to prevent duplicates"""
        try:
            if self.db.use_database:
                # Load existing workflow IDs
                workflow_response = self.db.client.table("workflow").select("id").execute()
                self.processed_workflow_ids = {w["id"] for w in (workflow_response.data or [])}
                
                # Load existing block IDs  
                blocks_response = self.db.client.table("workflow_blocks").select("id").execute()
                self.processed_block_ids = {b["id"] for b in (blocks_response.data or [])}
                
            else:
                # Load from mock data
                self.processed_workflow_ids = set(self.db.mock_workflows.keys())
                self.processed_block_ids = set()
                for blocks in self.db.mock_blocks.values():
                    self.processed_block_ids.update(block["id"] for block in blocks)
            
            logger.info(f"Loaded {len(self.processed_workflow_ids)} existing workflows, {len(self.processed_block_ids)} existing blocks")
            
        except Exception as e:
            logger.warning(f"Could not load existing IDs: {e}")
            self.processed_workflow_ids = set()
            self.processed_block_ids = set()
    
    async def _get_existing_workflow_count(self) -> int:
        """Get count of existing workflows in output table"""
        try:
            if self.db.use_database:
                response = self.db.client.table("workflow").select("id", count="exact").execute()
                return response.count or 0
            else:
                return len(self.db.mock_workflows)
        except:
            return 0
    
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
    
    async def _store_workflow_with_duplicate_check(
        self, 
        workflow_data: Dict[str, Any], 
        workflow_blocks: List[Dict[str, Any]], 
        force_reprocess: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Store workflow and blocks with duplicate prevention"""
        try:
            workflow_id = workflow_data['id']
            
            # Store workflow in output table
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
                
                # Use upsert for duplicate handling or insert for strict duplicate prevention
                if force_reprocess:
                    workflow_response = self.db.client.table("workflow").upsert(db_workflow_data).execute()
                else:
                    # Check if exists first
                    existing = self.db.client.table("workflow").select("id").eq("id", workflow_id).execute()
                    if existing.data:
                        logger.warning(f"Workflow {workflow_id} already exists, skipping")
                        return None
                    workflow_response = self.db.client.table("workflow").insert(db_workflow_data).execute()
                
                # Prepare and store blocks with duplicate prevention
                new_blocks = []
                for block in workflow_blocks:
                    block_id = block['id']
                    
                    # Skip if block already exists
                    if block_id in self.processed_block_ids and not force_reprocess:
                        logger.info(f"Block {block_id} already exists, skipping")
                        continue
                    
                    db_block = {
                        'id': block_id,
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
                    new_blocks.append(db_block)
                    self.processed_block_ids.add(block_id)
                
                if new_blocks:
                    if force_reprocess:
                        blocks_response = self.db.client.table("workflow_blocks").upsert(new_blocks).execute()
                    else:
                        blocks_response = self.db.client.table("workflow_blocks").insert(new_blocks).execute()
                
                logger.info(f"✅ Migrated workflow {workflow_id} with {len(new_blocks)} new blocks to OUTPUT tables")
                return workflow_data
                
            else:
                # Store in mock data with duplicate prevention
                if workflow_id not in self.db.mock_workflows or force_reprocess:
                    self.db.mock_workflows[workflow_id] = workflow_data
                    self.db.mock_blocks[workflow_id] = workflow_blocks
                    logger.info(f"✅ Migrated workflow {workflow_id} to mock OUTPUT data")
                    return workflow_data
                else:
                    logger.info(f"Workflow {workflow_id} already exists in mock data, skipping")
                    return None
                
        except Exception as e:
            logger.error(f"Error migrating workflow {workflow_data['id']}: {e}")
            return None
    
    async def _mark_migration_completed(self, migration_result: Dict[str, Any]) -> None:
        """Mark migration as completed (optional metadata tracking)"""
        try:
            migration_metadata = {
                "migration_id": str(uuid.uuid4()),
                "completed_at": datetime.utcnow().isoformat(),
                "source": "csv_workflow_rows_and_blocks",
                "destination": "supabase_workflow_and_blocks",
                "result": migration_result
            }
            
            # Could store in a migrations table if needed
            logger.info(f"📋 Migration completed: {migration_metadata['migration_id']}")
            
        except Exception as e:
            logger.warning(f"Could not mark migration as completed: {e}")
    
    async def get_migration_status(self) -> Dict[str, Any]:
        """Get comprehensive migration status"""
        try:
            # Count input data
            workflow_rows = await self._get_workflow_rows()
            workflow_blocks_rows = await self._get_workflow_blocks_rows()
            
            # Count output data
            output_workflows = 0
            output_blocks = 0
            
            if self.db.use_database:
                try:
                    workflow_response = self.db.client.table("workflow").select("id", count="exact").execute()
                    output_workflows = workflow_response.count or 0
                    
                    blocks_response = self.db.client.table("workflow_blocks").select("id", count="exact").execute()
                    output_blocks = blocks_response.count or 0
                except:
                    output_workflows = len(self.db.mock_workflows)
                    output_blocks = sum(len(blocks) for blocks in self.db.mock_blocks.values())
            else:
                output_workflows = len(self.db.mock_workflows)
                output_blocks = sum(len(blocks) for blocks in self.db.mock_blocks.values())
            
            migration_completed = await self._is_migration_completed()
            
            return {
                "migration_status": {
                    "completed": migration_completed,
                    "input_data": {
                        "csv_workflow_rows": len(workflow_rows),
                        "csv_workflow_blocks_rows": len(workflow_blocks_rows)
                    },
                    "output_data": {
                        "supabase_workflows": output_workflows,
                        "supabase_workflow_blocks": output_blocks
                    },
                    "migration_ratio": f"{output_workflows}/{len(workflow_rows)}" if workflow_rows else "0/0",
                    "database_type": 'supabase' if self.db.use_database else 'mock'
                },
                "instructions": {
                    "first_time": "POST /api/csv/process - Run one-time migration",
                    "check_status": "GET /api/csv/status - Check migration progress", 
                    "force_rerun": "POST /api/csv/process?force_reprocess=true - Rerun migration",
                    "view_results": "GET /api/workflows - View migrated workflows"
                },
                "data_flow": "CSV Input (workflow_rows, workflow_blocks_rows) → API Processing → Supabase Output (workflow, workflow_blocks)"
            }
            
        except Exception as e:
            logger.error(f"Error getting migration status: {e}")
            return {
                "error": str(e),
                "migration_available": False
            }

# Global instance
csv_processor = CSVProcessor() 