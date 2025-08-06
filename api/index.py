"""
Ultra-simple Vercel Python function for testing runtime
No FastAPI - pure Python HTTP handler
"""
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        
        # Set response headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Route responses based on path
        if '/api/health' in path:
            response = {
                "status": "healthy",
                "message": "Basic Python handler working!",
                "deployment": "vercel-basic-handler",
                "path": path
            }
        elif '/api/templates' in path:
            response = {
                "templates": {
                    "test": {
                        "name": "test",
                        "display_name": "Test Template", 
                        "description": "Basic test template",
                        "category": "Test"
                    }
                },
                "message": "Basic templates working",
                "handler": "pure-python"
            }
        else:
            response = {
                "name": "Agent Forge API",
                "status": "basic-handler-working",
                "message": "Ultra-simple Python function successful!",
                "path": path
            }
        
        # Send JSON response
        self.wfile.write(json.dumps(response).encode())
        
    def do_POST(self):
        self.do_GET()  # Handle POST same as GET for now
