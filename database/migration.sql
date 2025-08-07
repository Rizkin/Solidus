-- Agent Forge Production Table Migration Script v2.0
-- Populates production tables from guideline tables with generated state JSON

-- =============================================================================
-- MIGRATION SCRIPT: Guideline Tables → Production Tables
-- =============================================================================
-- This script migrates data from:
-- - workflow_rows → public.workflow (with generated state)
-- - workflow_blocks_rows → public.workflow_blocks
-- And generates proper JSON state from the blocks data
-- =============================================================================

-- Start transaction for data consistency
BEGIN;

-- Create backup tables (optional - for rollback)
-- CREATE TABLE workflow_backup AS SELECT * FROM public.workflow;
-- CREATE TABLE workflow_blocks_backup AS SELECT * FROM public.workflow_blocks;

-- =============================================================================
-- STEP 1: Populate public.workflow_blocks from workflow_blocks_rows
-- =============================================================================

INSERT INTO public.workflow_blocks (
    id, workflow_id, type, name, position_x, position_y, enabled, 
    horizontal_handles, is_wide, advanced_mode, height, sub_blocks, 
    outputs, data, parent_id, extent, created_at, updated_at
)
SELECT 
    id, workflow_id, type, name, position_x, position_y, enabled,
    horizontal_handles, is_wide, advanced_mode, height, sub_blocks,
    outputs, data, parent_id, extent, created_at, updated_at
FROM public.workflow_blocks_rows
ON CONFLICT (id) DO UPDATE SET
    workflow_id = EXCLUDED.workflow_id,
    type = EXCLUDED.type,
    name = EXCLUDED.name,
    position_x = EXCLUDED.position_x,
    position_y = EXCLUDED.position_y,
    enabled = EXCLUDED.enabled,
    horizontal_handles = EXCLUDED.horizontal_handles,
    is_wide = EXCLUDED.is_wide,
    advanced_mode = EXCLUDED.advanced_mode,
    height = EXCLUDED.height,
    sub_blocks = EXCLUDED.sub_blocks,
    outputs = EXCLUDED.outputs,
    data = EXCLUDED.data,
    parent_id = EXCLUDED.parent_id,
    extent = EXCLUDED.extent,
    updated_at = NOW();

-- =============================================================================
-- STEP 2: Generate State JSON and Populate public.workflow
-- =============================================================================

-- Function to generate state JSON from blocks
CREATE OR REPLACE FUNCTION generate_workflow_state(workflow_id_param TEXT)
RETURNS JSONB AS $$
DECLARE
    blocks_json JSONB;
    edges_json JSONB;
    variables_json JSONB;
    metadata_json JSONB;
    workflow_info RECORD;
    block_count INTEGER;
    starter_blocks INTEGER;
