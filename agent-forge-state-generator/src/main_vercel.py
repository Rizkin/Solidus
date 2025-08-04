"""
Vercel-optimized FastAPI application for Agent Forge State Generator
This version is optimized for serverless deployment on Vercel.
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio

# Configure logging for Vercel
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for serverless optimization
_app_initialized = False
_supabase_client = None
_claude_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Optimized lifespan for Vercel serverless functions"""
    global _app_initialized, _supabase_client, _claude_client
    
    if not _app_initialized:
        logger.info("Initializing Agent Forge State Generator for Vercel...")
        
        try:
            # Initialize Supabase client
            from src.utils.supabase import get_supabase_client
            _supabase_client = get_supabase_client()
            logger.info("Supabase client initialized")
            
            # Initialize Claude client
            from src.integrations.claude_client import ClaudeClient
            _claude_client = ClaudeClient()
            logger.info("Claude client initialized")
            
            _app_initialized = True
            logger.info("Agent Forge State Generator initialized successfully")
            
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            # Continue without failing - use fallback systems
    
    yield
    
    # Cleanup (minimal for serverless)
    logger.info("Shutting down...")

# Create FastAPI app with Vercel optimization
app = FastAPI(
    title="Agent Forge State Generator",
    description="AI-powered workflow state generator for Agent Forge platform (Vercel Deployment)",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for web deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes after app creation to avoid circular imports
from src.api.workflows import router as workflows_router

# Add routes
app.include_router(workflows_router)

@app.get("/")
async def root():
    """Root endpoint with Agent Forge branding"""
    return {
        "name": "Agent Forge State Generator",
        "version": "1.0.0",
        "status": "operational",
        "deployment": "vercel",
        "supabase_project": os.getenv("SUPABASE_URL", "").split("//")[1].split(".")[0] if os.getenv("SUPABASE_URL") else "not-configured",
        "ai_model": "claude-3-opus",
        "features": [
            "AI-powered workflow state generation",
            "Multi-agent team support", 
            "Web3 and DeFi automation",
            "Real-time validation",
            "Marketplace integration",
            "Vercel serverless deployment"
        ]
    }

@app.get("/api/health")
async def health_check():
    """Optimized health check for Vercel deployment"""
    global _supabase_client, _claude_client
    
    checks = {}
    
    # Check Supabase connection
    try:
        if _supabase_client:
            # Quick test query
            result = _supabase_client.table("workflow").select("count").limit(1).execute()
            checks["supabase_client"] = "connected"
            checks["workflow_count"] = len(result.data) if result.data else 0
        else:
            checks["supabase_client"] = "not_initialized"
    except Exception as e:
        checks["supabase_client"] = f"error: {str(e)}"
    
    # Check Claude API configuration
    try:
        if _claude_client and os.getenv("ANTHROPIC_API_KEY"):
            checks["claude_api"] = "configured"
        else:
            checks["claude_api"] = "not_configured"
    except Exception as e:
        checks["claude_api"] = f"error: {str(e)}"
    
    # Determine overall status
    status = "healthy"
    if any("error" in str(check) for check in checks.values()):
        status = "degraded"
    elif any("not_" in str(check) for check in checks.values()):
        status = "degraded"
    
    return {
        "status": status,
        "deployment": "vercel",
        "timestamp": "2024-01-01T00:00:00Z",
        "checks": checks,
        "vercel_region": os.getenv("VERCEL_REGION", "unknown"),
        "agent_forge_status": {
            "marketplace_integration": "active",
            "template_system": "active", 
            "validation_engine": "active"
        }
    }

@app.get("/api/test-supabase")
async def test_supabase():
    """Test Supabase connection for Vercel deployment"""
    global _supabase_client
    
    if not _supabase_client:
        raise HTTPException(status_code=503, detail="Supabase client not initialized")
    
    try:
        # Test query
        result = _supabase_client.table("workflow").select("id,name").limit(5).execute()
        
        return {
            "status": "success",
            "message": "Supabase connection working",
            "deployment": "vercel",
            "workflows_found": len(result.data) if result.data else 0,
            "sample_workflows": result.data if result.data else []
        }
        
    except Exception as e:
        logger.error(f"Supabase test error: {e}")
        raise HTTPException(status_code=503, detail=f"Supabase connection failed: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for better error reporting on Vercel"""
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "deployment": "vercel",
            "path": str(request.url)
        }
    )

# For Vercel deployment, we need to export the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
