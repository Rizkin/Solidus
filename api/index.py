"""
Agent Forge API - FastAPI Implementation
Now that Vercel configuration is fixed, we can use proper FastAPI
"""
from fastapi import FastAPI
from datetime import datetime
import os

# Create FastAPI app with proper docs configuration
app = FastAPI(
    title="Agent Forge API",
    description="AI-powered workflow automation platform with professional templates",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

@app.get("/api/")
async def api_root():
    """Simple API status - confirms API is functional"""
    return {
        "message": "Agent Forge API is fully functional! 🚀",
        "status": "operational",
        "version": "1.0.0",
        "documentation": "/api/docs",
        "endpoints": {
            "health": "/api/health",
            "templates": "/api/templates",
            "docs": "/api/docs"
        }
    }

@app.get("/")
async def root():
    """Root endpoint with redirect info"""
    return {
        "name": "Agent Forge API", 
        "message": "API is working! Visit /api/docs for documentation",
        "api_base": "/api/",
        "documentation": "/api/docs",
        "status": "ready"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "Agent Forge API",
        "deployment": "vercel-fastapi",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": "All systems operational"
    }

@app.get("/api/templates")
async def get_templates():
    """Get available workflow templates"""
    return {
        "templates": {
            "trading_bot": {
                "name": "trading_bot",
                "display_name": "Crypto Trading Bot", 
                "description": "Automated trading with stop-loss and take-profit",
                "category": "Web3 Trading",
                "tags": ["trading", "crypto", "finance"],
                "complexity": "Complex",
                "customizable_fields": ["trading_pair", "stop_loss", "take_profit"]
            },
            "lead_generation": {
                "name": "lead_generation", 
                "display_name": "Lead Generation System",
                "description": "Capture and qualify leads from multiple sources", 
                "category": "Sales & Marketing",
                "tags": ["sales", "marketing", "crm"],
                "complexity": "Medium",
                "customizable_fields": ["source", "crm_integration"]
            },
            "ai_research": {
                "name": "ai_research",
                "display_name": "AI Research Assistant",
                "description": "Multi-agent research collaboration system",
                "category": "AI Automation", 
                "tags": ["research", "ai", "analysis"],
                "complexity": "Complex",
                "customizable_fields": ["research_topic", "depth_level"]
            }
        },
        "total_count": 3,
        "categories": ["Web3 Trading", "Sales & Marketing", "AI Automation"],
        "message": "Professional workflow templates available",
        "api_version": "1.0.0"
    }

# Export for Vercel
handler = app
