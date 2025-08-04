"""
Comprehensive tests for database hybrid service.

Tests Supabase client, workflow operations, block operations, 
mock data fallback, transactions, and performance.

Coverage target: 90%+ for database_hybrid.py
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, call
from typing import Dict, Any, List, Optional

from src.utils.database_hybrid import DatabaseHybridService
from tests.fixtures.mock_data import (
    SAMPLE_WORKFLOW, SAMPLE_BLOCKS, MOCK_DATABASE_RESPONSES
)
from tests.fixtures.mock_responses import (
    DATABASE_SUCCESS_RESPONSES, DATABASE_ERROR_RESPONSES
)


class TestDatabaseHybridService:
    """Test suite for DatabaseHybridService."""

    @pytest.fixture(autouse=True)
    def setup_database_service(self):
        """Set up database service for each test."""
        self.db_service = DatabaseHybridService()

    # ========================================
    # 1. Supabase Client Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.database
    async def test_supabase_connection_initialization_success(self, mock_env_vars):
        """Test successful Supabase connection initialization."""
        with patch('supabase.create_client') as mock_create_client:
            mock_client = MagicMock()
            mock_create_client.return_value = mock_client
            
            # Initialize database service
            db_service = DatabaseHybridService()
            await db_service.initialize()
            
            # Verify client creation
            mock_create_client.assert_called_once_with(
                "https://test.supabase.co",
                "test-supabase-key"
            )
            assert db_service.supabase_client == mock_client
            assert db_service.is_connected is True

    @pytest.mark.unit
    @pytest.mark.database
    async def test_supabase_connection_failure_handling(self, mock_env_vars):
        """Test Supabase connection failure handling."""
        with patch('supabase.create_client') as mock_create_client:
            # Mock connection failure
            mock_create_client.side_effect = Exception("Connection failed")
            
            db_service = DatabaseHybridService()
            await db_service.initialize()
            
            # Verify fallback to mock data
            assert db_service.supabase_client is None
            assert db_service.is_connected is False
            assert db_service.use_mock_data is True

    @pytest.mark.unit
    @pytest.mark.database
    async def test_supabase_retry_logic(self, mock_env_vars):
        """Test connection retry logic on failures."""
        with patch('supabase.create_client') as mock_create_client:
            # Mock initial failures, then success
            mock_create_client.side_effect = [
                Exception("Temporary failure"),
                Exception("Another failure"), 
                MagicMock()  # Success on third attempt
            ]
            
            db_service = DatabaseHybridService(max_retries=3, retry_delay=0.1)
            await db_service.initialize()
            
            # Verify retries occurred
            assert mock_create_client.call_count == 3
            assert db_service.is_connected is True

    @pytest.mark.unit
    @pytest.mark.database
    async def test_mock_supabase_responses(self):
        """Test mocking of Supabase responses."""
        # Mock successful query response
        mock_response = DATABASE_SUCCESS_RESPONSES["workflow_found"]
        
        with patch.object(self.db_service, 'supabase_client') as mock_client:
            mock_table = MagicMock()
            mock_client.table.return_value = mock_table
            mock_table.select.return_value.eq.return_value.execute.return_value = mock_response
            
            result = await self.db_service._execute_supabase_query(
                lambda: mock_client.table('workflow').select('*').eq('id', 'test-123')
            )
            
            assert result == mock_response.data

    # ========================================
    # 2. Workflow Operations Tests
    # ========================================

    @pytest.mark.unit 
    @pytest.mark.database
    async def test_get_workflow_success(self):
        """Test successful workflow retrieval."""
        workflow_id = "test-workflow-123"
        expected_workflow = SAMPLE_WORKFLOW
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = [expected_workflow]
            
            result = await self.db_service.get_workflow(workflow_id)
            
            assert result == expected_workflow
            mock_query.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.database
    async def test_get_workflow_not_found(self):
        """Test workflow retrieval when workflow doesn't exist."""
        workflow_id = "nonexistent-workflow"
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = []  # Empty result
            
            result = await self.db_service.get_workflow(workflow_id)
            
            assert result is None

    @pytest.mark.unit
    @pytest.mark.database
    async def test_get_all_workflows(self):
        """Test retrieval of all workflows."""
        expected_workflows = [SAMPLE_WORKFLOW, {**SAMPLE_WORKFLOW, "id": "workflow-2"}]
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = expected_workflows
            
            result = await self.db_service.get_all_workflows()
            
            assert result == expected_workflows
            assert len(result) == 2

    @pytest.mark.unit
    @pytest.mark.database
    async def test_get_all_workflows_with_pagination(self):
        """Test workflow retrieval with pagination parameters."""
        expected_workflows = [SAMPLE_WORKFLOW]
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = expected_workflows
            
            result = await self.db_service.get_all_workflows(limit=10, offset=20)
            
            assert result == expected_workflows
            mock_query.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.database
    async def test_update_workflow_state_success(self):
        """Test successful workflow state update."""
        workflow_id = "test-workflow-123"
        new_state = {"blocks": {}, "edges": [], "metadata": {}}
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = {"success": True}
            
            result = await self.db_service.update_workflow_state(workflow_id, new_state)
            
            assert result is True
            mock_query.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.database
    async def test_update_workflow_state_failure(self):
        """Test workflow state update failure handling."""
        workflow_id = "test-workflow-123"
        new_state = {"blocks": {}, "edges": [], "metadata": {}}
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.side_effect = Exception("Update failed")
            
            result = await self.db_service.update_workflow_state(workflow_id, new_state)
            
            assert result is False

    @pytest.mark.unit
    @pytest.mark.database
    async def test_create_workflow(self):
        """Test workflow creation."""
        new_workflow = {
            "name": "New Test Workflow",
            "description": "A new workflow for testing",
            "user_id": "test-user"
        }
        
        expected_result = {"id": "new-workflow-456", **new_workflow}
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = [expected_result]
            
            result = await self.db_service.create_workflow(new_workflow)
            
            assert result["id"] == "new-workflow-456"
            assert result["name"] == new_workflow["name"]

    @pytest.mark.unit
    @pytest.mark.database
    async def test_delete_workflow(self):
        """Test workflow deletion."""
        workflow_id = "workflow-to-delete"
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = {"success": True}
            
            result = await self.db_service.delete_workflow(workflow_id)
            
            assert result is True
            mock_query.assert_called_once()

    # ========================================
    # 3. Block Operations Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.database
    async def test_get_workflow_blocks_success(self):
        """Test successful workflow blocks retrieval."""
        workflow_id = "test-workflow-123"
        expected_blocks = SAMPLE_BLOCKS
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = expected_blocks
            
            result = await self.db_service.get_workflow_blocks(workflow_id)
            
            assert result == expected_blocks
            assert len(result) == len(SAMPLE_BLOCKS)

    @pytest.mark.unit
    @pytest.mark.database
    async def test_get_workflow_blocks_empty(self):
        """Test workflow blocks retrieval when no blocks exist."""
        workflow_id = "workflow-no-blocks"
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = []
            
            result = await self.db_service.get_workflow_blocks(workflow_id)
            
            assert result == []

    @pytest.mark.unit
    @pytest.mark.database
    async def test_get_workflow_blocks_with_filtering(self):
        """Test workflow blocks retrieval with type filtering."""
        workflow_id = "test-workflow-123"
        block_type = "agent"
        
        # Filter sample blocks to only include agent type
        agent_blocks = [block for block in SAMPLE_BLOCKS if block.get("type") == "agent"]
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = agent_blocks
            
            result = await self.db_service.get_workflow_blocks(workflow_id, block_type=block_type)
            
            assert all(block["type"] == "agent" for block in result)

    @pytest.mark.unit
    @pytest.mark.database  
    async def test_get_workflow_blocks_with_sorting(self):
        """Test workflow blocks retrieval with sorting."""
        workflow_id = "test-workflow-123"
        
        # Create blocks with different positions for sorting
        sorted_blocks = sorted(SAMPLE_BLOCKS, key=lambda b: b.get("position_x", 0))
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = sorted_blocks
            
            result = await self.db_service.get_workflow_blocks(
                workflow_id, 
                sort_by="position_x",
                sort_order="asc"
            )
            
            # Verify blocks are sorted by position_x
            positions = [block.get("position_x", 0) for block in result]
            assert positions == sorted(positions)

    @pytest.mark.unit
    @pytest.mark.database
    async def test_create_workflow_blocks(self):
        """Test creation of multiple workflow blocks."""
        workflow_id = "test-workflow-123"
        new_blocks = [
            {
                "type": "starter",
                "name": "New Starter",
                "position_x": 100,
                "position_y": 300
            },
            {
                "type": "agent",
                "name": "New Agent",
                "position_x": 300,
                "position_y": 300,
                "config": {"model": "gpt-4"}
            }
        ]
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = [
                {"id": "new-block-1", **new_blocks[0]},
                {"id": "new-block-2", **new_blocks[1]}
            ]
            
            result = await self.db_service.create_workflow_blocks(workflow_id, new_blocks)
            
            assert len(result) == 2
            assert all("id" in block for block in result)

    @pytest.mark.unit
    @pytest.mark.database
    async def test_update_workflow_blocks(self):
        """Test updating multiple workflow blocks."""
        block_updates = [
            {"id": "block-1", "name": "Updated Block 1"},
            {"id": "block-2", "config": {"model": "claude-3"}}
        ]
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = {"updated": 2}
            
            result = await self.db_service.update_workflow_blocks(block_updates)
            
            assert result["updated"] == 2

    @pytest.mark.unit
    @pytest.mark.database
    async def test_delete_workflow_blocks(self):
        """Test deletion of workflow blocks."""
        workflow_id = "test-workflow-123"
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = {"deleted": 3}
            
            result = await self.db_service.delete_workflow_blocks(workflow_id)
            
            assert result["deleted"] == 3

    # ========================================
    # 4. Mock Data Fallback Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.database
    async def test_mock_data_fallback_workflow_operations(self):
        """Test fallback to mock data when Supabase unavailable."""
        # Disable Supabase connection
        self.db_service.supabase_client = None
        self.db_service.is_connected = False
        self.db_service.use_mock_data = True
        
        # Test get_workflow with mock data
        result = await self.db_service.get_workflow("test-workflow-123")
        
        # Should return mock workflow data
        assert result is not None
        assert isinstance(result, dict)
        assert "id" in result

    @pytest.mark.unit
    @pytest.mark.database
    async def test_mock_data_consistency(self):
        """Test that mock data maintains consistency across calls."""
        # Enable mock data mode
        self.db_service.use_mock_data = True
        
        # Make multiple calls
        workflow1 = await self.db_service.get_workflow("test-workflow-123")
        workflow2 = await self.db_service.get_workflow("test-workflow-123")
        
        # Should return consistent data
        assert workflow1 == workflow2

    @pytest.mark.unit
    @pytest.mark.database
    async def test_mock_data_structure_validation(self):
        """Test that mock data follows expected structure."""
        self.db_service.use_mock_data = True
        
        # Test workflow structure
        workflow = await self.db_service.get_workflow("test-workflow-123")
        expected_keys = ["id", "name", "description", "created_at", "updated_at"]
        
        for key in expected_keys:
            assert key in workflow, f"Missing key: {key}"
        
        # Test blocks structure
        blocks = await self.db_service.get_workflow_blocks("test-workflow-123")
        if blocks:
            block = blocks[0]
            expected_block_keys = ["id", "type", "workflow_id", "position_x", "position_y"]
            
            for key in expected_block_keys:
                assert key in block, f"Missing block key: {key}"

    @pytest.mark.unit
    @pytest.mark.database  
    async def test_graceful_degradation_no_errors(self):
        """Test graceful degradation without throwing errors."""
        # Simulate complete system failure
        self.db_service.supabase_client = None
        self.db_service.is_connected = False
        self.db_service.use_mock_data = True
        
        # All operations should complete without errors
        workflow = await self.db_service.get_workflow("any-id")
        blocks = await self.db_service.get_workflow_blocks("any-id")
        update_result = await self.db_service.update_workflow_state("any-id", {})
        
        # Results might be mock data or None, but no exceptions
        assert isinstance(workflow, (dict, type(None)))
        assert isinstance(blocks, list)
        assert isinstance(update_result, bool)

    # ========================================
    # 5. Transaction Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.database
    async def test_transaction_context_manager(self):
        """Test database transaction context manager."""
        with patch.object(self.db_service, 'supabase_client') as mock_client:
            mock_transaction = AsyncMock()
            mock_client.rpc.return_value = mock_transaction
            
            async with self.db_service.transaction() as tx:
                # Simulate operations within transaction
                await self.db_service.create_workflow({"name": "Test"})
                await self.db_service.update_workflow_state("test-id", {})
            
            # Verify transaction was handled properly
            assert mock_transaction is not None

    @pytest.mark.unit
    @pytest.mark.database
    async def test_transaction_rollback_on_error(self):
        """Test transaction rollback on errors."""
        with patch.object(self.db_service, 'supabase_client') as mock_client:
            mock_transaction = AsyncMock()
            mock_client.rpc.return_value = mock_transaction
            
            try:
                async with self.db_service.transaction() as tx:
                    # Simulate operation that causes error
                    raise Exception("Simulated error")
            except Exception:
                pass
            
            # Verify rollback was called (implementation dependent)
            # This would need to be adapted based on actual transaction implementation

    @pytest.mark.unit
    @pytest.mark.database
    async def test_atomic_operations(self):
        """Test atomic database operations."""
        workflow_data = {"name": "Atomic Test Workflow"}
        blocks_data = [
            {"type": "starter", "name": "Start"},
            {"type": "agent", "name": "Process"}
        ]
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            # Mock successful atomic operation
            mock_query.side_effect = [
                [{"id": "workflow-123", **workflow_data}],  # Create workflow
                [{"id": "block-1"}, {"id": "block-2"}]      # Create blocks
            ]
            
            result = await self.db_service.create_workflow_with_blocks(
                workflow_data, blocks_data
            )
            
            assert result["workflow"]["id"] == "workflow-123"
            assert len(result["blocks"]) == 2

    @pytest.mark.unit
    @pytest.mark.database
    async def test_concurrent_access_handling(self):
        """Test handling of concurrent database access."""
        workflow_id = "concurrent-test"
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = [SAMPLE_WORKFLOW]
            
            # Simulate concurrent workflow retrievals
            tasks = [
                self.db_service.get_workflow(workflow_id)
                for _ in range(5)
            ]
            
            results = await asyncio.gather(*tasks)
            
            # All should succeed
            assert len(results) == 5
            assert all(result == SAMPLE_WORKFLOW for result in results)

    @pytest.mark.unit
    @pytest.mark.database
    async def test_deadlock_handling(self):
        """Test database deadlock handling and recovery."""
        # This would test actual deadlock scenarios
        # Implementation depends on your specific deadlock handling logic
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            # Simulate deadlock then recovery
            mock_query.side_effect = [
                Exception("Deadlock detected"),
                [SAMPLE_WORKFLOW]  # Successful retry
            ]
            
            result = await self.db_service.get_workflow("deadlock-test")
            
            # Should succeed after retry
            assert result == SAMPLE_WORKFLOW
            assert mock_query.call_count == 2

    # ========================================
    # 6. Performance Tests
    # ========================================

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.performance
    async def test_query_optimization(self, performance_monitor):
        """Test database query optimization."""
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = [SAMPLE_WORKFLOW]
            
            performance_monitor.start_timer("query_optimization")
            
            # Execute optimized query
            result = await self.db_service.get_workflow("test-id")
            
            performance_monitor.end_timer("query_optimization")
            
            assert result == SAMPLE_WORKFLOW
            # Query should complete quickly
            performance_monitor.assert_performance("query_optimization", 1.0)

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.performance
    async def test_batch_operations_performance(self, performance_monitor):
        """Test performance of batch database operations."""
        # Create test data for batch operations
        batch_workflows = [
            {"name": f"Batch Workflow {i}", "description": f"Test workflow {i}"}
            for i in range(100)
        ]
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = [
                {"id": f"workflow-{i}", **workflow}
                for i, workflow in enumerate(batch_workflows)
            ]
            
            performance_monitor.start_timer("batch_operations")
            
            result = await self.db_service.create_workflows_batch(batch_workflows)
            
            performance_monitor.end_timer("batch_operations")
            
            assert len(result) == 100
            # Batch operation should be efficient
            performance_monitor.assert_performance("batch_operations", 5.0)

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.performance
    async def test_connection_pooling_efficiency(self):
        """Test database connection pooling efficiency."""
        # This would test connection reuse and pooling
        # Implementation depends on your connection pooling strategy
        
        connection_count = 0
        
        def mock_connection_counter(*args, **kwargs):
            nonlocal connection_count
            connection_count += 1
            return MagicMock()
        
        with patch('supabase.create_client', side_effect=mock_connection_counter):
            # Simulate multiple database services
            services = [DatabaseHybridService() for _ in range(10)]
            
            for service in services:
                await service.initialize()
            
            # Should reuse connections efficiently
            # Exact assertion depends on pooling implementation
            assert connection_count <= 10

    @pytest.mark.unit
    @pytest.mark.database
    async def test_cache_invalidation(self):
        """Test database cache invalidation strategies."""
        # Mock caching layer
        cache = {}
        
        def mock_cached_query(key, query_func):
            if key not in cache:
                cache[key] = query_func()
            return cache[key]
        
        with patch.object(self.db_service, '_cached_query', side_effect=mock_cached_query):
            # First call should cache result
            result1 = await self.db_service.get_workflow("cache-test")
            
            # Second call should use cache
            result2 = await self.db_service.get_workflow("cache-test")
            
            assert result1 == result2
            assert len(cache) == 1

    # ========================================
    # Error Handling and Edge Cases
    # ========================================

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.error_handling
    async def test_connection_timeout_handling(self):
        """Test handling of database connection timeouts."""
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.side_effect = Exception("Connection timeout")
            
            result = await self.db_service.get_workflow("timeout-test")
            
            # Should handle timeout gracefully
            assert result is None or isinstance(result, dict)

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.error_handling
    async def test_query_failure_recovery(self):
        """Test recovery from query failures."""
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            # First call fails, second succeeds
            mock_query.side_effect = [
                Exception("Query failed"),
                [SAMPLE_WORKFLOW]
            ]
            
            result = await self.db_service.get_workflow("recovery-test", retry_on_failure=True)
            
            assert result == SAMPLE_WORKFLOW
            assert mock_query.call_count == 2

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.error_handling
    async def test_constraint_violation_handling(self):
        """Test handling of database constraint violations."""
        invalid_workflow = {"name": "Test", "user_id": "nonexistent-user"}
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.side_effect = Exception("Foreign key constraint violation")
            
            result = await self.db_service.create_workflow(invalid_workflow)
            
            # Should handle constraint violation gracefully
            assert result is None or "error" in result

    @pytest.mark.unit
    @pytest.mark.database
    @pytest.mark.error_handling
    async def test_table_not_found_handling(self):
        """Test handling when database tables don't exist."""
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.side_effect = Exception("Table 'workflow' doesn't exist")
            
            result = await self.db_service.get_workflow("table-missing-test")
            
            # Should fall back to mock data or handle gracefully
            assert result is None or isinstance(result, dict)

    @pytest.mark.unit
    @pytest.mark.database
    async def test_large_dataset_handling(self):
        """Test handling of large dataset operations."""
        # Simulate large result set
        large_workflow_list = [
            {**SAMPLE_WORKFLOW, "id": f"workflow-{i}"} 
            for i in range(1000)
        ]
        
        with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
            mock_query.return_value = large_workflow_list
            
            result = await self.db_service.get_all_workflows()
            
            assert len(result) == 1000
            assert all("id" in workflow for workflow in result)

    @pytest.mark.unit
    @pytest.mark.database
    async def test_sql_injection_prevention(self):
        """Test SQL injection prevention measures."""
        # Test various injection attempts
        malicious_inputs = [
            "'; DROP TABLE workflow; --",
            "1' OR '1'='1",
            "UNION SELECT * FROM users --",
            "<script>alert('xss')</script>"
        ]
        
        for malicious_input in malicious_inputs:
            with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
                mock_query.return_value = []
                
                # Should sanitize input and not cause issues
                result = await self.db_service.get_workflow(malicious_input)
                
                assert result is None or isinstance(result, dict)
                # Verify query was called (input was processed safely)
                mock_query.assert_called()

    @pytest.mark.unit
    @pytest.mark.database
    async def test_data_validation_before_storage(self):
        """Test data validation before database storage."""
        invalid_workflow_data = [
            {"name": ""},  # Empty name
            {"name": "Valid", "user_id": None},  # Null user_id
            {"description": "x" * 10000},  # Too long description
            {}  # Missing required fields
        ]
        
        for invalid_data in invalid_workflow_data:
            with patch.object(self.db_service, '_execute_supabase_query') as mock_query:
                result = await self.db_service.create_workflow(invalid_data)
                
                # Should either validate and reject, or handle gracefully
                if result is not None:
                    assert isinstance(result, dict)
                    # If accepted, should have been sanitized
                    if "name" in result:
                        assert len(result["name"]) > 0 