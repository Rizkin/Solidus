# src/services/lookup_service.py
import hashlib
import json
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import logging
from src.utils.database_hybrid import db_service

logger = logging.getLogger(__name__)

class WorkflowLookupService:
    """Intelligent caching system for workflow generation"""
    
    def __init__(self):
        self.db_service = db_service
        self.similarity_threshold = 0.8
        self.use_ai_adaptation = True
    
    def generate_lookup_key(self, input_data: Dict[str, Any]) -> str:
        """Generate a unique key for the input pattern"""
        # Create a normalized representation of the input
        normalized = {
            'workflow_type': input_data.get('workflow_type', 'unknown'),
            'block_count': len(input_data.get('blocks', [])),
            'block_types': sorted(list(set(b.get('type') for b in input_data.get('blocks', [])))),
            'has_edges': len(input_data.get('edges', [])) > 0
        }
        
        # Create hash
        key_string = json.dumps(normalized, sort_keys=True)
        return hashlib.sha256(key_string.encode()).hexdigest()[:16]
    
    async def find_similar_workflows(
        self, 
        workflow_data: Dict[str, Any]
    ) -> Optional[Tuple[Dict[str, Any], float]]:
        """Find similar workflows in the lookup table"""
        try:
            # Extract characteristics
            workflow_type = workflow_data.get('workflow_type', 'general')
            blocks = workflow_data.get('blocks', [])
            block_types = [b.get('type') for b in blocks if b.get('type')]
            block_count = len(blocks)
            
            logger.info(f"Looking for similar workflows: type={workflow_type}, blocks={block_count}")
            
            if self.db_service.use_database:
                # Use database function for similarity search
                try:
                    result = self.db_service.client.rpc(
                        'find_similar_workflows',
                        {
                            'p_workflow_type': workflow_type,
                            'p_block_types': block_types,
                            'p_block_count': block_count,
                            'p_similarity_threshold': self.similarity_threshold
                        }
                    ).execute()
                    
                    if result.data and len(result.data) > 0:
                        best_match = result.data[0]
                        if best_match['similarity_score'] >= self.similarity_threshold:
                            logger.info(f"Found similar workflow with {best_match['similarity_score']:.2%} similarity")
                            
                            # Update usage count
                            self.db_service.client.table('workflow_lookup').update({
                                'usage_count': best_match['usage_count'] + 1,
                                'last_used_at': datetime.utcnow().isoformat()
                            }).eq('id', best_match['lookup_id']).execute()
                            
                            return (
                                best_match['generated_state'],
                                best_match['similarity_score']
                            )
                except Exception as db_error:
                    logger.warning(f"Database lookup failed, using fallback: {db_error}")
            
            # Fallback to mock similarity search
            return await self._mock_similarity_search(workflow_data)
            
        except Exception as e:
            logger.error(f"Error finding similar workflows: {e}")
            return None
    
    async def _mock_similarity_search(self, workflow_data: Dict[str, Any]) -> Optional[Tuple[Dict[str, Any], float]]:
        """Mock similarity search for development/fallback"""
        # Simple pattern matching for common workflow types
        workflow_type = workflow_data.get('workflow_type', 'general')
        block_count = len(workflow_data.get('blocks', []))
        
        # Return a mock cached result for testing
        if workflow_type in ['trading_bot', 'lead_generation'] and block_count >= 3:
            mock_state = {
                "blocks": {
                    "starter_1": {
                        "id": "starter_1",
                        "type": "starter",
                        "name": "Workflow Trigger",
                        "position": {"x": 100, "y": 100},
                        "subBlocks": {"startWorkflow": "manual"}
                    }
                },
                "edges": [],
                "subflows": {},
                "variables": {},
                "metadata": {
                    "cached": True,
                    "workflow_type": workflow_type,
                    "similarity_score": 0.85,
                    "generated_at": datetime.utcnow().isoformat()
                }
            }
            
            logger.info(f"Using mock cached result for {workflow_type}")
            return (mock_state, 0.85)
        
        return None
    
    async def store_workflow_pattern(
        self,
        input_data: Dict[str, Any],
        generated_state: Dict[str, Any],
        generation_time: float
    ) -> bool:
        """Store a new workflow pattern in the lookup table"""
        try:
            lookup_key = self.generate_lookup_key(input_data)
            blocks = input_data.get('blocks', [])
            
            # Prepare data for storage
            lookup_data = {
                'lookup_key': lookup_key,
                'input_pattern': {
                    'original_input': input_data,
                    'characteristics': {
                        'block_count': len(blocks),
                        'has_edges': len(input_data.get('edges', [])) > 0,
                        'complexity': self._calculate_complexity(input_data)
                    }
                },
                'workflow_type': input_data.get('workflow_type', 'general'),
                'block_count': len(blocks),
                'block_types': [b.get('type') for b in blocks if b.get('type')],
                'generated_state': generated_state,
                'avg_generation_time': generation_time
            }
            
            if self.db_service.use_database:
                # Store in database
                result = self.db_service.client.table('workflow_lookup').upsert(
                    lookup_data,
                    on_conflict='lookup_key'
                ).execute()
                
                logger.info(f"Stored workflow pattern with key: {lookup_key}")
            else:
                # Store in mock cache (in-memory)
                if not hasattr(self.db_service, 'mock_lookup_cache'):
                    self.db_service.mock_lookup_cache = {}
                
                self.db_service.mock_lookup_cache[lookup_key] = lookup_data
                logger.info(f"Stored workflow pattern in mock cache: {lookup_key}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error storing workflow pattern: {e}")
            return False
    
    async def create_temp_record(
        self,
        session_id: str,
        input_data: Dict[str, Any]
    ) -> str:
        """Create a temporary record for processing"""
        try:
            if self.db_service.use_database:
                result = self.db_service.client.table('workflow_temp').insert({
                    'session_id': session_id,
                    'input_data': input_data,
                    'processing_status': 'pending'
                }).execute()
                
                return result.data[0]['id']
            else:
                # Mock temp record
                temp_id = f"temp_{session_id}_{datetime.utcnow().timestamp()}"
                logger.info(f"Created mock temp record: {temp_id}")
                return temp_id
                
        except Exception as e:
            logger.error(f"Error creating temp record: {e}")
            # Return a fallback ID
            return f"fallback_{session_id}"
    
    async def update_temp_record(
        self,
        temp_id: str,
        ai_response: Dict[str, Any],
        lookup_match_id: Optional[str] = None,
        similarity_score: Optional[float] = None
    ):
        """Update temporary record with results"""
        try:
            update_data = {
                'ai_response': ai_response,
                'processing_status': 'completed',
                'completed_at': datetime.utcnow().isoformat()
            }
            
            if lookup_match_id:
                update_data['lookup_match_id'] = lookup_match_id
            if similarity_score:
                update_data['similarity_score'] = similarity_score
            
            if self.db_service.use_database:
                self.db_service.client.table('workflow_temp').update(
                    update_data
                ).eq('id', temp_id).execute()
            else:
                logger.info(f"Mock update temp record: {temp_id}")
            
        except Exception as e:
            logger.error(f"Error updating temp record: {e}")
    
    def _calculate_complexity(self, workflow_data: Dict[str, Any]) -> str:
        """Calculate workflow complexity"""
        blocks = len(workflow_data.get('blocks', []))
        edges = len(workflow_data.get('edges', []))
        
        if blocks <= 3 and edges <= 2:
            return 'simple'
        elif blocks <= 7 and edges <= 6:
            return 'medium'
        else:
            return 'complex'
    
    async def adapt_cached_state(
        self,
        cached_state: Dict[str, Any],
        current_input: Dict[str, Any],
        similarity_score: float
    ) -> Dict[str, Any]:
        """Adapt cached state to current requirements"""
        logger.info(f"Adapting cached state with {similarity_score:.2%} similarity")
        
        adapted_state = json.loads(json.dumps(cached_state))  # Deep copy
        
        # Update metadata
        if 'metadata' not in adapted_state:
            adapted_state['metadata'] = {}
        
        adapted_state['metadata'].update({
            'adapted_from_cache': True,
            'similarity_score': similarity_score,
            'adaptation_time': datetime.utcnow().isoformat(),
            'cache_performance': 'high' if similarity_score > 0.9 else 'medium'
        })
        
        # Update block positions if needed
        current_blocks = current_input.get('blocks', [])
        if current_blocks and 'blocks' in adapted_state:
            for block in current_blocks:
                block_id = block.get('id')
                if block_id and block_id in adapted_state['blocks']:
                    # Preserve original positions
                    adapted_state['blocks'][block_id]['position'] = {
                        'x': block.get('position_x', 100),
                        'y': block.get('position_y', 100)
                    }
        
        # Update workflow variables if provided
        current_variables = current_input.get('variables', {})
        if current_variables:
            if 'variables' not in adapted_state:
                adapted_state['variables'] = {}
            adapted_state['variables'].update(current_variables)
        
        logger.info("State adaptation completed")
        return adapted_state
    
    async def get_cache_statistics(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        try:
            if self.db_service.use_database:
                # Get database stats
                stats = self.db_service.client.table('workflow_lookup').select(
                    'workflow_type',
                    'usage_count',
                    'avg_generation_time'
                ).execute()
                
                if stats.data:
                    total_patterns = len(stats.data)
                    total_uses = sum(item['usage_count'] for item in stats.data)
                    avg_time_saved = sum(item['avg_generation_time'] for item in stats.data) / total_patterns if total_patterns > 0 else 0
                    
                    return {
                        "total_patterns_cached": total_patterns,
                        "total_cache_hits": total_uses,
                        "average_time_saved": f"{avg_time_saved:.2f}s",
                        "cache_hit_rate": f"{(total_uses / (total_uses + total_patterns)) * 100:.1f}%" if total_uses > 0 else "0%",
                        "ai_calls_saved": max(0, total_uses - total_patterns)
                    }
            
            # Mock stats
            return {
                "total_patterns_cached": 5,
                "total_cache_hits": 12,
                "average_time_saved": "1.8s",
                "cache_hit_rate": "70.6%",
                "ai_calls_saved": 7,
                "status": "mock_data"
            }
            
        except Exception as e:
            logger.error(f"Error getting cache statistics: {e}")
            return {"error": str(e)}

# Create singleton instance
lookup_service = WorkflowLookupService() 