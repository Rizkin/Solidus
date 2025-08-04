# CSV Processing Guide

## Overview

The Agent Forge State Generator includes a comprehensive CSV processing system that reads workflow data from CSV-based tables (`workflow_rows` and `workflow_blocks_rows`) and converts them into proper Agent Forge workflow states stored in Supabase tables (`public.workflow` and `public.workflow_blocks`).

## Architecture

```
CSV Data (Input)          →    Processing Engine    →    Supabase Tables (Output)
├── workflow_rows         →    CSV Processor        →    public.workflow
└── workflow_blocks_rows  →    State Generator      →    public.workflow_blocks
```

## Database Schema

### Input Tables (CSV Source)

#### workflow_rows
```sql
CREATE TABLE public.workflow_rows (
    id text PRIMARY KEY,
    user_id text NOT NULL,
    workspace_id text NULL,
    folder_id text NULL,
    name text NOT NULL,
    description text NULL,
    color text DEFAULT '#3972F6',
    variables json DEFAULT '{}',
    is_published boolean DEFAULT false,
    created_at timestamp DEFAULT now(),
    updated_at timestamp DEFAULT now()
);
```

#### workflow_blocks_rows
```sql
CREATE TABLE public.workflow_blocks_rows (
    id text PRIMARY KEY,
    workflow_id text NOT NULL,
    type text NOT NULL,
    name text NOT NULL,
    position_x numeric NOT NULL,
    position_y numeric NOT NULL,
    enabled boolean DEFAULT true,
    horizontal_handles boolean DEFAULT true,
    is_wide boolean DEFAULT false,
    advanced_mode boolean DEFAULT false,
    height numeric DEFAULT 80,
    sub_blocks jsonb DEFAULT '{}',
    outputs jsonb DEFAULT '{}',
    data jsonb DEFAULT '{}',
    parent_id text NULL,
    extent text NULL
);
```

### Output Tables (Agent Forge Format)

#### public.workflow
```sql
CREATE TABLE public.workflow (
    id text PRIMARY KEY,
    user_id text NOT NULL,
    workspace_id text NULL,
    folder_id text NULL,
    name text NOT NULL,
    description text NULL,
    state json NOT NULL,           -- Generated workflow state
    color text DEFAULT '#3972F6',
    last_synced timestamp NOT NULL,
    created_at timestamp NOT NULL,
    updated_at timestamp NOT NULL,
    is_deployed boolean DEFAULT false,
    deployed_state json NULL,
    deployed_at timestamp NULL,
    collaborators json DEFAULT '[]',
    run_count integer DEFAULT 0,
    last_run_at timestamp NULL,
    variables json DEFAULT '{}',
    is_published boolean DEFAULT false,
    marketplace_data json NULL
);
```

#### public.workflow_blocks
```sql
CREATE TABLE public.workflow_blocks (
    id text PRIMARY KEY,
    workflow_id text NOT NULL,
    type text NOT NULL,
    name text NOT NULL,
    position_x numeric NOT NULL,
    position_y numeric NOT NULL,
    enabled boolean DEFAULT true,
    horizontal_handles boolean DEFAULT true,
    is_wide boolean DEFAULT false,
    advanced_mode boolean DEFAULT false,
    height numeric DEFAULT 80,
    sub_blocks jsonb DEFAULT '{}',
    outputs jsonb DEFAULT '{}',
    data jsonb DEFAULT '{}',
    parent_id text NULL,
    extent text NULL,
    created_at timestamp DEFAULT now(),
    updated_at timestamp DEFAULT now(),
    FOREIGN KEY (workflow_id) REFERENCES workflow (id) ON DELETE CASCADE
);
```

## Setup Instructions

### 1. Create Supabase Tables

Execute the SQL schema in your Supabase SQL Editor:

```bash
# Run this in Supabase SQL Editor
cat scripts/create_supabase_schema.sql
```

### 2. Load Sample Data

Insert sample CSV data:

```bash
# Run this in Supabase SQL Editor
cat scripts/sample_data_inserts.sql
```

### 3. Configure Environment

Set up your Supabase credentials:

```bash
# In your .env file
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your_service_role_key
```

## API Endpoints

### Process CSV Data

Convert CSV data to Agent Forge workflows:

```bash
POST /api/csv/process
```

