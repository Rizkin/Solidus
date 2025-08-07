-- Agent Forge State Generator - Database Schema
-- Complete schema with all tables, relationships, and indexes

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Core workflow table (Agent Forge compatible)
CREATE TABLE public.workflow (
    id text PRIMARY KEY,
    user_id text NOT NULL,
    workspace_id text NULL,
    folder_id text NULL,
    name text NOT NULL,
    description text NULL,
    state json NOT NULL,
    color text NOT NULL DEFAULT '#3972F6',
    last_synced timestamp without time zone NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    is_deployed boolean NOT NULL DEFAULT false,
    deployed_state json NULL,
    deployed_at timestamp without time zone NULL,
    collaborators json NOT NULL DEFAULT '[]',
    run_count integer NOT NULL DEFAULT 0,
    last_run_at timestamp without time zone NULL,
    variables json NULL DEFAULT '{}',
    is_published boolean NOT NULL DEFAULT false,
    marketplace_data json NULL
);

-- Workflow blocks table (CSV structure compatible)
CREATE TABLE public.workflow_blocks (
    id text PRIMARY KEY,
    workflow_id text NOT NULL,
    type text NOT NULL,
    name text NOT NULL,
    position_x numeric NOT NULL,
    position_y numeric NOT NULL,
    enabled boolean NOT NULL DEFAULT true,
    horizontal_handles boolean NOT NULL DEFAULT true,
    is_wide boolean NOT NULL DEFAULT false,
    advanced_mode boolean NOT NULL DEFAULT false,
    height numeric NOT NULL DEFAULT 0,
    sub_blocks jsonb NOT NULL DEFAULT '{}',
    outputs jsonb NOT NULL DEFAULT '{}',
    data jsonb NULL DEFAULT '{}',
    parent_id text NULL,
    extent text NULL,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_at timestamp without time zone NOT NULL DEFAULT now()
);

-- Workflow rows table (CSV structure compatible)  
CREATE TABLE public.workflow_rows (
    id text PRIMARY KEY,
    user_id text NOT NULL,
    workspace_id text NULL,
    folder_id text NULL,
    name text NOT NULL,
    description text NULL,
    state json NOT NULL,
    color text NOT NULL DEFAULT '#3972F6',
    last_synced timestamp without time zone NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    is_deployed boolean NOT NULL DEFAULT false,
    deployed_state json NULL,
    deployed_at timestamp without time zone NULL,
    collaborators json NOT NULL DEFAULT '[]',
    run_count integer NOT NULL DEFAULT 0,
    last_run_at timestamp without time zone NULL,
    variables json NULL DEFAULT '{}',
    is_published boolean NOT NULL DEFAULT false,
    marketplace_data json NULL
);

-- Intelligent caching table with vector embeddings
CREATE TABLE public.workflow_lookup (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    lookup_key TEXT NOT NULL UNIQUE,
    input_pattern JSONB NOT NULL,
    workflow_type TEXT NOT NULL,
    block_count INTEGER,
    block_types TEXT[],
    generated_state JSONB NOT NULL,
    usage_count INTEGER DEFAULT 1,
    avg_generation_time FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_used_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    confidence_score FLOAT DEFAULT 1.0,
    semantic_description TEXT,
    embedding vector(1536) -- OpenAI embeddings
);

-- Performance indexes
CREATE INDEX workflow_blocks_workflow_id_idx ON workflow_blocks(workflow_id);
CREATE INDEX workflow_blocks_parent_id_idx ON workflow_blocks(parent_id);
CREATE INDEX workflow_lookup_key_idx ON workflow_lookup(lookup_key);
CREATE INDEX workflow_lookup_embedding_idx ON workflow_lookup 
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Foreign Key Constraints

-- Parent-Child: Workflow to Blocks
ALTER TABLE public.workflow_blocks 
ADD CONSTRAINT fk_workflow 
FOREIGN KEY (workflow_id) 
REFERENCES public.workflow(id) 
ON DELETE CASCADE;

-- Self-referential: Block Hierarchy
ALTER TABLE public.workflow_blocks 
ADD CONSTRAINT fk_parent_block 
FOREIGN KEY (parent_id) 
REFERENCES public.workflow_blocks(id) 
ON DELETE SET NULL; 