# src/utils/database_hybrid.py
from typing import Dict, Any, List, Optional
import logging
from src.utils.supabase import supabase_client
from src.models.connection import AsyncSessionLocal
from src.models.database import Workflow, WorkflowBlock
from sqlalchemy import select
import json

logger = logging.getLogger(__name__)

class DatabaseHybridService:
    """Hybrid service using both Supabase client and SQLAlchemy"""
    
    def __init__(self):
        self.supabase = supabase_client
        self.session_factory = AsyncSessionLocal
    
    async def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow by ID using Supabase client"""
        try:
            result = self.supabase.table('workflow').select("*").eq('id', workflow_id).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting workflow {workflow_id}: {e}")
            return None
    
    async def get_workflow_blocks(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get all blocks for a workflow using Supabase client"""
        try:
            result = self.supabase.table('workflow_blocks').select("*").eq('workflow_id', workflow_id).execute()
            
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting blocks for workflow {workflow_id}: {e}")
            return []
    
    async def update_workflow_state(self, workflow_id: str, state: Dict[str, Any]) -> bool:
        """Update workflow state using Supabase client"""
        try:
            result = self.supabase.table('workflow').update({
                'state': state,
                'updated_at': 'now()'
            }).eq('id', workflow_id).execute()
            
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"Error updating workflow state {workflow_id}: {e}")
            return False
    
    async def get_all_workflows(self) -> List[Dict[str, Any]]:
        """Get all workflows using Supabase client"""
        try:
            result = self.supabase.table('workflow').select("*").execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting all workflows: {e}")
            return []
    
    async def get_workflow_with_blocks(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow with its blocks"""
        workflow = await self.get_workflow(workflow_id)
        if not workflow:
            return None
        
        blocks = await self.get_workflow_blocks(workflow_id)
        
        return {
            **workflow,
            'blocks': blocks
        }
    
    async def create_workflow(self, workflow_data: Dict[str, Any]) -> Optional[str]:
        """Create a new workflow"""
        try:
            result = self.supabase.table('workflow').insert(workflow_data).execute()
            
            if result.data:
                return result.data[0]['id']
            return None
        except Exception as e:
            logger.error(f"Error creating workflow: {e}")
            return None
    
    async def create_workflow_block(self, block_data: Dict[str, Any]) -> Optional[str]:
        """Create a new workflow block"""
        try:
            result = self.supabase.table('workflow_blocks').insert(block_data).execute()
            
            if result.data:
                return result.data[0]['id']
            return None
        except Exception as e:
            logger.error(f"Error creating workflow block: {e}")
            return None

# Create singleton instance
db_service = DatabaseHybridService()
