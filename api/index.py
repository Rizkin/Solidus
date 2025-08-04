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

# Store import error message
import_error = None

# Simple approach - try to import and use the app directly
try:
    from src.main import app
    print("✅ Successfully imported main app")
except Exception as e:
    import_error = str(e)
    print(f"❌ Failed to import main app: {import_error}")
    
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
            "error": import_error or "Unknown error"
        }
    
    @app.get("/api/health")
    async def health():
        return {
            "status": "healthy",
            "deployment": "vercel-serverless",
            "handler": "fallback",
            "import_error": import_error or "Unknown error"
        }
    
    @app.get("/api/debug/env")
    async def debug_env():
        """Debug endpoint to check environment variables"""
        env_vars = {}
        for key, value in os.environ.items():
            if any(keyword in key.upper() for keyword in ['SUPABASE', 'ANTHROPIC', 'VERCEL']):
                # Mask sensitive values
                env_vars[key] = f"SET ({len(value)} chars)" if value else "NOT_SET"
            elif key in ['PATH', 'PYTHONPATH']:
                # Show first few chars for path variables
                env_vars[key] = value[:50] + "..." if len(value) > 50 else value
        
        return {
            "environment_variables": env_vars,
            "supabase_url": os.getenv("SUPABASE_URL", "NOT_SET"),
            "supabase_key": "SET" if os.getenv("SUPABASE_SERVICE_KEY") else "NOT_SET",
            "anthropic_key": "SET" if os.getenv("ANTHROPIC_API_KEY") else "NOT_SET"
        }
    
    print("🔄 Using minimal fallback app")

# Export the app directly - no complex handling
# Vercel should handle the ASGI conversion automatically
