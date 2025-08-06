"""
Simple HTTP handler for Vercel (no FastAPI)
Testing basic serverless function functionality
"""
from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "message": "Simple handler working!",
            "path": self.path,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "success",
            "handler": "simple.py"
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_POST(self):
        self.do_GET()  # Handle POST same as GET for now 