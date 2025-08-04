# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from src.models.connection import engine, get_db
from src.models.database import Base
from src.utils.supabase import supabase_client
from src.utils.config import settings
from src.api.workflows import router as workflow_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    logger.info("Starting Agent Forge State Generator...")
    logger.info(f"Connected to Supabase project: {settings.supabase_project_id}")
    
    # Test Supabase connection
    try:
        # Test query using Supabase client
        result = supabase_client.table('workflow').select("count").execute()
        logger.info(f"Supabase connection successful. Workflows in database: {len(result.data) if result.data else 0}")
    except Exception as e:
        logger.error(f"Supabase connection failed: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Agent Forge State Generator...")
    await engine.dispose()

# Create FastAPI app
app = FastAPI(
    title="Agent Forge Workflow State Generator",
    description="AI-powered state generator for Agent Forge workflows",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for Supabase
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://acptpimmuyvhjrsmzltc.supabase.co",
        "https://*.supabase.co"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include workflow routes
app.include_router(workflow_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Agent Forge State Generator",
        "version": "1.0.0",
        "status": "operational",
        "supabase_project": settings.supabase_project_id,
        "ai_model": "claude-3-opus",
        "features": [
            "AI-powered workflow state generation",
            "Agent Forge pattern detection",
            "9-validator compliance checking",
            "Edge inference from positions",
            "Fallback generation system"
        ]
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "checks": {}
    }
    
    # Check database connection
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        health_status["checks"]["database"] = "connected"
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["checks"]["database"] = f"error: {str(e)}"
    
    # Check Supabase client
    try:
        result = supabase_client.table('workflow').select("count").execute()
        health_status["checks"]["supabase_client"] = "connected"
        health_status["checks"]["workflow_count"] = len(result.data) if result.data else 0
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["checks"]["supabase_client"] = f"error: {str(e)}"
    
    # Check Claude API (basic check)
    try:
        from src.integrations.claude_client import claude_client
        health_status["checks"]["claude_api"] = "configured"
    except Exception as e:
        health_status["checks"]["claude_api"] = f"error: {str(e)}"
    
    return health_status

@app.get("/api/test-supabase")
async def test_supabase():
    """Test Supabase connection and data"""
    try:
        # Get workflows using Supabase client
        workflows = supabase_client.table('workflow').select("*").execute()
        
        # Get workflow blocks
        blocks = supabase_client.table('workflow_blocks').select("*").execute()
        
        return {
            "status": "success",
            "workflows": {
                "count": len(workflows.data) if workflows.data else 0,
                "data": workflows.data[:2] if workflows.data else []  # First 2 workflows
            },
            "blocks": {
                "count": len(blocks.data) if blocks.data else 0,
                "types": list(set([b['type'] for b in blocks.data])) if blocks.data else []
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
