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
    
    // Set up tab switching
    setupTabSwitching();
});

// Set up tab switching functionality
function setupTabSwitching() {
    document.querySelectorAll('.result-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and content
            document.querySelectorAll('.result-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.result-tab-content').forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab
            tab.classList.add('active');
            
            // Show corresponding content
            const tabName = tab.getAttribute('data-tab');
            document.getElementById(`${tabName}-content`).classList.add('active');
        });
    });
}

// Copy to clipboard function
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.innerText;
    
    navigator.clipboard.writeText(text).then(() => {
        // Show temporary confirmation
        const originalText = element.innerText;
        element.innerText = "Copied to clipboard!";
        setTimeout(() => {
            element.innerText = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}

// Handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const generateBtn = document.getElementById('generateBtn');
    const resultDiv = document.getElementById('result');
    const workflowStateOutput = document.getElementById('workflow-state-output');
    const sqlOutput = document.getElementById('sql-output');
    const validationOutput = document.getElementById('validation-output');
    
    // Show loading state
    generateBtn.disabled = true;
    generateBtn.textContent = '⏳ Generating...';
    
    resultDiv.style.display = 'block';
    workflowStateOutput.innerHTML = '<div class="loading">🔄 Generating workflow state and blocks...</div>';
    
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
        
        // Display the results
        displayWorkflowStateResult(result);
        displaySQLResult(formData, result);
        displayValidationResult(result);
        
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
        folder_id: formData.get('folder_id') || null,
        name: formData.get('workflow_name'),
        description: formData.get('description') || null,
        color: formData.get('color') || '#3972F6',
        variables: formData.get('variables') || '{}',
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
        const horizontalHandles = blockItem.querySelector('select[name="horizontal_handles"]').value === 'true';
        const isWide = blockItem.querySelector('select[name="is_wide"]').value === 'true';
        const advancedMode = blockItem.querySelector('select[name="advanced_mode"]').value === 'true';
        const height = parseFloat(blockItem.querySelector('input[name="height"]').value) || 0;
        const subBlocks = blockItem.querySelector('textarea[name="sub_blocks"]').value || '{}';
        const outputs = blockItem.querySelector('textarea[name="outputs"]').value || '{}';
        const data = blockItem.querySelector('textarea[name="data"]').value || '{}';
        const parentId = blockItem.querySelector('input[name="parent_id"]').value || null;
        const extent = blockItem.querySelector('input[name="extent"]').value || null;
        
        // Validate JSON
        let subBlocksJson, outputsJson, dataJson;
        try {
            subBlocksJson = JSON.parse(subBlocks);
            outputsJson = JSON.parse(outputs);
            dataJson = JSON.parse(data);
        } catch (e) {
            console.warn(`⚠️ Invalid JSON in block ${blockId}, using empty objects`);
            subBlocksJson = {};
            outputsJson = {};
            dataJson = {};
        }
        
        blocks_rows.push({
            id: blockId,
            workflow_id: workflow_rows.id,
            type: blockType,
            name: blockName,
            position_x: positionX,
            position_y: positionY,
            enabled: enabled,
            horizontal_handles: horizontalHandles,
            is_wide: isWide,
            advanced_mode: advancedMode,
            height: height,
            sub_blocks: subBlocksJson,
            outputs: outputsJson,
            data: dataJson,
            parent_id: parentId,
            extent: extent,
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

// Display workflow state result
function displayWorkflowStateResult(result) {
    const outputDiv = document.getElementById('workflow-state-output');
    
    // Format the JSON output nicely
    const formattedJson = JSON.stringify(result, null, 2);
    
    outputDiv.innerHTML = `
        <div style="margin-bottom: 10px;">
            <strong>✅ Success!</strong> Generated workflow state with ${result.generated_state ? Object.keys(result.generated_state.blocks).length : 0} blocks
        </div>
        ${formattedJson}
    `;
}

// Display SQL result
function displaySQLResult(formData, result) {
    const outputDiv = document.getElementById('sql-output');
    
    // Generate SQL INSERT statements
    const workflowData = formData.workflow_rows;
    const blocksData = formData.blocks_rows;
    
    let sqlOutput = "-- Insert workflow into public.workflow_rows\n";
    sqlOutput += `INSERT INTO public.workflow_rows (\n`;
    sqlOutput += `    id, user_id, workspace_id, folder_id, name, description, color, variables, \n`;
    sqlOutput += `    is_published, created_at, updated_at, last_synced, state\n`;
    sqlOutput += `) VALUES (\n`;
    sqlOutput += `    '${workflowData.id}',\n`;
    sqlOutput += `    '${workflowData.user_id}',\n`;
    sqlOutput += `    ${workflowData.workspace_id ? `'${workflowData.workspace_id}'` : 'NULL'},\n`;
    sqlOutput += `    ${workflowData.folder_id ? `'${workflowData.folder_id}'` : 'NULL'},\n`;
    sqlOutput += `    '${workflowData.name}',\n`;
    sqlOutput += `    ${workflowData.description ? `'${workflowData.description.replace(/'/g, "''")}'` : 'NULL'},\n`;
    sqlOutput += `    '${workflowData.color}',\n`;
    sqlOutput += `    '${workflowData.variables.replace(/'/g, "''")}',\n`;
    sqlOutput += `    ${workflowData.is_published},\n`;
    sqlOutput += `    '${workflowData.created_at}',\n`;
    sqlOutput += `    '${workflowData.updated_at}',\n`;
    sqlOutput += `    '${workflowData.last_synced}',\n`;
    sqlOutput += `    '{}'::json\n`;
    sqlOutput += `);\n\n`;
    
    sqlOutput += "-- Insert blocks into public.workflow_blocks_rows\n";
    blocksData.forEach((block, index) => {
        sqlOutput += `INSERT INTO public.workflow_blocks_rows (\n`;
        sqlOutput += `    id, workflow_id, type, name, position_x, position_y, enabled,\n`;
        sqlOutput += `    horizontal_handles, is_wide, advanced_mode, height, sub_blocks, outputs, data,\n`;
        sqlOutput += `    parent_id, extent, created_at, updated_at\n`;
        sqlOutput += `) VALUES (\n`;
        sqlOutput += `    '${block.id}',\n`;
        sqlOutput += `    '${block.workflow_id}',\n`;
        sqlOutput += `    '${block.type}',\n`;
        sqlOutput += `    '${block.name}',\n`;
        sqlOutput += `    ${block.position_x},\n`;
        sqlOutput += `    ${block.position_y},\n`;
        sqlOutput += `    ${block.enabled},\n`;
        sqlOutput += `    ${block.horizontal_handles},\n`;
        sqlOutput += `    ${block.is_wide},\n`;
        sqlOutput += `    ${block.advanced_mode},\n`;
        sqlOutput += `    ${block.height},\n`;
        sqlOutput += `    '${JSON.stringify(block.sub_blocks).replace(/'/g, "''")}'::jsonb,\n`;
        sqlOutput += `    '${JSON.stringify(block.outputs).replace(/'/g, "''")}'::jsonb,\n`;
        sqlOutput += `    '${JSON.stringify(block.data).replace(/'/g, "''")}'::jsonb,\n`;
        sqlOutput += `    ${block.parent_id ? `'${block.parent_id}'` : 'NULL'},\n`;
        sqlOutput += `    ${block.extent ? `'${block.extent}'` : 'NULL'},\n`;
        sqlOutput += `    '${block.created_at}',\n`;
        sqlOutput += `    '${block.updated_at}'\n`;
        sqlOutput += `);\n\n`;
    });
    
    outputDiv.innerHTML = sqlOutput;
}

// Display validation result
function displayValidationResult(result) {
    const outputDiv = document.getElementById('validation-output');
    
    // Format the validation output nicely
    const validationData = {
        isValid: result.validation ? result.validation.is_valid : true,
        warnings: result.validation ? result.validation.warnings : [],
        errors: result.validation ? result.validation.errors : [],
        generatedAt: new Date().toISOString(),
        workflowId: result.workflow_id
    };
    
    const formattedJson = JSON.stringify(validationData, null, 2);
    
    outputDiv.innerHTML = `
        <div style="margin-bottom: 10px;">
            <strong>✅ Validation Results</strong>
        </div>
        ${formattedJson}
    `;
}

// Display error message
function displayError(errorMessage) {
    const outputDiv = document.getElementById('workflow-state-output');
    
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
    
    // Hide other tabs and show workflow state tab
    document.querySelectorAll('.result-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.result-tab-content').forEach(c => c.classList.remove('active'));
    document.querySelector('.result-tab[data-tab="workflow-state"]').classList.add('active');
    document.getElementById('workflow-state-content').classList.add('active');
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
            <div class="form-row">
                <div class="form-group">
                    <label>Horizontal Handles</label>
                    <select name="horizontal_handles">
                        <option value="true" selected>true</option>
                        <option value="false">false</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Is Wide</label>
                    <select name="is_wide">
                        <option value="false" selected>false</option>
                        <option value="true">true</option>
                    </select>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Advanced Mode</label>
                    <select name="advanced_mode">
                        <option value="false" selected>false</option>
                        <option value="true">true</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Height</label>
                    <input type="number" name="height" value="0">
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
            <div class="form-group">
                <label>Data (JSON)</label>
                <textarea name="data" placeholder='{"key": "value"}'>{}</textarea>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Parent ID</label>
                    <input type="text" name="parent_id" value="">
                </div>
                <div class="form-group">
                    <label>Extent</label>
                    <input type="text" name="extent" value="">
                </div>
            </div>
        </div>
    `;
    
    blocksContainer.insertAdjacentHTML('beforeend', blockHtml);
}

// Remove a block from the form
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
            header.innerHTML = `Block ${index + 1} <button type="button" class="remove-block" onclick="removeBlock(this)">Remove</button>`;
        });
        blockCounter = remainingBlocks.length;
    } else {
        alert('Cannot remove the last block. At least one block is required.');
    }
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
                <div class="form-row">
                    <div class="form-group">
                        <label>Horizontal Handles</label>
                        <select name="horizontal_handles">
                            <option value="true" selected>true</option>
                            <option value="false">false</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Is Wide</label>
                        <select name="is_wide">
                            <option value="false" selected>false</option>
                            <option value="true">true</option>
                        </select>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Advanced Mode</label>
                        <select name="advanced_mode">
                            <option value="false" selected>false</option>
                            <option value="true">true</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Height</label>
                        <input type="number" name="height" value="0">
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
                <div class="form-group">
                    <label>Data (JSON)</label>
                    <textarea name="data" placeholder='{"key": "value"}'>{}</textarea>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Parent ID</label>
                        <input type="text" name="parent_id" value="">
                    </div>
                    <div class="form-group">
                        <label>Extent</label>
                        <input type="text" name="extent" value="">
                    </div>
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
    document.getElementById('folder_id').value = '';
    document.getElementById('color').value = '#3972F6';
    document.getElementById('description').value = 'Automated crypto trading bot with AI decision making and risk management';
    document.getElementById('variables').value = '{"trading_pair": "BTC/USD", "stop_loss": 0.02}';
    
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
            <div class="form-row">
                <div class="form-group">
                    <label>Horizontal Handles</label>
                    <select name="horizontal_handles">
                        <option value="true" selected>true</option>
                        <option value="false">false</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Is Wide</label>
                    <select name="is_wide">
                        <option value="false" selected>false</option>
                        <option value="true">true</option>
                    </select>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Advanced Mode</label>
                    <select name="advanced_mode">
                        <option value="false" selected>false</option>
                        <option value="true">true</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Height</label>
                    <input type="number" name="height" value="0">
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
            <div class="form-group">
                <label>Data (JSON)</label>
                <textarea name="data">{}</textarea>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Parent ID</label>
                    <input type="text" name="parent_id" value="">
                </div>
                <div class="form-group">
                    <label>Extent</label>
                    <input type="text" name="extent" value="">
                </div>
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
            <div class="form-row">
                <div class="form-group">
                    <label>Horizontal Handles</label>
                    <select name="horizontal_handles">
                        <option value="true" selected>true</option>
                        <option value="false">false</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Is Wide</label>
                    <select name="is_wide">
                        <option value="false" selected>false</option>
                        <option value="true">true</option>
                    </select>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Advanced Mode</label>
                    <select name="advanced_mode">
                        <option value="false" selected>false</option>
                        <option value="true">true</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Height</label>
                    <input type="number" name="height" value="0">
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
            <div class="form-group">
                <label>Data (JSON)</label>
                <textarea name="data">{}</textarea>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Parent ID</label>
                    <input type="text" name="parent_id" value="">
                </div>
                <div class="form-group">
                    <label>Extent</label>
                    <input type="text" name="extent" value="">
                </div>
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
            <div class="form-row">
                <div class="form-group">
                    <label>Horizontal Handles</label>
                    <select name="horizontal_handles">
                        <option value="true" selected>true</option>
                        <option value="false">false</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Is Wide</label>
                    <select name="is_wide">
                        <option value="false" selected>false</option>
                        <option value="true">true</option>
                    </select>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Advanced Mode</label>
                    <select name="advanced_mode">
                        <option value="false" selected>false</option>
                        <option value="true">true</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Height</label>
                    <input type="number" name="height" value="0">
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
            <div class="form-group">
                <label>Data (JSON)</label>
                <textarea name="data">{"risk_tolerance": 0.02}</textarea>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Parent ID</label>
                    <input type="text" name="parent_id" value="">
                </div>
                <div class="form-group">
                    <label>Extent</label>
                    <input type="text" name="extent" value="">
                </div>
            </div>
        </div>
    `;
    
    blocksContainer.innerHTML = starterBlockHtml + apiBlockHtml + agentBlockHtml;
    blockCounter = 3;
    
    console.log('📝 Loaded example trading bot workflow data');
} 