-- Agent Forge State Generator - Supabase Schema
-- Create the required tables for workflow processing

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create workflow table (Master workflow table)
CREATE TABLE public.workflow (
    id text NOT NULL,
    user_id text NOT NULL,
    workspace_id text NULL,
    folder_id text NULL,
    name text NOT NULL,
    description text NULL,
    state json NOT NULL,
    color text NOT NULL DEFAULT '#3972F6'::text,
    last_synced timestamp without time zone NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    is_deployed boolean NOT NULL DEFAULT false,
    deployed_state json NULL,
    deployed_at timestamp without time zone NULL,
    collaborators json NOT NULL DEFAULT '[]'::json,
    run_count integer NOT NULL DEFAULT 0,
    last_run_at timestamp without time zone NULL,
    variables json NULL DEFAULT '{}'::json,
    is_published boolean NOT NULL DEFAULT false,
    marketplace_data json NULL,
    CONSTRAINT workflow_pkey PRIMARY KEY (id)
) TABLESPACE pg_default;

-- Create workflow_blocks table (Workflow blocks detail table)
CREATE TABLE public.workflow_blocks (
    id text NOT NULL,
    workflow_id text NOT NULL,
    type text NOT NULL,
    name text NOT NULL,
    position_x numeric NOT NULL,
    position_y numeric NOT NULL,
    enabled boolean NOT NULL DEFAULT true,
    horizontal_handles boolean NOT NULL DEFAULT true,
    is_wide boolean NOT NULL DEFAULT false,
    advanced_mode boolean NOT NULL DEFAULT false,
    height numeric NOT NULL DEFAULT '0'::numeric,
    sub_blocks jsonb NOT NULL DEFAULT '{}'::jsonb,
    outputs jsonb NOT NULL DEFAULT '{}'::jsonb,
    data jsonb NULL DEFAULT '{}'::jsonb,
    parent_id text NULL,
    extent text NULL,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_at timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT workflow_blocks_pkey PRIMARY KEY (id)
) TABLESPACE pg_default;

-- Add Foreign Key Constraints for Relationships

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

-- Create workflow_rows table (Guideline/input table - mirrors workflow structure)
CREATE TABLE public.workflow_rows (
    id text NOT NULL,
    user_id text NOT NULL,
    workspace_id text NULL,
    folder_id text NULL,
    name text NOT NULL,
    description text NULL,
    state json NOT NULL,
    color text NOT NULL DEFAULT '#3972F6'::text,
    last_synced timestamp without time zone NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    is_deployed boolean NOT NULL DEFAULT false,
    deployed_state json NULL,
    deployed_at timestamp without time zone NULL,
    collaborators json NOT NULL DEFAULT '[]'::json,
    run_count integer NOT NULL DEFAULT 0,
    last_run_at timestamp without time zone NULL,
    variables json NULL DEFAULT '{}'::json,
    is_published boolean NOT NULL DEFAULT false,
    marketplace_data json NULL,
    CONSTRAINT workflow_rows_pkey PRIMARY KEY (id)
) TABLESPACE pg_default;

-- Create workflow_blocks_rows table (Guideline/input table - mirrors workflow_blocks)
CREATE TABLE public.workflow_blocks_rows (
    id text NOT NULL,
    workflow_id text NOT NULL,
    type text NOT NULL,
    name text NOT NULL,
    position_x numeric NOT NULL,
    position_y numeric NOT NULL,
    enabled boolean NOT NULL DEFAULT true,
    horizontal_handles boolean NOT NULL DEFAULT true,
    is_wide boolean NOT NULL DEFAULT false,
    advanced_mode boolean NOT NULL DEFAULT false,
    height numeric NOT NULL DEFAULT '0'::numeric,
    sub_blocks jsonb NOT NULL DEFAULT '{}'::jsonb,
    outputs jsonb NOT NULL DEFAULT '{}'::jsonb,
    data jsonb NULL DEFAULT '{}'::jsonb,
    parent_id text NULL,
    extent text NULL,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_at timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT workflow_blocks_rows_pkey PRIMARY KEY (id)
) TABLESPACE pg_default;

-- Create lookup table for intelligent caching
CREATE TABLE public.workflow_lookup (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    lookup_key TEXT NOT NULL, -- Hash of input parameters
    input_pattern JSONB NOT NULL, -- Original input characteristics
    workflow_type TEXT NOT NULL, -- Type of workflow requested
    block_count INTEGER,
    block_types TEXT[], -- Array of block types
    generated_state JSONB NOT NULL, -- The AI-generated state
    usage_count INTEGER DEFAULT 1,
    avg_generation_time FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_used_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    confidence_score FLOAT DEFAULT 1.0, -- How reliable this pattern is
    semantic_description TEXT, -- Rich description for embeddings
    embedding vector(1536), -- OpenAI embedding vector
    UNIQUE(lookup_key)
);

-- Create indexes for workflow_lookup
CREATE INDEX IF NOT EXISTS idx_workflow_lookup_key ON workflow_lookup(lookup_key);
CREATE INDEX IF NOT EXISTS idx_workflow_lookup_type ON workflow_lookup(workflow_type);
CREATE INDEX IF NOT EXISTS idx_workflow_lookup_usage ON workflow_lookup(usage_count DESC);
CREATE INDEX IF NOT EXISTS workflow_lookup_embedding_idx 
    ON workflow_lookup USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Create temporary table for AI processing
