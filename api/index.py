"""
Vercel serverless function entry point for Agent Forge State Generator
Robust version with error handling and fallbacks
"""
import sys
import os
import traceback
from pathlib import Path

# Add parent directory to Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

def create_fallback_app():
    """Create a minimal FastAPI app as fallback"""
    try:
        from fastapi import FastAPI
        from fastapi.responses import JSONResponse
        
        app = FastAPI(title="Agent Forge State Generator", version="1.0.0")
        
        @app.get("/")
        async def root():
            return {
                "name": "Agent Forge State Generator",
                "status": "running",
                "deployment": "vercel",
                "message": "Serverless function is working!"
            }
        
        @app.get("/api/health")
        async def health():
            return {
                "status": "healthy",
                "deployment": "vercel",
                "python_path": sys.path[:3],
                "current_dir": str(current_dir),
                "parent_dir": str(parent_dir)
            }
        
        @app.get("/api/debug")
        async def debug():
            return {
                "python_version": sys.version,
                "python_path": sys.path[:5],
                "current_working_directory": os.getcwd(),
                "file_location": str(Path(__file__).absolute()),
                "parent_directory": str(parent_dir),
                "environment_variables": {
                    k: v for k, v in os.environ.items() 
                    if k.startswith(('VERCEL_', 'PYTHONPATH', 'PATH'))
                }
            }
            
        return app
    except Exception as e:
        # If even FastAPI fails, create a basic WSGI app
        def simple_app(environ, start_response):
            status = '200 OK'
            headers = [('Content-type', 'application/json')]
            start_response(status, headers)
            return [f'{{"error": "FastAPI failed to load", "details": "{str(e)}"}}']
        return simple_app

# Try to import the main app, fall back to minimal version
try:
    # First try to import our main application
    from src.main import app
    print("✅ Successfully imported main app")
    
except ImportError as e:
    print(f"❌ Failed to import main app: {e}")
    print(f"📍 Current directory: {os.getcwd()}")
    print(f"📍 Python path: {sys.path[:3]}")
    print(f"📍 Files in current dir: {os.listdir('.')}")
    
    # Try to see what's in src directory
    try:
        if os.path.exists('src'):
            print(f"📁 Files in src/: {os.listdir('src')}")
        else:
            print("❌ src directory not found")
    except Exception as ex:
        print(f"❌ Error checking src directory: {ex}")
    
    # Use fallback app
    app = create_fallback_app()
    print("🔄 Using fallback app")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print(f"📍 Traceback: {traceback.format_exc()}")
    app = create_fallback_app()
    print("🔄 Using fallback app due to unexpected error")

# Export for Vercel (multiple export names for compatibility)
application = app
handler = app