**Response:**
```json
{
  "message": "Successfully processed 3 workflows from CSV data",
  "processed_count": 3,
  "processed_workflows": [
    {
      "id": "wf_001",
      "name": "Trading Bot Workflow",
      "description": "Automated cryptocurrency trading with risk management",
      "block_count": 5,
      "edge_count": 4
    }
  ],
  "status": "success",
  "timestamp": "2024-01-04T15:30:00Z"
}
```

### Check Processing Status

Get current processing status:

```bash
GET /api/csv/status
```

**Response:**
```json
{
  "csv_processing_status": {
    "csv_workflow_rows": 3,
    "csv_workflow_blocks_rows": 12,
    "processed_workflows": 3,
    "database_type": "supabase",
    "processing_available": true
  },
  "instructions": {
    "setup": "1. Create tables using scripts/create_supabase_schema.sql",
    "load_data": "2. Load sample data using scripts/sample_data_inserts.sql",
    "process": "3. Call POST /api/csv/process to convert CSV data to workflows"
  }
}
```

### List Processed Workflows

View all processed workflows:

```bash
GET /api/workflows?user_id=user_123&limit=50
```

**Response:**
```json
{
  "workflows": [
    {
      "id": "wf_001",
      "name": "Trading Bot Workflow",
      "description": "Automated cryptocurrency trading with risk management",
      "user_id": "user_123",
      "workspace_id": "ws_456",
      "color": "#FF6B6B",
      "is_published": false,
      "created_at": "2024-01-04T10:00:00Z",
      "updated_at": "2024-01-04T15:30:00Z",
      "block_count": 5
    }
  ],
  "total_count": 3,
  "user_filter": "user_123",
  "limit": 50
}
```

## State Generation Process

### 1. Data Extraction
- Reads workflow metadata from `workflow_rows`
- Reads block data from `workflow_blocks_rows`
- Groups blocks by workflow_id

### 2. State JSON Generation
The processor generates a complete Agent Forge state object:

```json
{
  "blocks": {
    "block_001": {
      "id": "block_001",
      "type": "starter",
      "name": "Market Monitor",
      "position_x": 100,
      "position_y": 100,
      "sub_blocks": {
        "startWorkflow": "schedule",
        "scheduleType": "interval",
        "interval": "1m"
      },
      "enabled": true,
      "horizontal_handles": true,
      "is_wide": false,
      "advanced_mode": false,
      "height": 80
    }
  },
  "edges": [
    {
      "from": "block_001",
      "to": "block_002",
      "type": "success"
    }
  ],
  "subflows": {},
  "variables": {
    "TRADING_PAIR": "BTC/USD",
    "STOP_LOSS": -5,
    "TAKE_PROFIT": 10
  },
  "metadata": {
    "version": "1.0.0",
    "createdAt": "2024-01-04T15:30:00Z",
    "updatedAt": "2024-01-04T15:30:00Z",
    "processedFrom": "csv_data",
    "blockCount": 5,
    "edgeCount": 4
  }
}
```

### 3. Edge Generation
- Automatically creates edges from block `outputs` configuration
- Supports multiple output types (success, error, buy, sell, etc.)
- Prevents self-loops and invalid connections

### 4. Database Storage
- Stores complete workflow in `public.workflow` table
- Stores individual blocks in `public.workflow_blocks` table
- Maintains referential integrity with foreign keys

## Block Types Supported

### Starter Blocks
```json
{
  "type": "starter",
  "sub_blocks": {
    "startWorkflow": "schedule|webhook|manual",
    "scheduleType": "interval|daily|weekly",
    "interval": "1m|5m|1h",
    "webhookPath": "/webhook-path"
  }
}
```

### Agent Blocks
```json
{
  "type": "agent",
  "sub_blocks": {
    "model": "gpt-4|claude-3-sonnet|gemini-pro",
    "systemPrompt": "Agent instructions",
    "temperature": 0.3
  }
}
```

### API Blocks
```json
{
  "type": "api",
  "sub_blocks": {
    "url": "https://api.example.com/endpoint",
    "method": "GET|POST|PUT|DELETE",
    "headers": {"Authorization": "Bearer {{env.TOKEN}}"},
    "params": {"key": "value"}
  }
}
```

### Output Blocks
```json
{
  "type": "output",
  "sub_blocks": {
    "outputType": "email|webhook|sms",
    "channels": ["email@example.com"],
    "template": "template_name"
  }
}
```

