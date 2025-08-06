// Agent Forge Demo UI - JavaScript
// MVP Demo Interface for Technical Interview

let blockCounter = 1;

// API Configuration
const API_BASE = window.location.origin; // Use current origin (works for both local and Vercel)

// Initialize the demo UI
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Agent Forge Demo UI Loaded');
    
    // Set up form submission
    const form = document.getElementById('demoForm');
    form.addEventListener('submit', handleFormSubmit);
    
    // Load example data by default for demo
    setTimeout(loadExample, 500);
});

// Handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const generateBtn = document.getElementById('generateBtn');
    const resultDiv = document.getElementById('result');
    const outputDiv = document.getElementById('output');
    
    // Show loading state
    generateBtn.disabled = true;
    generateBtn.textContent = '⏳ Generating...';
    
    resultDiv.style.display = 'block';
    outputDiv.innerHTML = '<div class="loading">🔄 Generating workflow state and blocks...</div>';
    
    try {
        // Collect form data
        const formData = collectFormData();
        console.log('📤 Sending data:', formData);
        
        // Call the API
        const response = await fetch(`${API_BASE}/generate-state`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status} - ${response.statusText}`);
        }
        
        const result = await response.json();
        console.log('📥 Received result:', result);
        
        // Display the result
        displayResult(result);
        
    } catch (error) {
        console.error('❌ Error:', error);
        displayError(error.message);
    } finally {
        // Reset button
        generateBtn.disabled = false;
        generateBtn.textContent = '🚀 Generate Workflow State';
    }
}

// Collect form data into the required format
function collectFormData() {
    const form = document.getElementById('demoForm');
    const formData = new FormData(form);
    
    // Collect workflow rows data
    const workflow_rows = {
        id: formData.get('workflow_id'),
        user_id: formData.get('user_id'),
        workspace_id: formData.get('workspace_id') || null,
        folder_id: null,
        name: formData.get('workflow_name'),
        description: formData.get('description') || null,
        color: '#3972F6',
        variables: '{}',
        is_published: false,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        last_synced: new Date().toISOString(),
        state: '{}'
    };
    
    // Collect blocks data
    const blocks_rows = [];
    const blockItems = document.querySelectorAll('.block-item');
    
    blockItems.forEach((blockItem) => {
        const blockId = blockItem.querySelector('input[name="block_id"]').value;
        const blockType = blockItem.querySelector('select[name="block_type"]').value;
        const blockName = blockItem.querySelector('input[name="block_name"]').value;
        const enabled = blockItem.querySelector('select[name="enabled"]').value === 'true';
        const positionX = parseFloat(blockItem.querySelector('input[name="position_x"]').value) || 0;
        const positionY = parseFloat(blockItem.querySelector('input[name="position_y"]').value) || 0;
        const subBlocks = blockItem.querySelector('textarea[name="sub_blocks"]').value || '{}';
        const outputs = blockItem.querySelector('textarea[name="outputs"]').value || '{}';
        
        // Validate JSON
        let subBlocksJson, outputsJson;
        try {
            subBlocksJson = JSON.parse(subBlocks);
            outputsJson = JSON.parse(outputs);
        } catch (e) {
            console.warn(`⚠️ Invalid JSON in block ${blockId}, using empty objects`);
            subBlocksJson = {};
            outputsJson = {};
        }
        
        blocks_rows.push({
            id: blockId,
            workflow_id: workflow_rows.id,
            type: blockType,
            name: blockName,
            position_x: positionX,
            position_y: positionY,
            enabled: enabled,
            horizontal_handles: true,
            is_wide: false,
            advanced_mode: false,
            height: 0,
            sub_blocks: subBlocksJson,
            outputs: outputsJson,
            data: {},
            parent_id: null,
            extent: null,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
        });
    });
    
    return {
        workflow_id: workflow_rows.id,
        workflow_rows: workflow_rows,
        blocks_rows: blocks_rows
    };
}

// Display successful result
function displayResult(result) {
    const outputDiv = document.getElementById('output');
    
    // Format the JSON output nicely
    const formattedJson = JSON.stringify(result, null, 2);
    
    outputDiv.innerHTML = `
        <div style="margin-bottom: 10px;">
            <strong>✅ Success!</strong> Generated workflow state with ${result.blocks ? Object.keys(result.blocks).length : 0} blocks
        </div>
        ${formattedJson}
    `;
    
    // Scroll to results
    outputDiv.scrollIntoView({ behavior: 'smooth' });
}

// Display error message
function displayError(errorMessage) {
    const outputDiv = document.getElementById('output');
    
    outputDiv.innerHTML = `
        <div class="error">
            <strong>❌ Error generating workflow state:</strong><br>
            ${errorMessage}
            <br><br>
            <strong>Troubleshooting:</strong>
            <ul>
                <li>Check that all required fields are filled</li>
                <li>Ensure JSON fields contain valid JSON</li>
                <li>Verify the API server is running</li>
            </ul>
        </div>
    `;
    
    // Scroll to results
    outputDiv.scrollIntoView({ behavior: 'smooth' });
}

// Add a new block to the form
function addBlock() {
    blockCounter++;
    const blocksContainer = document.getElementById('blocksContainer');
    
    const blockHtml = `
        <div class="block-item">
            <h4>Block ${blockCounter} <button type="button" class="remove-block" onclick="removeBlock(this)">Remove</button></h4>
            <div class="form-row">
                <div class="form-group">
                    <label>Block ID*</label>
                    <input type="text" name="block_id" value="block-${blockCounter}-${Date.now()}" required>
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
                    <input type="text" name="block_name" value="Block ${blockCounter}" required>
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

// Remove a block from the form
function removeBlock(button) {
    const blockItem = button.closest('.block-item');
    blockItem.remove();
}

// Clear the entire form
function clearForm() {
    if (confirm('Are you sure you want to clear all form data?')) {
        document.getElementById('demoForm').reset();
        
        // Reset blocks to just one starter block
        const blocksContainer = document.getElementById('blocksContainer');
        blocksContainer.innerHTML = `
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
                        <input type="text" name="block_name" value="Start" required>
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
        `;
        
        blockCounter = 1;
        
        // Hide results
        document.getElementById('result').style.display = 'none';
    }
}

// Load example data for demonstration
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
    
    // Add agent block
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
                    <input type="text" name="block_name" value="Trading Decision Agent" required>
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
                <textarea name="sub_blocks">{"model":{"id":"model","type":"combobox","value":"gpt-4"},"systemPrompt":{"id":"systemPrompt","type":"long-input","value":"You are a crypto trading agent. Analyze market data and make buy/sell decisions based on risk parameters."}}</textarea>
            </div>
            <div class="form-group">
                <label>Outputs (JSON)</label>
                <textarea name="outputs">{"model":"string","tokens":"any","content":"string","toolCalls":"any"}</textarea>
            </div>
        </div>
    `;
    
    blocksContainer.innerHTML = starterBlockHtml + apiBlockHtml + agentBlockHtml;
    blockCounter = 3;
    
    console.log('📝 Loaded example trading bot workflow data');
} 