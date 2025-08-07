# Agent Forge API Documentation v2.0

## Overview

Agent Forge is an AI-powered workflow automation platform that generates workflow state JSON objects from database records. The system reads from `workflow_rows` and `workflow_blocks_rows` tables and produces Agent Forge-compatible state objects with blocks, edges, and metadata.

### Key Features
- **🤖 AI-Powered Generation**: Claude AI for intelligent workflow state creation
- **⚡ RAG Caching**: 70-80% cost reduction through intelligent pattern matching  
- **🗄️ Database Integration**: PostgreSQL/Supabase with hybrid fallbacks
- **✅ 9-Validator System**: Comprehensive compliance checking
- **📊 Real-time Analytics**: Performance monitoring and metrics

## Base URL

```
Production: https://solidus-olive.vercel.app
Local Dev:  http://localhost:8000
```

## Authentication

### API Keys (Optional)

For enhanced security and access to premium features:

```bash
# Set your API key as an environment variable
export AGENT_FORGE_API_KEY="agf_live_1a2b3c4d5e6f7g8h9i0j"

# Use in requests
curl -H "Authorization: Bearer $AGENT_FORGE_API_KEY" \
  -H "Content-Type: application/json" \
  https://solidus-olive.vercel.app/api/workflows/wf1/generate-state
```

### Rate Limiting

| User Type | Limit | Window |
|-----------|-------|--------|
| Anonymous | 100 requests | 1 hour |
| Authenticated | 1,000 requests | 1 hour |
| Premium | 10,000 requests | 1 hour |

Rate limit headers are included in all responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Core Endpoints

### GET /api/
**Simple API status endpoint - confirms API is functional**

**Example Request:**
```bash
curl https://solidus-olive.vercel.app/api/
```

**Response:**
```json
{
  "message": "Agent Forge API is fully functional! 🚀",
  "status": "operational",
  "version": "2.0.0",
  "api_ready": true,
  "endpoints": {
    "health": "/api/health",
    "docs": "/api/docs",
    "templates": "/api/templates",
    "workflows": "/api/workflows/*",
    "generate": "/generate-state"
  },
  "features": {
    "ai_generation": true,
    "rag_caching": true,
    "analytics": true,
    "validation": true
  }
}
```

### GET /api/health
**Comprehensive health check endpoint for monitoring**

**Example Request:**
```bash
curl https://solidus-olive.vercel.app/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Agent Forge API",
  "deployment": "vercel-serverless",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "2.0.0",
  "uptime": "99.9%",
  "dependencies": {
    "database": {
      "status": "connected",
      "response_time_ms": 45,
      "connection_pool": "healthy"
    },
    "ai_services": {
      "claude": "operational",
      "openai": "operational",
      "fallback": "ready"
    },
    "cache": {
      "hit_rate": "78.5%",
      "size_mb": 124.7,
      "status": "optimal"
    }
  },
  "metrics": {
    "requests_per_minute": 45,
    "avg_response_time_ms": 187,
    "error_rate": "0.02%"
  }
}
```

## Template Management

### GET /api/templates
**Get available workflow templates with detailed metadata**

**Query Parameters:**
- `category` (optional): Filter by category
- `complexity` (optional): Filter by complexity level
- `tags` (optional): Comma-separated list of tags

**Example Request:**
```bash
curl "https://solidus-olive.vercel.app/api/templates?category=Web3%20Trading&complexity=Complex"
```

