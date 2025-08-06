// Agent Forge Frontend JavaScript - MOCK VERSION FOR TESTING
const API_BASE = 'https://solidus-olive.vercel.app/api';

// Mock data for testing while API is down
const MOCK_TEMPLATES = {
    "lead_generation": {
        "name": "lead_generation",
        "display_name": "Lead Generation System",
        "description": "Capture and qualify leads from multiple sources",
        "category": "Sales & Marketing",
        "tags": ["sales", "marketing", "crm"],
        "complexity": "Medium",
        "estimated_runtime": "24/7",
        "customizable_fields": ["source", "crm_integration"]
    },
    "trading_bot": {
        "name": "trading_bot", 
        "display_name": "Crypto Trading Bot",
        "description": "Automated trading with stop-loss and take-profit",
        "category": "Web3 Trading",
        "tags": ["trading", "crypto", "finance"],
        "complexity": "Complex", 
        "estimated_runtime": "24/7",
        "customizable_fields": ["trading_pair", "stop_loss"]
    },
    "ai_research": {
        "name": "ai_research",
        "display_name": "AI Research Assistant", 
        "description": "Multi-agent research collaboration system",
        "category": "AI Automation",
        "tags": ["research", "ai", "analysis"],
        "complexity": "Complex",
        "estimated_runtime": "On-demand",
        "customizable_fields": ["research_topic", "depth_level"]
    }
};

const MOCK_CATEGORIES = ["Sales & Marketing", "Web3 Trading", "AI Automation"];

// Global state
let templates = {};
let workflows = [];
let analytics = {};
let selectedTemplate = null;
let useMockData = true; // Enable mock mode

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupNavigation();
    loadTemplates();
    setupEventListeners();
}

function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    navButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;
            
            // Remove active class from all buttons and tabs
            navButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(tab => tab.classList.remove('active'));
            
            // Add active class to clicked button and corresponding tab
            button.classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');
            
            // Load content based on tab
            switch(tabName) {
                case 'templates':
                    loadTemplates();
                    break;
                case 'workflows':
                    loadWorkflows();
                    break;
                case 'create':
                    showCreateForm();
                    break;
                case 'analytics':
                    loadAnalytics();
                    break;
            }
        });
    });
}

function setupEventListeners() {
    // Modal close listeners
    document.querySelector('.modal-close').addEventListener('click', closeModal);
    document.getElementById('template-modal').addEventListener('click', (e) => {
        if (e.target.id === 'template-modal') closeModal();
    });
    
    // Create workflow button
    document.getElementById('create-from-template').addEventListener('click', createWorkflowFromTemplate);
}

// API Functions
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Call failed:', error);
        showToast('API call failed: ' + error.message, 'error');
        throw error;
    }
}

// Templates Functions
async function loadTemplates() {
    try {
        showLoading('templates-grid');
        
        if (useMockData) {
            // Use mock data for testing
            console.log("🧪 Using mock data - API is down");
            templates = MOCK_TEMPLATES;
            displayTemplates(templates);
            setupCategoryFilter(MOCK_CATEGORIES);
            showToast("🧪 Demo Mode: Using mock templates (API unavailable)", "info");
            return;
        }
        
        const data = await apiCall('/templates');
        templates = data.templates;
        
        displayTemplates(templates);
        setupCategoryFilter(data.categories);
    } catch (error) {
        console.log("❌ API failed, falling back to mock data");
        templates = MOCK_TEMPLATES;
        displayTemplates(templates);
        setupCategoryFilter(MOCK_CATEGORIES);
        showToast("⚠️ API unavailable - showing demo templates", "error");
    }
}