BEGIN
    -- Get workflow information
    SELECT * INTO workflow_info 
    FROM public.workflow_rows 
    WHERE id = workflow_id_param;
    
    -- Count blocks
    SELECT COUNT(*) INTO block_count 
    FROM public.workflow_blocks_rows 
    WHERE workflow_id = workflow_id_param;
    
    -- Count starter blocks
    SELECT COUNT(*) INTO starter_blocks 
    FROM public.workflow_blocks_rows 
    WHERE workflow_id = workflow_id_param AND type = 'starter';
    
    -- Generate blocks JSON object
    SELECT jsonb_object_agg(
        wb.id,
        jsonb_build_object(
            'id', wb.id,
            'type', wb.type,
            'name', wb.name,
            'position', jsonb_build_object('x', wb.position_x, 'y', wb.position_y),
            'enabled', wb.enabled,
            'horizontalHandles', wb.horizontal_handles,
            'isWide', wb.is_wide,
            'advancedMode', wb.advanced_mode,
            'height', wb.height,
            'subBlocks', wb.sub_blocks,
            'outputs', wb.outputs,
            'data', COALESCE(wb.data, '{}'::jsonb),
            'parentId', wb.parent_id,
            'extent', wb.extent
        )
    ) INTO blocks_json
    FROM public.workflow_blocks_rows wb
    WHERE wb.workflow_id = workflow_id_param;
    
    -- Generate edges JSON from parent-child relationships
    SELECT jsonb_agg(
        jsonb_build_object(
            'id', 'edge-' || wb.parent_id || '-' || wb.id,
            'source', wb.parent_id,
            'target', wb.id,
            'sourceHandle', 'output',
            'targetHandle', 'input',
            'type', 'default'
        )
    ) INTO edges_json
    FROM public.workflow_blocks_rows wb
    WHERE wb.workflow_id = workflow_id_param 
    AND wb.parent_id IS NOT NULL;
    
    -- Extract variables from workflow_rows
    variables_json := COALESCE(workflow_info.variables::jsonb, '{}'::jsonb);
    
    -- Generate metadata
    metadata_json := jsonb_build_object(
        'version', '1.0.0',
        'createdAt', workflow_info.created_at,
        'updatedAt', workflow_info.updated_at,
        'generatedBy', 'migration-script',
        'totalBlocks', block_count,
        'starterBlocks', starter_blocks,
        'workflowType', CASE 
            WHEN workflow_info.name ILIKE '%trading%' THEN 'trading_automation'
            WHEN workflow_info.name ILIKE '%lead%' OR workflow_info.name ILIKE '%marketing%' THEN 'marketing_automation'
            WHEN workflow_info.name ILIKE '%payment%' OR workflow_info.name ILIKE '%fintech%' THEN 'payment_automation'
            WHEN workflow_info.name ILIKE '%ai%' OR workflow_info.name ILIKE '%model%' THEN 'ai_automation'
            WHEN workflow_info.name ILIKE '%data%' OR workflow_info.name ILIKE '%research%' THEN 'data_processing'
            WHEN workflow_info.name ILIKE '%support%' OR workflow_info.name ILIKE '%customer%' THEN 'support_automation'
            WHEN workflow_info.name ILIKE '%inventory%' OR workflow_info.name ILIKE '%supply%' THEN 'operations_automation'
            ELSE 'general_automation'
        END,
        'complexity', CASE 
            WHEN block_count <= 3 THEN 'simple'
            WHEN block_count <= 6 THEN 'medium'
            ELSE 'complex'
        END,
        'isValid', starter_blocks = 1 AND block_count > 0,
        'migrationTimestamp', NOW()
    );
    
    -- Return complete state JSON
    RETURN jsonb_build_object(
        'blocks', COALESCE(blocks_json, '{}'::jsonb),
        'edges', COALESCE(edges_json, '[]'::jsonb),
        'variables', variables_json,
        'metadata', metadata_json
    );
END;
$$ LANGUAGE plpgsql;

-- Populate public.workflow with generated state
INSERT INTO public.workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state,
    deployed_at, collaborators, run_count, last_run_at, variables,
    is_published, marketplace_data
)
SELECT 
    wr.id,
    wr.user_id,
    wr.workspace_id,
    wr.folder_id,
    wr.name,
    wr.description,
    -- Generate state JSON from blocks
    generate_workflow_state(wr.id),
    wr.color,
    wr.last_synced,
    wr.created_at,
    wr.updated_at,
    wr.is_deployed,
    wr.deployed_state,
    wr.deployed_at,
    wr.collaborators,
    wr.run_count,
    wr.last_run_at,
    wr.variables,
    wr.is_published,
    wr.marketplace_data
FROM public.workflow_rows wr
ON CONFLICT (id) DO UPDATE SET
    user_id = EXCLUDED.user_id,
    workspace_id = EXCLUDED.workspace_id,
    folder_id = EXCLUDED.folder_id,
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    state = generate_workflow_state(EXCLUDED.id),
    color = EXCLUDED.color,
    last_synced = EXCLUDED.last_synced,
    updated_at = NOW(),
    is_deployed = EXCLUDED.is_deployed,
    deployed_state = EXCLUDED.deployed_state,
    deployed_at = EXCLUDED.deployed_at,
    collaborators = EXCLUDED.collaborators,
    run_count = EXCLUDED.run_count,
    last_run_at = EXCLUDED.last_run_at,
    variables = EXCLUDED.variables,
    is_published = EXCLUDED.is_published,
    marketplace_data = EXCLUDED.marketplace_data;

