"""
Demo Handler for Agent Forge - Working Implementation
Uses BaseHTTPRequestHandler pattern (proven to work in this Vercel setup)
"""
from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        
        # Set response headers
        self.send_response(200)
        self.send_header('Content-type', 'text/html' if path == '/demo' else 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if path == '/demo':
            # Serve demo UI HTML
            demo_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent Forge - Demo UI</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }
        .status {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .api-test {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        button {
            background-color: #3972F6;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
        button:hover { background-color: #2551CC; }
        #output {
            background-color: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 13px;
            white-space: pre-wrap;
            margin-top: 20px;
            min-height: 100px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Agent Forge - Demo Interface</h1>
            <p>Basic demo showing working API endpoints</p>
        </div>
        
        <div class="status">
            ✅ Demo UI is working! The API endpoints below use the working BaseHTTPRequestHandler pattern.
        </div>
        
        <div class="api-test">
            <h3>API Endpoint Tests</h3>
            <button onclick="testEndpoint('/api/')">Test API Status</button>
            <button onclick="testEndpoint('/api/health')">Test Health</button>
            <button onclick="testEndpoint('/api/templates')">Test Templates</button>
            <button onclick="generateState()">Generate Sample State</button>
        </div>
        
        <div id="output">Click a button above to test API endpoints...</div>
    </div>
    
    <script>
        async function testEndpoint(endpoint) {
            const output = document.getElementById('output');
            output.textContent = 'Loading...';
            
            try {
                const response = await fetch(endpoint);
                const data = await response.json();
                output.textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                output.textContent = 'Error: ' + error.message;
            }
        }
        
        function generateState() {
            const output = document.getElementById('output');
            const sampleState = {
                "success": true,
                "message": "Sample workflow state generated",
                "workflow_id": "demo-001",
                "generated_state": {
                    "blocks": {
                        "starter_1": {
                            "id": "starter_1",
                            "type": "starter",
                            "name": "Start Workflow",
                            "position": {"x": 100, "y": 100},
                            "enabled": true,
                            "subBlocks": {},
                            "outputs": {}
                        }
                    },
                    "edges": [],
                    "variables": {},
                    "metadata": {
                        "version": "1.0.0",
                        "createdAt": "''' + datetime.utcnow().isoformat() + '''Z",
                        "generatedBy": "demo-handler"
                    }
                },
                "timestamp": "''' + datetime.utcnow().isoformat() + '''Z"
            };
            output.textContent = JSON.stringify(sampleState, null, 2);
        }
    </script>
</body>
</html>
            '''
            self.wfile.write(demo_html.encode())
            
        else:
            # JSON response for other paths
            response = {
                "message": "Demo handler working!",
                "path": path,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "status": "success",
                "note": "Using BaseHTTPRequestHandler pattern"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_POST(self):
        # Handle POST requests (for future state generation)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "message": "Demo POST endpoint working",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "note": "Ready for state generation implementation"
        }
        self.wfile.write(json.dumps(response, indent=2).encode()) 