### Tool Blocks
```json
{
  "type": "tool",
  "sub_blocks": {
    "toolType": "web3|scraper|custom",
    "configuration": {}
  }
}
```

## Usage Examples

### Example 1: Process Trading Bot Workflow

1. **Load CSV Data:**
```sql
INSERT INTO workflow_rows (id, user_id, workspace_id, name, description, color, variables)
VALUES ('wf_trading', 'user_123', 'ws_456', 'Trading Bot', 'Crypto trading automation', '#FF6B6B', 
        '{"TRADING_PAIR": "BTC/USD", "STOP_LOSS": -5}');

INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, sub_blocks, outputs)
VALUES 
('starter_1', 'wf_trading', 'starter', 'Market Monitor', 100, 100, 
 '{"startWorkflow": "schedule", "interval": "1m"}', '{"success": "api_1"}'),
('api_1', 'wf_trading', 'api', 'Get Price', 300, 100,
 '{"url": "https://api.binance.com/api/v3/ticker/price", "method": "GET"}', '{"success": "agent_1"}');
```

2. **Process via API:**
```bash
curl -X POST https://your-app.vercel.app/api/csv/process
```

3. **View Result:**
```bash
curl https://your-app.vercel.app/api/workflows/wf_trading/state
```

### Example 2: Multi-Agent Research Workflow

```sql
-- Workflow with multiple AI agents
INSERT INTO workflow_rows (id, user_id, name, description, variables)
VALUES ('wf_research', 'user_456', 'Research Team', 'Multi-agent research', 
        '{"RESEARCH_TOPIC": "AI Trends", "AGENT_COUNT": 3}');

-- Coordinator agent
INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, sub_blocks, outputs)
VALUES ('coordinator', 'wf_research', 'agent', 'Research Coordinator', 200, 200,
        '{"model": "gpt-4", "systemPrompt": "Coordinate research tasks"}', 
        '{"data_task": "data_agent", "analysis_task": "analysis_agent"}');

-- Specialized agents
INSERT INTO workflow_blocks_rows (id, workflow_id, type, name, position_x, position_y, sub_blocks, outputs)
VALUES 
('data_agent', 'wf_research', 'agent', 'Data Researcher', 400, 150,
 '{"model": "claude-3-sonnet", "systemPrompt": "Gather quantitative data"}', '{"complete": "synthesizer"}'),
('analysis_agent', 'wf_research', 'agent', 'Trend Analyst', 400, 250,
 '{"model": "gemini-pro", "systemPrompt": "Analyze trends"}', '{"complete": "synthesizer"}');
```

## Error Handling

### Common Issues

1. **Missing CSV Data:**
```json
{
  "message": "No workflows were processed",
  "processed_count": 0,
  "status": "warning",
  "suggestion": "Check if CSV tables (workflow_rows, workflow_blocks_rows) contain data"
}
```

2. **Database Connection Issues:**
- Falls back to mock data processing
- Still generates valid state JSON
- Logs warnings for debugging

3. **Invalid Block Configuration:**
- Validates block types and required fields
- Provides detailed error messages
- Continues processing other valid blocks

### Debugging

1. **Check Processing Status:**
```bash
curl https://your-app.vercel.app/api/csv/status
```

2. **View Debug Information:**
```bash
curl https://your-app.vercel.app/api/debug
```

3. **Check Logs:**
- Monitor application logs for processing details
- Look for validation warnings and errors

## Integration with Agent Forge

After processing, the generated workflows are fully compatible with Agent Forge:

1. **State Format:** Matches Agent Forge specification exactly
2. **Block Types:** Supports all Agent Forge block types
3. **Validation:** Passes Agent Forge compliance checks
4. **Export:** Can be exported for use in Agent Forge platform

## Best Practices

1. **Data Preparation:**
   - Ensure all required fields are populated
   - Use consistent naming conventions
   - Validate JSON fields before insertion

2. **Processing:**
   - Process in batches for large datasets
   - Monitor processing status
   - Validate results after processing

3. **Deployment:**
   - Set up proper Supabase credentials
   - Test with sample data first
   - Monitor for processing errors

4. **Maintenance:**
   - Regular backups of processed workflows
   - Monitor database performance
   - Update block type configurations as needed 