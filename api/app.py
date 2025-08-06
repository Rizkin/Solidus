"""
Vercel handler for FastAPI application
Routes requests to the main FastAPI app with full functionality
"""
import sys
import os

# Add the project root to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from src.main import app
    
    # Export the FastAPI app for Vercel
    # This allows Vercel to serve the FastAPI application as a serverless function
    handler = app
    
except ImportError as e:
    # Fallback if import fails
    print(f"Import error: {e}")
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    # Create a minimal fallback app
    handler = FastAPI(title="Agent Forge - Import Error")
    
    @handler.get("/")
    async def fallback():
        return JSONResponse({
            "error": "Import failed",
            "message": f"Could not import main app: {str(e)}",
            "status": "fallback_mode"
        })
    
    @handler.get("/{path:path}")
    async def fallback_all(path: str):
        return JSONResponse({
            "error": "Import failed", 
            "path": path,
            "message": f"Could not import main app: {str(e)}",
            "status": "fallback_mode"
        }) 