**Response:**
```json
{
  "templates": {
    "trading_bot": {
      "id": "trading_bot",
      "name": "trading_bot",
      "display_name": "Crypto Trading Bot",
      "description": "Automated trading with stop-loss and take-profit",
      "category": "Web3 Trading",
      "tags": ["trading", "crypto", "finance", "automation"],
      "complexity": "Complex",
      "estimated_setup_time": "15-30 minutes",
      "customizable_fields": {
        "trading_pair": {
          "type": "string",
          "description": "Trading pair symbol",
          "example": "BTC/USD",
          "required": true
        },
        "stop_loss": {
          "type": "number",
          "description": "Stop loss percentage",
          "example": 0.02,
          "range": [0.01, 0.1]
        },
        "take_profit": {
          "type": "number", 
          "description": "Take profit percentage",
          "example": 0.05,
          "range": [0.01, 0.2]
        }
      },
      "blocks": {
        "starter": 1,
        "api": 2,
        "agent": 1,
        "action": 3,
        "decision": 2
      },
      "use_cases": [
        "Automated cryptocurrency trading",
        "Risk management with stop-loss",
        "Profit optimization strategies"
      ]
    },
    "lead_generation": {
      "id": "lead_generation",
      "display_name": "Lead Generation Pipeline",
      "description": "Automated lead capture and qualification",
      "category": "Sales & Marketing",
      "tags": ["sales", "marketing", "leads", "crm"],
      "complexity": "Medium",
      "estimated_setup_time": "10-20 minutes"
    }
  },
  "metadata": {
    "total_count": 13,
    "categories": ["Web3 Trading", "Sales & Marketing", "AI Automation", "Data Processing"],
    "complexity_levels": ["Simple", "Medium", "Complex", "Expert"],
    "most_popular": ["trading_bot", "lead_generation", "ai_research"]
  },
  "message": "Professional workflow templates available",
  "api_version": "2.0.0"
}
```

### GET /api/templates/{template_id}
**Get detailed template configuration**

**Path Parameters:**
- `template_id` (string): Template identifier

**Example Request:**
```bash
curl https://solidus-olive.vercel.app/api/templates/trading_bot
```

## Workflow State Generation

### POST /generate-state
**Generate workflow state from provided data (Demo Endpoint)**

**Request Headers:**
```
Content-Type: application/json
Authorization: Bearer <api_key> (optional)
```

**Request Body:**
```json
{
  "workflow_id": "demo-trading-bot-001",
  "workflow_rows": {
    "id": "demo-trading-bot-001", 
    "user_id": "user_123",
    "workspace_id": "ws_456",
    "name": "Advanced Trading Bot",
    "description": "Automated crypto trading with AI decision making and risk management",
    "color": "#3972F6",
    "variables": {
      "trading_pair": "BTC/USD",
      "stop_loss": 0.02,
      "take_profit": 0.05,
      "risk_tolerance": "medium"
    },
    "is_published": false,
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "last_synced": "2024-01-15T10:30:00Z",
    "state": "{}"
  },
  "blocks_rows": [
    {
      "id": "block-starter-001",
      "workflow_id": "demo-trading-bot-001",
      "type": "starter",
      "name": "Start Trading Bot",
      "position_x": 100,
      "position_y": 100,
      "enabled": true,
      "horizontal_handles": true,
      "is_wide": false,
      "advanced_mode": false,
      "height": 0,
      "sub_blocks": {
        "startWorkflow": {
          "id": "startWorkflow",
          "type": "dropdown",
          "value": "manual"
        },
        "scheduleType": {
          "id": "scheduleType", 
          "type": "dropdown",
          "value": "daily"
        }
      },
      "outputs": {
        "response": {
          "type": {"input": "any"}
        }
      },
      "data": {
        "trigger_conditions": ["market_open", "volatility_threshold"]
      },
      "parent_id": null,
      "extent": null,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    },
    {
      "id": "block-api-001",
      "workflow_id": "demo-trading-bot-001", 
      "type": "api",
      "name": "Fetch Market Data",
      "position_x": 300,
      "position_y": 100,
      "enabled": true,
      "sub_blocks": {
        "url": {
          "id": "url",
          "type": "short-input",
          "value": "https://api.coingecko.com/api/v3/coins/bitcoin"
        },
        "method": {
          "id": "method",
          "type": "dropdown", 
          "value": "GET"
        },
        "headers": {
          "id": "headers",
          "type": "json-input",
          "value": {"Content-Type": "application/json"}
        }
      },
      "outputs": {
        "data": "any",
        "status": "number",
        "headers": "json"
      },
      "data": {
        "timeout": 30000,
        "retry_count": 3
      }
    }
  ],
  "options": {
    "validate_output": true,
    "include_metadata": true,
    "use_ai_enhancement": true
  }
}
```

