"""
Agent Forge State Generator - Main FastAPI Application
Full-featured version with all API endpoints
"""
import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Configure logging
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to include workflows router
try:
    from src.api.workflows import router as workflows_router
    app.include_router(workflows_router)
    logger.info("✅ Workflows router included")
except ImportError as e:
    logger.warning(f"❌ Could not import workflows router: {e}")
    logger.info("🔄 Running in minimal mode")

@app.get("/")
async def root():
    """Root endpoint with Agent Forge branding"""
    
    # Check if we have full functionality
    has_workflows = hasattr(app, 'routes') and any('/api/workflows' in str(route.path) for route in app.routes if hasattr(route, 'path'))
    
    return {
        "name": "Agent Forge State Generator",
        "version": "1.0.0",
        "status": "operational",
        "deployment": "vercel-serverless",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": "🚀 Agent Forge State Generator is running successfully on Vercel!",
        "features": [
            "AI-powered workflow state generation",
            "Template-based workflow creation",
            "Multi-agent team support", 
            "Web3 and DeFi automation",
            "Real-time validation",
            "Marketplace integration"
        ],
        "api_status": {
            "full_api": has_workflows,
            "endpoints": {
                "health": "/api/health",
                "docs": "/docs",
                "templates": "/api/templates" if has_workflows else "Not available",
                "workflows": "/api/workflows" if has_workflows else "Not available"
            }
        },
        "environment": {
            "has_anthropic_key": bool(os.getenv("ANTHROPIC_API_KEY")),
            "has_supabase": bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_KEY")),
            "deployment_mode": "full" if has_workflows else "minimal"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring"""
    
    # Check database connection if available
    db_status = {"status": "not_configured", "type": "none"}
    try:
        from src.utils.database_hybrid import db_service
        db_health = await db_service.health_check()
        db_status = db_health
    except ImportError:
        db_status = {"status": "not_available", "type": "import_error"}
    except Exception as e:
        db_status = {"status": "error", "type": "exception", "error": str(e)}
    
    # Check AI integration
    ai_status = {
        "anthropic_configured": bool(os.getenv("ANTHROPIC_API_KEY")),
        "status": "configured" if os.getenv("ANTHROPIC_API_KEY") else "not_configured"
    }
    
    return {
        "status": "healthy",
        "deployment": "vercel-serverless",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "agent-forge-state-generator",
        "version": "1.0.0",
        "components": {
            "api": "operational",
            "database": db_status,
            "ai_integration": ai_status
        },
        "environment": {
            "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
            "vercel_region": os.getenv("VERCEL_REGION", "unknown"),
            "vercel_url": os.getenv("VERCEL_URL", "unknown")
        }
    }

@app.get("/api/templates")
async def list_templates():
    """List available workflow templates"""
    try:
        from src.services.templates import get_all_templates
        templates = get_all_templates()
        
        return {
            "templates": templates,
            "total_templates": len(templates),
            "deployment": "vercel-serverless",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "categories": list(set(t.get('category', 'General') for t in templates))
        }
    except ImportError:
        # Fallback templates
        return {
            "templates": [
                {
                    "name": "trading_bot",
                    "display_name": "Crypto Trading Bot",
                    "description": "Automated trading with stop-loss and take-profit",
                    "category": "Web3 Trading",
                    "complexity": "Complex",
                    "customizable_fields": ["trading_pair", "stop_loss", "take_profit"]
                },
                {
                    "name": "lead_generation",
                    "display_name": "Lead Generation System",
                    "description": "Capture and qualify leads from multiple sources",
                    "category": "Sales & Marketing",
                    "complexity": "Medium",
                    "customizable_fields": ["source", "crm_integration"]
                },
                {
                    "name": "multi_agent_research",
                    "display_name": "Multi-Agent Research Team",
                    "description": "Collaborative AI agents for research tasks",
                    "category": "AI Automation",
                    "complexity": "Complex",
                    "customizable_fields": ["research_topic", "agent_count"]
                },
                {
                    "name": "web3_automation",
                    "display_name": "Web3 DeFi Automation",
                    "description": "Smart contract monitoring and DeFi operations",
                    "category": "Blockchain",
                    "complexity": "Complex",
                    "customizable_fields": ["chain", "contract_address"]
                }
            ],
            "total_templates": 4,
            "deployment": "vercel-serverless",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "note": "Fallback templates - full service may not be available"
        }

@app.get("/api/debug")
async def debug_info():
    """Debug information for troubleshooting"""
    
    # Check what services are available
    services_status = {}
    
    try:
        from src.services.state_generator import state_generator
        services_status["state_generator"] = "available"
    except ImportError:
        services_status["state_generator"] = "not_available"
    
    try:
        from src.services.validation import validator
        services_status["validator"] = "available"
    except ImportError:
        services_status["validator"] = "not_available"
    
    try:
        from src.services.templates import get_all_templates
        services_status["templates"] = "available"
    except ImportError:
        services_status["templates"] = "not_available"
    
    try:
        from src.utils.database_hybrid import db_service
        services_status["database"] = "available"
    except ImportError:
        services_status["database"] = "not_available"
    
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
        "services_status": services_status,
        "api_routes": [
            {"path": route.path, "methods": list(route.methods)} 
            for route in app.routes 
            if hasattr(route, 'path') and hasattr(route, 'methods')
        ],
        "file_system": {
            "root_files": os.listdir(".") if os.path.exists(".") else [],
            "src_exists": os.path.exists("src"),
            "api_exists": os.path.exists("api"),
            "src_contents": os.listdir("src") if os.path.exists("src") else []
        }
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
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "suggestion": "Check /api/debug for more information"
        }
    )

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 