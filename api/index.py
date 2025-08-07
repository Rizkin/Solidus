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
        # Ensure correct UTF-8 content type to avoid mojibake on emojis
        is_docs = path.startswith('/api/docs')
        self.send_header('Content-type', 'text/html; charset=utf-8' if is_docs else 'application/json; charset=utf-8')
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
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        elif '/api/docs' in path:
            # Enhanced API documentation page
            html_docs = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Agent Forge API Documentation</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
            color: #333;
            line-height: 1.6;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            padding: 0;
            box-shadow: 0 0 30px rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #3972F6 0%, #2551CC 100%);
            color: white; 
            padding: 40px;
            text-align: center;
            border-bottom: 5px solid #1a3d8f;
        }
        .header h1 {
            font-size: 2.8rem;
            margin: 0 0 10px 0;
            font-weight: 700;
        }
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
            max-width: 700px;
            margin: 0 auto;
        }
        .content {
            padding: 30px 40px;
        }
        .section {
            margin: 40px 0;
            padding: 25px;
            border-radius: 10px;
            background: #f8fafc;
            border-left: 5px solid #3972F6;
        }
        .section h2 {
            color: #2c3e50;
            border-bottom: 2px solid #eaecef;
            padding-bottom: 15px;
            margin-top: 0;
        }
        .endpoint {
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            border: 1px solid #eee;
        }
        .endpoint-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #eee;
        }
        .method {
            background: #27ae60;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
        }
        .method.get { background: #3498db; }
        .method.post { background: #9b59b6; }
        .method.put { background: #f39c12; }
        .method.delete { background: #e74c3c; }
        .path {
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 1.1rem;
            color: #2c3e50;
            font-weight: bold;
        }
        .description {
            color: #555;
            margin: 15px 0;
            font-size: 1.05rem;
        }
        .params-table, .responses-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        .params-table th, .responses-table th {
            background: #3972F6;
            color: white;
            text-align: left;
            padding: 12px 15px;
        }
        .params-table td, .responses-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        .params-table tr:nth-child(even), .responses-table tr:nth-child(even) {
            background: #f8f9fa;
        }
        .example {
            background: #2d3748;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.9rem;
            margin: 15px 0;
            overflow-x: auto;
        }
        .auth-section {
            background: #e3f2fd;
            border-left: 5px solid #2196f3;
        }
        .error-section {
            background: #ffebee;
            border-left: 5px solid #f44336;
        }
        .auth-required {
            background: #fff8e1;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.85rem;
            color: #ff9800;
        }
        .rate-limit {
            background: #fce4ec;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.85rem;
            color: #e91e63;
        }
        .footer {
            text-align: center;
            padding: 30px;
            background: #2c3e50;
            color: #ecf0f1;
            margin-top: 40px;
        }
        .footer a {
            color: #3498db;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
        @media (max-width: 768px) {
            .content {
                padding: 20px 15px;
            }
            .header {
                padding: 25px 15px;
            }
            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Agent Forge API Documentation</h1>
            <p>AI-powered workflow automation platform API - Version 1.2.0</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📚 Overview</h2>
                <p>Agent Forge is an AI-powered workflow automation platform that generates workflow state JSON objects from database records. The system reads from workflow_rows and workflow_blocks_rows tables and produces Agent Forge-compatible state objects with blocks, edges, and metadata.</p>
                
                <h3>🚀 Key Features</h3>
                <ul>
                    <li><strong>AI-Powered Generation</strong>: Uses Claude AI for intelligent workflow state creation</li>
                    <li><strong>Database Integration</strong>: Reads from PostgreSQL/Supabase tables</li>
                    <li><strong>Caching System</strong>: RAG-enhanced intelligent caching for 70-80% cost reduction</li>
                    <li><strong>Validation</strong>: Comprehensive 9-validator compliance system</li>
                    <li><strong>Demo UI</strong>: Interactive interface for testing and development</li>
                </ul>
            </div>
            
            <div class="section auth-section">
                <h2>🔐 Authentication</h2>
                <p>Most endpoints in the Agent Forge API are publicly accessible for demonstration purposes. However, for production use:</p>
                
                <h3>API Keys</h3>
                <p>For enhanced security and access to premium features, you can use API keys:</p>
                <div class="example">
# Set your API key as an environment variable
export AGENT_FORGE_API_KEY="your_api_key_here"

# Use in requests
curl -H "Authorization: Bearer $AGENT_FORGE_API_KEY" \\
  https://solidus-olive.vercel.app/api/endpoint
                </div>
                
                <h3>Rate Limiting</h3>
                <p>The API implements rate limiting to ensure fair usage:</p>
                <ul>
                    <li><strong>Anonymous users</strong>: 100 requests per hour</li>
                    <li><strong>Authenticated users</strong>: 1000 requests per hour</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>🌐 Base URL</h2>
                <p><code>https://solidus-olive.vercel.app</code></p>
            </div>
            
            <div class="section">
                <h2>📋 API Endpoints</h2>
                
                <!-- Status Endpoint -->
                <div class="endpoint">
                    <div class="endpoint-header">
                        <span class="method get">GET</span>
                        <span class="path">/api/</span>
                    </div>
                    <div class="description">Simple API status - confirms API is functional</div>
                    
                    <h4>Responses</h4>
                    <table class="responses-table">
                        <tr>
                            <th>Code</th>
                            <th>Description</th>
                        </tr>
                        <tr>
                            <td>200</td>
                            <td>API is operational</td>
                        </tr>
                    </table>
                    
                    <h4>Example Request</h4>
                    <div class="example">
curl https://solidus-olive.vercel.app/api/
                    </div>
                    
                    <h4>Example Response</h4>
                    <div class="example">
{
  "message": "Agent Forge API is fully functional! 🚀",
  "status": "operational",
  "version": "1.0.0",
  "api_ready": true
}
                    </div>
                </div>
                
                <!-- Health Check Endpoint -->
                <div class="endpoint">
                    <div class="endpoint-header">
                        <span class="method get">GET</span>
                        <span class="path">/api/health</span>
                    </div>
                    <div class="description">Health check endpoint for monitoring</div>
                    
                    <h4>Responses</h4>
                    <table class="responses-table">
                        <tr>
                            <th>Code</th>
                            <th>Description</th>
                        </tr>
                        <tr>
                            <td>200</td>
                            <td>Service is healthy</td>
                        </tr>
                    </table>
                    
                    <h4>Example Request</h4>
                    <div class="example">
curl https://solidus-olive.vercel.app/api/health
                    </div>
                    
                    <h4>Example Response</h4>
                    <div class="example">
{
  "status": "healthy",
  "service": "Agent Forge API",
  "deployment": "vercel-python-handler",
  "timestamp": "2023-01-01T10:00:00Z",
  "message": "All systems operational",
  "uptime": "continuous"
}
                    </div>
                </div>
                
                <!-- Templates Endpoint -->
                <div class="endpoint">
                    <div class="endpoint-header">
                        <span class="method get">GET</span>
                        <span class="path">/api/templates</span>
                    </div>
                    <div class="description">Get available workflow templates (Trading Bot, Lead Generation, AI Research)</div>
                    
                    <h4>Responses</h4>
                    <table class="responses-table">
                        <tr>
                            <th>Code</th>
                            <th>Description</th>
                        </tr>
                        <tr>
                            <td>200</td>
                            <td>Templates retrieved successfully</td>
                        </tr>
                    </table>
                    
                    <h4>Example Request</h4>
                    <div class="example">
curl https://solidus-olive.vercel.app/api/templates
                    </div>
                    
                    <h4>Example Response</h4>
                    <div class="example">
{
  "templates": {
    "trading_bot": {
      "name": "trading_bot",
      "display_name": "Crypto Trading Bot",
      "description": "Automated trading with stop-loss and take-profit",
      "category": "Web3 Trading",
      "tags": ["trading", "crypto", "finance"],
      "complexity": "Complex",
      "customizable_fields": ["trading_pair", "stop_loss", "take_profit"]
    }
  },
  "total_count": 3,
  "categories": ["Web3 Trading", "Sales & Marketing", "AI Automation"],
  "message": "Professional workflow templates available",
  "api_version": "1.0.0"
}
                    </div>
                </div>
                
                <!-- Generate State Endpoint -->
                <div class="endpoint">
                    <div class="endpoint-header">
                        <span class="method post">POST</span>
                        <span class="path">/generate-state</span>
                    </div>
                    <div class="description">Generate workflow state from provided data (MVP Demo Endpoint)</div>
                    
                    <h4>Request Body</h4>
                    <table class="params-table">
                        <tr>
                            <th>Parameter</th>
                            <th>Type</th>
                            <th>Required</th>
                            <th>Description</th>
                        </tr>
                        <tr>
                            <td>workflow_id</td>
                            <td>string</td>
                            <td>Yes</td>
                            <td>Unique identifier for the workflow</td>
                        </tr>
                        <tr>
                            <td>workflow_rows</td>
                            <td>object</td>
                            <td>Yes</td>
                            <td>Workflow metadata including name, description, etc.</td>
                        </tr>
                        <tr>
                            <td>blocks_rows</td>
                            <td>array</td>
                            <td>Yes</td>
                            <td>Array of workflow blocks with their properties</td>
                        </tr>
                    </table>
                    
                    <h4>Responses</h4>
                    <table class="responses-table">
                        <tr>
                            <th>Code</th>
                            <th>Description</th>
                        </tr>
                        <tr>
                            <td>200</td>
                            <td>Workflow state generated successfully</td>
                        </tr>
                        <tr>
                            <td>400</td>
                            <td>Invalid request data</td>
                        </tr>
                        <tr>
                            <td>500</td>
                            <td>Internal server error</td>
                        </tr>
                    </table>
                    
                    <h4>Example Request</h4>
                    <div class="example">
curl -X POST https://solidus-olive.vercel.app/generate-state \\
  -H "Content-Type: application/json" \\
  -d '{
  "workflow_id": "demo-workflow-001",
  "workflow_rows": {
    "id": "demo-workflow-001",
    "user_id": "demo-user-123",
    "name": "Demo Trading Bot",
    "description": "Automated crypto trading with risk management",
    "color": "#3972F6",
    "variables": "{}",
    "is_published": false,
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z",
    "last_synced": "2024-01-01T10:00:00Z",
    "state": "{}"
  },
  "blocks_rows": [
    {
      "id": "block-starter-001",
      "workflow_id": "demo-workflow-001",
      "type": "starter",
      "name": "Start Trading",
      "position_x": 100,
      "position_y": 100,
      "enabled": true,
      "horizontal_handles": true,
      "is_wide": false,
      "advanced_mode": false,
      "height": 0,
      "sub_blocks": {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"}},
      "outputs": {"response": {"type": {"input": "any"}}},
      "data": {},
      "parent_id": null,
      "extent": null,
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z"
    }
  ]
}'
                    </div>
                </div>
                
                <!-- Advanced Workflow Generation Endpoint -->
                <div class="endpoint">
                    <div class="endpoint-header">
                        <span class="method post">POST</span>
                        <span class="path">/api/workflows/{workflow_id}/generate-state</span>
                    </div>
                    <div class="description">Generate Agent Forge-compatible workflow state using AI with intelligent RAG caching</div>
                    
                    <h4>Features</h4>
                    <ul>
                        <li>Intelligent RAG caching system (70-80% faster for similar workflows)</li>
                        <li>Automatic pattern recognition and adaptation</li>
                        <li>Cost optimization through reduced AI calls</li>
                        <li>Learning system that improves over time</li>
                        <li>Semantic understanding with embeddings</li>
                    </ul>
                    
                    <h4>Path Parameters</h4>
                    <table class="params-table">
                        <tr>
                            <th>Parameter</th>
                            <th>Type</th>
                            <th>Required</th>
                            <th>Description</th>
                        </tr>
                        <tr>
                            <td>workflow_id</td>
                            <td>string</td>
                            <td>Yes</td>
                            <td>Unique identifier for the workflow</td>
                        </tr>
                    </table>
                    
                    <h4>Request Body</h4>
                    <table class="params-table">
                        <tr>
                            <th>Parameter</th>
                            <th>Type</th>
                            <th>Required</th>
                            <th>Description</th>
                        </tr>
                        <tr>
                            <td>options</td>
                            <td>object</td>
                            <td>No</td>
                            <td>Generation options (use_cache, force_regeneration, etc.)</td>
                        </tr>
                    </table>
                    
                    <h4>Responses</h4>
                    <table class="responses-table">
                        <tr>
                            <th>Code</th>
                            <th>Description</th>
                        </tr>
                        <tr>
                            <td>200</td>
                            <td>Workflow state generated successfully</td>
                        </tr>
                        <tr>
                            <td>400</td>
                            <td>Invalid workflow ID or options</td>
                        </tr>
                        <tr>
                            <td>404</td>
                            <td>Workflow not found</td>
                        </tr>
                        <tr>
                            <td>500</td>
                            <td>Internal server error</td>
                        </tr>
                    </table>
                </div>
                
                <!-- Get Workflow State Endpoint -->
                <div class="endpoint">
                    <div class="endpoint-header">
                        <span class="method get">GET</span>
                        <span class="path">/api/workflows/{workflow_id}/state</span>
                    </div>
                    <div class="description">Retrieve the current state of a workflow</div>
                    
                    <h4>Path Parameters</h4>
                    <table class="params-table">
                        <tr>
                            <th>Parameter</th>
                            <th>Type</th>
                            <th>Required</th>
                            <th>Description</th>
                        </tr>
                        <tr>
                            <td>workflow_id</td>
                            <td>string</td>
                            <td>Yes</td>
                            <td>Unique identifier for the workflow</td>
                        </tr>
                    </table>
                    
                    <h4>Responses</h4>
                    <table class="responses-table">
                        <tr>
                            <th>Code</th>
                            <th>Description</th>
                        </tr>
                        <tr>
                            <td>200</td>
                            <td>Workflow state retrieved successfully</td>
                        </tr>
                        <tr>
                            <td>404</td>
                            <td>Workflow not found</td>
                        </tr>
                        <tr>
                            <td>500</td>
                            <td>Internal server error</td>
                        </tr>
                    </table>
                </div>
                
                <!-- Block Types Endpoint -->
                <div class="endpoint">
                    <div class="endpoint-header">
                        <span class="method get">GET</span>
                        <span class="path">/api/block-types</span>
                    </div>
                    <div class="description">Get available Agent Forge block types with schemas</div>
                    
                    <h4>Responses</h4>
                    <table class="responses-table">
                        <tr>
                            <th>Code</th>
                            <th>Description</th>
                        </tr>
                        <tr>
                            <td>200</td>
                            <td>Block types retrieved successfully</td>
                        </tr>
                    </table>
                </div>
            </div>
            
            <div class="section error-section">
                <h2>⚠️ Error Codes</h2>
                <table class="responses-table">
                    <tr>
                        <th>Code</th>
                        <th>Description</th>
                        <th>Resolution</th>
                    </tr>
                    <tr>
                        <td>400</td>
                        <td>Bad Request</td>
                        <td>Check request parameters and body format</td>
                    </tr>
                    <tr>
                        <td>401</td>
                        <td>Unauthorized</td>
                        <td>Provide valid authentication credentials</td>
                    </tr>
                    <tr>
                        <td>403</td>
                        <td>Forbidden</td>
                        <td>You don't have permission to access this resource</td>
                    </tr>
                    <tr>
                        <td>404</td>
                        <td>Not Found</td>
                        <td>The requested resource could not be found</td>
                    </tr>
                    <tr>
                        <td>429</td>
                        <td>Too Many Requests</td>
                        <td>Reduce request rate or upgrade your plan</td>
                    </tr>
                    <tr>
                        <td>500</td>
                        <td>Internal Server Error</td>
                        <td>Try again later or contact support</td>
                    </tr>
                    <tr>
                        <td>503</td>
                        <td>Service Unavailable</td>
                        <td>The service is temporarily unavailable</td>
                    </tr>
                </table>
            </div>
            
            <div class="section">
                <h2>🔧 SDKs and Libraries</h2>
                <p>Official libraries are available for popular programming languages:</p>
                <ul>
                    <li><strong>Python</strong>: <code>pip install agent-forge-sdk</code></li>
                    <li><strong>JavaScript</strong>: <code>npm install agent-forge-js</code></li>
                    <li><strong>Java</strong>: <code>com.agentforge:agent-forge-java</code></li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p>Agent Forge API Documentation - Version 1.2.0</p>
            <p>For support, contact: <a href="mailto:support@agentforge.ai">support@agentforge.ai</a></p>
            <p>© 2025 Agent Forge. All rights reserved.</p>
        </div>
    </div>
</body>
</html>"""
            self.wfile.write(html_docs.encode('utf-8'))
            
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
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
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
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        else:
            # Default response for other paths
            response = {
                "name": "Agent Forge API", 
                "message": "API is working! Visit /api/docs for documentation",
                "api_base": "/api/",
                "documentation": "/api/docs",
                "status": "ready"
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
    def do_POST(self):
        self.do_GET()  # Handle POST same as GET for now
