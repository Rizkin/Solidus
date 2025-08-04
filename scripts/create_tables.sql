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

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_workflow_updated_at BEFORE UPDATE ON workflow
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workflow_blocks_updated_at BEFORE UPDATE ON workflow_blocks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert data from CSV samples
-- Insert workflows from workflow_rows.csv
INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES
(
    '79e8076f-0ae0-4b6f-9d14-65364ddae6d2',
    'sEfcNW1TZedrJ8mDW81UFVtZpZXVd3Mf',
    'f639bbc2-cbda-49c3-9301-9c632c8e86e2',
    NULL,
    'default-agent',
    'Your first workflow - start building here!',
    '{"blocks":{"cb7ebf84-9d43-45bf-a327-cca64d30d602":{"id":"cb7ebf84-9d43-45bf-a327-cca64d30d602","type":"starter","name":"Start","position":{"x":100,"y":100},"subBlocks":{"startWorkflow":{"id":"startWorkflow","type":"dropdown","value":"manual"},"webhookPath":{"id":"webhookPath","type":"short-input","value":""},"webhookSecret":{"id":"webhookSecret","type":"short-input","value":""},"scheduleType":{"id":"scheduleType","type":"dropdown","value":"daily"},"minutesInterval":{"id":"minutesInterval","type":"short-input","value":""},"minutesStartingAt":{"id":"minutesStartingAt","type":"short-input","value":""}},"outputs":{"response":{"type":{"input":"any"}}},"enabled":true,"horizontalHandles":true,"isWide":false,"height":95}},"edges":[],"subflows":{},"variables":{},"metadata":{"version":"1.0.0","createdAt":"2025-07-22T07:10:51.778Z","updatedAt":"2025-07-22T07:10:51.778Z"}}',
    '#3972F6',
    '2025-07-22 07:10:51.778',
    '2025-07-22 07:10:51.778',
    '2025-07-22 07:10:51.778',
    false,
    NULL,
    NULL,
    '[]',
    0,
    NULL,
    '{}',
    false,
    NULL
),
(
    '81e98d1e-459d-4e1d-b9c3-e1e56f8155ab',
    'H2sjCYSjVkkhay0GpyXM53XmEWwDVgjc',
    'd8b61a6b-d682-4d70-8f39-1261eb4d880b',
    NULL,
    'workflow-test',
    'Your first workflow - start building here!',
    '{"blocks":{"f668ee62-8abb-49df-9b4e-b7d5e18f11df":{"id":"f668ee62-8abb-49df-9b4e-b7d5e18f11df","type":"starter","name":"Start","position":{"x":100,"y":100},"subBlocks":{"startWorkflow":{"id":"startWorkflow","type":"dropdown","value":"manual"},"webhookPath":{"id":"webhookPath","type":"short-input","value":""},"webhookSecret":{"id":"webhookSecret","type":"short-input","value":""},"scheduleType":{"id":"scheduleType","type":"dropdown","value":"daily"},"minutesInterval":{"id":"minutesInterval","type":"short-input","value":""},"minutesStartingAt":{"id":"minutesStartingAt","type":"short-input","value":""}},"outputs":{"response":{"type":{"input":"any"}}},"enabled":true,"horizontalHandles":true,"isWide":false,"height":95}},"edges":[],"subflows":{},"variables":{},"metadata":{"version":"1.0.0","createdAt":"2025-07-21T14:25:55.945Z","updatedAt":"2025-07-21T14:25:55.945Z"}}',
    '#3972F6',
    '2025-07-21 14:25:55.945',
    '2025-07-21 14:25:55.945',
    '2025-07-22 07:38:15.676',
    false,
    NULL,
    NULL,
    '[]',
    0,
    NULL,
    '{}',
    false,
    NULL
),
(
    'af18372b-03e8-45fd-9be5-3ac559c88f57',
    'H2sjCYSjVkkhay0GpyXM53XmEWwDVgjc',
    'd8b61a6b-d682-4d70-8f39-1261eb4d880b',
    NULL,
    'arctic-constellation',
    'New workflow',
    '{"blocks":{"1814dd59-5ded-43ed-9b90-549861b8bbde":{"id":"1814dd59-5ded-43ed-9b90-549861b8bbde","type":"starter","name":"Start","position":{"x":100,"y":100},"subBlocks":{"startWorkflow":{"id":"startWorkflow","type":"dropdown","value":"manual"},"webhookPath":{"id":"webhookPath","type":"short-input","value":""},"webhookSecret":{"id":"webhookSecret","type":"short-input","value":""},"scheduleType":{"id":"scheduleType","type":"dropdown","value":"daily"},"minutesInterval":{"id":"minutesInterval","type":"short-input","value":""},"minutesStartingAt":{"id":"minutesStartingAt","type":"short-input","value":""},"hourlyMinute":{"id":"hourlyMinute","type":"short-input","value":""},"dailyTime":{"id":"dailyTime","type":"short-input","value":""},"weeklyDay":{"id":"weeklyDay","type":"dropdown","value":"MON"},"weeklyDayTime":{"id":"weeklyDayTime","type":"short-input","value":""},"monthlyDay":{"id":"monthlyDay","type":"short-input","value":""},"monthlyTime":{"id":"monthlyTime","type":"short-input","value":""},"cronExpression":{"id":"cronExpression","type":"short-input","value":""},"timezone":{"id":"timezone","type":"dropdown","value":"UTC"}},"outputs":{"response":{"type":{"input":"any"}}},"enabled":true,"horizontalHandles":true,"isWide":false,"height":95}},"edges":[],"subflows":{},"variables":{},"metadata":{"version":"1.0.0","createdAt":"2025-07-21T14:26:24.553Z","updatedAt":"2025-07-21T14:26:24.553Z"}}',
    '#15803D',
    '2025-07-21 14:26:24.553',
    '2025-07-21 14:26:24.553',
    '2025-07-21 14:26:24.553',
    false,
    NULL,
    NULL,
    '[]',
    0,
    NULL,
    '{}',
    false,
    NULL
);

