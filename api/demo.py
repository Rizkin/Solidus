"""
Demo Handler for Agent Forge - Full Interactive UI
Complete demo interface with workflow data input forms
"""
from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        
        # Set response headers
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Serve complete demo UI HTML
        demo_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Agent Forge - Demo UI</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'SF Pro Text', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #3972F6 0%, #2551CC 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
            margin: 5px 0;
        }
        .form-container {
            padding: 40px;
        }
        .section {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 30px;
            transition: all 0.3s ease;
        }
        .section:hover {
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .section h3 {
            color: #2d3748;
            margin-bottom: 20px;
            font-size: 1.4em;
            display: flex;
            align-items: center;
        }
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        .form-group {
            display: flex;
            flex-direction: column;
        }
        .form-group label {
            margin-bottom: 8px;
            font-weight: 600;
            color: #4a5568;
            font-size: 0.9em;
        }
        .form-group input,
        .form-group select,
        .form-group textarea {
            padding: 12px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.3s ease;
            font-family: inherit;
        }
        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #3972F6;
            box-shadow: 0 0 0 3px rgba(57, 114, 246, 0.1);
        }
        .form-group textarea {
            resize: vertical;
            min-height: 80px;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 12px;
        }
        .block-item {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            position: relative;
        }
        .block-item h4 {
            color: #2d3748;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .remove-block {
            background: #e53e3e;
            color: white;
            border: none;
            padding: 5px 12px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
        }
        .remove-block:hover {
            background: #c53030;
        }
        .add-block {
            background: #38a169;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
        }
        .add-block:hover {
            background: #2f855a;
            transform: translateY(-1px);
        }
        .button-group {
            display: flex;
            gap: 15px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        .button-group button {
            padding: 15px 25px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            flex: 1;
            min-width: 200px;
        }
        .generate-btn {
            background: linear-gradient(135deg, #3972F6 0%, #2551CC 100%);
            color: white;
        }
        .generate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(57, 114, 246, 0.3);
        }
        .clear-btn {
            background: #718096;
            color: white;
        }
        .clear-btn:hover {
            background: #4a5568;
        }
        .example-btn {
            background: #38a169;
            color: white;
        }
        .example-btn:hover {
            background: #2f855a;
        }
        .result {
            background: #f7fafc;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            padding: 25px;
            margin-top: 30px;
        }
        .result h3 {
            color: #2d3748;
            margin-bottom: 15px;
        }
        .json-output {
            background: #2d3748;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 13px;
            white-space: pre-wrap;
            max-height: 500px;
            overflow-y: auto;
            border: 1px solid #4a5568;
        }
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #3972F6;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .status-success {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .status-error {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        @media (max-width: 768px) {
            .form-row {
                grid-template-columns: 1fr;
            }
            .button-group {
                flex-direction: column;
            }
            .button-group button {
                min-width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Agent Forge - Demo UI</h1>
            <p>MVP Demo Interface for Technical Interview</p>
            <p><strong>Input sample workflow data and generate state/blocks JSON</strong></p>
        </div>

        <div class="form-container">
            <form id="demoForm">
                <!-- Workflow Rows Section -->
                <div class="section">
                    <h3>📋 Workflow Rows Data</h3>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="workflow_id">Workflow ID*</label>
                            <input type="text" id="workflow_id" name="workflow_id" value="demo-workflow-001" required>
                        </div>
                        <div class="form-group">
                            <label for="user_id">User ID*</label>
                            <input type="text" id="user_id" name="user_id" value="demo-user-123" required>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="workflow_name">Workflow Name*</label>
                            <input type="text" id="workflow_name" name="workflow_name" value="Demo Trading Bot" required>
                        </div>
                        <div class="form-group">
                            <label for="workspace_id">Workspace ID</label>
                            <input type="text" id="workspace_id" name="workspace_id" value="demo-workspace-456">
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="description">Description</label>
                        <textarea id="description" name="description" placeholder="Automated crypto trading with risk management">Automated crypto trading with risk management</textarea>
                    </div>
                </div>

                <!-- Workflow Blocks Rows Section -->
                <div class="section">
                    <h3>🧩 Workflow Blocks Rows Data</h3>
                    <div class="blocks-container" id="blocksContainer">
                        <!-- Initial starter block -->
                        <div class="block-item">
                            <h4>Block 1 <button type="button" class="remove-block" onclick="removeBlock(this)">Remove</button></h4>
                            <div class="form-row">
                                <div class="form-group">
                                    <label>Block ID*</label>
                                    <input type="text" name="block_id" value="block-starter-001" required>
                                </div>
                                <div class="form-group">
                                    <label>Block Type*</label>
                                    <select name="block_type" required>
                                        <option value="starter" selected>starter</option>
                                        <option value="agent">agent</option>
                                        <option value="api">api</option>
                                        <option value="webhook">webhook</option>
                                        <option value="action">action</option>
                                    </select>
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group">
                                    <label>Block Name*</label>
                                    <input type="text" name="block_name" value="Start Trading" required>
                                </div>
                                <div class="form-group">
                                    <label>Enabled</label>
                                    <select name="enabled">
                                        <option value="true" selected>true</option>
                                        <option value="false">false</option>
                                    </select>
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group">
                                    <label>Position X*</label>
                                    <input type="number" name="position_x" value="100" required>
                                </div>
                                <div class="form-group">
                                    <label>Position Y*</label>
                                    <input type="number" name="position_y" value="100" required>
                                </div>
                            </div>
                            <div class="form-group">
                                <label>Sub Blocks (JSON)</label>
                                <textarea name="sub_blocks" placeholder='{"key": "value"}'>{}</textarea>
                            </div>
                            <div class="form-group">
                                <label>Outputs (JSON)</label>
                                <textarea name="outputs" placeholder='{"key": "value"}'>{}</textarea>
                            </div>
                        </div>
                    </div>
                    <button type="button" class="add-block" onclick="addBlock()">+ Add Another Block</button>
                </div>

                <div class="button-group">
                    <button type="button" class="generate-btn" onclick="generateState()">🚀 Generate Workflow State</button>
                    <button type="button" class="clear-btn" onclick="clearForm()">🗑️ Clear Form</button>
                    <button type="button" class="example-btn" onclick="loadExample()">📝 Load Example Data</button>
                </div>
            </form>

            <div id="result" class="result" style="display: none;">
                <h3>📊 Generated Workflow State & Blocks</h3>
                <div id="output" class="json-output"></div>
            </div>
        </div>
    </div>

    <script>
        let blockCounter = 1;

        // Generate workflow state
        async function generateState() {
            const resultDiv = document.getElementById('result');
            const outputDiv = document.getElementById('output');
            
            resultDiv.style.display = 'block';
            outputDiv.innerHTML = '<div class="loading"></div>Generating workflow state...';
            
            try {
                // Collect form data
                const workflowData = {
                    workflow_id: document.getElementById('workflow_id').value,
                    user_id: document.getElementById('user_id').value,
                    name: document.getElementById('workflow_name').value,
                    workspace_id: document.getElementById('workspace_id').value,
                    description: document.getElementById('description').value
                };
                
                // Collect blocks data
                const blocks = [];
                const blockItems = document.querySelectorAll('.block-item');
                
                blockItems.forEach((item, index) => {
                    const blockData = {
                        id: item.querySelector('[name="block_id"]').value,
                        workflow_id: workflowData.workflow_id,
                        type: item.querySelector('[name="block_type"]').value,
                        name: item.querySelector('[name="block_name"]').value,
                        enabled: item.querySelector('[name="enabled"]').value === 'true',
                        position_x: parseInt(item.querySelector('[name="position_x"]').value),
                        position_y: parseInt(item.querySelector('[name="position_y"]').value),
                        sub_blocks: item.querySelector('[name="sub_blocks"]').value || '{}',
                        outputs: item.querySelector('[name="outputs"]').value || '{}'
                    };
                    blocks.push(blockData);
                });
                
                // Create the request payload
                const requestData = {
                    workflow_rows: workflowData,
                    workflow_blocks_rows: blocks
                };
                
                // Generate sample state (since we can't call the full API)
                const generatedState = {
                    success: true,
                    message: "Workflow state generated successfully",
                    workflow_id: workflowData.workflow_id,
                    generated_state: {
                        blocks: {},
                        edges: [],
                        variables: {},
                        metadata: {
                            version: "1.0.0",
                            createdAt: new Date().toISOString(),
                            generatedBy: "demo-handler",
                            totalBlocks: blocks.length
                        }
                    },
                    input_data: requestData,
                    timestamp: new Date().toISOString()
                };
                
                // Convert blocks to state format
                blocks.forEach(block => {
                    generatedState.generated_state.blocks[block.id] = {
                        id: block.id,
                        type: block.type,
                        name: block.name,
                        position: { x: block.position_x, y: block.position_y },
                        enabled: block.enabled,
                        subBlocks: JSON.parse(block.sub_blocks || '{}'),
                        outputs: JSON.parse(block.outputs || '{}')
                    };
                });
                
                outputDiv.innerHTML = JSON.stringify(generatedState, null, 2);
                
                // Show success status
                const statusDiv = document.createElement('div');
                statusDiv.className = 'status-success';
                statusDiv.innerHTML = '✅ Workflow state generated successfully! Data shown below.';
                resultDiv.insertBefore(statusDiv, outputDiv);
                
                setTimeout(() => {
                    statusDiv.remove();
                }, 5000);
                
            } catch (error) {
                outputDiv.innerHTML = 'Error generating state: ' + error.message;
                
                // Show error status
                const statusDiv = document.createElement('div');
                statusDiv.className = 'status-error';
                statusDiv.innerHTML = '❌ Error: ' + error.message;
                resultDiv.insertBefore(statusDiv, outputDiv);
                
                setTimeout(() => {
                    statusDiv.remove();
                }, 5000);
            }
        }

        // Add new block
        function addBlock() {
            blockCounter++;
            const blocksContainer = document.getElementById('blocksContainer');
            
            const blockHtml = `
                <div class="block-item">
                    <h4>Block ${blockCounter} <button type="button" class="remove-block" onclick="removeBlock(this)">Remove</button></h4>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Block ID*</label>
                            <input type="text" name="block_id" value="block-${blockCounter}-001" required>
                        </div>
                        <div class="form-group">
                            <label>Block Type*</label>
                            <select name="block_type" required>
                                <option value="starter">starter</option>
                                <option value="agent">agent</option>
                                <option value="api" selected>api</option>
                                <option value="webhook">webhook</option>
                                <option value="action">action</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Block Name*</label>
                            <input type="text" name="block_name" value="New Block ${blockCounter}" required>
                        </div>
                        <div class="form-group">
                            <label>Enabled</label>
                            <select name="enabled">
                                <option value="true" selected>true</option>
                                <option value="false">false</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Position X*</label>
                            <input type="number" name="position_x" value="${100 + (blockCounter * 200)}" required>
                        </div>
                        <div class="form-group">
                            <label>Position Y*</label>
                            <input type="number" name="position_y" value="100" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Sub Blocks (JSON)</label>
                        <textarea name="sub_blocks" placeholder='{"key": "value"}'>{}</textarea>
                    </div>
                    <div class="form-group">
                        <label>Outputs (JSON)</label>
                        <textarea name="outputs" placeholder='{"key": "value"}'>{}</textarea>
                    </div>
                </div>
            `;
            
            blocksContainer.insertAdjacentHTML('beforeend', blockHtml);
        }

        // Remove block
        function removeBlock(button) {
            const blockItem = button.closest('.block-item');
            const blocksContainer = document.getElementById('blocksContainer');
            
            // Don't remove if it's the last block
            if (blocksContainer.children.length > 1) {
                blockItem.remove();
                
                // Renumber remaining blocks
                const remainingBlocks = blocksContainer.querySelectorAll('.block-item');
                remainingBlocks.forEach((block, index) => {
                    const header = block.querySelector('h4');
                    const blockId = block.querySelector('[name="block_id"]');
                    header.innerHTML = `Block ${index + 1} <button type="button" class="remove-block" onclick="removeBlock(this)">Remove</button>`;
                    
                    if (blockId.value.includes('block-') && blockId.value.includes('-001')) {
                        blockId.value = `block-${index + 1}-001`;
                    }
                });
                blockCounter = remainingBlocks.length;
            } else {
                alert('Cannot remove the last block. At least one block is required.');
            }
        }

        // Clear form
        function clearForm() {
            if (confirm('Are you sure you want to clear all form data?')) {
                // Reset workflow data
                document.getElementById('workflow_id').value = '';
                document.getElementById('user_id').value = '';
                document.getElementById('workflow_name').value = '';
                document.getElementById('workspace_id').value = '';
                document.getElementById('description').value = '';
                
                // Reset blocks
                const blocksContainer = document.getElementById('blocksContainer');
                blocksContainer.innerHTML = '';
                blockCounter = 0;
                addBlock(); // Add one default block
                
                // Hide results
                document.getElementById('result').style.display = 'none';
            }
        }

        // Load example data
        function loadExample() {
            // Set workflow data
            document.getElementById('workflow_id').value = 'demo-trading-bot-001';
            document.getElementById('user_id').value = 'demo-user-123';
            document.getElementById('workflow_name').value = 'Demo Trading Bot';
            document.getElementById('workspace_id').value = 'demo-workspace-456';
            document.getElementById('description').value = 'Automated crypto trading bot with AI decision making and risk management';
            
            // Clear existing blocks and add example blocks
            const blocksContainer = document.getElementById('blocksContainer');
            blocksContainer.innerHTML = '';
            blockCounter = 0;
            
            // Add starter block
            const starterBlockHtml = `
                <div class="block-item">
                    <h4>Block 1 - Starter <button type="button" class="remove-block" onclick="removeBlock(this)">Remove</button></h4>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Block ID*</label>
                            <input type="text" name="block_id" value="block-starter-001" required>
                        </div>
                        <div class="form-group">
                            <label>Block Type*</label>
                            <select name="block_type" required>
                                <option value="starter" selected>starter</option>
                                <option value="agent">agent</option>
                                <option value="api">api</option>
                                <option value="webhook">webhook</option>
                                <option value="action">action</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Block Name*</label>
                            <input type="text" name="block_name" value="Start Trading Bot" required>
                        </div>
                        <div class="form-group">
                            <label>Enabled</label>
                            <select name="enabled">
                                <option value="true" selected>true</option>
                                <option value="false">false</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Position X*</label>
                            <input type="number" name="position_x" value="100" required>
                        </div>
                        <div class="form-group">
                            <label>Position Y*</label>
                            <input type="number" name="position_y" value="100" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Sub Blocks (JSON)</label>
                        <textarea name="sub_blocks">{"startWorkflow":{"id":"startWorkflow","type":"dropdown","value":"manual"},"scheduleType":{"id":"scheduleType","type":"dropdown","value":"daily"}}</textarea>
                    </div>
                    <div class="form-group">
                        <label>Outputs (JSON)</label>
                        <textarea name="outputs">{"response":{"type":{"input":"any"}}}</textarea>
                    </div>
                </div>
            `;
            
            // Add API block
            const apiBlockHtml = `
                <div class="block-item">
                    <h4>Block 2 - API <button type="button" class="remove-block" onclick="removeBlock(this)">Remove</button></h4>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Block ID*</label>
                            <input type="text" name="block_id" value="block-api-001" required>
                        </div>
                        <div class="form-group">
                            <label>Block Type*</label>
                            <select name="block_type" required>
                                <option value="starter">starter</option>
                                <option value="agent">agent</option>
                                <option value="api" selected>api</option>
                                <option value="webhook">webhook</option>
                                <option value="action">action</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Block Name*</label>
                            <input type="text" name="block_name" value="Fetch Market Data" required>
                        </div>
                        <div class="form-group">
                            <label>Enabled</label>
                            <select name="enabled">
                                <option value="true" selected>true</option>
                                <option value="false">false</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Position X*</label>
                            <input type="number" name="position_x" value="300" required>
                        </div>
                        <div class="form-group">
                            <label>Position Y*</label>
                            <input type="number" name="position_y" value="100" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Sub Blocks (JSON)</label>
                        <textarea name="sub_blocks">{"url":{"id":"url","type":"short-input","value":"https://api.coingecko.com/api/v3/coins/bitcoin"},"method":{"id":"method","type":"dropdown","value":"GET"}}</textarea>
                    </div>
                    <div class="form-group">
                        <label>Outputs (JSON)</label>
                        <textarea name="outputs">{"data":"any","status":"number","headers":"json"}</textarea>
                    </div>
                </div>
            `;

            // Add Agent block  
            const agentBlockHtml = `
                <div class="block-item">
                    <h4>Block 3 - Agent <button type="button" class="remove-block" onclick="removeBlock(this)">Remove</button></h4>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Block ID*</label>
                            <input type="text" name="block_id" value="block-agent-001" required>
                        </div>
                        <div class="form-group">
                            <label>Block Type*</label>
                            <select name="block_type" required>
                                <option value="starter">starter</option>
                                <option value="agent" selected>agent</option>
                                <option value="api">api</option>
                                <option value="webhook">webhook</option>
                                <option value="action">action</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Block Name*</label>
                            <input type="text" name="block_name" value="AI Trading Decision" required>
                        </div>
                        <div class="form-group">
                            <label>Enabled</label>
                            <select name="enabled">
                                <option value="true" selected>true</option>
                                <option value="false">false</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Position X*</label>
                            <input type="number" name="position_x" value="500" required>
                        </div>
                        <div class="form-group">
                            <label>Position Y*</label>
                            <input type="number" name="position_y" value="100" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Sub Blocks (JSON)</label>
                        <textarea name="sub_blocks">{"prompt":{"id":"prompt","type":"long-input","value":"Analyze the market data and decide whether to buy, sell, or hold"},"model":{"id":"model","type":"dropdown","value":"gpt-4"}}</textarea>
                    </div>
                    <div class="form-group">
                        <label>Outputs (JSON)</label>
                        <textarea name="outputs">{"decision":"string","confidence":"number","reasoning":"string"}</textarea>
                    </div>
                </div>
            `;
            
            blocksContainer.innerHTML = starterBlockHtml + apiBlockHtml + agentBlockHtml;
            blockCounter = 3;
            
            // Hide results
            document.getElementById('result').style.display = 'none';
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🚀 Agent Forge Demo UI Loaded');
        });
    </script>
</body>
</html>
        '''
        
        self.wfile.write(demo_html.encode('utf-8'))

    def do_POST(self):
        # Handle POST requests for state generation
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # For now, return a sample response
        response = {
            "success": True,
            "message": "Demo POST endpoint working",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8')) 