"""
Simple test handler for Vercel debugging
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI(title="Agent Forge Test")

@app.get("/")
async def test_root():
    return JSONResponse({
        "message": "Test handler working!",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "success"
    })

@app.get("/test")
async def test_endpoint():
    return JSONResponse({
        "test": "Basic FastAPI working in Vercel",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

# Export for Vercel
handler = app 