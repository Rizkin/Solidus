"""
Comprehensive tests for Enhanced Lookup Service (RAG caching system).

Tests lookup key generation, similarity search, pattern storage, cache adaptation,
temp record management, and semantic search.

Coverage target: 90%+ for lookup_service.py
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any, List

from src.services.enhanced_lookup_service import EnhancedLookupService
from tests.fixtures.mock_data import CACHE_TEST_PATTERNS
from tests.fixtures.mock_responses import (
    OPENAI_SUCCESS_RESPONSES, CACHE_OPERATION_RESULTS
)


class TestEnhancedLookupService:
    """Test suite for EnhancedLookupService."""

    @pytest.fixture(autouse=True)
    def setup_lookup_service(self, mock_db_service):
        """Set up lookup service for each test."""
        self.lookup_service = EnhancedLookupService(mock_db_service)
        self.mock_db = mock_db_service

    # ========================================
    # 1. Lookup Key Generation Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.cache
    def test_lookup_key_generation_consistency(self):
        """Test that lookup key generation is consistent for same inputs."""
        workflow_data = {
            "blocks": ["starter", "agent", "api"],
            "connections": 2,
            "complexity": "medium"
        }
        
        # Generate key multiple times
        key1 = self.lookup_service._generate_lookup_key(workflow_data)
        key2 = self.lookup_service._generate_lookup_key(workflow_data)
        key3 = self.lookup_service._generate_lookup_key(workflow_data)
        
        # Should be identical
        assert key1 == key2 == key3
        assert isinstance(key1, str)
        assert len(key1) > 0

    @pytest.mark.unit
    @pytest.mark.cache
    def test_lookup_key_uniqueness_different_inputs(self):
        """Test that different inputs generate different lookup keys."""
        workflow1 = {"blocks": ["starter", "agent"], "connections": 1}
        workflow2 = {"blocks": ["starter", "api"], "connections": 1}
        workflow3 = {"blocks": ["starter", "agent", "api"], "connections": 2}
        
        key1 = self.lookup_service._generate_lookup_key(workflow1)
        key2 = self.lookup_service._generate_lookup_key(workflow2)
        key3 = self.lookup_service._generate_lookup_key(workflow3)
        
        # Should all be different
        assert key1 != key2
        assert key2 != key3
        assert key1 != key3

    @pytest.mark.unit
    @pytest.mark.cache
    def test_lookup_key_similar_patterns(self):
        """Test lookup key generation for similar but not identical patterns."""
        pattern1 = {"blocks": ["starter", "agent", "api"], "connections": 2}
        pattern2 = {"blocks": ["starter", "agent", "api"], "connections": 3}  # Different connections
        pattern3 = {"blocks": ["starter", "agent", "tool"], "connections": 2}  # Different block type
        
        key1 = self.lookup_service._generate_lookup_key(pattern1)
        key2 = self.lookup_service._generate_lookup_key(pattern2)
        key3 = self.lookup_service._generate_lookup_key(pattern3)
        
        # Similar patterns should have different keys
        assert key1 != key2
        assert key1 != key3
        assert key2 != key3

    @pytest.mark.unit
    @pytest.mark.cache
    def test_lookup_key_hash_collision_handling(self):
        """Test handling of potential hash collisions."""
        # Create many different patterns to test collision resistance
        patterns = []
        for i in range(100):
            pattern = {
                "blocks": ["starter", "agent", f"block_{i}"],
                "connections": i % 10,
                "metadata": {"index": i}
            }
            patterns.append(pattern)
        
        keys = [self.lookup_service._generate_lookup_key(p) for p in patterns]
        
        # Should have high uniqueness (allowing for some potential collisions)
        unique_keys = set(keys)
        collision_rate = 1 - (len(unique_keys) / len(keys))
        
        # Collision rate should be very low
        assert collision_rate < 0.05, f"Hash collision rate too high: {collision_rate}"

    @pytest.mark.unit
    @pytest.mark.cache
    def test_lookup_key_special_characters(self):
        """Test lookup key generation with special characters in input."""
        special_patterns = [
            {"name": "workflow with spaces", "type": "test"},
            {"name": "workflow-with-dashes", "type": "test"},
            {"name": "workflow_with_underscores", "type": "test"},
            {"name": "workflow.with.dots", "type": "test"},
            {"name": "workflow@with#symbols!", "type": "test"},
            {"name": "workflow/with\\slashes", "type": "test"}
        ]
        
        keys = []
        for pattern in special_patterns:
            key = self.lookup_service._generate_lookup_key(pattern)
            keys.append(key)
            
            # Key should be valid string without special characters that could cause issues
            assert isinstance(key, str)
            assert len(key) > 0
            # Should not contain problematic characters for database/filesystem use
            assert not any(char in key for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|'])
        
        # All keys should be unique
        assert len(set(keys)) == len(keys)

    # ========================================
    # 2. Similarity Search Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_similarity_search_exact_match(self):
        """Test similarity search with exact pattern match."""
        # Setup exact match scenario
        query_pattern = {
            "block_types": ["starter", "agent", "api"],
            "connection_count": 2,
            "workflow_type": "trading_bot"
        }
        
        # Mock database response with exact match
        self.mock_db.query_similar_patterns = AsyncMock(return_value=[
            {
                "pattern_key": self.lookup_service._generate_lookup_key(query_pattern),
                "similarity": 1.0,
                "cached_state": {"blocks": {}, "edges": []},
                "usage_count": 5
            }
        ])
        
        result = await self.lookup_service.find_similar_workflows_structural(query_pattern)
        
        assert result["found"] is True
        assert result["similarity"] == 1.0
        assert "cached_state" in result

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_similarity_search_high_similarity(self):
        """Test similarity search with high similarity (>80% match)."""
        query_pattern = {
            "block_types": ["starter", "agent", "api"],
            "connection_count": 2
        }
        
        # Mock database response with high similarity match
        self.mock_db.query_similar_patterns = AsyncMock(return_value=[
            {
                "pattern_key": "similar_pattern_key",
                "similarity": 0.87,
                "cached_state": {"blocks": {}, "edges": []},
                "usage_count": 3
            }
        ])
        
        result = await self.lookup_service.find_similar_workflows_structural(query_pattern)
        
        assert result["found"] is True
        assert result["similarity"] >= 0.8
        assert result["needs_adaptation"] is True

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_similarity_search_no_matches(self):
        """Test similarity search when no similar patterns exist."""
        query_pattern = {
            "block_types": ["starter", "agent", "custom_block"],
            "connection_count": 5
        }
        
        # Mock database response with no matches
        self.mock_db.query_similar_patterns = AsyncMock(return_value=[])
        
        result = await self.lookup_service.find_similar_workflows_structural(query_pattern)
        
        assert result["found"] is False
        assert result["searched_patterns"] is not None
        assert result["best_match"] is None

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_similarity_search_multiple_matches_ranking(self):
        """Test similarity search with multiple matches and proper ranking."""
        query_pattern = {
            "block_types": ["starter", "agent", "api"],
            "connection_count": 2
        }
        
        # Mock multiple matches with different similarities
        matches = [
            {"pattern_key": "pattern1", "similarity": 0.95, "usage_count": 10},
            {"pattern_key": "pattern2", "similarity": 0.87, "usage_count": 5},
            {"pattern_key": "pattern3", "similarity": 0.82, "usage_count": 15}
        ]
        
        self.mock_db.query_similar_patterns = AsyncMock(return_value=matches)
        
        result = await self.lookup_service.find_similar_workflows_structural(query_pattern)
        
        assert result["found"] is True
        # Should return highest similarity match
        assert result["similarity"] == 0.95
        assert "all_matches" in result
        assert len(result["all_matches"]) == 3

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_similarity_threshold_filtering(self):
        """Test that similarity search respects threshold filtering."""
        query_pattern = {"block_types": ["starter", "agent"]}
        
        # Mock matches below threshold
        low_similarity_matches = [
            {"pattern_key": "pattern1", "similarity": 0.65},
            {"pattern_key": "pattern2", "similarity": 0.72}
        ]
        
        self.mock_db.query_similar_patterns = AsyncMock(return_value=low_similarity_matches)
        
        result = await self.lookup_service.find_similar_workflows_structural(
            query_pattern, 
            similarity_threshold=0.8
        )
        
        # Should not find matches below threshold
        assert result["found"] is False

    # ========================================
    # 3. Pattern Storage Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_pattern_storage_new_pattern(self):
        """Test storing a new workflow pattern."""
        new_pattern = {
            "workflow_id": "test-workflow-123",
            "block_types": ["starter", "agent", "api"],
            "connection_count": 2,
            "cached_state": {"blocks": {}, "edges": []},
            "metadata": {"workflow_type": "trading_bot"}
        }
        
        # Mock successful storage
        self.mock_db.insert_workflow_pattern = AsyncMock(return_value=True)
        
        result = await self.lookup_service.store_workflow_pattern(new_pattern)
        
        assert result is True
        self.mock_db.insert_workflow_pattern.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_pattern_storage_update_existing(self):
        """Test updating an existing workflow pattern."""
        existing_pattern_key = "existing_pattern_123"
        updated_pattern = {
            "workflow_id": "test-workflow-123",
            "block_types": ["starter", "agent", "api"],
            "connection_count": 2,
            "cached_state": {"blocks": {}, "edges": []},
            "usage_count": 6  # Updated usage count
        }
        
        # Mock existing pattern found
        self.mock_db.get_pattern_by_key = AsyncMock(return_value={
            "pattern_key": existing_pattern_key,
            "usage_count": 5
        })
        
        # Mock successful update
        self.mock_db.update_workflow_pattern = AsyncMock(return_value=True)
        
        result = await self.lookup_service.update_pattern_usage(existing_pattern_key)
        
        assert result is True
        self.mock_db.update_workflow_pattern.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_pattern_storage_usage_count_increment(self):
        """Test that pattern usage count increments properly."""
        pattern_key = "usage_test_pattern"
        initial_count = 3
        
        # Mock pattern with initial usage count
        self.mock_db.get_pattern_by_key = AsyncMock(return_value={
            "pattern_key": pattern_key,
            "usage_count": initial_count
        })
        
        # Mock successful increment
        self.mock_db.increment_pattern_usage = AsyncMock(return_value=initial_count + 1)
        
        new_count = await self.lookup_service.increment_pattern_usage(pattern_key)
        
        assert new_count == initial_count + 1
        self.mock_db.increment_pattern_usage.assert_called_once_with(pattern_key)

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_pattern_storage_timestamp_updates(self):
        """Test that pattern timestamps are updated correctly."""
        pattern_key = "timestamp_test_pattern"
        
        # Mock pattern update with timestamp
        self.mock_db.update_pattern_timestamp = AsyncMock(return_value=True)
        
        result = await self.lookup_service.update_pattern_access_time(pattern_key)
        
        assert result is True
        self.mock_db.update_pattern_timestamp.assert_called_once()

    # ========================================  
    # 4. Cache Adaptation Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_cache_adaptation_minor_changes(self):
        """Test cache adaptation for minor workflow changes."""
        cached_pattern = {
            "cached_state": {
                "blocks": {
                    "starter-1": {"type": "starter", "name": "Start"},
                    "agent-1": {"type": "agent", "name": "AI Agent", "config": {"model": "gpt-4"}},
                    "api-1": {"type": "api", "name": "API Call"}
                },
                "edges": [{"from": "starter-1", "to": "agent-1"}]
            }
        }
        
        requested_changes = {
            "agent_model": "claude-3",
            "api_url": "https://api.example.com/v2"
        }
        
        adapted_state = await self.lookup_service.adapt_cached_state(
            cached_pattern["cached_state"], 
            requested_changes
        )
        
        # Verify adaptations were applied
        agent_block = adapted_state["blocks"]["agent-1"]
        assert agent_block["config"]["model"] == "claude-3"
        
        # Structure should remain intact
        assert len(adapted_state["blocks"]) == len(cached_pattern["cached_state"]["blocks"])

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_cache_adaptation_major_changes(self):
        """Test cache adaptation for major workflow changes."""
        cached_pattern = {
            "cached_state": {
                "blocks": {
                    "starter-1": {"type": "starter"},
                    "agent-1": {"type": "agent"}
                },
                "edges": [{"from": "starter-1", "to": "agent-1"}]
            }
        }
        
        major_changes = {
            "add_blocks": [{"type": "api", "name": "New API"}],
            "remove_blocks": ["agent-1"],
            "new_connections": [{"from": "starter-1", "to": "api-1"}]
        }
        
        adapted_state = await self.lookup_service.adapt_cached_state(
            cached_pattern["cached_state"],
            major_changes
        )
        
        # Major changes should be reflected
        blocks = adapted_state["blocks"]
        assert "agent-1" not in blocks  # Removed
        assert any(block["type"] == "api" for block in blocks.values())  # Added

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_cache_adaptation_similarity_thresholds(self):
        """Test different similarity thresholds for cache adaptation."""
        test_cases = [
            (0.95, "minor_adaptation"),    # High similarity - minor changes
            (0.85, "moderate_adaptation"), # Medium similarity - moderate changes  
            (0.75, "major_adaptation")     # Lower similarity - major changes
        ]
        
        for similarity, expected_level in test_cases:
            adaptation_level = self.lookup_service._determine_adaptation_level(similarity)
            
            assert adaptation_level == expected_level

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_cache_adaptation_performance_tracking(self):
        """Test that cache adaptation tracks performance metrics."""
        cached_state = {"blocks": {}, "edges": []}
        changes = {"minor": "change"}
        
        # Mock performance tracking
        with patch.object(self.lookup_service, '_track_adaptation_performance') as mock_track:
            adapted_state = await self.lookup_service.adapt_cached_state(cached_state, changes)
            
            # Should track adaptation performance
            mock_track.assert_called_once()

    # ========================================
    # 5. Temp Record Management Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_temp_record_creation(self):
        """Test creation of temporary workflow records."""
        workflow_data = {
            "workflow_id": "temp-workflow-123",
            "pattern": {"blocks": ["starter", "agent"]},
            "session_id": "session-456"
        }
        
        # Mock successful temp record creation
        self.mock_db.create_temp_record = AsyncMock(return_value="temp-record-789")
        
        temp_id = await self.lookup_service.create_temp_workflow_record(workflow_data)
        
        assert temp_id == "temp-record-789"
        self.mock_db.create_temp_record.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_temp_record_update_with_results(self):
        """Test updating temp records with generation results."""
        temp_record_id = "temp-record-123"
        generation_results = {
            "generated_state": {"blocks": {}, "edges": []},
            "generation_time": 2.5,
            "cache_hit": False
        }
        
        # Mock successful update
        self.mock_db.update_temp_record = AsyncMock(return_value=True)
        
        result = await self.lookup_service.update_temp_record_with_results(
            temp_record_id,
            generation_results
        )
        
        assert result is True
        self.mock_db.update_temp_record.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_temp_record_cleanup_old_records(self):
        """Test cleanup of old temporary records."""
        # Mock old temp records
        old_records = [
            {"id": "old-1", "created_at": "2024-01-01T00:00:00Z"},
            {"id": "old-2", "created_at": "2024-01-01T01:00:00Z"}
        ]
        
        self.mock_db.get_old_temp_records = AsyncMock(return_value=old_records)
        self.mock_db.delete_temp_records = AsyncMock(return_value=2)
        
        deleted_count = await self.lookup_service.cleanup_old_temp_records(max_age_hours=24)
        
        assert deleted_count == 2
        self.mock_db.delete_temp_records.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_temp_record_session_management(self):
        """Test session-based temp record management."""
        session_id = "session-test-123"
        
        # Mock session records
        session_records = [
            {"id": "temp-1", "session_id": session_id},
            {"id": "temp-2", "session_id": session_id}
        ]
        
        self.mock_db.get_session_temp_records = AsyncMock(return_value=session_records)
        
        records = await self.lookup_service.get_session_temp_records(session_id)
        
        assert len(records) == 2
        assert all(record["session_id"] == session_id for record in records)

    # ========================================
    # 6. Semantic Search Tests (with embeddings)
    # ========================================

    @pytest.mark.unit
    @pytest.mark.cache
    @pytest.mark.ai
    async def test_semantic_search_openai_embeddings(self, mock_env_vars):
        """Test semantic search using OpenAI embeddings."""
        query = "I need a crypto trading bot with stop loss functionality"
        
        # Mock OpenAI embedding response
        with patch('openai.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_client.embeddings.create.return_value = OPENAI_SUCCESS_RESPONSES["embedding"]
            mock_openai_class.return_value = mock_client
            
            # Mock database similarity search
            self.mock_db.vector_similarity_search = AsyncMock(return_value=[
                {
                    "workflow_id": "trading-bot-123",
                    "similarity": 0.87,
                    "cached_state": {"blocks": {}, "edges": []},
                    "description": "Crypto trading bot with risk management"
                }
            ])
            
            results = await self.lookup_service.semantic_search_workflows(query)
            
            assert len(results) > 0
            assert results[0]["similarity"] > 0.8
            mock_client.embeddings.create.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_semantic_search_vector_similarity(self):
        """Test vector similarity calculations in semantic search."""
        query_embedding = [0.1] * 1536
        
        # Mock stored embeddings
        stored_embeddings = [
            {"workflow_id": "workflow-1", "embedding": [0.1] * 1536},    # Identical
            {"workflow_id": "workflow-2", "embedding": [0.2] * 1536},    # Different
            {"workflow_id": "workflow-3", "embedding": [0.11] * 1536}    # Very similar
        ]
        
        similarities = []
        for stored in stored_embeddings:
            similarity = self.lookup_service._calculate_cosine_similarity(
                query_embedding, 
                stored["embedding"]   
            )
            similarities.append(similarity)
        
        # Verify similarity calculations
        assert similarities[0] == 1.0  # Identical vectors
        assert similarities[2] > similarities[1]  # More similar vector has higher score

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_semantic_search_natural_language_queries(self):
        """Test semantic search with various natural language queries."""
        test_queries = [
            "Create a lead generation workflow for LinkedIn",
            "I want to automate social media posting across platforms",
            "Build a customer support chatbot with escalation",
            "Set up automated data pipeline from database to analytics",
            "Need workflow for processing and analyzing financial reports"
        ]
        
        # Mock embedding generation for all queries
        with patch.object(self.lookup_service, 'generate_embedding') as mock_embed:
            mock_embed.return_value = [0.1] * 1536
            
            # Mock database search results
            self.mock_db.vector_similarity_search = AsyncMock(return_value=[
                {"workflow_id": "match-1", "similarity": 0.85}
            ])
            
            for query in test_queries:
                results = await self.lookup_service.semantic_search_workflows(query)
                
                # Should process each query successfully
                assert isinstance(results, list)
                mock_embed.assert_called()

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_semantic_search_ranking_accuracy(self):
        """Test accuracy of semantic search result ranking."""
        query = "trading bot with technical analysis"
        
        # Mock search results with different relevance scores
        mock_results = [
            {"workflow_id": "crypto-bot", "similarity": 0.92, "description": "Crypto trading bot"},
            {"workflow_id": "stock-trader", "similarity": 0.88, "description": "Stock trading system"},
            {"workflow_id": "price-alert", "similarity": 0.75, "description": "Price alert system"},
            {"workflow_id": "portfolio", "similarity": 0.65, "description": "Portfolio tracker"}
        ]
        
        self.mock_db.vector_similarity_search = AsyncMock(return_value=mock_results)
        
        results = await self.lookup_service.semantic_search_workflows(query)
        
        # Results should be ranked by similarity
        similarities = [result["similarity"] for result in results]
        assert similarities == sorted(similarities, reverse=True)

    # ========================================
    # Performance and Integration Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.cache
    @pytest.mark.performance
    async def test_lookup_service_performance_benchmarks(self, performance_monitor):
        """Test lookup service performance benchmarks."""
        test_operations = [
            ("pattern_lookup", self.lookup_service.find_similar_workflows_structural, 
             {"block_types": ["starter", "agent"]}),
            ("pattern_storage", self.lookup_service.store_workflow_pattern,
             {"workflow_id": "test", "pattern": {}}),
            ("cache_adaptation", self.lookup_service.adapt_cached_state,
             ({"blocks": {}}, {"change": "minor"}))
        ]
        
        # Mock all database operations for performance testing
        self.mock_db.query_similar_patterns = AsyncMock(return_value=[])
        self.mock_db.insert_workflow_pattern = AsyncMock(return_value=True)
        
        for operation_name, operation_func, operation_args in test_operations:
            performance_monitor.start_timer(operation_name)
            
            if isinstance(operation_args, dict):
                await operation_func(operation_args)
            else:
                await operation_func(*operation_args)
            
            performance_monitor.end_timer(operation_name)
            
            # Each operation should complete quickly
            performance_monitor.assert_performance(operation_name, 2.0)

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_hybrid_search_integration(self):
        """Test integration of structural and semantic search."""
        query_data = {
            "natural_language": "I need a trading bot for cryptocurrency",
            "structural_pattern": {"block_types": ["starter", "agent", "api"]}
        }
        
        # Mock both search types
        with patch.object(self.lookup_service, 'find_similar_workflows_structural') as mock_structural:
            mock_structural.return_value = {"found": True, "similarity": 0.85}
            
            with patch.object(self.lookup_service, 'semantic_search_workflows') as mock_semantic:
                mock_semantic.return_value = [{"workflow_id": "semantic-match", "similarity": 0.90}]
                
                result = await self.lookup_service.find_similar_workflows_hybrid(query_data)
                
                # Should combine both search methods
                assert result["structural_match"]["found"] is True
                assert len(result["semantic_matches"]) > 0
                assert result["best_match_method"] in ["structural", "semantic", "hybrid"]

    @pytest.mark.unit
    @pytest.mark.cache
    async def test_cache_statistics_tracking(self):
        """Test comprehensive cache statistics tracking."""
        # Mock database statistics
        self.mock_db.get_cache_hit_stats = AsyncMock(return_value={
            "total_requests": 100,
            "cache_hits": 75,
            "cache_misses": 25,
            "hit_rate": 0.75
        })
        
        self.mock_db.get_ai_usage_stats = AsyncMock(return_value={
            "total_ai_calls": 25,
            "cost_saved": 15.50,
            "average_response_time": 2.3
        })
        
        stats = await self.lookup_service.get_comprehensive_cache_statistics()
        
        # Verify comprehensive statistics
        assert "cache_performance" in stats
        assert "ai_usage" in stats
        assert "cost_analysis" in stats
        assert stats["cache_performance"]["hit_rate"] == 0.75 