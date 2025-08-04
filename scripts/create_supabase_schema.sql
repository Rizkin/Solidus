-- Agent Forge State Generator - Supabase Schema
-- Create the required tables for workflow processing

-- Create workflow table
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

-- Create workflow_blocks table
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
    CONSTRAINT workflow_blocks_pkey PRIMARY KEY (id),
    CONSTRAINT workflow_blocks_workflow_id_workflow_id_fk 
        FOREIGN KEY (workflow_id) REFERENCES workflow (id) ON DELETE CASCADE
) TABLESPACE pg_default;

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS workflow_blocks_workflow_id_idx 
    ON public.workflow_blocks USING btree (workflow_id) TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS workflow_blocks_parent_id_idx 
    ON public.workflow_blocks USING btree (parent_id) TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS workflow_blocks_workflow_parent_idx 
    ON public.workflow_blocks USING btree (workflow_id, parent_id) TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS workflow_blocks_workflow_type_idx 
    ON public.workflow_blocks USING btree (workflow_id, type) TABLESPACE pg_default;

-- Create sample data tables for CSV input processing
CREATE TABLE public.workflow_rows (
    id text NOT NULL,
    user_id text NOT NULL,
    workspace_id text NULL,
    folder_id text NULL,
    name text NOT NULL,
    description text NULL,
    color text NOT NULL DEFAULT '#3972F6'::text,
    variables json NULL DEFAULT '{}'::json,
    is_published boolean NOT NULL DEFAULT false,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_at timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT workflow_rows_pkey PRIMARY KEY (id)
) TABLESPACE pg_default;

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
    CONSTRAINT workflow_blocks_rows_pkey PRIMARY KEY (id)
) TABLESPACE pg_default; 