**Success Response (200):**
```json
{
  "success": true,
  "workflow_id": "demo-trading-bot-001",
  "generated_state": {
    "blocks": {
      "block-starter-001": {
        "id": "block-starter-001",
        "type": "starter", 
        "name": "Start Trading Bot",
        "position": {"x": 100, "y": 100},
        "enabled": true,
        "subBlocks": {
          "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"},
          "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "daily"}
        },
        "outputs": {
          "response": {"type": {"input": "any"}}
        },
        "data": {
          "trigger_conditions": ["market_open", "volatility_threshold"]
        }
      },
      "block-api-001": {
        "id": "block-api-001",
        "type": "api",
        "name": "Fetch Market Data", 
        "position": {"x": 300, "y": 100},
        "enabled": true,
        "subBlocks": {
          "url": {"id": "url", "type": "short-input", "value": "https://api.coingecko.com/api/v3/coins/bitcoin"},
          "method": {"id": "method", "type": "dropdown", "value": "GET"}
        },
        "outputs": {
          "data": "any",
          "status": "number", 
          "headers": "json"
        }
      }
    },
    "edges": [
      {
        "id": "edge-001",
        "source": "block-starter-001",
        "target": "block-api-001",
        "sourceHandle": "response",
        "targetHandle": "trigger"
      }
    ],
    "variables": {
      "trading_pair": "BTC/USD",
      "stop_loss": 0.02,
      "take_profit": 0.05
    },
    "metadata": {
      "version": "1.0.0",
      "created_at": "2024-01-15T10:30:00Z",
      "generated_by": "agent-forge-ai",
      "total_blocks": 2,
      "workflow_type": "trading_automation",
      "complexity_score": 7.5,
      "estimated_runtime": "5-10 minutes"
    }
  },
  "validation": {
    "passed": true,
    "validators_run": 9,
    "compliance_score": 95.5,
    "warnings": [],
    "suggestions": [
      "Consider adding error handling blocks",
      "Add logging for better debugging"
    ]
  },
  "performance": {
    "generation_time_ms": 847,
    "cache_hit": false,
    "ai_tokens_used": 1247,
    "cost_estimate_usd": 0.0089
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### POST /api/workflows/{workflow_id}/generate-state
**Advanced AI-powered state generation with RAG caching**

**Features:**
- 🧠 **Intelligent RAG Caching**: 70-80% faster for similar workflows
- 🔍 **Pattern Recognition**: Automatic adaptation and learning
- 💰 **Cost Optimization**: Reduced AI calls through smart caching
- 📈 **Learning System**: Improves accuracy over time
- 🎯 **Semantic Understanding**: Context-aware generation

**Path Parameters:**
- `workflow_id` (string, required): Unique identifier for the workflow

**Request Body:**
```json
{
  "options": {
    "use_cache": true,
    "force_regeneration": false,
    "ai_provider": "claude", 
    "complexity_level": "auto",
    "include_analytics": true,
    "validation_level": "strict"
  },
  "context": {
    "user_preferences": {
      "block_naming_style": "descriptive",
      "connection_style": "explicit"
    },
    "workflow_type": "trading_automation",
    "target_platform": "agent_forge"
  }
}
```

**Response Headers:**
```
X-Cache-Status: HIT|MISS|PARTIAL
X-Generation-Time: 847ms
X-AI-Tokens-Used: 1247
X-Cost-Estimate: $0.0089
```

## Block Types & Schemas

### GET /api/block-types
**Get comprehensive block type definitions with schemas**

**Query Parameters:**
- `category` (optional): Filter by block category
- `include_examples` (boolean): Include usage examples

**Example Request:**
```bash
curl "https://solidus-olive.vercel.app/api/block-types?include_examples=true"
```

**Response:**
```json
{
  "block_types": {
    "starter": {
      "category": "trigger",
      "description": "Entry point for workflows - defines how workflows are initiated",
      "icon": "▶️",
      "color": "#4CAF50",
      "properties": {
        "trigger_type": ["manual", "webhook", "schedule", "event"],
        "max_concurrent": "number",
        "timeout_seconds": "number"
      },
      "sub_blocks": {
        "startWorkflow": {
          "type": "dropdown",
          "description": "How the workflow is triggered",
          "options": ["manual", "webhook", "schedule", "event"],
          "default": "manual",
          "required": true
        },
        "webhookPath": {
          "type": "short-input", 
          "description": "Path for webhook triggers",
          "pattern": "^/[a-zA-Z0-9-_/]+$",
          "required_if": "trigger_type=webhook"
        },
        "scheduleType": {
          "type": "dropdown",
          "description": "Type of schedule",
          "options": ["daily", "hourly", "weekly", "monthly", "cron"],
          "required_if": "trigger_type=schedule"
        },
        "timezone": {
          "type": "dropdown",
          "description": "Timezone for scheduled runs",
          "options": ["UTC", "America/New_York", "Europe/London", "Asia/Tokyo"],
          "default": "UTC"
        }
      },
      "outputs": {
        "response": {
          "type": "any",
          "description": "Trigger response data"
        },
        "timestamp": {
          "type": "string",
          "description": "Trigger timestamp"
        }
      },
      "examples": [
        {
          "name": "Manual Trigger",
          "sub_blocks": {
            "startWorkflow": {"value": "manual"}
          }
        },
        {
          "name": "Daily Schedule",
          "sub_blocks": {
            "startWorkflow": {"value": "schedule"},
            "scheduleType": {"value": "daily"},
            "timezone": {"value": "UTC"}
          }
        }
      ]
    },
    "api": {
      "category": "integration",
      "description": "HTTP API calls to external services",
      "icon": "🌐",
      "color": "#2196F3",
      "properties": {
        "method": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "timeout_ms": "number",
        "retry_count": "number"
      },
      "sub_blocks": {
        "url": {
          "type": "short-input",
          "description": "API endpoint URL",
          "pattern": "^https?://",
          "required": true
        },
        "method": {
          "type": "dropdown",
          "options": ["GET", "POST", "PUT", "DELETE", "PATCH"],
          "default": "GET"
        },
        "headers": {
          "type": "json-input", 
          "description": "HTTP headers as JSON object",
          "default": {}
        },
        "body": {
          "type": "json-input",
          "description": "Request body for POST/PUT requests",
          "required_if": "method=POST|PUT|PATCH"
        }
      },
      "outputs": {
        "data": {
          "type": "any",
          "description": "Response data"
        },
        "status": {
          "type": "number", 
          "description": "HTTP status code"
        },
        "headers": {
          "type": "json",
          "description": "Response headers"
        }
      }
    },
    "agent": {
      "category": "ai",
      "description": "AI-powered decision making and content generation",
      "icon": "🤖",
      "color": "#9C27B0",
      "sub_blocks": {
        "model": {
          "type": "combobox",
          "options": ["gpt-4", "gpt-3.5-turbo", "claude-3", "claude-2"],
          "default": "gpt-4"
        },
        "systemPrompt": {
          "type": "long-input",
          "description": "System instructions for the AI",
          "placeholder": "You are a helpful assistant..."
        },
        "temperature": {
          "type": "slider",
          "min": 0,
          "max": 1,
          "step": 0.1,
          "default": 0.7
        }
      }
    }
  },
  "categories": {
    "trigger": ["starter"],
    "integration": ["api", "webhook", "database"],
    "ai": ["agent", "classifier"],
    "logic": ["decision", "loop", "parallel"],
    "action": ["action", "notification", "transform"]
  },
  "metadata": {
    "total_types": 15,
    "most_used": ["starter", "api", "agent", "action"],
    "version": "2.0.0"
  }
}
```

## Workflow Management

### GET /api/workflows
**List all workflows with filtering and pagination**

**Query Parameters:**
- `page` (number): Page number (default: 1)
- `limit` (number): Items per page (default: 20, max: 100)
- `user_id` (string): Filter by user
- `workspace_id` (string): Filter by workspace
- `status` (string): Filter by status
- `search` (string): Search in name/description

**Example Request:**
```bash
curl "https://solidus-olive.vercel.app/api/workflows?user_id=user_123&limit=10&search=trading"
```

### GET /api/workflows/{workflow_id}
**Get detailed workflow information**

### PUT /api/workflows/{workflow_id}
**Update workflow configuration**

### DELETE /api/workflows/{workflow_id}
**Delete workflow and associated data**

## Analytics & Monitoring

### GET /api/analytics/performance
**Get system performance metrics**

**Response:**
```json
{
  "cache_performance": {
    "hit_rate": 78.5,
    "miss_rate": 21.5, 
    "total_requests": 15420,
    "cache_size_mb": 124.7,
    "avg_response_time_cache_hit_ms": 45,
    "avg_response_time_cache_miss_ms": 2340
  },
  "ai_usage": {
    "total_requests_today": 1247,
    "tokens_consumed": 892456,
    "cost_today_usd": 12.34,
    "average_generation_time_ms": 1847,
    "providers": {
      "claude": {"requests": 892, "tokens": 645234},
      "openai": {"requests": 355, "tokens": 247222}
    }
  },
  "validation_stats": {
    "total_validations": 3456,
    "pass_rate": 94.2,
    "common_failures": [
      {"type": "missing_starter_block", "count": 45},
      {"type": "invalid_connections", "count": 23}
    ]
  }
}
```

## Error Handling

### Error Response Format

All errors follow a consistent format:

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Workflow validation failed",
    "details": "Missing required starter block",
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_1a2b3c4d5e6f",
    "documentation_url": "https://docs.agentforge.com/errors/VALIDATION_FAILED"
  },
  "context": {
    "workflow_id": "demo-workflow-001",
    "validation_step": "block_structure_check",
    "failed_validators": ["starter_block_validator"]
  }
}
```

