"""
Vercel serverless function entry point for Agent Forge State Generator
Simple, direct approach for maximum compatibility
"""
import sys
import os
from pathlib import Path

# Add parent directory to Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Simple approach - try to import and use the app directly
try:
    from src.main import app
    print("✅ Successfully imported main app")
except Exception as e:
    print(f"❌ Failed to import main app: {e}")
    
    # Create minimal FastAPI app as fallback
    from fastapi import FastAPI
    
    app = FastAPI(title="Agent Forge State Generator", version="1.0.0")
    
    @app.get("/")
    async def root():
        return {
            "name": "Agent Forge State Generator",
            "status": "running",
            "deployment": "vercel-serverless",
            "message": "Minimal fallback handler working!",
            "error": str(e)
        }
    
    @app.get("/api/health")
    async def health():
        return {
            "status": "healthy",
            "deployment": "vercel-serverless",
            "handler": "fallback",
            "import_error": str(e)
        }
    
    print("🔄 Using minimal fallback app")

# Export the app directly - no complex handling
# Vercel should handle the ASGI conversion automatically