-- Insert workflow blocks from workflow_blocks_rows.csv
INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y, enabled,
    horizontal_handles, is_wide, advanced_mode, height, sub_blocks,
    outputs, data, parent_id, extent, created_at, updated_at
) VALUES
(
    '135552e8-592e-4567-bf09-156b0a5e28f0',
    '81e98d1e-459d-4e1d-b9c3-e1e56f8155ab',
    'agent',
    'Agent 1',
    556.9230769230769,
    -119.80769230769232,
    true,
    true,
    false,
    false,
    0,
    '{"model":{"id":"model","type":"combobox","value":"gemini-2.5-pro"},"tools":{"id":"tools","type":"tool-input","value":[{"type":"elevenlabs","title":"ElevenLabs","params":{"apiKey":"sk_539725a6d8b99b16a11467e7b1cb7d514233f90a58dc4823","voiceId":"Xb7hH8MSUJpSbSDYk0k2"},"isExpanded":true,"usageControl":"auto"}]},"apiKey":{"id":"apiKey","type":"short-input","value":"AIzaSyByzvH03g09lJrv9t6OLJ9GlQqrNUuqRJY"},"memories":{"id":"memories","type":"short-input","value":null},"userPrompt":{"id":"userPrompt","type":"long-input","value":"<start>"},"temperature":{"id":"temperature","type":"slider","value":null},"systemPrompt":{"id":"systemPrompt","type":"long-input","value":"You are an assistant that transitions what the user says into text to speech using elevenlabs and sends them the URL to the output."},"azureEndpoint":{"id":"azureEndpoint","type":"short-input","value":null},"responseFormat":{"id":"responseFormat","type":"code","value":null},"azureApiVersion":{"id":"azureApiVersion","type":"short-input","value":null}}',
    '{"model":"string","tokens":"any","content":"string","toolCalls":"any"}',
    '{}',
    NULL,
    NULL,
    '2025-07-21 14:26:18.934438',
    '2025-07-22 07:24:24.532'
),
(
    '1814dd59-5ded-43ed-9b90-549861b8bbde',
    'af18372b-03e8-45fd-9be5-3ac559c88f57',
    'starter',
    'Start',
    100,
    100,
    true,
    true,
    false,
    false,
    95,
    '{"timezone":{"id":"timezone","type":"dropdown","value":"UTC"},"dailyTime":{"id":"dailyTime","type":"short-input","value":""},"weeklyDay":{"id":"weeklyDay","type":"dropdown","value":"MON"},"monthlyDay":{"id":"monthlyDay","type":"short-input","value":""},"monthlyTime":{"id":"monthlyTime","type":"short-input","value":""},"webhookPath":{"id":"webhookPath","type":"short-input","value":""},"hourlyMinute":{"id":"hourlyMinute","type":"short-input","value":""},"scheduleType":{"id":"scheduleType","type":"dropdown","value":"daily"},"startWorkflow":{"id":"startWorkflow","type":"dropdown","value":"manual"},"webhookSecret":{"id":"webhookSecret","type":"short-input","value":""},"weeklyDayTime":{"id":"weeklyDayTime","type":"short-input","value":""},"cronExpression":{"id":"cronExpression","type":"short-input","value":""},"minutesInterval":{"id":"minutesInterval","type":"short-input","value":""},"minutesStartingAt":{"id":"minutesStartingAt","type":"short-input","value":""}}',
    '{"response":{"type":{"input":"any"}}}',
    '{}',
    NULL,
    NULL,
    '2025-07-21 14:26:24.553',
    '2025-07-21 14:26:24.553'
),
(
    'a091ef02-b50b-425f-b5cf-f3a936281c32',
    '81e98d1e-459d-4e1d-b9c3-e1e56f8155ab',
    'api',
    'API 1',
    959.7926327015055,
    129.0738138570569,
    true,
    true,
    false,
    false,
    0,
    '{"url":{"id":"url","type":"short-input","value":"https://api.coingecko.com/api/v3/search/trending"},"body":{"id":"body","type":"code","value":null},"method":{"id":"method","type":"dropdown","value":null},"params":{"id":"params","type":"table","value":null},"headers":{"id":"headers","type":"table","value":[{"id":"58f892db-c69b-49d0-a803-33e9ed4c25e1","cells":{"Key":"Accept","Value":"application/json"}},{"id":"ba713868-ae3e-474b-b881-32fc893d173c","cells":{"Key":"","Value":""}}]}}',
    '{"data":"any","status":"number","headers":"json"}',
    '{}',
    NULL,
    NULL,
    '2025-07-22 07:13:20.298901',
    '2025-07-22 07:14:41.685'
),
(
    'cb7ebf84-9d43-45bf-a327-cca64d30d602',
    '79e8076f-0ae0-4b6f-9d14-65364ddae6d2',
    'starter',
    'Start',
    100,
    100,
    true,
    true,
    false,
    false,
    95,
    '{"webhookPath":{"id":"webhookPath","type":"short-input","value":""},"scheduleType":{"id":"scheduleType","type":"dropdown","value":"daily"},"startWorkflow":{"id":"startWorkflow","type":"dropdown","value":"manual"},"webhookSecret":{"id":"webhookSecret","type":"short-input","value":""},"minutesInterval":{"id":"minutesInterval","type":"short-input","value":""},"minutesStartingAt":{"id":"minutesStartingAt","type":"short-input","value":""}}',
    '{"response":{"type":{"input":"any"}}}',
    '{}',
    NULL,
    NULL,
    '2025-07-22 07:10:51.778',
    '2025-07-22 07:10:51.778'
),
(
    'f668ee62-8abb-49df-9b4e-b7d5e18f11df',
    '81e98d1e-459d-4e1d-b9c3-e1e56f8155ab',
    'starter',
    'Start',
    100,
    100,
    true,
    true,
    false,
    false,
    95,
    '{"webhookPath":{"id":"webhookPath","type":"short-input","value":"732a975e-4a63-4c5c-bee4-d8061444ae24"},"scheduleType":{"id":"scheduleType","type":"dropdown","value":"daily"},"startWorkflow":{"id":"startWorkflow","type":"dropdown","value":"manual"},"webhookSecret":{"id":"webhookSecret","type":"short-input","value":""},"providerConfig":{"id":"providerConfig","type":"unknown","value":{}},"minutesInterval":{"id":"minutesInterval","type":"short-input","value":""},"webhookProvider":{"id":"webhookProvider","type":"unknown","value":"generic"},"minutesStartingAt":{"id":"minutesStartingAt","type":"short-input","value":""}}',
    '{"response":{"type":{"input":"any"}}}',
    '{}',
    NULL,
    NULL,
    '2025-07-21 14:25:55.945',
    '2025-07-22 07:15:51.356'
);

-- Grant permissions
GRANT ALL ON workflow TO postgres;
GRANT ALL ON workflow_blocks TO postgres; 