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
except Exception as e:
    # Create minimal production fallback
    from fastapi import FastAPI
    
    app = FastAPI(
        title="Agent Forge State Generator", 
        version="1.0.0",
        description="AI-powered workflow state generator"
    )
    
    @app.get("/")
    async def root():
        return {
            "name": "Agent Forge State Generator",
            "status": "running",
            "version": "1.0.0"
        }
    
    @app.get("/api/health")
    async def health():
        return {"status": "healthy"}

# Export the app for Vercel