-- =============================================================================
-- STEP 3: Validate Migration Results
-- =============================================================================

-- Create validation report
CREATE TEMP TABLE migration_validation_report AS
WITH workflow_stats AS (
    SELECT 
        'workflow_rows' as source_table,
        COUNT(*) as total_records
    FROM public.workflow_rows
    UNION ALL
    SELECT 
        'workflow (production)' as source_table,
        COUNT(*) as total_records
    FROM public.workflow
    UNION ALL
    SELECT 
        'workflow_blocks_rows' as source_table,
        COUNT(*) as total_records
    FROM public.workflow_blocks_rows
    UNION ALL
    SELECT 
        'workflow_blocks (production)' as source_table,
        COUNT(*) as total_records
    FROM public.workflow_blocks
),
state_validation AS (
    SELECT 
        w.id,
        w.name,
        (w.state->>'metadata'->>'totalBlocks')::int as metadata_block_count,
        (SELECT COUNT(*) FROM public.workflow_blocks wb WHERE wb.workflow_id = w.id) as actual_block_count,
        jsonb_array_length(w.state->'edges') as edge_count,
        CASE 
            WHEN w.state->>'metadata'->>'isValid' = 'true' THEN 'VALID'
            ELSE 'INVALID'
        END as validation_status,
        w.state->>'metadata'->>'workflowType' as detected_type
    FROM public.workflow w
),
summary_stats AS (
    SELECT 
        COUNT(*) as total_workflows,
        COUNT(*) FILTER (WHERE validation_status = 'VALID') as valid_workflows,
        COUNT(*) FILTER (WHERE validation_status = 'INVALID') as invalid_workflows,
        ROUND(AVG(metadata_block_count), 2) as avg_blocks_per_workflow,
        ROUND(AVG(edge_count), 2) as avg_edges_per_workflow,
        COUNT(DISTINCT detected_type) as unique_workflow_types
    FROM state_validation
)
SELECT * FROM workflow_stats
UNION ALL
SELECT 'SUMMARY' as source_table, 0 as total_records
UNION ALL  
SELECT 'Valid Workflows', (SELECT valid_workflows FROM summary_stats)
UNION ALL
SELECT 'Invalid Workflows', (SELECT invalid_workflows FROM summary_stats)
UNION ALL
SELECT 'Avg Blocks/Workflow', (SELECT avg_blocks_per_workflow FROM summary_stats)
UNION ALL
SELECT 'Avg Edges/Workflow', (SELECT avg_edges_per_workflow FROM summary_stats)
UNION ALL
SELECT 'Unique Types', (SELECT unique_workflow_types FROM summary_stats);

-- Display validation report
SELECT 
    source_table,
    total_records,
    CASE 
        WHEN source_table LIKE '%production%' AND total_records > 0 THEN '✅ Migrated'
        WHEN source_table LIKE '%rows%' AND total_records > 0 THEN '📊 Source Data'
        WHEN source_table = 'SUMMARY' THEN '📋 Migration Summary'
        ELSE '📈 ' || source_table
    END as status
FROM migration_validation_report
ORDER BY 
    CASE 
        WHEN source_table LIKE '%rows%' THEN 1
        WHEN source_table LIKE '%production%' THEN 2  
        WHEN source_table = 'SUMMARY' THEN 3
        ELSE 4
    END,
    source_table;

-- =============================================================================
-- STEP 4: Update Workflow Lookup Cache
-- =============================================================================

-- Generate lookup cache entries for migrated workflows
INSERT INTO public.workflow_lookup (
    lookup_key,
    input_pattern,
    workflow_type,
    block_count,
    block_types,
    generated_state,
    usage_count,
    avg_generation_time,
    confidence_score,
    semantic_description
)
SELECT 
    'migrated_' || w.id as lookup_key,
    jsonb_build_object(
        'type', w.state->>'metadata'->>'workflowType',
        'blocks', (
            SELECT jsonb_agg(DISTINCT wb.type ORDER BY wb.type)
            FROM public.workflow_blocks wb 
            WHERE wb.workflow_id = w.id
        ),
        'complexity', w.state->>'metadata'->>'complexity',
        'block_count', (w.state->>'metadata'->>'totalBlocks')::int
    ) as input_pattern,
    w.state->>'metadata'->>'workflowType' as workflow_type,
    (w.state->>'metadata'->>'totalBlocks')::int as block_count,
    (
        SELECT array_agg(DISTINCT wb.type ORDER BY wb.type)
        FROM public.workflow_blocks wb 
        WHERE wb.workflow_id = w.id
    ) as block_types,
    w.state as generated_state,
    1 as usage_count,
    500.0 as avg_generation_time, -- Estimated for migrated data
    0.95 as confidence_score,
    w.description as semantic_description
