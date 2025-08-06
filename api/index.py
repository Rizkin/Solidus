"""
Minimal Vercel ASGI app - Essential dependencies only
Testing basic FastAPI deployment without complex dependencies
"""
from fastapi import FastAPI
import os
from datetime import datetime

# Create the minimal FastAPI app
app = FastAPI(
    title="Agent Forge API - Minimal",
    version="1.0.0",
    description="Minimal version for debugging Vercel deployment"
)

@app.get("/")
async def root():
    return {
        "name": "Agent Forge State Generator",
        "status": "minimal-mode",
        "version": "1.0.0",
        "mode": "essential-dependencies-only",
        "message": "Basic FastAPI deployment test successful!"
    }

@app.get("/api/health") 
async def health():
    return {
        "status": "healthy",
        "deployment": "vercel-minimal",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "dependencies": ["fastapi", "pydantic", "python-dotenv"],
        "message": "Minimal API working - dependencies resolved!"
    }

@app.get("/api/templates")
async def templates():
    # Return mock templates without database dependencies
    return {
        "templates": {
            "minimal_test": {
                "name": "minimal_test",
                "display_name": "Minimal Test Template",
                "description": "Basic template for testing deployment",
                "category": "Test",
                "tags": ["test", "minimal"],
                "complexity": "Simple",
                "customizable_fields": ["name", "description"]
            },
            "basic_workflow": {
                "name": "basic_workflow", 
                "display_name": "Basic Workflow",
                "description": "Simple workflow template",
                "category": "Basic",
                "tags": ["workflow", "simple"],
                "complexity": "Simple",
                "customizable_fields": ["workflow_name"]
            }
        },
        "total_count": 2,
        "categories": ["Test", "Basic"],
        "status": "minimal-mode-active",
        "message": "Templates endpoint working without complex dependencies"
    }

# Correct ASGI export for Vercel
app = app