### Error Codes

| Code | Status | Description | Resolution |
|------|---------|-------------|------------|
| `INVALID_REQUEST` | 400 | Malformed request body or parameters | Check request format and required fields |
| `UNAUTHORIZED` | 401 | Missing or invalid authentication | Provide valid API key in Authorization header |
| `FORBIDDEN` | 403 | Insufficient permissions | Check API key permissions or upgrade plan |
| `WORKFLOW_NOT_FOUND` | 404 | Workflow does not exist | Verify workflow_id exists in database |
| `VALIDATION_FAILED` | 422 | Workflow data failed validation | Fix validation errors listed in details |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests | Reduce request rate or upgrade plan |
| `AI_SERVICE_ERROR` | 502 | AI provider unavailable | Try again later, fallback rules applied |
| `DATABASE_ERROR` | 503 | Database connection failed | Service temporarily unavailable |
| `GENERATION_TIMEOUT` | 504 | AI generation took too long | Reduce complexity or try again |

### Error Examples

**400 Bad Request:**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Missing required field",
    "details": "Field 'workflow_id' is required but was not provided",
    "field": "workflow_id",
    "received_value": null
  }
}
```

**422 Validation Failed:**
```json
{
  "error": {
    "code": "VALIDATION_FAILED", 
    "message": "Workflow validation failed",
    "details": "Multiple validation errors found",
    "validation_errors": [
      {
        "validator": "starter_block_validator",
        "message": "Every workflow must have exactly one starter block",
        "found_count": 0,
        "required_count": 1
      },
      {
        "validator": "connection_validator",
        "message": "Block 'block-api-001' has invalid connection",
        "block_id": "block-api-001",
        "issue": "No valid input connection found"
      }
    ]
  }
}
```

**429 Rate Limit:**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded",
    "details": "You have exceeded your hourly rate limit of 1000 requests",
    "retry_after_seconds": 3600,
    "current_usage": 1001,
    "limit": 1000,
    "window": "1 hour"
  }
}
```