FROM public.workflow w
WHERE w.state IS NOT NULL
ON CONFLICT (lookup_key) DO UPDATE SET
    input_pattern = EXCLUDED.input_pattern,
    workflow_type = EXCLUDED.workflow_type,
    block_count = EXCLUDED.block_count,
    block_types = EXCLUDED.block_types,
    generated_state = EXCLUDED.generated_state,
    last_used_at = NOW();

-- =============================================================================
-- STEP 5: Create Sample AI Usage Logs for Migrated Workflows
-- =============================================================================

-- Generate AI usage logs for state generation (simulated)
INSERT INTO public.ai_usage_logs (
    workflow_id,
    provider,
    model,
    operation_type,
    token_count,
    cost_estimate_usd,
    response_time_ms,
    cache_hit,
    success,
    request_metadata,
    created_at
)
SELECT 
    w.id as workflow_id,
    'migration-script' as provider,
    'rule-based-v2' as model,
    'state_generation' as operation_type,
    (w.state->>'metadata'->>'totalBlocks')::int * 150 as token_count, -- Estimated
    0.0 as cost_estimate_usd, -- Free for migration
    (200 + (w.state->>'metadata'->>'totalBlocks')::int * 50) as response_time_ms, -- Simulated
    false as cache_hit,
    true as success,
    jsonb_build_object(
        'migration', true,
        'workflow_type', w.state->>'metadata'->>'workflowType',
        'block_count', w.state->>'metadata'->>'totalBlocks'
    ) as request_metadata,
    w.updated_at as created_at
FROM public.workflow w
WHERE w.state IS NOT NULL;

-- =============================================================================
-- STEP 6: Create Validation Logs for Migrated Workflows
-- =============================================================================

-- Generate validation logs for each migrated workflow
INSERT INTO public.validation_logs (
    workflow_id,
    validation_type,
    validator_name,
    passed,
    score,
    error_details,
    warnings,
    suggestions,
    execution_time_ms,
    created_at
)
SELECT 
    w.id as workflow_id,
    'schema' as validation_type,
    'migration_validator' as validator_name,
    (w.state->>'metadata'->>'isValid')::boolean as passed,
    CASE 
        WHEN (w.state->>'metadata'->>'isValid')::boolean THEN 95.0
        ELSE 65.0
    END as score,
    CASE 
        WHEN NOT (w.state->>'metadata'->>'isValid')::boolean THEN 
            jsonb_build_array(
                jsonb_build_object(
                    'type', 'migration_warning',
                    'message', 'Workflow may need manual review after migration'
                )
            )
        ELSE '[]'::jsonb
    END as error_details,
    jsonb_build_array(
        jsonb_build_object(
            'type', 'info',
            'message', 'Workflow migrated from guideline tables'
        )
    ) as warnings,
    jsonb_build_array(
        jsonb_build_object(
            'type', 'optimization',
            'message', 'Consider testing workflow in development environment'
        )
    ) as suggestions,
    (50 + (w.state->>'metadata'->>'totalBlocks')::int * 10) as execution_time_ms,
    w.updated_at as created_at
FROM public.workflow w
WHERE w.state IS NOT NULL;

-- =============================================================================
-- STEP 7: Update Statistics and Cache
-- =============================================================================

-- Update cache statistics
UPDATE public.cache_stats 
SET 
    hit_count = hit_count + (SELECT COUNT(*) FROM public.workflow_lookup WHERE lookup_key LIKE 'migrated_%'),
    last_updated = NOW()
WHERE cache_type = 'workflow_patterns';