CREATE TABLE public.workflow_temp (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id TEXT NOT NULL,
    input_data JSONB NOT NULL,
    ai_response JSONB,
    lookup_match_id UUID REFERENCES workflow_lookup(id),
    similarity_score FLOAT,
    processing_status TEXT DEFAULT 'pending', -- pending, processing, completed, failed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Create index for session lookups
CREATE INDEX IF NOT EXISTS idx_workflow_temp_session ON workflow_temp(session_id);
CREATE INDEX IF NOT EXISTS idx_workflow_temp_status ON workflow_temp(processing_status);

-- Create similarity search function (structured)
CREATE OR REPLACE FUNCTION find_similar_workflows(
    p_workflow_type TEXT,
    p_block_types TEXT[],
    p_block_count INTEGER,
    p_similarity_threshold FLOAT DEFAULT 0.8
)
RETURNS TABLE (
    lookup_id UUID,
    similarity_score FLOAT,
    generated_state JSONB,
    usage_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        wl.id,
        -- Calculate similarity score based on multiple factors
        (
            CASE WHEN wl.workflow_type = p_workflow_type THEN 0.4 ELSE 0.0 END +
            CASE 
                WHEN wl.block_count = p_block_count THEN 0.3
                WHEN ABS(wl.block_count - p_block_count) <= 2 THEN 0.2
                ELSE 0.0
            END +
            -- Array similarity for block types
            (
                SELECT COUNT(*)::FLOAT / GREATEST(
                    array_length(wl.block_types, 1),
                    array_length(p_block_types, 1)
                ) * 0.3
                FROM unnest(wl.block_types) AS a(type)
                WHERE a.type = ANY(p_block_types)
            )
        ) AS similarity,
        wl.generated_state,
        wl.usage_count
    FROM workflow_lookup wl
    WHERE 
        -- Basic filters for performance
        wl.workflow_type = p_workflow_type OR 
        wl.block_types && p_block_types -- Has overlapping block types
    ORDER BY similarity DESC, wl.usage_count DESC
    LIMIT 5;
END;
$$ LANGUAGE plpgsql;

-- Create semantic similarity search function (RAG)
CREATE OR REPLACE FUNCTION search_similar_workflows_semantic(
    query_embedding vector,
    match_threshold float DEFAULT 0.8,
    match_count int DEFAULT 5
)
RETURNS TABLE (
    lookup_id UUID,
    similarity_score float,
    generated_state jsonb,
    semantic_description text
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        wl.id,
        1 - (wl.embedding <=> query_embedding) as similarity,
        wl.generated_state,
        wl.semantic_description
    FROM workflow_lookup wl
    WHERE 1 - (wl.embedding <=> query_embedding) > match_threshold
    ORDER BY wl.embedding <=> query_embedding
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql; 

-- Create cache statistics table
CREATE TABLE public.cache_stats (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    cache_type TEXT NOT NULL, -- 'template', 'pattern', 'semantic', etc.
    hit_count INTEGER DEFAULT 0,
    miss_count INTEGER DEFAULT 0,
    hit_rate FLOAT GENERATED ALWAYS AS (
        CASE WHEN (hit_count + miss_count) > 0 
        THEN hit_count::FLOAT / (hit_count + miss_count) 
        ELSE 0 END
    ) STORED,
    period_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    period_end TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create AI usage logs table
CREATE TABLE public.ai_usage_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    provider TEXT NOT NULL, -- 'anthropic', 'openai', 'fallback'
    model TEXT NOT NULL, -- 'claude-3-5-sonnet', 'text-embedding-3-small', etc.
    operation_type TEXT NOT NULL, -- 'generation', 'embedding', 'validation'
    workflow_id TEXT REFERENCES workflow(id),
    token_count INTEGER,
    cost_estimate FLOAT,
    response_time FLOAT, -- in milliseconds
    status TEXT NOT NULL, -- 'success', 'error', 'timeout'
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create Indexes for Performance (as specified in the task)

-- Parent-Child: Workflow to Blocks
CREATE INDEX workflow_blocks_workflow_id_idx ON public.workflow_blocks(workflow_id);

-- Self-referential: Block Hierarchy
CREATE INDEX workflow_blocks_parent_id_idx ON public.workflow_blocks(parent_id);

-- Composite indexes for performance
CREATE INDEX workflow_blocks_workflow_parent_idx ON public.workflow_blocks(workflow_id, parent_id);
CREATE INDEX workflow_blocks_workflow_type_idx ON public.workflow_blocks(workflow_id, type);

-- Additional indexes for other tables
CREATE INDEX IF NOT EXISTS idx_cache_stats_type ON cache_stats(cache_type);
CREATE INDEX IF NOT EXISTS idx_cache_stats_period ON cache_stats(period_start, period_end);
CREATE INDEX IF NOT EXISTS idx_ai_usage_provider ON ai_usage_logs(provider);
CREATE INDEX IF NOT EXISTS idx_ai_usage_model ON ai_usage_logs(model);
CREATE INDEX IF NOT EXISTS idx_ai_usage_date ON ai_usage_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_ai_usage_workflow ON ai_usage_logs(workflow_id); 