## SDKs and Libraries

### Python SDK
```bash
pip install agent-forge-python
```

```python
from agent_forge import AgentForgeClient

client = AgentForgeClient(api_key="agf_live_1a2b3c4d5e6f")

# Generate workflow state
result = client.workflows.generate_state(
    workflow_id="demo-workflow-001",
    options={"use_cache": True}
)

# Get templates
templates = client.templates.list(category="Web3 Trading")
```

### JavaScript SDK
```bash
npm install @agent-forge/js-sdk
```

```javascript
import { AgentForge } from '@agent-forge/js-sdk';

const client = new AgentForge({
  apiKey: 'agf_live_1a2b3c4d5e6f',
  baseURL: 'https://solidus-olive.vercel.app'
});

// Generate workflow state
const result = await client.workflows.generateState({
  workflowId: 'demo-workflow-001',
  options: { useCache: true }
});
```

## Webhooks

### Workflow Events

Agent Forge can send webhooks for important workflow events:

**Event Types:**
- `workflow.created`
- `workflow.updated` 
- `workflow.deleted`
- `workflow.state_generated`
- `workflow.validation_failed`

**Webhook Payload:**
```json
{
  "event": "workflow.state_generated",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "workflow_id": "demo-workflow-001",
    "user_id": "user_123",
    "generation_time_ms": 847,
    "cache_hit": false,
    "validation_passed": true
  },
  "webhook_id": "wh_1a2b3c4d5e6f"
}
```

