"""
Agent Forge API - Improved Python Handler
Reliable Vercel deployment with clean status messages and documentation
"""
from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        
        # Set response headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json' if not path.endswith('/docs') else 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Route responses based on path
        if path == '/api/':
            # Clean functional status message as requested
            response = {
                "message": "Agent Forge API is fully functional! 🚀",
                "status": "operational", 
                "version": "1.0.0",
                "api_ready": True
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif '/api/docs' in path:
            # API documentation page
            html_docs = """
<!DOCTYPE html>
<html>
<head>
    <title>Agent Forge API Documentation</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 40px; background: #f8f9fa; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 20px; margin-bottom: 30px; }
        .endpoint { background: #ecf0f1; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #3498db; }
        .method { color: #27ae60; font-weight: bold; }
        .path { color: #e74c3c; font-weight: bold; }
        .description { color: #555; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Agent Forge API Documentation</h1>
            <p>AI-powered workflow automation platform API</p>
        </div>
        
        <div class="endpoint">
            <div><span class="method">GET</span> <span class="path">/api/</span></div>
            <div class="description">Simple API status - confirms API is functional</div>
        </div>
        
        <div class="endpoint">
            <div><span class="method">GET</span> <span class="path">/api/health</span></div>
            <div class="description">Health check endpoint for monitoring</div>
        </div>
        
        <div class="endpoint">
            <div><span class="method">GET</span> <span class="path">/api/templates</span></div>
            <div class="description">Get available workflow templates (Trading Bot, Lead Generation, AI Research)</div>
        </div>
        
        <div class="endpoint">
            <div><span class="method">GET</span> <span class="path">/api/docs</span></div>
            <div class="description">This API documentation page</div>
        </div>
        
        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
            <strong>Status:</strong> ✅ Operational<br>
            <strong>Version:</strong> 1.0.0<br>
            <strong>Deployment:</strong> Vercel Serverless
        </div>
    </div>
</body>
</html>"""
            self.wfile.write(html_docs.encode())
            
        elif '/api/health' in path:
            # Health check with monitoring info
            response = {
                "status": "healthy",
                "service": "Agent Forge API",
                "deployment": "vercel-python-handler", 
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "message": "All systems operational",
                "uptime": "continuous"
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif '/api/templates' in path:
            # Professional templates
            response = {
                "templates": {
                    "trading_bot": {
                        "name": "trading_bot",
                        "display_name": "Crypto Trading Bot", 
                        "description": "Automated trading with stop-loss and take-profit",
                        "category": "Web3 Trading",
                        "tags": ["trading", "crypto", "finance"],
                        "complexity": "Complex",
                        "customizable_fields": ["trading_pair", "stop_loss", "take_profit"]
                    },
                    "lead_generation": {
                        "name": "lead_generation", 
                        "display_name": "Lead Generation System",
                        "description": "Capture and qualify leads from multiple sources", 
                        "category": "Sales & Marketing",
                        "tags": ["sales", "marketing", "crm"],
                        "complexity": "Medium",
                        "customizable_fields": ["source", "crm_integration"]
                    },
                    "ai_research": {
                        "name": "ai_research",
                        "display_name": "AI Research Assistant",
                        "description": "Multi-agent research collaboration system",
                        "category": "AI Automation", 
                        "tags": ["research", "ai", "analysis"],
                        "complexity": "Complex",
                        "customizable_fields": ["research_topic", "depth_level"]
                    }
                },
                "total_count": 3,
                "categories": ["Web3 Trading", "Sales & Marketing", "AI Automation"],
                "message": "Professional workflow templates available",
                "api_version": "1.0.0"
            }
            self.wfile.write(json.dumps(response).encode())
            
        else:
            # Default response for other paths
            response = {
                "name": "Agent Forge API", 
                "message": "API is working! Visit /api/docs for documentation",
                "api_base": "/api/",
                "documentation": "/api/docs",
                "status": "ready"
            }
            self.wfile.write(json.dumps(response).encode())
            
    def do_POST(self):
        self.do_GET()  # Handle POST same as GET for now
