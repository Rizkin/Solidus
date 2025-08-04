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

# Debug environment variables
print("DEBUG: Checking environment variables...")
print(f"SUPABASE_URL: {'SET' if os.getenv('SUPABASE_URL') else 'NOT_SET'}")
print(f"SUPABASE_SERVICE_KEY: {'SET' if os.getenv('SUPABASE_SERVICE_KEY') else 'NOT_SET'}")
print(f"ANTHROPIC_API_KEY: {'SET' if os.getenv('ANTHROPIC_API_KEY') else 'NOT_SET'}")

# Simple approach - try to import and use the app directly
try:
    print("Trying to import src.main...")
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
    
    @app.get("/api/debug/supabase-test")
    async def supabase_test():
        """Test Supabase client import and initialization"""
        result = {
            "supabase_library": "not_tested",
            "client_creation": "not_tested",
            "error": None
        }
        
        try:
            # Test importing Supabase
            import supabase
            result["supabase_library"] = f"imported_version_{supabase.__version__}"
            
            # Test getting environment variables
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
            
            result["env_vars"] = {
                "url_set": bool(supabase_url),
                "key_set": bool(supabase_key),
                "url_length": len(supabase_url) if supabase_url else 0,
                "key_length": len(supabase_key) if supabase_key else 0
            }
            
            # Test creating client if variables are available
            if supabase_url and supabase_key:
                try:
                    from supabase import create_client
                    result["client_creation"] = "attempting"
                    client = create_client(supabase_url, supabase_key)
                    result["client_creation"] = "success"
                except Exception as client_error:
                    result["client_creation"] = f"failed: {str(client_error)}"
            else:
                result["client_creation"] = "skipped_no_credentials"
                
        except Exception as import_error:
            result["supabase_library"] = f"import_failed: {str(import_error)}"
            result["error"] = str(import_error)
        
        return result
    
    print("🔄 Using minimal fallback app")

# Export the app directly - no complex handling
# Vercel should handle the ASGI conversion automatically