function displayTemplates(templatesToShow) {
    const grid = document.getElementById('templates-grid');
    
    if (Object.keys(templatesToShow).length === 0) {
        grid.innerHTML = `
            <div class="no-results">
                <i class="fas fa-search"></i>
                <p>No templates found</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = Object.entries(templatesToShow).map(([key, template]) => `
        <div class="template-card" onclick="showTemplateDetails('${key}')">
            <div class="template-header">
                <div class="template-icon">
                    <i class="${getTemplateIcon(template.category)}"></i>
                </div>
                <div class="template-info">
                    <h3>${template.display_name}</h3>
                    <span class="template-category">${template.category}</span>
                </div>
            </div>
            <p class="template-description">${template.description}</p>
            <div class="template-footer">
                <div class="template-tags">
                    ${template.tags.slice(0, 3).map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
                <span class="complexity ${template.complexity.toLowerCase()}">${template.complexity}</span>
            </div>
        </div>
    `).join('');
}

function setupCategoryFilter(categories) {
    const categoryButtons = document.getElementById('category-buttons');
    
    categoryButtons.innerHTML = categories.map(category => `
        <button class="filter-btn" data-category="${category}">${category}</button>
    `).join('');
    
    // Add event listeners to filter buttons
    document.querySelectorAll('.filter-btn').forEach(button => {
        button.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            const category = button.dataset.category;
            if (category === 'all') {
                displayTemplates(templates);
            } else {
                const filtered = Object.fromEntries(
                    Object.entries(templates).filter(([key, template]) => 
                        template.category === category
                    )
                );
                displayTemplates(filtered);
            }
        });
    });
}

function getTemplateIcon(category) {
    const icons = {
        'Web3 Trading': 'fas fa-coins',
        'Sales & Marketing': 'fas fa-chart-line',
        'AI Automation': 'fas fa-robot',
        'Customer Service': 'fas fa-headset',
        'Blockchain': 'fab fa-ethereum',
        'Data Processing': 'fas fa-database',
        'Content & Media': 'fas fa-pen-fancy',
        'Communication': 'fas fa-comments',
        'Social Media': 'fab fa-twitter',
        'E-commerce': 'fas fa-shopping-cart',
        'Human Resources': 'fas fa-users',
        'Finance': 'fas fa-dollar-sign',
        'Project Management': 'fas fa-tasks'
    };
    return icons[category] || 'fas fa-cog';
}

function showTemplateDetails(templateKey) {
    const template = templates[templateKey];
    if (!template) return;
    
    selectedTemplate = templateKey;
    document.getElementById('modal-title').textContent = template.display_name;
    
    document.getElementById('modal-body').innerHTML = `
        <div class="template-details">
            <div class="detail-section">
                <h4>Description</h4>
                <p>${template.description}</p>
            </div>
            
            <div class="detail-section">
                <h4>Category</h4>
                <span class="template-category">${template.category}</span>
            </div>
            
            <div class="detail-section">
                <h4>Complexity</h4>
                <span class="complexity ${template.complexity.toLowerCase()}">${template.complexity}</span>
            </div>
            
            <div class="detail-section">
                <h4>Runtime</h4>
                <p>${template.estimated_runtime}</p>
            </div>
            
            <div class="detail-section">
                <h4>Tags</h4>
                <div class="template-tags">
                    ${template.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            </div>
            
            <div class="detail-section">
                <h4>Customizable Fields</h4>
                <div class="customizable-fields">
                    ${template.customizable_fields.map(field => `
                        <div class="form-group">
                            <label class="form-label">${formatFieldName(field)}</label>
                            <input type="text" class="form-input" id="field-${field}" placeholder="Enter ${field}">
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
    
    showModal();
}

function formatFieldName(field) {
    return field.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

async function createWorkflowFromTemplate() {
    if (!selectedTemplate) return;
    
    const template = templates[selectedTemplate];
    const customization = {};
    
    // Collect customization data
    template.customizable_fields.forEach(field => {
        const input = document.getElementById(`field-${field}`);
        if (input && input.value.trim()) {
            customization[field] = input.value.trim();
        }
    });
    
    try {
        showLoadingButton('create-from-template', 'Creating...');
        
        if (useMockData) {
            // Mock workflow creation
            await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate delay
            showToast(`🧪 Mock: Workflow "${template.display_name}" created successfully!`, 'success');
            closeModal();
            document.querySelector('[data-tab="workflows"]').click();
            return;
        }
        
        const result = await apiCall(`/workflows/templates/${selectedTemplate}`, {
            method: 'POST',
            body: JSON.stringify(customization)
        });
        
        showToast(`✅ Workflow "${result.name}" created successfully!`, 'success');
        closeModal();
        
        // Switch to workflows tab and reload
        document.querySelector('[data-tab="workflows"]').click();
        
    } catch (error) {
        showToast('🧪 Mock: Workflow creation simulated (API unavailable)', 'error');
        closeModal();
        document.querySelector('[data-tab="workflows"]').click();
    } finally {
        resetButton('create-from-template', 'Create Workflow');
    }
}

// Workflows Functions
async function loadWorkflows() {
    try {
        showLoading('workflows-grid');
        const data = await apiCall('/workflows');
        workflows = data.workflows;
        
        displayWorkflows(workflows);
    } catch (error) {
        document.getElementById('workflows-grid').innerHTML = `
            <div class="error">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Failed to load workflows</p>
            </div>
        `;
    }
}

function displayWorkflows(workflowsToShow) {
    const grid = document.getElementById('workflows-grid');
    
    if (workflowsToShow.length === 0) {
        grid.innerHTML = `
            <div class="no-results">
                <i class="fas fa-project-diagram"></i>
                <p>No workflows found. Create your first workflow from a template!</p>
                <button class="btn btn-primary" onclick="document.querySelector('[data-tab=\\"templates\\"]').click()">
                    Browse Templates
                </button>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = workflowsToShow.map(workflow => `
        <div class="workflow-card">
            <div class="template-header">
                <div class="template-icon" style="background: ${workflow.color}">
                    <i class="fas fa-project-diagram"></i>
                </div>
                <div class="template-info">
                    <h3>${workflow.name}</h3>
                    <span class="template-category">User: ${workflow.user_id.substring(0, 8)}...</span>
                </div>
            </div>
            <p class="template-description">${workflow.description || 'No description'}</p>
            <div class="template-footer">
                <div class="template-tags">
                    <span class="tag">${workflow.block_count} blocks</span>
                    <span class="tag">${workflow.is_published ? 'Published' : 'Draft'}</span>
                </div>
                <div class="workflow-actions">
                    <button class="btn btn-secondary btn-sm" onclick="generateState('${workflow.id}')">
                        <i class="fas fa-magic"></i> Generate State
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

async function generateState(workflowId) {
    try {
        showToast('🔄 Generating AI workflow state...', 'info');
        
        const result = await apiCall(`/workflows/${workflowId}/generate-state`, {
            method: 'POST'
        });
        
        showToast(`✅ State generated with ${Object.keys(result.generated_state.blocks).length} blocks!`, 'success');
        
        // Optionally show more details
        console.log('Generated state:', result);
        
    } catch (error) {
        showToast('Failed to generate state: ' + error.message, 'error');
    }
}

// Analytics Functions
async function loadAnalytics() {
    try {
        showLoading('analytics-grid');
        
        if (useMockData) {
            // Mock analytics data
            analytics = {
                cache_statistics: {
                    cache_hit_rate: "73.2%",
                    total_patterns_cached: 156,
                    average_time_saved: "2.4s",
                    ai_calls_saved: 1247
                },
                system_info: {
                    database_connected: false,
                    rag_enhanced: false,
                    openai_embeddings: false
                },
                performance_benefits: {
                    speed_improvement: "5-10x faster",
                    cost_reduction: "70-80% savings"
                }
            };
            displayAnalytics(analytics);
            showToast("🧪 Demo Mode: Mock analytics data", "info");
            return;
        }
        
        const data = await apiCall('/workflows/cache/stats');
        analytics = data;
        
        displayAnalytics(analytics);
    } catch (error) {
        // Use mock data as fallback
        analytics = {
            cache_statistics: {
                cache_hit_rate: "Demo Mode",
                total_patterns_cached: "N/A",
                average_time_saved: "N/A",
                ai_calls_saved: "N/A"
            },
            system_info: {
                database_connected: false,
                rag_enhanced: false,
                openai_embeddings: false
            },
            performance_benefits: {
                speed_improvement: "API Unavailable",
                cost_reduction: "Demo Mode"
            }
        };
        displayAnalytics(analytics);
        showToast("⚠️ Analytics unavailable - showing demo data", "error");
    }
}

function displayAnalytics(data) {
    const grid = document.getElementById('analytics-grid');
    
    grid.innerHTML = `
        <div class="analytics-card">
            <h3><i class="fas fa-tachometer-alt"></i> Cache Performance</h3>
            <div class="metric">
                <span class="metric-label">Cache Hit Rate</span>
                <span class="metric-value">${data.cache_statistics.cache_hit_rate}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Patterns Cached</span>
                <span class="metric-value">${data.cache_statistics.total_patterns_cached}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Time Saved</span>
                <span class="metric-value">${data.cache_statistics.average_time_saved}</span>
            </div>
        </div>
        
        <div class="analytics-card">
            <h3><i class="fas fa-chart-bar"></i> System Status</h3>
            <div class="metric">
                <span class="metric-label">Database Connected</span>
                <span class="metric-value">${data.system_info.database_connected ? '✅ Yes' : '❌ No'}</span>
            </div>
            <div class="metric">
                <span class="metric-label">RAG Enhanced</span>
                <span class="metric-value">${data.system_info.rag_enhanced ? '✅ Yes' : '❌ No'}</span>
            </div>
            <div class="metric">
                <span class="metric-label">OpenAI Embeddings</span>
                <span class="metric-value">${data.system_info.openai_embeddings ? '✅ Yes' : '❌ No'}</span>
            </div>
        </div>
        
        <div class="analytics-card">
            <h3><i class="fas fa-rocket"></i> Performance Benefits</h3>
            <div class="metric">
                <span class="metric-label">Speed Improvement</span>
                <span class="metric-value">${data.performance_benefits.speed_improvement}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Cost Reduction</span>
                <span class="metric-value">${data.performance_benefits.cost_reduction}</span>
            </div>
            <div class="metric">
                <span class="metric-label">AI Calls Saved</span>
                <span class="metric-value">${data.cache_statistics.ai_calls_saved}</span>
            </div>
        </div>
    `;
}

// Create Form Functions
function showCreateForm() {
    const form = document.getElementById('create-form');
    
    form.innerHTML = `
        <div class="create-options">
            <div class="option-card" onclick="document.querySelector('[data-tab=\\"templates\\"]').click()">
                <div class="option-icon">
                    <i class="fas fa-layer-group"></i>
                </div>
                <h3>From Template</h3>
                <p>Choose from our professional templates and customize them for your needs</p>
                <button class="btn btn-primary">Browse Templates</button>
            </div>
            
            <div class="option-card" onclick="showCustomForm()">
                <div class="option-icon">
                    <i class="fas fa-code"></i>
                </div>  
                <h3>Custom Workflow</h3>
                <p>Build a completely custom workflow from scratch</p>
                <button class="btn btn-secondary">Coming Soon</button>
            </div>
        </div>
    `;
}

// Utility Functions
function showModal() {
    document.getElementById('template-modal').classList.add('active');
}

function closeModal() {
    document.getElementById('template-modal').classList.remove('active');
    selectedTemplate = null;
}

function showLoading(containerId) {
    document.getElementById(containerId).innerHTML = `
        <div class="loading">
            <i class="fas fa-spinner fa-spin"></i>
            <p>Loading...</p>
        </div>
    `;
}

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const icon = toast.querySelector('.toast-icon');
    const messageEl = toast.querySelector('.toast-message');
    
    // Set icon based on type
    const icons = {
        'success': 'fas fa-check-circle',
        'error': 'fas fa-exclamation-circle',
        'info': 'fas fa-info-circle'
    };
    
    icon.className = `toast-icon ${icons[type] || icons.info}`;
    messageEl.textContent = message;
    
    // Remove existing type classes and add new one
    toast.className = `toast ${type}`;
    
    // Show toast
    toast.classList.add('show');
    
    // Hide after 4 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 4000);
}

function showLoadingButton(buttonId, text) {
    const button = document.getElementById(buttonId);
    button.disabled = true;
    button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${text}`;
}

function resetButton(buttonId, text) {
    const button = document.getElementById(buttonId);
    button.disabled = false;
    button.innerHTML = text;
}

// Add custom CSS for additional components
const additionalCSS = `
    .no-results, .error {
        text-align: center;
        padding: 4rem 2rem;
        color: rgba(255, 255, 255, 0.7);
        grid-column: 1 / -1;
    }
    
    .no-results i, .error i {
        font-size: 3rem;
        margin-bottom: 1rem;
        color: rgba(255, 255, 255, 0.5);
    }
    
    .create-options {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .option-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .option-card:hover {
        transform: translateY(-8px);
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(0, 212, 255, 0.3);
    }
    
    .option-icon {
        width: 80px;
        height: 80px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        background: linear-gradient(45deg, #00d4ff, #4ecdc4);
        color: #000;
        margin: 0 auto 1.5rem;
    }
    
    .option-card h3 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: #ffffff;
    }
    
    .option-card p {
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .btn-sm {
        padding: 0.5rem 1rem;
        font-size: 0.875rem;
    }
    
    .workflow-actions {
        display: flex;
        gap: 0.5rem;
    }
    
    .detail-section {
        margin-bottom: 2rem;
    }
    
    .detail-section h4 {
        color: #00d4ff;
        margin-bottom: 0.75rem;
        font-size: 1.1rem;
    }
    
    .detail-section p {
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.6;
    }
`;

// Inject additional CSS
const style = document.createElement('style');
style.textContent = additionalCSS;
document.head.appendChild(style); 