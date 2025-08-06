"""
Vercel ASGI app - correct format for Python on Vercel
"""
from fastapi import FastAPI

# Create the FastAPI app
app = FastAPI(
    title="Agent Forge Test",
    version="1.0.0"
)

@app.get("/")
@app.get("/api/health")
async def health():
    return {
        "status": "healthy", 
        "message": "ASGI format test",
        "deployment": "vercel-python"
    }

@app.get("/api/templates")
async def templates():
    return {
        "templates": {"test": "working"},
        "message": "Templates endpoint test"
    }

# This is the correct export for Vercel ASGI
app = app
