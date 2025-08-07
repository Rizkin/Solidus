-- Agent Forge State Generator - Database Schema v2.0
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
    state json NOT NULL DEFAULT '{}',
    color text NOT NULL DEFAULT '#3972F6',
    last_synced timestamp without time zone NOT NULL DEFAULT now(),
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_at timestamp without time zone NOT NULL DEFAULT now(),
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

-- Workflow blocks rows table (Guideline/input table - mirrors workflow_blocks)
CREATE TABLE public.workflow_blocks_rows (
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

-- Cache performance statistics
CREATE TABLE public.cache_stats (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    cache_type TEXT NOT NULL,
    hit_count INTEGER DEFAULT 0,
    miss_count INTEGER DEFAULT 0,
    hit_rate FLOAT GENERATED ALWAYS AS (
        CASE 
            WHEN (hit_count + miss_count) > 0 THEN 
                (hit_count::FLOAT / (hit_count + miss_count)) * 100
            ELSE 0 
        END
    ) STORED,
    total_requests INTEGER GENERATED ALWAYS AS (hit_count + miss_count) STORED,
    avg_response_time_ms FLOAT,
    cache_size_mb FLOAT,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI usage tracking and cost monitoring
CREATE TABLE public.ai_usage_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    workflow_id TEXT,
    provider TEXT NOT NULL, -- 'claude', 'openai', 'fallback'
    model TEXT NOT NULL,
    operation_type TEXT NOT NULL, -- 'generation', 'embedding', 'validation'
    token_count INTEGER,
    cost_estimate_usd DECIMAL(10,6),
    response_time_ms INTEGER,
    cache_hit BOOLEAN DEFAULT false,
    success BOOLEAN DEFAULT true,
    error_message TEXT,
    request_metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Validation results tracking
CREATE TABLE public.validation_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    validation_type TEXT NOT NULL, -- 'schema', 'business_rules', 'compliance'
    validator_name TEXT NOT NULL,
    passed BOOLEAN NOT NULL,
    score FLOAT, -- 0-100 compliance score
    error_details JSONB,
    warnings JSONB,
    suggestions JSONB,
    execution_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User and workspace tables for complete relational integrity
CREATE TABLE public.users (
    id text PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    avatar_url TEXT,
    plan_type TEXT DEFAULT 'free', -- 'free', 'pro', 'enterprise'
    api_key_hash TEXT,
    rate_limit_per_hour INTEGER DEFAULT 100,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE public.workspaces (
    id text PRIMARY KEY,
    name TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    plan_type TEXT DEFAULT 'free',
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE public.workflow_folders (
    id text PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    name TEXT NOT NULL,
    parent_folder_id TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Performance indexes
CREATE INDEX workflow_blocks_workflow_id_idx ON public.workflow_blocks(workflow_id);
CREATE INDEX workflow_blocks_parent_id_idx ON public.workflow_blocks(parent_id);
CREATE INDEX workflow_blocks_type_idx ON public.workflow_blocks(type);
CREATE INDEX workflow_blocks_workflow_type_idx ON public.workflow_blocks(workflow_id, type);
CREATE INDEX workflow_blocks_workflow_parent_idx ON public.workflow_blocks(workflow_id, parent_id);

-- Indexes for workflow_blocks_rows (guideline table)
CREATE INDEX workflow_blocks_rows_workflow_id_idx ON public.workflow_blocks_rows(workflow_id);
CREATE INDEX workflow_blocks_rows_parent_id_idx ON public.workflow_blocks_rows(parent_id);
CREATE INDEX workflow_blocks_rows_type_idx ON public.workflow_blocks_rows(type);

-- Cache and analytics indexes
CREATE INDEX workflow_lookup_key_idx ON public.workflow_lookup(lookup_key);
CREATE INDEX workflow_lookup_type_idx ON public.workflow_lookup(workflow_type);
CREATE INDEX workflow_lookup_usage_idx ON public.workflow_lookup(usage_count DESC);
CREATE INDEX workflow_lookup_embedding_idx ON public.workflow_lookup 
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- AI usage logs indexes
CREATE INDEX ai_usage_logs_workflow_id_idx ON public.ai_usage_logs(workflow_id);
CREATE INDEX ai_usage_logs_provider_idx ON public.ai_usage_logs(provider);
CREATE INDEX ai_usage_logs_created_at_idx ON public.ai_usage_logs(created_at DESC);
CREATE INDEX ai_usage_logs_cost_idx ON public.ai_usage_logs(cost_estimate_usd DESC);

-- Validation logs indexes
CREATE INDEX validation_logs_workflow_id_idx ON public.validation_logs(workflow_id);
CREATE INDEX validation_logs_type_idx ON public.validation_logs(validation_type);
CREATE INDEX validation_logs_passed_idx ON public.validation_logs(passed);

-- User and workspace indexes
CREATE INDEX users_email_idx ON public.users(email);
CREATE INDEX users_plan_type_idx ON public.users(plan_type);
CREATE INDEX workspaces_owner_id_idx ON public.workspaces(owner_id);

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

-- Guideline table relationships
ALTER TABLE public.workflow_blocks_rows 
ADD CONSTRAINT fk_workflow_rows 
FOREIGN KEY (workflow_id) 
REFERENCES public.workflow_rows(id) 
ON DELETE CASCADE;

ALTER TABLE public.workflow_blocks_rows 
ADD CONSTRAINT fk_parent_block_rows 
FOREIGN KEY (parent_id) 
REFERENCES public.workflow_blocks_rows(id) 
ON DELETE SET NULL;

-- User and workspace relationships
ALTER TABLE public.workflow 
ADD CONSTRAINT fk_workflow_user 
FOREIGN KEY (user_id) 
REFERENCES public.users(id) 
ON DELETE CASCADE;

ALTER TABLE public.workflow 
ADD CONSTRAINT fk_workflow_workspace 
FOREIGN KEY (workspace_id) 
REFERENCES public.workspaces(id) 
ON DELETE SET NULL;

ALTER TABLE public.workflow 
ADD CONSTRAINT fk_workflow_folder 
FOREIGN KEY (folder_id) 
REFERENCES public.workflow_folders(id) 
ON DELETE SET NULL;

ALTER TABLE public.workflow_rows 
ADD CONSTRAINT fk_workflow_rows_user 
FOREIGN KEY (user_id) 
REFERENCES public.users(id) 
ON DELETE CASCADE;

ALTER TABLE public.workflow_rows 
ADD CONSTRAINT fk_workflow_rows_workspace 
FOREIGN KEY (workspace_id) 
REFERENCES public.workspaces(id) 
ON DELETE SET NULL;

ALTER TABLE public.workspaces 
ADD CONSTRAINT fk_workspace_owner 
FOREIGN KEY (owner_id) 
REFERENCES public.users(id) 
ON DELETE CASCADE;

ALTER TABLE public.workflow_folders 
ADD CONSTRAINT fk_folder_workspace 
FOREIGN KEY (workspace_id) 
REFERENCES public.workspaces(id) 
ON DELETE CASCADE;

ALTER TABLE public.workflow_folders 
ADD CONSTRAINT fk_folder_parent 
FOREIGN KEY (parent_folder_id) 
REFERENCES public.workflow_folders(id) 
ON DELETE SET NULL;

-- Analytics table relationships
ALTER TABLE public.ai_usage_logs 
ADD CONSTRAINT fk_ai_usage_workflow 
FOREIGN KEY (workflow_id) 
REFERENCES public.workflow(id) 
ON DELETE SET NULL;

ALTER TABLE public.validation_logs 
ADD CONSTRAINT fk_validation_workflow 
FOREIGN KEY (workflow_id) 
REFERENCES public.workflow(id) 
ON DELETE CASCADE;

-- Useful views for common queries

-- View: Workflow with block counts
CREATE VIEW public.workflow_summary AS
SELECT 
    w.id,
    w.name,
    w.description,
    w.user_id,
    w.workspace_id,
    w.created_at,
    w.updated_at,
    COUNT(wb.id) as block_count,
    COUNT(wb.id) FILTER (WHERE wb.type = 'starter') as starter_count,
    COUNT(wb.id) FILTER (WHERE wb.type = 'action') as action_count,
    COUNT(wb.id) FILTER (WHERE wb.type = 'decision') as decision_count,
    COUNT(wb.id) FILTER (WHERE wb.enabled = true) as enabled_blocks,
    w.run_count,
    w.is_published
FROM public.workflow w
LEFT JOIN public.workflow_blocks wb ON w.id = wb.workflow_id
GROUP BY w.id, w.name, w.description, w.user_id, w.workspace_id, 
         w.created_at, w.updated_at, w.run_count, w.is_published;

-- View: Cache performance metrics
CREATE VIEW public.cache_performance AS
SELECT 
    cache_type,
    hit_count,
    miss_count,
    hit_rate,
    total_requests,
    avg_response_time_ms,
    cache_size_mb,
    last_updated
FROM public.cache_stats
ORDER BY hit_rate DESC;

-- View: AI usage summary
CREATE VIEW public.ai_usage_summary AS
SELECT 
    DATE_TRUNC('day', created_at) as date,
    provider,
    COUNT(*) as request_count,
    SUM(token_count) as total_tokens,
    SUM(cost_estimate_usd) as total_cost_usd,
    AVG(response_time_ms) as avg_response_time_ms,
    COUNT(*) FILTER (WHERE cache_hit = true) as cache_hits,
    COUNT(*) FILTER (WHERE success = true) as successful_requests
FROM public.ai_usage_logs
GROUP BY DATE_TRUNC('day', created_at), provider
ORDER BY date DESC, total_cost_usd DESC;

-- Trigger functions for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply update triggers
CREATE TRIGGER update_workflow_updated_at 
    BEFORE UPDATE ON public.workflow 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workflow_blocks_updated_at 
    BEFORE UPDATE ON public.workflow_blocks 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workflow_rows_updated_at 
    BEFORE UPDATE ON public.workflow_rows 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workflow_blocks_rows_updated_at 
    BEFORE UPDATE ON public.workflow_blocks_rows 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON public.users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workspaces_updated_at 
    BEFORE UPDATE ON public.workspaces 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE public.workflow IS 'Main workflow table storing Agent Forge compatible workflows';
COMMENT ON TABLE public.workflow_blocks IS 'Workflow blocks with position and configuration data';
COMMENT ON TABLE public.workflow_rows IS 'Guideline table mirroring workflow structure for data input';
COMMENT ON TABLE public.workflow_blocks_rows IS 'Guideline table mirroring workflow_blocks for data input';
COMMENT ON TABLE public.workflow_lookup IS 'RAG caching table with vector embeddings for pattern matching';
COMMENT ON TABLE public.cache_stats IS 'Performance statistics for caching system';
COMMENT ON TABLE public.ai_usage_logs IS 'AI service usage tracking for cost monitoring and analytics';
COMMENT ON TABLE public.validation_logs IS 'Workflow validation results and compliance tracking';

-- Initial data for cache_stats
INSERT INTO public.cache_stats (cache_type, hit_count, miss_count, avg_response_time_ms, cache_size_mb)
VALUES 
    ('workflow_patterns', 0, 0, 0, 0),
    ('ai_responses', 0, 0, 0, 0),
    ('template_cache', 0, 0, 0, 0)
ON CONFLICT DO NOTHING; 