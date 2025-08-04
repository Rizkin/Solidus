"""
Database Hybrid Utility
Provides database operations with fallback to mock data
"""
import os
import json
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class DatabaseService:
    """Hybrid database service with Supabase integration and fallback"""
    
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
        self.use_database = bool(self.supabase_url and self.supabase_key)
        
        if self.use_database:
            try:
                from supabase import create_client
                self.client = create_client(self.supabase_url, self.supabase_key)
                logger.info("✅ Supabase connection established")
            except ImportError:
                logger.warning("❌ Supabase library not installed, using mock data")
                self.use_database = False
            except Exception as e:
                logger.warning(f"❌ Supabase connection failed: {e}, using mock data")
                self.use_database = False
        else:
            logger.info("🔄 Using mock database (no Supabase credentials)")
        
        # Mock data storage
        self.mock_workflows = {}
        self.mock_blocks = {}
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Initialize mock data for development/testing"""
        sample_workflow_id = "sample-workflow-123"
        
        self.mock_workflows[sample_workflow_id] = {
            "id": sample_workflow_id,
            "user_id": "user-123",
            "workspace_id": "workspace-123",
            "name": "Sample Trading Bot",
            "description": "A sample trading bot workflow for demonstration",
            "state": {
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
                    "agent_1": {
                        "id": "agent_1",
                        "type": "agent",
                        "name": "Trading Agent",
                        "position_x": 300,
                        "position_y": 100,
                        "sub_blocks": {
                            "model": "gpt-4",
                            "systemPrompt": "Analyze market data and make trading decisions",
                            "temperature": 0.3
                        }
                    }
                },
                "edges": [{"from": "starter_1", "to": "agent_1"}],
                "subflows": {},
                "variables": {
                    "TRADING_PAIR": "BTC/USD",
                    "STOP_LOSS": -5,
                    "TAKE_PROFIT": 10
                },
                "metadata": {
                    "version": "1.0.0",
                    "createdAt": "2024-01-04T10:00:00Z",
                    "updatedAt": "2024-01-04T10:00:00Z"
                }
            },
            "color": "#FF6B6B",
            "is_published": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Mock blocks for the sample workflow
        self.mock_blocks[sample_workflow_id] = [
            {
                "id": "starter_1",
                "workflow_id": sample_workflow_id,
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
            {
                "id": "agent_1",
                "workflow_id": sample_workflow_id,
                "type": "agent",
                "name": "Trading Agent",
                "position_x": 300,
                "position_y": 100,
                "sub_blocks": {
                    "model": "gpt-4",
                    "systemPrompt": "Analyze market data and make trading decisions",
                    "temperature": 0.3
                }
            }
        ]
    
    async def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow by ID"""
        if self.use_database:
            try:
                response = self.client.table("workflows").select("*").eq("id", workflow_id).execute()
                if response.data:
                    workflow = response.data[0]
                    # Parse state if it's a string
                    if isinstance(workflow.get("state"), str):
                        try:
                            workflow["state"] = json.loads(workflow["state"])
                        except json.JSONDecodeError:
                            pass
                    return workflow
                return None
            except Exception as e:
                logger.error(f"Database error: {e}")
                return self.mock_workflows.get(workflow_id)
        else:
            return self.mock_workflows.get(workflow_id)
    
    async def get_workflow_blocks(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get blocks for a workflow"""
        if self.use_database:
            try:
                response = self.client.table("workflow_blocks").select("*").eq("workflow_id", workflow_id).execute()
                return response.data or []
            except Exception as e:
                logger.error(f"Database error: {e}")
                return self.mock_blocks.get(workflow_id, [])
        else:
            return self.mock_blocks.get(workflow_id, [])
    
    async def get_workflow_with_blocks(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow with its blocks"""
        workflow = await self.get_workflow(workflow_id)
        if workflow:
            blocks = await self.get_workflow_blocks(workflow_id)
            workflow["blocks"] = blocks
        return workflow
    
    async def create_workflow(self, workflow_data: Dict[str, Any]) -> Optional[str]:
        """Create a new workflow"""
        workflow_id = workflow_data.get("id") or str(uuid.uuid4())
        
        if self.use_database:
            try:
                # Prepare data for database
                db_data = workflow_data.copy()
                
                # Convert state to JSON string if it's a dict
                if isinstance(db_data.get("state"), dict):
                    db_data["state"] = json.dumps(db_data["state"])
                
                # Ensure required fields
                db_data.update({
                    "id": workflow_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                })
                
                response = self.client.table("workflows").insert(db_data).execute()
                if response.data:
                    return workflow_id
                return None
            except Exception as e:
                logger.error(f"Database error: {e}")
                # Fall back to mock storage
                self.mock_workflows[workflow_id] = workflow_data
                return workflow_id
        else:
            # Mock storage
            workflow_data["id"] = workflow_id
            workflow_data["created_at"] = datetime.utcnow()
            workflow_data["updated_at"] = datetime.utcnow()
            self.mock_workflows[workflow_id] = workflow_data
            return workflow_id
    
    async def update_workflow_state(self, workflow_id: str, state: Dict[str, Any]) -> bool:
        """Update workflow state"""
        if self.use_database:
            try:
                state_json = json.dumps(state) if isinstance(state, dict) else state
                response = self.client.table("workflows").update({
                    "state": state_json,
                    "updated_at": datetime.utcnow().isoformat()
                }).eq("id", workflow_id).execute()
                return bool(response.data)
            except Exception as e:
                logger.error(f"Database error: {e}")
                # Fall back to mock update
                if workflow_id in self.mock_workflows:
                    self.mock_workflows[workflow_id]["state"] = state
                    self.mock_workflows[workflow_id]["updated_at"] = datetime.utcnow()
                    return True
                return False
        else:
            # Mock update
            if workflow_id in self.mock_workflows:
                self.mock_workflows[workflow_id]["state"] = state
                self.mock_workflows[workflow_id]["updated_at"] = datetime.utcnow()
                return True
            return False
    
    async def create_workflow_blocks(self, workflow_id: str, blocks: List[Dict[str, Any]]) -> bool:
        """Create blocks for a workflow"""
        if self.use_database:
            try:
                # Prepare blocks for database
                db_blocks = []
                for block in blocks:
                    db_block = block.copy()
                    db_block["workflow_id"] = workflow_id
                    
                    # Convert sub_blocks to JSON string if it's a dict
                    if isinstance(db_block.get("sub_blocks"), dict):
                        db_block["sub_blocks"] = json.dumps(db_block["sub_blocks"])
                    
                    db_blocks.append(db_block)
                
                response = self.client.table("workflow_blocks").insert(db_blocks).execute()
                return bool(response.data)
            except Exception as e:
                logger.error(f"Database error: {e}")
                # Fall back to mock storage
                self.mock_blocks[workflow_id] = blocks
                return True
        else:
            # Mock storage
            self.mock_blocks[workflow_id] = blocks
            return True
    
    async def list_workflows(self, user_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """List workflows from output tables (after CSV migration)"""
        try:
            if self.use_database:
                query = self.client.table("workflow").select("*")
                
                if user_id:
                    query = query.eq("user_id", user_id)
                    
                query = query.limit(limit)
                response = query.execute()
                
                workflows = response.data or []
                
                # Parse JSON fields back to objects
                for workflow in workflows:
                    if isinstance(workflow.get('state'), str):
                        try:
                            workflow['state'] = json.loads(workflow['state'])
                        except:
                            workflow['state'] = {}
                    
                    if isinstance(workflow.get('variables'), str):
                        try:
                            workflow['variables'] = json.loads(workflow['variables'])
                        except:
                            workflow['variables'] = {}
                    
                    if isinstance(workflow.get('collaborators'), str):
                        try:
                            workflow['collaborators'] = json.loads(workflow['collaborators'])
                        except:
                            workflow['collaborators'] = []
                
                return workflows
                
            else:
                # Return mock data
                workflows = list(self.mock_workflows.values())
                
                if user_id:
                    workflows = [w for w in workflows if w.get('user_id') == user_id]
                
                return workflows[:limit]
                
        except Exception as e:
            logger.error(f"Error listing workflows: {e}")
            return []
    
    async def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow"""
        if self.use_database:
            try:
                # Delete blocks first
                self.client.table("workflow_blocks").delete().eq("workflow_id", workflow_id).execute()
                
                # Delete workflow
                response = self.client.table("workflows").delete().eq("id", workflow_id).execute()
                return bool(response.data)
            except Exception as e:
                logger.error(f"Database error: {e}")
                # Fall back to mock deletion
                if workflow_id in self.mock_workflows:
                    del self.mock_workflows[workflow_id]
                if workflow_id in self.mock_blocks:
                    del self.mock_blocks[workflow_id]
                return True
        else:
            # Mock deletion
            deleted = False
            if workflow_id in self.mock_workflows:
                del self.mock_workflows[workflow_id]
                deleted = True
            if workflow_id in self.mock_blocks:
                del self.mock_blocks[workflow_id]
                deleted = True
            return deleted
    
    async def get_workflow_count(self) -> int:
        """Get total workflow count"""
        if self.use_database:
            try:
                response = self.client.table("workflows").select("id", count="exact").execute()
                return response.count or 0
            except Exception as e:
                logger.error(f"Database error: {e}")
                return len(self.mock_workflows)
        else:
            return len(self.mock_workflows)
    
    async def search_workflows(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search workflows by name or description"""
        if self.use_database:
            try:
                response = self.client.table("workflows").select("*").or_(
                    f"name.ilike.%{query}%,description.ilike.%{query}%"
                ).limit(limit).execute()
                
                workflows = response.data or []
                
                # Parse state for each workflow
                for workflow in workflows:
                    if isinstance(workflow.get("state"), str):
                        try:
                            workflow["state"] = json.loads(workflow["state"])
                        except json.JSONDecodeError:
                            pass
                
                return workflows
            except Exception as e:
                logger.error(f"Database error: {e}")
                # Fall back to mock search
                query_lower = query.lower()
                return [
                    w for w in self.mock_workflows.values()
                    if query_lower in w.get("name", "").lower() or 
                       query_lower in w.get("description", "").lower()
                ][:limit]
        else:
            # Mock search
            query_lower = query.lower()
            return [
                w for w in self.mock_workflows.values()
                if query_lower in w.get("name", "").lower() or 
                   query_lower in w.get("description", "").lower()
                ][:limit]
    
    async def health_check(self) -> Dict[str, Any]:
        """Check database health"""
        if self.use_database:
            try:
                # Simple query to test connection
                response = self.client.table("workflows").select("id").limit(1).execute()
                return {
                    "status": "healthy",
                    "database": "supabase",
                    "connected": True,
                    "mock_workflows": len(self.mock_workflows)
                }
            except Exception as e:
                return {
                    "status": "degraded",
                    "database": "supabase",
                    "connected": False,
                    "error": str(e),
                    "fallback": "mock_data",
                    "mock_workflows": len(self.mock_workflows)
                }
        else:
            return {
                "status": "mock",
                "database": "mock_data",
                "connected": False,
                "mock_workflows": len(self.mock_workflows),
                "note": "Using mock data - set SUPABASE_URL and SUPABASE_SERVICE_KEY for database"
            }

# Global instance
db_service = DatabaseService() 