"""
Agent Forge State Generator - Main FastAPI Application
Full-featured version with all API endpoints
"""
import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("🚀 Agent Forge State Generator starting up...")
    
    # Check available services
    has_supabase = bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_KEY"))
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    
    if has_supabase:
        logger.info("✅ Supabase configuration detected")
    else:
        logger.info("🔄 Using mock database (no Supabase credentials configured)")
        
    if has_anthropic:
        logger.info("✅ Anthropic API key configured")
    else:
        logger.info("🔄 Using rule-based state generation (no AI key)")
        
    if has_openai:
        logger.info("✅ OpenAI API key configured")
    else:
        logger.info("🔄 OpenAI embeddings disabled (no API key)")
    
    yield
    
    logger.info("🔄 Agent Forge State Generator shutting down...")

# Create FastAPI application
app = FastAPI(
    title="Agent Forge State Generator",
    description="AI-powered workflow state generation platform with RAG caching and semantic search",
    version="1.2.0",
    lifespan=lifespan
)

# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for demo UI
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    logger.info("✅ Static files mounted at /static")
except Exception as e:
    logger.warning(f"⚠️ Could not mount static files: {e}")

# Try to include full API if available
try:
    from src.api.workflows import router as workflows_router
    app.include_router(workflows_router)
    logger.info("✅ Workflows router included")
except ImportError as e:
    logger.warning(f"⚠️ Could not import workflows router: {e}")
    logger.info("🔄 Running in minimal mode")

# Pydantic models for demo API
class WorkflowRowsData(BaseModel):
    id: str
    user_id: str
    workspace_id: Optional[str] = None
    folder_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    color: str = "#3972F6"
    variables: str = "{}"
    is_published: bool = False
    created_at: str
    updated_at: str
    last_synced: str
    state: str = "{}"

class WorkflowBlocksRowsData(BaseModel):
    id: str
    workflow_id: str
    type: str
    name: str
    position_x: float
    position_y: float
    enabled: bool = True
    horizontal_handles: bool = True
    is_wide: bool = False
    advanced_mode: bool = False
    height: float = 0
    sub_blocks: Dict[str, Any] = {}
    outputs: Dict[str, Any] = {}
    data: Dict[str, Any] = {}
    parent_id: Optional[str] = None
    extent: Optional[str] = None
    created_at: str
    updated_at: str

class GenerateStateRequest(BaseModel):
    workflow_id: str
    workflow_rows: WorkflowRowsData
    blocks_rows: List[WorkflowBlocksRowsData]

@app.get("/")
async def root():
    """Root endpoint with Agent Forge branding"""
    
    # Check if we have full functionality
    has_workflows = hasattr(app, 'routes') and any('/api/workflows' in str(route.path) for route in app.routes if hasattr(route, 'path'))
    
    return {
        "name": "Agent Forge State Generator",
        "version": "1.2.0",
        "status": "operational",
        "deployment": "vercel-serverless",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": "🚀 Agent Forge State Generator MVP with Demo UI!",
        "features": [
            "AI-powered workflow state generation",
            "Demo UI for technical interview",
            "RAG-enhanced intelligent caching", 
            "Semantic search capabilities",
            "Rule-based fallback generation",
            "Real-time validation"
        ],
        "demo": {
            "ui_endpoint": "/demo",
            "description": "Interactive demo interface for workflow state generation",
            "usage": "Visit /demo to input sample workflow data and generate state JSON"
        },
        "api_status": {
            "full_api": has_workflows,
            "endpoints": {
                "health": "/api/health",
                "docs": "/docs", 
                "demo": "/demo",
                "generate": "/generate-state",
                "templates": "/api/templates" if has_workflows else "Not available",
                "workflows": "/api/workflows" if has_workflows else "Not available"
            }
        },
        "environment": {
            "has_anthropic_key": bool(os.getenv("ANTHROPIC_API_KEY")),
            "has_supabase": bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_KEY")),
            "has_openai": bool(os.getenv("OPENAI_API_KEY")),
            "deployment_mode": "full" if has_workflows else "minimal"
        }
    }

@app.get("/demo", response_class=HTMLResponse)
async def demo_ui():
    """Serve the demo UI for technical interview"""
    try:
        with open("static/index.html", "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(
            content="""
            <html><head><title>Demo UI - File Not Found</title></head>
            <body>
                <h1>🚨 Demo UI Not Available</h1>
                <p>The demo UI file (static/index.html) was not found.</p>
                <p>Please ensure the static files are properly deployed.</p>
                <p><a href="/">← Back to API</a></p>
            </body></html>
            """,
            status_code=404
        )

