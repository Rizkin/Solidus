-- scripts/create_tables.sql
-- Agent Forge Workflow State Generator Database Schema
-- Matches EXACT structure from CSV files

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS workflow_blocks CASCADE;
DROP TABLE IF EXISTS workflow CASCADE;

-- Create workflow table (from workflow_rows.csv structure)
CREATE TABLE workflow (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    workspace_id TEXT,
    folder_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    state JSON NOT NULL,
    color TEXT NOT NULL DEFAULT '#3972F6',
    last_synced TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    is_deployed BOOLEAN NOT NULL DEFAULT FALSE,
    deployed_state JSON,
    deployed_at TIMESTAMP WITHOUT TIME ZONE,
    collaborators JSON NOT NULL DEFAULT '[]'::json,
    run_count INTEGER NOT NULL DEFAULT 0,
    last_run_at TIMESTAMP WITHOUT TIME ZONE,
    variables JSON DEFAULT '{}'::json,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    marketplace_data JSON
);

-- Create workflow_blocks table (from workflow_blocks_rows.csv structure)
CREATE TABLE workflow_blocks (
    id TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    type TEXT NOT NULL,
    name TEXT NOT NULL,
    position_x NUMERIC NOT NULL,
    position_y NUMERIC NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    horizontal_handles BOOLEAN NOT NULL DEFAULT TRUE,
    is_wide BOOLEAN NOT NULL DEFAULT FALSE,
    advanced_mode BOOLEAN NOT NULL DEFAULT FALSE,
    height NUMERIC NOT NULL DEFAULT 0,
    sub_blocks JSONB NOT NULL DEFAULT '{}'::jsonb,
    outputs JSONB NOT NULL DEFAULT '{}'::jsonb,
    data JSONB DEFAULT '{}'::jsonb,
    parent_id TEXT,
    extent TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT workflow_blocks_workflow_id_fk 
        FOREIGN KEY (workflow_id) 
        REFERENCES workflow(id) 
        ON DELETE CASCADE
);

-- Create indexes for performance
CREATE INDEX idx_workflow_blocks_workflow_id ON workflow_blocks(workflow_id);
CREATE INDEX idx_workflow_blocks_type ON workflow_blocks(type);
CREATE INDEX idx_workflow_blocks_parent_id ON workflow_blocks(parent_id);
CREATE INDEX idx_workflow_user_id ON workflow(user_id);
CREATE INDEX idx_workflow_workspace_id ON workflow(workspace_id);
CREATE INDEX idx_workflow_is_published ON workflow(is_published);

-- Grant permissions
GRANT ALL ON workflow TO postgres;
GRANT ALL ON workflow_blocks TO postgres;
