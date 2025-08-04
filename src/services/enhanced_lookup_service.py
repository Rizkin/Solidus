# src/services/enhanced_lookup_service.py
import hashlib
import json
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import logging
import asyncio
import time

logger = logging.getLogger(__name__)

class EnhancedLookupService:
    """Enhanced lookup service with RAG capabilities"""
    
    def __init__(self, db_service, openai_api_key: Optional[str] = None):
        self.db_service = db_service
        self.similarity_threshold = 0.8
        self.use_ai_adaptation = True
        self.embedding_model = "text-embedding-3-small"  # Cheaper, faster
        
        # Initialize OpenAI client if key provided
        self.openai_client = None
        if openai_api_key:
            try:
                import openai
                self.openai_client = openai.AsyncOpenAI(api_key=openai_api_key)
                logger.info("✅ OpenAI embeddings enabled for RAG")
            except ImportError:
                logger.warning("❌ OpenAI library not installed, embeddings disabled")
        else:
            logger.info("🔄 OpenAI embeddings disabled (no API key)")

    async def log_ai_usage(self, provider: str, model: str, operation_type: str, 
                          workflow_id: Optional[str] = None, token_count: Optional[int] = None, 
                          cost_estimate: Optional[float] = None, response_time: Optional[float] = None, 
                          status: str = "success", error_message: Optional[str] = None):
        """Log AI usage to the ai_usage_logs table"""
        try:
            if self.db_service.use_database:
                log_data = {
                    "provider": provider,
                    "model": model,
                    "operation_type": operation_type,
                    "workflow_id": workflow_id,
                    "token_count": token_count,
                    "cost_estimate": cost_estimate,
                    "response_time": response_time,
                    "status": status,
                    "error_message": error_message,
                    "created_at": datetime.utcnow().isoformat()
                }
                
                result = self.db_service.client.table('ai_usage_logs').insert(log_data).execute()
                logger.debug(f"AI usage logged: {provider}/{model} - {operation_type}")
        except Exception as e:
            logger.error(f"Failed to log AI usage: {e}")

    async def log_cache_stats(self, cache_type: str, hit: bool):
        """Log cache hit/miss to the cache_stats table"""
        try:
            if self.db_service.use_database:
                # Try to find existing stats for today
                today = datetime.utcnow().date().isoformat()
                
                # Check if we have stats for today
                existing = self.db_service.client.table('cache_stats').select(
                    'id', 'hit_count', 'miss_count'
                ).eq('cache_type', cache_type).eq('period_start', today).execute()
                
                if existing.data:
                    # Update existing record
                    record = existing.data[0]
                    if hit:
                        new_hit_count = record['hit_count'] + 1
                        new_miss_count = record['miss_count']
                    else:
                        new_hit_count = record['hit_count']
                        new_miss_count = record['miss_count'] + 1
                    
                    self.db_service.client.table('cache_stats').update({
                        'hit_count': new_hit_count,
                        'miss_count': new_miss_count
                    }).eq('id', record['id']).execute()
                else:
                    # Create new record
                    self.db_service.client.table('cache_stats').insert({
                        'cache_type': cache_type,
                        'hit_count': 1 if hit else 0,
                        'miss_count': 0 if hit else 1,
                        'period_start': today
                    }).execute()
                    
                logger.debug(f"Cache stats logged: {cache_type} - {'HIT' if hit else 'MISS'}")
        except Exception as e:
            logger.error(f"Failed to log cache stats: {e}")
    
    async def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for workflow description"""
        if not self.openai_client:
            logger.warning("OpenAI client not initialized - no API key")
            return None
            
        start_time = time.time()
        try:
            logger.info(f"Generating embedding for text: {text[:50]}...")
            response = await self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Estimate cost (OpenAI text-embedding-3-small: $0.00002 per 1K tokens)
            token_count = len(text.split()) * 1.3  # Rough token estimation
            cost_estimate = (token_count / 1000) * 0.00002
            
            # Log AI usage
            await self.log_ai_usage(
                provider="openai",
                model=self.embedding_model,
                operation_type="embedding",
                token_count=int(token_count),
                cost_estimate=cost_estimate,
                response_time=response_time,
                status="success"
            )
            
            logger.info("✅ Embedding generated successfully")
            return response.data[0].embedding
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            await self.log_ai_usage(
                provider="openai",
                model=self.embedding_model,
                operation_type="embedding",
                response_time=response_time,
                status="error",
                error_message=str(e)
            )
            logger.error(f"❌ Error generating embedding: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            return None
    
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
    
    async def create_semantic_description(self, workflow_data: Dict[str, Any]) -> str:
        """Create rich semantic description for embedding"""
        blocks = workflow_data.get('blocks', [])
        block_types = [b.get('type') for b in blocks if b.get('type')]
        
        # Build semantic description
        description_parts = [
            f"Workflow type: {workflow_data.get('workflow_type', 'general')}",
            f"Block types: {', '.join(block_types)}",
            f"Block count: {len(blocks)}"
        ]
        
        # Add block-specific details
        for block in blocks:
            if block['type'] == 'agent':
                model = block.get('sub_blocks', {}).get('model', 'unknown')
                prompt = block.get('sub_blocks', {}).get('systemPrompt', '')[:100]
                description_parts.append(f"AI agent using {model}: {prompt}")
            elif block['type'] == 'api':
                endpoint = block.get('sub_blocks', {}).get('endpoint', '')
                description_parts.append(f"API integration: {endpoint}")
            elif block['type'] == 'starter':
                trigger = block.get('sub_blocks', {}).get('startWorkflow', 'manual')
                description_parts.append(f"Trigger: {trigger}")
        
        # Add workflow purpose (from name/description)
        workflow_name = workflow_data.get('name', 'Unnamed Workflow')
        workflow_desc = workflow_data.get('description', '')
        description_parts.insert(0, f"Purpose: {workflow_name} - {workflow_desc}")
        
        return " | ".join(description_parts)
    
    async def find_similar_workflows_structural(
        self, 
        workflow_data: Dict[str, Any]
    ) -> Optional[Tuple[Dict[str, Any], float]]:
        """Find similar workflows using structural matching"""
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
    
    async def find_similar_workflows_semantic(
        self, 
        workflow_data: Dict[str, Any]
    ) -> Optional[Tuple[Dict[str, Any], float]]:
        """Find similar workflows using semantic embeddings"""
        if not self.openai_client or not self.db_service.use_database:
            return None
            
        try:
            # Create semantic description and embedding
            semantic_desc = await self.create_semantic_description(workflow_data)
            embedding = await self.generate_embedding(semantic_desc)
            
            if not embedding:
                return None
            
            # Semantic search
            semantic_results = self.db_service.client.rpc(
                'search_similar_workflows_semantic',
                {
                    'query_embedding': embedding,
                    'match_threshold': 0.75,
                    'match_count': 5
                }
            ).execute()
            
            if semantic_results.data and len(semantic_results.data) > 0:
                best_semantic = semantic_results.data[0]
                return (
                    best_semantic['generated_state'],
                    best_semantic['similarity_score']
                )
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return None
        
        return None
    
    async def find_similar_workflows_hybrid(
        self, 
        workflow_data: Dict[str, Any]
    ) -> Optional[Tuple[Dict[str, Any], float, str]]:
        """Hybrid search: structural + semantic with cache statistics"""
        
        # 1. Try structural match first (fast)
        structural_match = await self.find_similar_workflows_structural(workflow_data)
        
        if structural_match and structural_match[1] >= 0.9:
            # High confidence structural match
            await self.log_cache_stats("structural_match", hit=True)
            logger.info(f"✅ Structural cache hit: {structural_match[1]:.1%} similarity")
            return (*structural_match, "structural")
        
        # 2. Try semantic search if available
        semantic_match = await self.find_similar_workflows_semantic(workflow_data)
        
        if semantic_match and semantic_match[1] >= 0.85:
            # High confidence semantic match
            await self.log_cache_stats("semantic_match", hit=True)
            logger.info(f"✅ Semantic cache hit: {semantic_match[1]:.1%} similarity")
            return (*semantic_match, "semantic")
        
        # 3. Return best available match
        if structural_match:
            await self.log_cache_stats("structural_match", hit=True)
            logger.info(f"✅ Lower confidence structural hit: {structural_match[1]:.1%}")
            return (*structural_match, "structural")
        elif semantic_match:
            await self.log_cache_stats("semantic_match", hit=True)
            logger.info(f"✅ Lower confidence semantic hit: {semantic_match[1]:.1%}")
            return (*semantic_match, "semantic")
        
        # Cache miss - log it
        await self.log_cache_stats("overall", hit=False)
        logger.info("❌ Cache miss - no similar workflow found")
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
    
    async def store_workflow_pattern_with_embedding(
        self,
        input_data: Dict[str, Any],
        generated_state: Dict[str, Any],
        generation_time: float
    ) -> bool:
        """Store a new workflow pattern with embedding"""
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
            
            # Add semantic description and embedding if available
            if self.openai_client:
                semantic_desc = await self.create_semantic_description(input_data)
                lookup_data['semantic_description'] = semantic_desc
                
                embedding = await self.generate_embedding(semantic_desc)
                if embedding:
                    lookup_data['embedding'] = embedding
            
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
        """Get cache performance statistics from cache_stats table"""
        try:
            if self.db_service.use_database:
                # Get cache statistics from the database
                stats_query = self.db_service.client.table('cache_stats').select(
                    'cache_type', 'hit_count', 'miss_count', 'hit_rate', 'period_start'
                ).order('period_start', desc=True).limit(30).execute()  # Last 30 days
                
                if stats_query.data:
                    # Calculate overall stats
                    total_hits = sum(row['hit_count'] for row in stats_query.data)
                    total_misses = sum(row['miss_count'] for row in stats_query.data)
                    total_requests = total_hits + total_misses
                    overall_hit_rate = (total_hits / total_requests * 100) if total_requests > 0 else 0
                    
                    # Get AI usage stats
                    ai_stats = self.db_service.client.table('ai_usage_logs').select(
                        'provider', 'operation_type', 'cost_estimate', 'response_time'
                    ).execute()
                    
                    total_ai_cost = sum(float(row.get('cost_estimate', 0) or 0) for row in ai_stats.data) if ai_stats.data else 0
                    ai_calls_made = len(ai_stats.data) if ai_stats.data else 0
                    
                    # Estimate savings (assuming 70% cache hit rate saves costs)
                    estimated_saved_calls = int(total_hits * 0.7) if total_hits > 0 else 0
                    estimated_saved_cost = estimated_saved_calls * 0.01  # Rough estimate
                    
                    return {
                        "total_requests": total_requests,
                        "cache_hits": total_hits,
                        "cache_misses": total_misses,
                        "hit_rate": f"{overall_hit_rate:.1f}%",
                        "ai_calls_made": ai_calls_made,
                        "ai_calls_saved": estimated_saved_calls,
                        "total_ai_cost": f"${total_ai_cost:.4f}",
                        "estimated_cost_saved": f"${estimated_saved_cost:.4f}",
                        "cache_breakdown": {
                            row['cache_type']: {
                                'hits': row['hit_count'],
                                'misses': row['miss_count'],
                                'hit_rate': f"{row['hit_rate']:.1f}%" if row['hit_rate'] else "0%"
                            }
                            for row in stats_query.data
                        },
                        "status": "database_connected"
                    }
            
            # Mock stats fallback
            return {
                "total_requests": 17,
                "cache_hits": 12,
                "cache_misses": 5,
                "hit_rate": "70.6%",
                "ai_calls_made": 5,
                "ai_calls_saved": 12,
                "total_ai_cost": "$0.0045",
                "estimated_cost_saved": "$0.0120",
                "status": "mock_data"
            }
            
        except Exception as e:
            logger.error(f"Error getting cache statistics: {e}")
            return {"error": str(e)} 