## Data Flow Architecture

### Input Processing
1. **Query Phase**: Join `workflow_blocks_rows` with `workflow_rows`
2. **Validation Phase**: Run 9-validator compliance system
3. **Cache Check**: Search RAG cache for similar patterns

### Generation Pipeline
1. **Pattern Matching**: Semantic similarity search with embeddings
2. **AI Generation**: Claude AI for complex state creation
3. **Fallback Logic**: Rule-based generation if AI unavailable
4. **Post-processing**: Format output to Agent Forge schema

### State Mapping
```json
{
  "mapping": {
    "workflow_blocks_rows.id": "blocks.{id}.id",
    "workflow_blocks_rows.position_x": "blocks.{id}.position.x", 
    "workflow_blocks_rows.position_y": "blocks.{id}.position.y",
    "workflow_blocks_rows.sub_blocks": "blocks.{id}.subBlocks",
    "workflow_blocks_rows.outputs": "blocks.{id}.outputs",
    "workflow_blocks_rows.parent_id": "edges[].source"
  }
}
```

### Persistence Strategy
1. **State Storage**: Write to `public.workflow.state` as JSONB
2. **Cache Update**: Store successful patterns in `workflow_lookup`
3. **Analytics**: Log metrics to `ai_usage_logs` and `cache_stats`

## Testing

### Test Endpoints

**GET /api/test/health**
```json
{
  "test_results": {
    "database_connection": "✅ Connected",
    "ai_services": "✅ Operational", 
    "cache_system": "✅ Functional",
    "validation_engine": "✅ Ready"
  }
}
```

### Sample Test Data

Use these sample requests for testing:

```bash
# Test basic health
curl https://solidus-olive.vercel.app/api/health

# Test templates
curl https://solidus-olive.vercel.app/api/templates

# Test state generation
curl -X POST https://solidus-olive.vercel.app/generate-state \
  -H "Content-Type: application/json" \
  -d @test_data/sample_workflow.json
```

## Changelog

### v2.0.0 (2024-01-15)
- 🚀 Enhanced RAG caching system
- 📊 Real-time analytics dashboard
- 🔧 Improved error handling
- 📱 New mobile-friendly demo UI
- 🎯 9-validator compliance system

### v1.0.0 (2023-12-01)
- 🎉 Initial release
- 🤖 Claude AI integration
- 🗄️ Supabase database support
- ✅ Basic validation system

---

**Documentation Version**: 2.0.0  
**Last Updated**: January 15, 2024  
**API Version**: 2.0.0

For support, contact: [support@agentforge.com](mailto:support@agentforge.com)  
Documentation: [https://docs.agentforge.com](https://docs.agentforge.com) 