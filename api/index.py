"""
Vercel serverless function entry point for Agent Forge State Generator
Production deployment - clean and optimized
"""
import sys
import os
from pathlib import Path

# Add parent directory to Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Try to import the main app
try:
    from src.main import app
    print("✅ Successfully imported main app")
except Exception as e:
    print(f"❌ Failed to import main app: {e}")
    # Create minimal production fallback
    from fastapi import FastAPI
    
    app = FastAPI(
        title="Agent Forge State Generator", 
        version="1.0.0",
        description="AI-powered workflow state generator - Fallback Mode",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    @app.get("/")
    async def root():
        return {
            "name": "Agent Forge State Generator",
            "status": "running - fallback mode", 
            "version": "1.0.0",
            "mode": "fallback",
            "message": "Main app import failed, running minimal version"
        }
    
    @app.get("/api/health")
    async def health():
        return {
            "status": "healthy",
            "mode": "fallback",
            "message": "Minimal health check"
        }

# Export the app for Vercel
handler = app
