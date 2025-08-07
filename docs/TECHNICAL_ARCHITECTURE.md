# Technical Architecture - Agent Forge Platform

**System Architecture Documentation v2.0 (Updated 2025-01)**

---

## System Overview

AI-powered workflow automation platform with:

- **Backend**: FastAPI REST API with intelligent caching
- **AI Engine**: Multi-provider integration (Claude, OpenAI)
- **Database**: Supabase PostgreSQL with hybrid fallbacks
- **RAG System**: Vector embeddings for pattern matching
- **Deployment**: Serverless on Vercel

### Key Metrics
- 13 professional templates
- 9-validator compliance system
- 70-80% cost reduction via caching
- 5-10x speed improvement with RAG
- 99.9% uptime target

---

## High-Level Architecture

```mermaid
graph TB
    subgraph "Gateway"
        LB[Load Balancer]
        CDN[CDN Edge]
    end
    
    subgraph "Application"
        API[FastAPI Server]
        TEMPLATES[Template Service]
        STATE_GEN[State Generator]
        VALIDATOR[Validation Engine]
        CACHE[RAG Cache]
    end
    
    subgraph "AI Services"
        CLAUDE[Claude AI]
        OPENAI[OpenAI Embeddings]
        FALLBACK[Rule-Based]
    end
    
    subgraph "Data"
        SUPABASE[(Supabase)]
        MOCK[(Mock DB)]
        VECTOR[(Vector Store)]
    end
    
    LB --> API
    API --> TEMPLATES
    API --> STATE_GEN
    API --> VALIDATOR
    API --> CACHE
    
    STATE_GEN --> CLAUDE
    STATE_GEN --> FALLBACK
    CACHE --> OPENAI
    
    API --> SUPABASE
    API --> MOCK
    CACHE --> VECTOR
```

---

## Component Architecture

### Core Services
- **Template Service**: 13 workflow templates with CRUD operations
- **State Generator**: AI-powered workflow state creation
- **Validation Engine**: 9-validator compliance system
- **RAG Cache**: Pattern recognition and similarity matching

### AI Integration
- **Primary**: Claude 3.5 Sonnet for generation
- **Embeddings**: OpenAI text-embedding-3-small
- **Fallback**: Rule-based pattern generation

### Data Layer (v2.0)
- **Primary**: Supabase PostgreSQL with pgvector
- **Guideline Tables**: `workflow_rows`, `workflow_blocks_rows`
- **Production Tables**: `workflow`, `workflow_blocks`
- **Analytics**: `cache_stats`, `ai_usage_logs`, `validation_logs`
- **Org**: `users`, `workspaces`, `workflow_folders`
- **Views**: `workflow_summary`, `cache_performance`, `ai_usage_summary`
- **Triggers**: Auto-maintain `updated_at`

---

## Data Flow

```mermaid
sequenceDiagram
    participant API
    participant TEMPLATE as Template Service
    participant STATE as State Generator
    participant CACHE as RAG Cache
    participant AI as AI Services
    participant DB as Database
    
    API->>TEMPLATE: get_templates()
    TEMPLATE-->>API: template_data
    
    API->>STATE: generate_state()
    STATE->>CACHE: check_pattern()
    
    alt Cache Hit
        CACHE-->>STATE: cached_state
    else Cache Miss
        STATE->>AI: generate()
        AI-->>STATE: ai_state
        STATE->>CACHE: store_pattern()
    end
    
    STATE->>DB: save_workflow()
    STATE-->>API: generated_state
```

---

## Database Schema (v2.0)

```mermaid
erDiagram
    USERS {
        text id PK
        text email
        text name
        text plan_type
    }
    WORKSPACES {
        text id PK
        text owner_id FK
        text name
    }
    WORKFLOW_ROWS {
        text id PK
        text user_id FK
        text workspace_id FK
        text name
        json state
        timestamp created_at
    }
    WORKFLOW_BLOCKS_ROWS {
        text id PK
        text workflow_id FK
        text type
        jsonb sub_blocks
        jsonb outputs
        jsonb data
        numeric position_x
        numeric position_y
        text parent_id FK
    }
    WORKFLOW {
        text id PK
        text name
        json state
        timestamp created_at
    }
    WORKFLOW_BLOCKS {
        text id PK
        text workflow_id FK
        text type
        jsonb data
        numeric position_x
        numeric position_y
        text parent_id FK
    }
    WORKFLOW_LOOKUP {
        uuid id PK
        text lookup_key
        jsonb generated_state
        vector embedding
        integer usage_count
    }
    CACHE_STATS {
        uuid id PK
        text cache_type
        integer hit_count
        integer miss_count
        float hit_rate
    }
    AI_USAGE_LOGS {
        uuid id PK
        text workflow_id FK
        text provider
        text model
        integer token_count
        float cost_estimate
        timestamp created_at
    }
    VALIDATION_LOGS {
        uuid id PK
        text workflow_id FK
        text validation_type
        boolean passed
        float score
        timestamp created_at
    }

    USERS ||--o{ WORKSPACES : owns
    WORKSPACES ||--o{ WORKFLOW_ROWS : contains
    WORKFLOW_ROWS ||--o{ WORKFLOW_BLOCKS_ROWS : has
    WORKFLOW ||--o{ WORKFLOW_BLOCKS : has
    WORKFLOW ||--o{ WORKFLOW_LOOKUP : cached
```

---

## Migration & Population
- Script: `database/migration.sql`
- Function `generate_workflow_state(workflow_id)` assembles blocks/edges/metadata
- Copies guideline tables → production tables
- Populates cache lookup and analytics logs
- Emits validation and final reports

## Synthetic Data
- File: `database/synthetic-data.sql`
- 10 users, 5 workspaces, 15 workflows, 60+ blocks, analytics samples

## Monitoring & Analytics
- Views for summaries, performance dashboards
- Metrics: P95 latency, cache hit rate, AI cost/time

## Security
- Rate limiting, CORS, header hardening
- Secrets via env vars

## Links
- **API Docs**: https://solidus-olive.vercel.app/api/docs
- **PRD**: `docs/PRD.md`

---

*Architecture v2.0 | Updated 2025-01* 