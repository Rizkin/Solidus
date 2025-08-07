-- Agent Forge Database Migration Script
-- Migrate data from guideline tables to production tables

-- First, let's clear any existing data in production tables (for clean population)
-- WARNING: Only run this in development environments
-- TRUNCATE public.workflow_blocks, public.workflow RESTART IDENTITY CASCADE;

-- Copy from workflow_rows to public.workflow
INSERT INTO public.workflow (
    id, 
    name, 
    description, 
    user_id, 
    workspace_id, 
    folder_id, 
    state,
    color,
    last_synced,
    created_at,
    updated_at,
    is_deployed,
    deployed_state,
    deployed_at,
    collaborators,
    run_count,
    last_run_at,
    variables,
    is_published,
    marketplace_data
)
SELECT 
    id, 
    name, 
    description, 
    user_id, 
    workspace_id, 
    folder_id,
    -- Generate state JSON from blocks
    jsonb_build_object(
        'blocks', (
            SELECT jsonb_object_agg(
                b.id,
                jsonb_build_object(
                    'id', b.id,
                    'type', b.type,
                    'name', b.name,
                    'position', jsonb_build_object('x', b.position_x, 'y', b.position_y),
                    'data', b.data,
                    'outputs', b.outputs,
                    'subBlocks', b.sub_blocks,
                    'enabled', b.enabled,
                    'horizontalHandles', b.horizontal_handles,
                    'isWide', b.is_wide,
                    'advancedMode', b.advanced_mode,
                    'height', b.height
                )
            )
            FROM workflow_blocks_rows b
            WHERE b.workflow_id = workflow_rows.id
        ),
        'edges', '[]'::jsonb,  -- Empty edges array for now
        'variables', variables::jsonb,
        'metadata', jsonb_build_object(
            'version', '1.0.0',
            'createdAt', created_at,
            'updatedAt', updated_at
        )
    ) as state,
    color,
    last_synced,
    created_at,
    updated_at,
    is_deployed,
    deployed_state,
    deployed_at,
    collaborators,
    run_count,
    last_run_at,
    variables,
    is_published,
    marketplace_data
FROM workflow_rows
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    user_id = EXCLUDED.user_id,
    workspace_id = EXCLUDED.workspace_id,
    folder_id = EXCLUDED.folder_id,
    state = EXCLUDED.state,
    color = EXCLUDED.color,
    last_synced = EXCLUDED.last_synced,
    created_at = EXCLUDED.created_at,
    updated_at = EXCLUDED.updated_at,
    is_deployed = EXCLUDED.is_deployed,
    deployed_state = EXCLUDED.deployed_state,
    deployed_at = EXCLUDED.deployed_at,
    collaborators = EXCLUDED.collaborators,
    run_count = EXCLUDED.run_count,
    last_run_at = EXCLUDED.last_run_at,
    variables = EXCLUDED.variables,
    is_published = EXCLUDED.is_published,
    marketplace_data = EXCLUDED.marketplace_data;

-- Copy from workflow_blocks_rows to public.workflow_blocks
INSERT INTO public.workflow_blocks (
    id,
    workflow_id,
    type,
    name,
    position_x,
    position_y,
    enabled,
    horizontal_handles,
    is_wide,
    advanced_mode,
    height,
    sub_blocks,
    outputs,
    data,
    parent_id,
    extent,
    created_at,
    updated_at
)
SELECT 
    id,
    workflow_id,
    type,
    name,
    position_x,
    position_y,
    enabled,
    horizontal_handles,
    is_wide,
    advanced_mode,
    height,
    sub_blocks,
    outputs,
    data,
    parent_id,
    extent,
    created_at,
    updated_at
FROM workflow_blocks_rows
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
    created_at = EXCLUDED.created_at,
    updated_at = EXCLUDED.updated_at;

-- Verify the data was copied correctly
-- Count records in each table
SELECT 
    (SELECT COUNT(*) FROM public.workflow) as workflow_count,
    (SELECT COUNT(*) FROM workflow_rows) as workflow_rows_count,
    (SELECT COUNT(*) FROM public.workflow_blocks) as workflow_blocks_count,
    (SELECT COUNT(*) FROM workflow_blocks_rows) as workflow_blocks_rows_count;

-- Show sample data from production tables
SELECT 'workflow' as table_name, id, name FROM public.workflow LIMIT 5
UNION ALL
SELECT 'workflow_blocks' as table_name, id, name FROM public.workflow_blocks LIMIT 5; 