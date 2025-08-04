# src/services/templates.py
from typing import Dict, Any, List, Optional
from datetime import datetime
from uuid import uuid4
import json

class AgentForgeTemplates:
    """Template system for creating Agent Forge workflows"""
    
    def __init__(self):
        self.templates = {
            "lead_generation": self._lead_generation_template,
            "trading_bot": self._trading_bot_template,
            "multi_agent_research": self._multi_agent_research_template,
            "customer_support": self._customer_support_template,
            "web3_automation": self._web3_automation_template,
            "data_pipeline": self._data_pipeline_template,
            "content_generation": self._content_generation_template,
            "notification_system": self._notification_system_template
        }
    
    def _create_block(self, workflow_id: str, block_type: str, name: str, 
                     position: tuple, sub_blocks: Dict[str, Any], 
                     outputs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Helper to create Agent Forge block structure"""
        if outputs is None:
            outputs = self._get_default_outputs(block_type)
        
        return {
            "id": str(uuid4()),
            "workflow_id": workflow_id,
            "type": block_type,
            "name": name,
            "position_x": position[0],
            "position_y": position[1],
            "enabled": True,
            "horizontal_handles": True,
            "is_wide": block_type == "agent",
            "advanced_mode": False,
            "height": 120 if block_type == "agent" else 95,
            "sub_blocks": sub_blocks,
            "outputs": outputs,
            "data": {},
            "parent_id": None,
            "extent": None
        }
    
    def _get_default_outputs(self, block_type: str) -> Dict[str, Any]:
        """Get default outputs for block type"""
        defaults = {
            "starter": {"response": {"type": {"input": "any"}}},
            "agent": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"},
            "api": {"data": "any", "status": "number", "headers": "json"},
            "output": {"success": "boolean", "message": "string"},
            "tool": {"result": "any", "metadata": "json"}
        }
        return defaults.get(block_type, {"output": "any"})
    
    def _lead_generation_template(self, customization: Dict[str, Any]) -> Dict[str, Any]:
        """Lead generation workflow template"""
        workflow_id = str(uuid4())
        
        # Customizable parameters
        company_name = customization.get("company_name", "Your Company")
        target_industry = customization.get("target_industry", "technology")
        email_template = customization.get("email_template", "professional")
        
        blocks = []
        
        # Starter block - webhook trigger
        starter = self._create_block(
            workflow_id, "starter", "Lead Capture",
            (100, 200),
            {
                "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"},
                "webhookPath": {"id": "webhookPath", "type": "short-input", "value": "lead-capture"},
                "webhookSecret": {"id": "webhookSecret", "type": "short-input", "value": ""},
            }
        )
        blocks.append(starter)
        
        # Agent block - lead qualification
        agent = self._create_block(
            workflow_id, "agent", "Lead Qualifier",
            (350, 200),
            {
                "model": {"id": "model", "type": "combobox", "value": "gpt-4"},
                "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                               "value": f"You are a lead qualification agent for {company_name}. Analyze incoming leads and score them based on: company size, industry match ({target_industry}), budget indicators, and urgency. Provide a score 1-10 and qualification reason."},
                "temperature": {"id": "temperature", "type": "slider", "value": 0.3}
            }
        )
        blocks.append(agent)
        
        # API block - CRM integration
        crm = self._create_block(
            workflow_id, "api", "CRM Update",
            (600, 200),
            {
                "url": {"id": "url", "type": "short-input", "value": "https://api.hubspot.com/crm/v3/objects/contacts"},
                "method": {"id": "method", "type": "dropdown", "value": "POST"},
                "headers": {"id": "headers", "type": "table", "value": [
                    {"key": "Authorization", "value": "Bearer {{HUBSPOT_TOKEN}}"},
                    {"key": "Content-Type", "value": "application/json"}
                ]}
            }
        )
        blocks.append(crm)
        
        # Output block - notifications
        output = self._create_block(
            workflow_id, "output", "Lead Notification",
            (850, 200),
            {
                "outputType": {"id": "outputType", "type": "dropdown", "value": "email"},
                "channels": {"id": "channels", "type": "multi-select", "value": ["email", "slack"]},
                "emailConfig": {"id": "emailConfig", "type": "json", 
                              "value": {"to": "sales@company.com", "template": email_template}}
            }
        )
        blocks.append(output)
        
        # Create edges
        edges = [
            {"source": starter["id"], "target": agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": agent["id"], "target": crm["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": crm["id"], "target": output["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        return self._build_workflow(workflow_id, "Lead Generation System", 
                                  "Automated lead capture, qualification, and CRM integration",
                                  blocks, edges, customization)
    
    def _trading_bot_template(self, customization: Dict[str, Any]) -> Dict[str, Any]:
        """Crypto trading bot template"""
        workflow_id = str(uuid4())
        
        # Customizable parameters
        trading_pair = customization.get("trading_pair", "BTC/USD")
        stop_loss = customization.get("stop_loss", -5)
        take_profit = customization.get("take_profit", 10)
        
        blocks = []
        
        # Starter - scheduled monitoring
        starter = self._create_block(
            workflow_id, "starter", "Market Monitor",
            (100, 200),
            {
                "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"},
                "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "minutes"},
                "minutesInterval": {"id": "minutesInterval", "type": "short-input", "value": "5"},
                "timezone": {"id": "timezone", "type": "dropdown", "value": "UTC"}
            }
        )
        blocks.append(starter)
        
        # API - market data
        api = self._create_block(
            workflow_id, "api", "Market Data",
            (300, 200),
            {
                "url": {"id": "url", "type": "short-input", "value": "https://api.coingecko.com/api/v3/simple/price"},
                "method": {"id": "method", "type": "dropdown", "value": "GET"},
                "params": {"id": "params", "type": "table", "value": [
                    {"key": "ids", "value": "bitcoin,ethereum"},
                    {"key": "vs_currencies", "value": "usd"},
                    {"key": "include_24hr_change", "value": "true"}
                ]}
            }
        )
        blocks.append(api)
        
        # Agent - trading decision
        agent = self._create_block(
            workflow_id, "agent", "Trading Agent",
            (500, 200),
            {
                "model": {"id": "model", "type": "combobox", "value": "gpt-4"},
                "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                               "value": f"You are a crypto trading agent for {trading_pair}. Analyze market data and make trading decisions. Stop-loss: {stop_loss}%, Take-profit: {take_profit}%. Consider: price trends, volume, RSI, moving averages. Respond with BUY/SELL/HOLD and reasoning."},
                "temperature": {"id": "temperature", "type": "slider", "value": 0.2},
                "tools": {"id": "tools", "type": "tool-input", "value": [
                    {"type": "technical_analysis", "enabled": True},
                    {"type": "risk_calculator", "enabled": True}
                ]}
            }
        )
        blocks.append(agent)
        
        # API - execute trade
        execute = self._create_block(
            workflow_id, "api", "Execute Trade",
            (700, 200),
            {
                "url": {"id": "url", "type": "short-input", "value": "https://api.binance.com/api/v3/order"},
                "method": {"id": "method", "type": "dropdown", "value": "POST"},
                "headers": {"id": "headers", "type": "table", "value": [
                    {"key": "X-MBX-APIKEY", "value": "{{BINANCE_API_KEY}}"}
                ]}
            }
        )
        blocks.append(execute)
        
        # Output - trade notifications
        output = self._create_block(
            workflow_id, "output", "Trade Alert",
            (900, 200),
            {
                "outputType": {"id": "outputType", "type": "dropdown", "value": "multi"},
                "channels": {"id": "channels", "type": "multi-select", "value": ["email", "sms", "discord"]},
                "discordConfig": {"id": "discordConfig", "type": "json", 
                                "value": {"webhook": "https://discord.com/api/webhooks/..."}}
            }
        )
        blocks.append(output)
        
        edges = [
            {"source": starter["id"], "target": api["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": api["id"], "target": agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": agent["id"], "target": execute["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": execute["id"], "target": output["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        return self._build_workflow(workflow_id, "Crypto Trading Bot", 
                                  f"Automated {trading_pair} trading with stop-loss and take-profit",
                                  blocks, edges, customization)
    
    def _multi_agent_research_template(self, customization: Dict[str, Any]) -> Dict[str, Any]:
        """Multi-agent research team template"""
        workflow_id = str(uuid4())
        
        research_topic = customization.get("research_topic", "market analysis")
        
        blocks = []
        
        # Starter
        starter = self._create_block(
            workflow_id, "starter", "Research Request",
            (100, 300),
            {
                "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"},
                "webhookPath": {"id": "webhookPath", "type": "short-input", "value": "research-request"}
            }
        )
        blocks.append(starter)
        
        # Coordinator agent
        coordinator = self._create_block(
            workflow_id, "agent", "Research Coordinator",
            (300, 300),
            {
                "model": {"id": "model", "type": "combobox", "value": "claude-3"},
                "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                               "value": f"You coordinate research on {research_topic}. Break down queries into subtasks for specialist agents: market research, technical analysis, and competitive intelligence."},
                "temperature": {"id": "temperature", "type": "slider", "value": 0.5}
            }
        )
        blocks.append(coordinator)
        
        # Specialist agents
        specialists = [
            ("Market Research Agent", (500, 200), "market trends and consumer behavior"),
            ("Technical Agent", (500, 300), "technical specifications and implementation details"),
            ("Competitive Agent", (500, 400), "competitor analysis and market positioning")
        ]
        
        for name, position, specialty in specialists:
            agent = self._create_block(
                workflow_id, "agent", name,
                position,
                {
                    "model": {"id": "model", "type": "combobox", "value": "gpt-4"},
                    "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                                   "value": f"You specialize in {specialty}. Provide detailed analysis and insights in your domain."},
                    "temperature": {"id": "temperature", "type": "slider", "value": 0.7},
                    "tools": {"id": "tools", "type": "tool-input", "value": [
                        {"type": "web_search", "enabled": True},
                        {"type": "data_analysis", "enabled": True}
                    ]}
                }
            )
            blocks.append(agent)
        
        # Synthesis agent
        synthesis = self._create_block(
            workflow_id, "agent", "Research Synthesizer",
            (700, 300),
            {
                "model": {"id": "model", "type": "combobox", "value": "claude-3"},
                "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                               "value": "Synthesize research from multiple specialist agents into a comprehensive report with executive summary, key findings, and recommendations."},
                "temperature": {"id": "temperature", "type": "slider", "value": 0.4}
            }
        )
        blocks.append(synthesis)
        
        # Output
        output = self._create_block(
            workflow_id, "output", "Research Report",
            (900, 300),
            {
                "outputType": {"id": "outputType", "type": "dropdown", "value": "document"},
                "channels": {"id": "channels", "type": "multi-select", "value": ["email", "google_docs"]},
                "docConfig": {"id": "docConfig", "type": "json", 
                            "value": {"format": "pdf", "template": "research_report"}}
            }
        )
        blocks.append(output)
        
        # Create edges (coordinator to all specialists, all specialists to synthesis)
        edges = [
            {"source": starter["id"], "target": coordinator["id"], "sourceHandle": "output", "targetHandle": "input"},
        ]
        
        # Connect coordinator to specialists
        for i in range(2, 5):  # specialists are blocks 2, 3, 4
            edges.append({
                "source": coordinator["id"], 
                "target": blocks[i]["id"], 
                "sourceHandle": "output", 
                "targetHandle": "input"
            })
        
        # Connect specialists to synthesis
        for i in range(2, 5):
            edges.append({
                "source": blocks[i]["id"], 
                "target": synthesis["id"], 
                "sourceHandle": "output", 
                "targetHandle": "input"
            })
        
        edges.append({
            "source": synthesis["id"], 
            "target": output["id"], 
            "sourceHandle": "output", 
            "targetHandle": "input"
        })
        
        return self._build_workflow(workflow_id, "Multi-Agent Research Team", 
                                  f"Collaborative research system for {research_topic}",
                                  blocks, edges, customization)
    
    def _customer_support_template(self, customization: Dict[str, Any]) -> Dict[str, Any]:
        """Customer support automation template"""
        workflow_id = str(uuid4())
        
        company_name = customization.get("company_name", "Your Company")
        support_hours = customization.get("support_hours", "24/7")
        
        blocks = []
        
        # Starter - ticket webhook
        starter = self._create_block(
            workflow_id, "starter", "Support Ticket",
            (100, 200),
            {
                "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"},
                "webhookPath": {"id": "webhookPath", "type": "short-input", "value": "support-ticket"},
            }
        )
        blocks.append(starter)
        
        # Agent - ticket classifier
        classifier = self._create_block(
            workflow_id, "agent", "Ticket Classifier",
            (300, 200),
            {
                "model": {"id": "model", "type": "combobox", "value": "gpt-4"},
                "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                               "value": f"You are a customer support classifier for {company_name}. Categorize tickets: URGENT (billing, outages), HIGH (bugs, feature requests), MEDIUM (questions), LOW (feedback). Provide category and priority."},
                "temperature": {"id": "temperature", "type": "slider", "value": 0.2}
            }
        )
        blocks.append(classifier)
        
        # Agent - support agent
        support_agent = self._create_block(
            workflow_id, "agent", "Support Agent",
            (500, 200),
            {
                "model": {"id": "model", "type": "combobox", "value": "claude-3"},
                "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                               "value": f"You are a helpful customer support agent for {company_name}. Available {support_hours}. Provide clear, empathetic responses. Escalate to human if needed."},
                "temperature": {"id": "temperature", "type": "slider", "value": 0.6},
                "tools": {"id": "tools", "type": "tool-input", "value": [
                    {"type": "knowledge_base", "enabled": True},
                    {"type": "ticket_system", "enabled": True}
                ]}
            }
        )
        blocks.append(support_agent)
        
        # Output - customer response
        output = self._create_block(
            workflow_id, "output", "Customer Response",
            (700, 200),
            {
                "outputType": {"id": "outputType", "type": "dropdown", "value": "email"},
                "channels": {"id": "channels", "type": "multi-select", "value": ["email", "zendesk"]},
                "emailConfig": {"id": "emailConfig", "type": "json", 
                              "value": {"template": "support_response", "auto_close": False}}
            }
        )
        blocks.append(output)
        
        edges = [
            {"source": starter["id"], "target": classifier["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": classifier["id"], "target": support_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": support_agent["id"], "target": output["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        return self._build_workflow(workflow_id, "Customer Support Automation", 
                                  f"Automated ticket classification and response system for {company_name}",
                                  blocks, edges, customization)
    
    def _web3_automation_template(self, customization: Dict[str, Any]) -> Dict[str, Any]:
        """Web3 automation template"""
        workflow_id = str(uuid4())
        
        # Simplified template for Web3 automation
        blocks = []
        
        starter = self._create_block(
            workflow_id, "starter", "Blockchain Monitor",
            (100, 200),
            {
                "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"},
                "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "minutes"},
                "minutesInterval": {"id": "minutesInterval", "type": "short-input", "value": "10"}
            }
        )
        blocks.append(starter)
        
        edges = []
        
        return self._build_workflow(workflow_id, "Web3 Automation", 
                                  "Blockchain monitoring and automation",
                                  blocks, edges, customization)
    
    def _data_pipeline_template(self, customization: Dict[str, Any]) -> Dict[str, Any]:
        """Data pipeline template"""
        workflow_id = str(uuid4())
        blocks = []
        edges = []
        return self._build_workflow(workflow_id, "Data Pipeline", 
                                  "Automated data processing pipeline",
                                  blocks, edges, customization)
    
    def _content_generation_template(self, customization: Dict[str, Any]) -> Dict[str, Any]:
        """Content generation template"""
        workflow_id = str(uuid4())
        blocks = []
        edges = []
        return self._build_workflow(workflow_id, "Content Generation", 
                                  "AI-powered content creation system",
                                  blocks, edges, customization)
    
    def _notification_system_template(self, customization: Dict[str, Any]) -> Dict[str, Any]:
        """Notification system template"""
        workflow_id = str(uuid4())
        blocks = []
        edges = []
        return self._build_workflow(workflow_id, "Notification System", 
                                  "Multi-channel notification system",
                                  blocks, edges, customization)
    
    def _build_workflow(self, workflow_id: str, name: str, description: str, 
                       blocks: List[Dict[str, Any]], edges: List[Dict[str, str]], 
                       customization: Dict[str, Any]) -> Dict[str, Any]:
        """Build complete workflow structure"""
        
        # Create state structure
        blocks_dict = {block["id"]: {
            "id": block["id"],
            "type": block["type"],
            "name": block["name"],
            "position": {"x": block["position_x"], "y": block["position_y"]},
            "subBlocks": block["sub_blocks"],
            "outputs": block["outputs"],
            "enabled": block["enabled"],
            "horizontalHandles": block["horizontal_handles"],
            "isWide": block["is_wide"],
            "height": block["height"]
        } for block in blocks}
        
        state = {
            "blocks": blocks_dict,
            "edges": edges,
            "subflows": {},
            "variables": customization.get("variables", {}),
            "metadata": {
                "version": "1.0.0",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        return {
            "id": workflow_id,
            "user_id": "template-user",
            "workspace_id": "template-workspace",
            "name": name,
            "description": description,
            "state": state,  # Keep as dict, will be serialized when saved
            "color": "#3972F6",
            "last_synced": datetime.utcnow(),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_deployed": False,
            "collaborators": [],
            "run_count": 0,
            "variables": customization.get("variables", {}),
            "is_published": False,
            "marketplace_data": {
                "category": customization.get("category", "General"),
                "tags": customization.get("tags", []),
                "template": True
            }
        }

# Template service functions
template_service = AgentForgeTemplates()

def get_template_by_name(template_name: str) -> Optional[Dict[str, Any]]:
    """Get template by name"""
    if template_name in template_service.templates:
        return {"name": template_name, "generator": template_service.templates[template_name]}
    return None

def create_workflow_from_template(template: Dict[str, Any], customization: Dict[str, Any]) -> Dict[str, Any]:
    """Create workflow from template"""
    generator = template["generator"]
    return generator(customization)

def get_all_templates() -> List[Dict[str, Any]]:
    """Get all available templates"""
    templates = []
    
    template_info = {
        "lead_generation": {
            "name": "Lead Generation System",
            "description": "Automated lead capture, qualification, and CRM integration",
            "category": "Sales & Marketing",
            "complexity": "Medium",
            "blocks": ["starter", "agent", "api", "output"],
            "customizable": ["company_name", "target_industry", "email_template"]
        },
        "trading_bot": {
            "name": "Crypto Trading Bot",
            "description": "24/7 automated trading with stop-loss and take-profit",
            "category": "Web3 Trading",
            "complexity": "Complex",
            "blocks": ["starter", "api", "agent", "api", "output"],
            "customizable": ["trading_pair", "stop_loss", "take_profit"]
        },
        "multi_agent_research": {
            "name": "Multi-Agent Research Team",
            "description": "Collaborative research with specialist AI agents",
            "category": "Research & Analysis",
            "complexity": "Complex",
            "blocks": ["starter", "agent", "agent", "agent", "agent", "agent", "output"],
            "customizable": ["research_topic", "specialist_areas"]
        },
        "customer_support": {
            "name": "Customer Support Automation",
            "description": "Automated ticket classification and response system",
            "category": "Customer Service",
            "complexity": "Medium",
            "blocks": ["starter", "agent", "agent", "output"],
            "customizable": ["company_name", "support_hours"]
        },
        "web3_automation": {
            "name": "Web3 Automation",
            "description": "Blockchain monitoring and smart contract automation",
            "category": "Web3 & DeFi",
            "complexity": "Complex",
            "blocks": ["starter", "api", "agent", "api"],
            "customizable": ["blockchain", "contract_address"]
        },
        "data_pipeline": {
            "name": "Data Pipeline",
            "description": "Automated data extraction, transformation, and loading",
            "category": "Data Processing",
            "complexity": "Medium",
            "blocks": ["starter", "api", "agent", "api", "output"],
            "customizable": ["data_source", "transformation_rules"]
        },
        "content_generation": {
            "name": "Content Generation",
            "description": "AI-powered content creation and publishing",
            "category": "Content & Media",
            "complexity": "Medium",
            "blocks": ["starter", "agent", "api", "output"],
            "customizable": ["content_type", "publishing_channels"]
        },
        "notification_system": {
            "name": "Notification System",
            "description": "Multi-channel alert and notification system",
            "category": "Communication",
            "complexity": "Simple",
            "blocks": ["starter", "agent", "output"],
            "customizable": ["channels", "alert_conditions"]
        }
    }
    
    for template_name, info in template_info.items():
        templates.append({
            "id": template_name,
            **info
        })
    
    return templates
