"""
Minimal FastAPI handler for Vercel testing
No imports from main application - just basic FastAPI functionality
"""
from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="Minimal Test")

@app.get("/")
async def root():
    return {
        "message": "Minimal FastAPI working!",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "success"
    }

@app.get("/demo")
async def demo():
    return {
        "demo": "Minimal FastAPI demo working",
        "message": "This is a basic test without complex dependencies",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

# Export for Vercel
handler = app 