@app.post("/generate-state")
async def generate_state_demo(request: GenerateStateRequest):
    """
    Generate workflow state from provided data (MVP Demo Endpoint)
    
    This endpoint accepts workflow_rows and blocks_rows data directly
    and generates the Agent Forge compatible state JSON.
    """
    try:
        logger.info(f"🎯 Demo: Generating state for workflow {request.workflow_id}")
        
        # Import state generator if available
        try:
            from src.services.state_generator import state_generator
            from src.services.validation import validator
            
            # Use the actual state generator
            workflow_data = request.workflow_rows.dict()
            blocks_data = [block.dict() for block in request.blocks_rows]
            
            logger.info(f"📊 Processing {len(blocks_data)} blocks")
            
            # Generate state using the AI agent logic
            generated_state = await state_generator.generate_workflow_state_from_data(
                workflow_data, blocks_data
            )
            
            # Validate the generated state
            validation_result = validator.validate_state(generated_state)
            if not validation_result.is_valid:
                logger.warning(f"⚠️ Validation warnings: {validation_result.warnings}")
            
            return {
                "success": True,
                "workflow_id": request.workflow_id,
                "generated_state": generated_state,
                "validation": {
                    "is_valid": validation_result.is_valid,
                    "warnings": validation_result.warnings,
                    "errors": validation_result.errors
                },
                "metadata": {
                    "generation_method": "ai_agent",
                    "blocks_processed": len(blocks_data),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
            
        except ImportError:
            logger.info("🔄 Using rule-based fallback for demo")
            
            # Rule-based fallback generation
            generated_state = generate_state_rule_based(request.workflow_rows, request.blocks_rows)
            
            return {
                "success": True,
                "workflow_id": request.workflow_id,
                "generated_state": generated_state,
                "validation": {
                    "is_valid": True,
                    "warnings": [],
                    "errors": []
                },
                "metadata": {
                    "generation_method": "rule_based_fallback",
                    "blocks_processed": len(request.blocks_rows),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
            
    except Exception as e:
        logger.error(f"❌ Error generating state: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating workflow state: {str(e)}"
        )

def generate_state_rule_based(workflow_rows: WorkflowRowsData, blocks_rows: List[WorkflowBlocksRowsData]) -> Dict[str, Any]:
    """
    Rule-based state generation for demo (fallback when AI services unavailable)
    """
    
    # Generate blocks dictionary
    blocks_dict = {}
    edges = []
    
    for i, block in enumerate(blocks_rows):
        block_id = block.id
        
        # Create block definition
        blocks_dict[block_id] = {
            "id": block_id,
            "type": block.type,
            "name": block.name,
            "position": {
                "x": block.position_x,
                "y": block.position_y
            },
            "enabled": block.enabled,
            "horizontalHandles": block.horizontal_handles,
            "isWide": block.is_wide,
            "advancedMode": block.advanced_mode,
            "height": block.height,
            "subBlocks": block.sub_blocks,
            "outputs": block.outputs,
            "data": block.data
        }
        
        # Generate edges (simple sequential connection for demo)
        if i > 0:
            prev_block = blocks_rows[i-1]
            edges.append({
                "id": f"edge-{prev_block.id}-{block_id}",
                "source": prev_block.id,
                "target": block_id,
                "sourceHandle": "default",
                "targetHandle": "default",
                "type": "default"
            })
    
    # Generate complete state
    state = {
        "version": "1.0.0",
        "metadata": {
            "id": workflow_rows.id,
            "name": workflow_rows.name,
            "description": workflow_rows.description,
            "created_at": workflow_rows.created_at,
            "updated_at": workflow_rows.updated_at,
            "user_id": workflow_rows.user_id,
            "workspace_id": workflow_rows.workspace_id,
            "color": workflow_rows.color,
            "variables": json.loads(workflow_rows.variables) if workflow_rows.variables else {}
        },
        "blocks": blocks_dict,
        "edges": edges,
        "settings": {
            "theme": "default",
            "grid": True,
            "snap": True
        },
        "stats": {
            "total_blocks": len(blocks_rows),
            "block_types": list(set(block.type for block in blocks_rows)),
            "total_edges": len(edges)
        }
    }
    
    return state

@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "Agent Forge State Generator",
        "version": "1.2.0",
        "deployment": "vercel-serverless",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": "MVP with Demo UI operational",
        "features": {
            "demo_ui": True,
            "state_generation": True,
            "rule_based_fallback": True
        }
    }

# Redirect /frontend to main frontend if it exists
@app.get("/frontend")
async def redirect_to_frontend():
    """Redirect to main frontend"""
    return RedirectResponse(url="/frontend/")

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

# Export the FastAPI app for Vercel
# Vercel will automatically detect this as an ASGI app
handler = app 