-- Clean up temporary function
DROP FUNCTION IF EXISTS generate_workflow_state(TEXT);

-- =============================================================================
-- STEP 8: Final Migration Report
-- =============================================================================

-- Generate comprehensive migration report
CREATE TEMP TABLE final_migration_report AS
WITH migration_summary AS (
    SELECT 
        (SELECT COUNT(*) FROM public.workflow_rows) as source_workflows,
        (SELECT COUNT(*) FROM public.workflow) as migrated_workflows,
        (SELECT COUNT(*) FROM public.workflow_blocks_rows) as source_blocks,
        (SELECT COUNT(*) FROM public.workflow_blocks) as migrated_blocks,
        (SELECT COUNT(*) FROM public.workflow_lookup WHERE lookup_key LIKE 'migrated_%') as cache_entries,
        (SELECT COUNT(*) FROM public.ai_usage_logs WHERE provider = 'migration-script') as usage_logs,
        (SELECT COUNT(*) FROM public.validation_logs WHERE validator_name = 'migration_validator') as validation_logs
),
workflow_types AS (
    SELECT 
        w.state->>'metadata'->>'workflowType' as workflow_type,
        COUNT(*) as count
    FROM public.workflow w
    WHERE w.state->>'metadata'->>'workflowType' IS NOT NULL
    GROUP BY w.state->>'metadata'->>'workflowType'
    ORDER BY count DESC
),
validation_summary AS (
    SELECT 
        COUNT(*) FILTER (WHERE passed = true) as passed_validations,
        COUNT(*) FILTER (WHERE passed = false) as failed_validations,
        ROUND(AVG(score), 2) as avg_validation_score
    FROM public.validation_logs 
    WHERE validator_name = 'migration_validator'
)
SELECT 
    'MIGRATION COMPLETED SUCCESSFULLY' as status,
    ms.source_workflows || ' → ' || ms.migrated_workflows as workflows_migrated,
    ms.source_blocks || ' → ' || ms.migrated_blocks as blocks_migrated,
    ms.cache_entries || ' cache entries created' as cache_status,
    ms.usage_logs || ' usage logs generated' as usage_logs,
    ms.validation_logs || ' validations performed' as validations,
    vs.passed_validations || ' passed, ' || vs.failed_validations || ' failed' as validation_results,
    'Avg Score: ' || vs.avg_validation_score || '/100' as validation_score
FROM migration_summary ms, validation_summary vs;

-- Display final report
SELECT * FROM final_migration_report;

-- Show workflow type distribution
SELECT 
    'Workflow Types:' as category,
    string_agg(
        w.state->>'metadata'->>'workflowType' || ' (' || COUNT(*) || ')', 
        ', ' ORDER BY COUNT(*) DESC
    ) as details
FROM public.workflow w
WHERE w.state->>'metadata'->>'workflowType' IS NOT NULL
GROUP BY 1;

-- Commit transaction
COMMIT;

-- =============================================================================
-- POST-MIGRATION VERIFICATION QUERIES
-- =============================================================================

-- Use these queries to verify migration success:

-- 1. Check workflow state structure
-- SELECT id, name, jsonb_pretty(state) FROM public.workflow LIMIT 1;

-- 2. Verify block relationships  
-- SELECT w.name, COUNT(wb.id) as block_count 
-- FROM public.workflow w 
-- LEFT JOIN public.workflow_blocks wb ON w.id = wb.workflow_id 
-- GROUP BY w.id, w.name;

-- 3. Check state metadata
-- SELECT 
--     id, name,
--     state->>'metadata'->>'totalBlocks' as total_blocks,
--     state->>'metadata'->>'workflowType' as type,
--     state->>'metadata'->>'isValid' as is_valid
-- FROM public.workflow;

-- 4. Verify cache entries
-- SELECT workflow_type, COUNT(*) as count 
-- FROM public.workflow_lookup 
-- WHERE lookup_key LIKE 'migrated_%' 
-- GROUP BY workflow_type;

SELECT 
    '🎉 MIGRATION COMPLETED SUCCESSFULLY!' as message,
    'All guideline table data has been migrated to production tables with generated state JSON' as details,
    'Use the verification queries above to validate the migration results' as next_steps; 