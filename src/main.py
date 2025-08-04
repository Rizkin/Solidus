"""
Agent Forge State Generator - Main FastAPI Application
Minimal version optimized for Vercel serverless deployment
"""
import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Configure logging for serverless
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Agent Forge State Generator",
    description="AI-powered workflow state generator for Agent Forge platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with Agent Forge branding"""
    return {
        "name": "Agent Forge State Generator",
        "version": "1.0.0",
        "status": "operational",
        "deployment": "vercel-serverless",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "features": [
            "AI-powered workflow state generation",
            "Template-based workflow creation",
            "Multi-agent team support", 
            "Web3 and DeFi automation",
            "Real-time validation",
            "Marketplace integration"
        ],
        "endpoints": {
            "health": "/api/health",
            "docs": "/docs",
            "templates": "/api/templates",
            "debug": "/api/debug"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "deployment": "vercel-serverless",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
        "environment": {
            "vercel": os.getenv("VERCEL", "false"),
            "vercel_region": os.getenv("VERCEL_REGION", "unknown"),
            "vercel_url": os.getenv("VERCEL_URL", "unknown")
        },
        "agent_forge_status": {
            "core_api": "active",
            "template_system": "active",
            "ai_integration": "configured" if os.getenv("ANTHROPIC_API_KEY") else "not_configured",
            "database": "configured" if os.getenv("SUPABASE_URL") else "not_configured"
        }
    }

@app.get("/api/debug")
async def debug_info():
    """Debug information for troubleshooting"""
    return {
        "environment_info": {
            "current_working_directory": os.getcwd(),
            "python_path": os.sys.path[:5],
            "environment_variables": {
                k: v for k, v in os.environ.items() 
                if k.startswith(('VERCEL_', 'PYTHONPATH', 'SUPABASE_', 'ANTHROPIC_'))
            }
        },
        "deployment_info": {
            "vercel_deployment": os.getenv("VERCEL", "false"),
            "vercel_region": os.getenv("VERCEL_REGION", "unknown"),
            "vercel_url": os.getenv("VERCEL_URL", "unknown"),
            "function_name": os.getenv("AWS_LAMBDA_FUNCTION_NAME", "unknown")
        },
        "file_system": {
            "root_files": os.listdir(".") if os.path.exists(".") else [],
            "src_exists": os.path.exists("src"),
            "api_exists": os.path.exists("api")
        }
    }

@app.get("/api/templates")
async def list_templates():
    """List available workflow templates (minimal version)"""
    return {
        "templates": [
            {
                "name": "trading_bot",
                "display_name": "Crypto Trading Bot",
                "description": "Automated trading with stop-loss and take-profit",
                "category": "Web3 Trading",
                "status": "available"
            },
            {
                "name": "lead_generation", 
                "display_name": "Lead Generation System",
                "description": "Capture and qualify leads from multiple sources",
                "category": "Sales & Marketing",
                "status": "available"
            },
            {
                "name": "multi_agent_research",
                "display_name": "Multi-Agent Research Team", 
                "description": "Collaborative AI agents for research tasks",
                "category": "AI Automation",
                "status": "available"
            },
            {
                "name": "web3_automation",
                "display_name": "Web3 DeFi Automation",
                "description": "Smart contract monitoring and DeFi operations", 
                "category": "Blockchain",
                "status": "available"
            }
        ],
        "total_templates": 4,
        "deployment": "vercel-serverless"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for better error reporting"""
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "deployment": "vercel-serverless",
            "path": str(request.url),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 