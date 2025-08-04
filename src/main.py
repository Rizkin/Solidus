"""
Agent Forge State Generator - Main FastAPI Application
Ultra-minimal version for Vercel serverless deployment
"""
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create minimal FastAPI app
app = FastAPI(
    title="Agent Forge State Generator",
    description="AI-powered workflow state generator for Agent Forge platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with Agent Forge branding"""
    return {
        "name": "Agent Forge State Generator",
        "version": "1.0.0",
        "status": "operational",
        "deployment": "vercel-serverless",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": "🚀 Agent Forge State Generator is running successfully on Vercel!",
        "features": [
            "AI-powered workflow state generation",
            "Template-based workflow creation",
            "Multi-agent team support", 
            "Web3 and DeFi automation",
            "Real-time validation",
            "Marketplace integration"
        ]
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "deployment": "vercel-serverless",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "agent-forge-state-generator",
        "message": "All systems operational"
    }

@app.get("/api/templates")
async def list_templates():
    """List available workflow templates"""
    return {
        "templates": [
            {
                "name": "trading_bot",
                "display_name": "Crypto Trading Bot",
                "description": "Automated trading with stop-loss and take-profit",
                "category": "Web3 Trading",
                "status": "available"
            },
            {
                "name": "lead_generation", 
                "display_name": "Lead Generation System",
                "description": "Capture and qualify leads from multiple sources",
                "category": "Sales & Marketing",
                "status": "available"
            },
            {
                "name": "multi_agent_research",
                "display_name": "Multi-Agent Research Team", 
                "description": "Collaborative AI agents for research tasks",
                "category": "AI Automation",
                "status": "available"
            },
            {
                "name": "web3_automation",
                "display_name": "Web3 DeFi Automation",
                "description": "Smart contract monitoring and DeFi operations", 
                "category": "Blockchain",
                "status": "available"
            }
        ],
        "total_templates": 4,
        "deployment": "vercel-serverless",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    } 