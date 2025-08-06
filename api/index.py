"""
Vercel serverless function entry point for Agent Forge State Generator
Minimal debug version to isolate issues
"""
from fastapi import FastAPI

# Create minimal app first
app = FastAPI(
    title="Agent Forge State Generator",
    version="1.0.0", 
    description="AI-powered workflow state generator - Debug Mode"
)

@app.get("/")
async def root():
    return {
        "name": "Agent Forge State Generator",
        "status": "debug mode active",
        "version": "1.0.0",
        "message": "Minimal version working - will expand gradually"
    }

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "deployment": "vercel-serverless-debug",
        "message": "Basic health check working"
    }

@app.get("/api/templates")
async def get_templates_minimal():
    return {
        "templates": {
            "test_template": {
                "name": "test_template",
                "display_name": "Test Template",
                "description": "Minimal test template",
                "category": "Test",
                "tags": ["test"]
            }
        },
        "total_count": 1,
        "categories": ["Test"],
        "debug": "minimal templates working"
    }

# Export for Vercel
handler = app
