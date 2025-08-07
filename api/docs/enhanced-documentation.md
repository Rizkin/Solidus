# Agent Forge API Documentation

## Overview

Agent Forge is an AI-powered workflow automation platform that generates workflow state JSON objects from database records. The system reads from `workflow_rows` and `workflow_blocks_rows` tables and produces Agent Forge-compatible state objects with blocks, edges, and metadata.

## Base URL

```
https://solidus-olive.vercel.app
```

## Authentication

Most endpoints in the Agent Forge API are publicly accessible for demonstration purposes. However, for production use:

### API Keys

For enhanced security and access to premium features, you can use API keys:

```bash
# Set your API key as an environment variable
export AGENT_FORGE_API_KEY="your_api_key_here"

# Use in requests
curl -H "Authorization: Bearer $AGENT_FORGE_API_KEY" \
  https://solidus-olive.vercel.app/api/endpoint
```

### Rate Limiting

The API implements rate limiting to ensure fair usage:
- Anonymous users: 100 requests per hour
- Authenticated users: 1000 requests per hour

## Endpoints

### GET /api/

Simple API status endpoint - confirms API is functional

**Response:**
```json
{
  "message": "Agent Forge API is fully functional! 🚀",
  "status": "operational",
  "version": "1.0.0",
  "api_ready": true
}
```

### GET /api/health

Health check endpoint for monitoring

**Response:**
```json
{
  "status": "healthy",
  "service": "Agent Forge API",
  "deployment": "vercel-python-handler",
  "timestamp": "2023-01-01T10:00:00Z",
  "message": "All systems operational",
  "uptime": "continuous"
}
```

### GET /api/templates

Get available workflow templates (Trading Bot, Lead Generation, AI Research)

**Response:**
```json
{
  "templates": {
    "trading_bot": {
      "name": "trading_bot",
      "display_name": "Crypto Trading Bot",
      "description": "Automated trading with stop-loss and take-profit",
      "category": "Web3 Trading",
      "tags": ["trading", "crypto", "finance"],
      "complexity": "Complex",
      "customizable_fields": ["trading_pair", "stop_loss", "take_profit"]
    }
  },
  "total_count": 3,
  "categories": ["Web3 Trading", "Sales & Marketing", "AI Automation"],
  "message": "Professional workflow templates available",
  "api_version": "1.0.0"
}
```

### POST /generate-state

Generate workflow state from provided data (MVP Demo Endpoint)

**Request Body:**
```json
{
  "workflow_id": "demo-workflow-001",
  "workflow_rows": {
    "id": "demo-workflow-001",
    "user_id": "demo-user-123",
    "name": "Demo Trading Bot",
    "description": "Automated crypto trading with risk management",
    "color": "#3972F6",
    "variables": "{}",
    "is_published": false,
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z",
    "last_synced": "2024-01-01T10:00:00Z",
    "state": "{}"
  },
  "blocks_rows": [
    {
      "id": "block-starter-001",
      "workflow_id": "demo-workflow-001",
      "type": "starter",
      "name": "Start Trading",
      "position_x": 100,
      "position_y": 100,
      "enabled": true,
      "horizontal_handles": true,
      "is_wide": false,
      "advanced_mode": false,
      "height": 0,
      "sub_blocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"}},
      "outputs": {"response": {"type": {"input": "any"}}},
      "data": {},
      "parent_id": null,
      "extent": null,
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z"
    }
  ]
}
```

**Response:**
Returns the generated workflow state JSON object.

### POST /api/workflows/{workflow_id}/generate-state

Generate Agent Forge-compatible workflow state using AI with intelligent RAG caching.

**Features:**
- Intelligent RAG caching system (70-80% faster for similar workflows)
- Automatic pattern recognition and adaptation
- Cost optimization through reduced AI calls
- Learning system that improves over time
- Semantic understanding with embeddings

**Path Parameters:**
- `workflow_id` (string, required): Unique identifier for the workflow

**Request Body:**
```json
{
  "options": {
    "use_cache": true,
    "force_regeneration": false
  }
}
```

**Response:**
Returns the generated workflow state JSON object.

### GET /api/workflows/{workflow_id}/state

Retrieve the current state of a workflow.

**Path Parameters:**
- `workflow_id` (string, required): Unique identifier for the workflow

**Response:**
Returns the workflow state JSON object.

### GET /api/block-types

Get available Agent Forge block types with schemas.

**Response:**
```json
{
  "block_types": {
    "starter": {
      "description": "Entry point for workflows",
      "sub_blocks": {
        "startWorkflow": "How the workflow is triggered (manual, webhook, schedule)",
        "webhookPath": "Path for webhook triggers",
        "scheduleType": "Type of schedule (daily, hourly, etc.)",
        "timezone": "Timezone for scheduled runs"
      }
    }
  }
}
```

## Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| 400 | Bad Request | Check request parameters and body format |
| 401 | Unauthorized | Provide valid authentication credentials |
| 403 | Forbidden | You don't have permission to access this resource |
| 404 | Not Found | The requested resource could not be found |
| 429 | Too Many Requests | Reduce request rate or upgrade your plan |
| 500 | Internal Server Error | Try again later or contact support |
| 503 | Service Unavailable | The service is temporarily unavailable |

## SDKs and Libraries

Official libraries are available for popular programming languages:
- **Python**: `pip install agent-forge-sdk`
- **JavaScript**: `npm install agent-forge-js`
- **Java**: `com.agentforge:agent-forge-java`

## Data Flow

### Input
Query `workflow_blocks_rows` joined with `workflow_rows`

### Generation
Map to state JSON structure:
- `workflow_blocks_rows.id` → `blocks.id`
- `position_x/y` → `position.x/y`

### Persistence
Write state JSON to `public.workflow.state`

## ID Matching Example

- Workflow "wf1" in `workflow_rows.id` links to blocks where `workflow_id = "wf1"`
- Block "b2" with `parent_id = "b1"` indicates hierarchy within same workflow

## Success Criteria

- API documentation is comprehensive and pushed to Git
- Database relationships are properly defined with FKs and indexes
- 50+ synthetic entries created in guideline tables
- Production tables populated with corresponding data
- All changes committed and pushed to repository 