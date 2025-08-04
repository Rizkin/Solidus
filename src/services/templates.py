"""
Agent Forge Templates Service
Professional workflow templates for various use cases
"""
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

class TemplateService:
    """Service for managing Agent Forge workflow templates"""
    
    def __init__(self):
        self.templates = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize all available templates"""
        return {
            "lead_generation": {
                "name": "lead_generation",
                "display_name": "Lead Generation System",
                "description": "Capture and qualify leads from multiple sources",
                "category": "Sales & Marketing",
                "tags": ["sales", "marketing", "crm", "automation"],
                "complexity": "Medium",
                "estimated_runtime": "24/7",
                "customizable_fields": ["source", "crm_integration", "qualification_criteria"],
                "template_data": self._get_lead_generation_template()
            },
            "trading_bot": {
                "name": "trading_bot",
                "display_name": "Crypto Trading Bot",
                "description": "Automated trading with stop-loss and take-profit",
                "category": "Web3 Trading",
                "tags": ["trading", "crypto", "automation", "finance"],
                "complexity": "Complex",
                "estimated_runtime": "24/7",
                "customizable_fields": ["trading_pair", "stop_loss", "take_profit", "position_size"],
                "template_data": self._get_trading_bot_template()
            },
            "multi_agent_research": {
                "name": "multi_agent_research",
                "display_name": "Multi-Agent Research Team",
                "description": "Collaborative AI agents for research tasks",
                "category": "AI Automation",
                "tags": ["research", "ai", "collaboration", "analysis"],
                "complexity": "Complex",
                "estimated_runtime": "On-demand",
                "customizable_fields": ["research_topic", "agent_count", "depth_level"],
                "template_data": self._get_multi_agent_template()
            },
            "customer_support": {
                "name": "customer_support",
                "display_name": "Customer Support Automation",
                "description": "Automated ticket classification and response",
                "category": "Customer Service",
                "tags": ["support", "automation", "tickets", "ai"],
                "complexity": "Medium",
                "estimated_runtime": "24/7",
                "customizable_fields": ["channels", "escalation_rules", "response_templates"],
                "template_data": self._get_customer_support_template()
            },
            "web3_automation": {
                "name": "web3_automation",
                "display_name": "Web3 DeFi Automation",
                "description": "Smart contract monitoring and DeFi operations",
                "category": "Blockchain",
                "tags": ["web3", "defi", "blockchain", "smart-contracts"],
                "complexity": "Complex",
                "estimated_runtime": "24/7",
                "customizable_fields": ["chain", "contract_address", "gas_settings"],
                "template_data": self._get_web3_template()
            },
            "data_pipeline": {
                "name": "data_pipeline",
                "display_name": "Data Processing Pipeline",
                "description": "ETL processing and transformation",
                "category": "Data Processing",
                "tags": ["data", "etl", "processing", "automation"],
                "complexity": "Medium",
                "estimated_runtime": "Scheduled",
                "customizable_fields": ["data_source", "transformations", "output_format"],
                "template_data": self._get_data_pipeline_template()
            },
            "content_generation": {
                "name": "content_generation",
                "display_name": "Content Generation System",
                "description": "AI-powered writing and publishing",
                "category": "Content & Media",
                "tags": ["content", "writing", "ai", "publishing"],
                "complexity": "Medium",
                "estimated_runtime": "On-demand",
                "customizable_fields": ["content_type", "tone", "publishing_channels"],
                "template_data": self._get_content_generation_template()
            },
            "notification_system": {
                "name": "notification_system",
                "display_name": "Multi-Channel Notification System",
                "description": "Intelligent alerts across multiple channels",
                "category": "Communication",
                "tags": ["notifications", "alerts", "communication", "multi-channel"],
                "complexity": "Simple",
                "estimated_runtime": "24/7",
                "customizable_fields": ["channels", "alert_rules", "escalation_policy"],
                "template_data": self._get_notification_template()
            }
        }
    
    def get_all_templates(self) -> List[Dict[str, Any]]:
        """Get all available templates"""
        return [
            {
                "name": template["name"],
                "display_name": template["display_name"],
                "description": template["description"],
                "category": template["category"],
                "tags": template["tags"],
                "complexity": template["complexity"],
                "estimated_runtime": template["estimated_runtime"],
                "customizable_fields": template["customizable_fields"]
            }
            for template in self.templates.values()
        ]
    
    def get_template_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get template by name"""
        return self.templates.get(name)
    
    def create_workflow_from_template(self, template: Dict[str, Any], customization: Dict[str, Any]) -> Dict[str, Any]:
        """Create workflow from template with customizations"""
        template_data = template["template_data"].copy()
        
        # Apply customizations
        template_data = self._apply_customizations(template_data, customization, template["name"])
        
        # Generate unique IDs
        workflow_id = str(uuid.uuid4())
        template_data["id"] = workflow_id
        
        # Update metadata
        template_data["created_at"] = datetime.utcnow()
        template_data["updated_at"] = datetime.utcnow()
        template_data["template_source"] = template["name"]
        template_data["customizations"] = customization
        
        return template_data
    
    def _apply_customizations(self, template_data: Dict[str, Any], customization: Dict[str, Any], template_name: str) -> Dict[str, Any]:
        """Apply customizations to template data"""
        
        if template_name == "trading_bot":
            return self._customize_trading_bot(template_data, customization)
        elif template_name == "lead_generation":
            return self._customize_lead_generation(template_data, customization)
        elif template_name == "multi_agent_research":
            return self._customize_multi_agent(template_data, customization)
        elif template_name == "web3_automation":
            return self._customize_web3(template_data, customization)
        else:
            # Generic customization
            variables = template_data.get("state", {}).get("variables", {})
            for key, value in customization.items():
                variables[key.upper()] = value
            
            return template_data
    
    def _customize_trading_bot(self, template_data: Dict[str, Any], customization: Dict[str, Any]) -> Dict[str, Any]:
        """Customize trading bot template"""
        trading_pair = customization.get("trading_pair", "BTC/USDT")
        stop_loss = customization.get("stop_loss", -5)
        take_profit = customization.get("take_profit", 10)
        position_size = customization.get("position_size", 0.01)
        
        # Update name and description
        template_data["name"] = f"Trading Bot - {trading_pair}"
        template_data["description"] = f"Automated trading for {trading_pair} with {stop_loss}% stop-loss"
        
        # Update variables
        variables = template_data["state"]["variables"]
        variables.update({
            "TRADING_PAIR": trading_pair,
            "STOP_LOSS": stop_loss,
            "TAKE_PROFIT": take_profit,
            "POSITION_SIZE": position_size
        })
        
        # Update API block configurations
        blocks = template_data["state"]["blocks"]
        for block in blocks.values():
            if block.get("type") == "api" and "sub_blocks" in block:
                sub_blocks = block["sub_blocks"]
                if "params" in sub_blocks and isinstance(sub_blocks["params"], dict):
                    if "symbol" in sub_blocks["params"]:
                        sub_blocks["params"]["symbol"] = trading_pair.replace("/", "")
        
        return template_data
    
    def _customize_lead_generation(self, template_data: Dict[str, Any], customization: Dict[str, Any]) -> Dict[str, Any]:
        """Customize lead generation template"""
        source = customization.get("source", "website")
        crm_integration = customization.get("crm_integration", "hubspot")
        
        # Update name and description
        template_data["name"] = f"Lead Generation - {source.title()}"
        template_data["description"] = f"Lead capture and qualification from {source}"
        
        # Update variables
        variables = template_data["state"]["variables"]
        variables.update({
            "LEAD_SOURCE": source,
            "CRM_SYSTEM": crm_integration,
            "QUALIFICATION_THRESHOLD": customization.get("qualification_threshold", 7)
        })
        
        return template_data
    
    def _customize_multi_agent(self, template_data: Dict[str, Any], customization: Dict[str, Any]) -> Dict[str, Any]:
        """Customize multi-agent research template"""
        research_topic = customization.get("research_topic", "Market Analysis")
        agent_count = customization.get("agent_count", 3)
        depth_level = customization.get("depth_level", "comprehensive")
        
        # Update name and description
        template_data["name"] = f"Research Team - {research_topic}"
        template_data["description"] = f"Multi-agent research on {research_topic}"
        
        # Update variables
        variables = template_data["state"]["variables"]
        variables.update({
            "RESEARCH_TOPIC": research_topic,
            "AGENT_COUNT": agent_count,
            "RESEARCH_DEPTH": depth_level
        })
        
        return template_data
    
    def _customize_web3(self, template_data: Dict[str, Any], customization: Dict[str, Any]) -> Dict[str, Any]:
        """Customize Web3 automation template"""
        chain = customization.get("chain", "ethereum")
        contract_address = customization.get("contract_address", "0x...")
        
        # Update name and description
        template_data["name"] = f"Web3 Automation - {chain.title()}"
        template_data["description"] = f"Smart contract monitoring on {chain}"
        
        # Update variables
        variables = template_data["state"]["variables"]
        variables.update({
            "BLOCKCHAIN": chain,
            "CONTRACT_ADDRESS": contract_address,
            "GAS_LIMIT": customization.get("gas_limit", 21000)
        })
        
        return template_data
    
    # Template data methods
    def _get_lead_generation_template(self) -> Dict[str, Any]:
        """Lead generation workflow template"""
        return {
            "user_id": "template-user",
            "workspace_id": "template-workspace",
            "name": "Lead Generation System",
            "description": "Automated lead capture and qualification",
            "state": {
                "blocks": {
                    "starter_1": {
                        "id": "starter_1",
                        "type": "starter",
                        "name": "Lead Capture",
                        "position_x": 100,
                        "position_y": 100,
                        "sub_blocks": {
                            "startWorkflow": "webhook",
                            "webhookPath": "/lead-capture"
                        }
                    },
                    "agent_1": {
                        "id": "agent_1",
                        "type": "agent",
                        "name": "Lead Qualifier",
                        "position_x": 300,
                        "position_y": 100,
                        "sub_blocks": {
                            "model": "gpt-4",
                            "systemPrompt": "Qualify leads based on company size, budget, and fit",
                            "temperature": 0.5
                        }
                    },
                    "api_1": {
                        "id": "api_1",
                        "type": "api",
                        "name": "Save to CRM",
                        "position_x": 500,
                        "position_y": 100,
                        "sub_blocks": {
                            "url": "https://api.hubspot.com/contacts/v1/contact",
                            "method": "POST",
                            "headers": {"Authorization": "Bearer {{env.HUBSPOT_TOKEN}}"}
                        }
                    },
                    "output_1": {
                        "id": "output_1",
                        "type": "output",
                        "name": "Notify Sales",
                        "position_x": 700,
                        "position_y": 100,
                        "sub_blocks": {
                            "outputType": "email",
                            "channels": ["sales@company.com"]
                        }
                    }
                },
                "edges": [
                    {"from": "starter_1", "to": "agent_1"},
                    {"from": "agent_1", "to": "api_1"},
                    {"from": "api_1", "to": "output_1"}
                ],
                "subflows": {},
                "variables": {
                    "LEAD_SOURCE": "website",
                    "QUALIFICATION_THRESHOLD": 7,
                    "CRM_SYSTEM": "hubspot"
                },
                "metadata": {
                    "version": "1.0.0",
                    "createdAt": datetime.utcnow().isoformat() + "Z",
                    "updatedAt": datetime.utcnow().isoformat() + "Z"
                }
            },
            "color": "#4ECDC4"
        }
    
    def _get_trading_bot_template(self) -> Dict[str, Any]:
        """Trading bot workflow template"""
        return {
            "user_id": "template-user",
            "workspace_id": "template-workspace",
            "name": "Crypto Trading Bot",
            "description": "Automated cryptocurrency trading with risk management",
            "state": {
                "blocks": {
                    "starter_1": {
                        "id": "starter_1",
                        "type": "starter",
                        "name": "Market Monitor",
                        "position_x": 100,
                        "position_y": 100,
                        "sub_blocks": {
                            "startWorkflow": "schedule",
                            "scheduleType": "interval",
                            "interval": "1m"
                        }
                    },
                    "api_1": {
                        "id": "api_1",
                        "type": "api",
                        "name": "Fetch Price Data",
                        "position_x": 300,
                        "position_y": 100,
                        "sub_blocks": {
                            "url": "https://api.binance.com/api/v3/ticker/price",
                            "method": "GET",
                            "params": {"symbol": "BTCUSDT"}
                        }
                    },
                    "agent_1": {
                        "id": "agent_1",
                        "type": "agent",
                        "name": "Trading Decision",
                        "position_x": 500,
                        "position_y": 100,
                        "sub_blocks": {
                            "model": "gpt-4",
                            "systemPrompt": "Analyze market data and make trading decisions",
                            "temperature": 0.3
                        }
                    },
                    "api_2": {
                        "id": "api_2",
                        "type": "api",
                        "name": "Execute Trade",
                        "position_x": 700,
                        "position_y": 100,
                        "sub_blocks": {
                            "url": "https://api.binance.com/api/v3/order",
                            "method": "POST",
                            "headers": {"X-MBX-APIKEY": "{{env.BINANCE_API_KEY}}"}
                        }
                    }
                },
                "edges": [
                    {"from": "starter_1", "to": "api_1"},
                    {"from": "api_1", "to": "agent_1"},
                    {"from": "agent_1", "to": "api_2"}
                ],
                "subflows": {},
                "variables": {
                    "TRADING_PAIR": "BTC/USDT",
                    "STOP_LOSS": -5,
                    "TAKE_PROFIT": 10,
                    "POSITION_SIZE": 0.01
                },
                "metadata": {
                    "version": "1.0.0",
                    "createdAt": datetime.utcnow().isoformat() + "Z",
                    "updatedAt": datetime.utcnow().isoformat() + "Z"
                }
            },
            "color": "#FF6B6B"
        }
    
    def _get_multi_agent_template(self) -> Dict[str, Any]:
        """Multi-agent research template"""
        return {
            "user_id": "template-user",
            "workspace_id": "template-workspace",
            "name": "Multi-Agent Research Team",
            "description": "Collaborative AI agents for comprehensive research",
            "state": {
                "blocks": {
                    "starter_1": {
                        "id": "starter_1",
                        "type": "starter",
                        "name": "Research Request",
                        "position_x": 100,
                        "position_y": 200,
                        "sub_blocks": {
                            "startWorkflow": "manual"
                        }
                    },
                    "agent_1": {
                        "id": "agent_1",
                        "type": "agent",
                        "name": "Research Coordinator",
                        "position_x": 300,
                        "position_y": 200,
                        "sub_blocks": {
                            "model": "gpt-4",
                            "systemPrompt": "Coordinate research tasks among specialized agents",
                            "temperature": 0.6
                        }
                    },
                    "agent_2": {
                        "id": "agent_2",
                        "type": "agent",
                        "name": "Data Researcher",
                        "position_x": 500,
                        "position_y": 100,
                        "sub_blocks": {
                            "model": "claude-3-sonnet",
                            "systemPrompt": "Gather and analyze quantitative data",
                            "temperature": 0.4
                        }
                    },
                    "agent_3": {
                        "id": "agent_3",
                        "type": "agent",
                        "name": "Trend Analyst",
                        "position_x": 500,
                        "position_y": 300,
                        "sub_blocks": {
                            "model": "gemini-pro",
                            "systemPrompt": "Identify trends and patterns",
                            "temperature": 0.5
                        }
                    },
                    "agent_4": {
                        "id": "agent_4",
                        "type": "agent",
                        "name": "Report Writer",
                        "position_x": 700,
                        "position_y": 200,
                        "sub_blocks": {
                            "model": "gpt-4",
                            "systemPrompt": "Synthesize findings into comprehensive report",
                            "temperature": 0.3
                        }
                    }
                },
                "edges": [
                    {"from": "starter_1", "to": "agent_1"},
                    {"from": "agent_1", "to": "agent_2"},
                    {"from": "agent_1", "to": "agent_3"},
                    {"from": "agent_2", "to": "agent_4"},
                    {"from": "agent_3", "to": "agent_4"}
                ],
                "subflows": {},
                "variables": {
                    "RESEARCH_TOPIC": "Market Analysis",
                    "RESEARCH_DEPTH": "comprehensive",
                    "OUTPUT_FORMAT": "markdown"
                },
                "metadata": {
                    "version": "1.0.0",
                    "createdAt": datetime.utcnow().isoformat() + "Z",
                    "updatedAt": datetime.utcnow().isoformat() + "Z"
                }
            },
            "color": "#9B59B6"
        }
    
    def _get_customer_support_template(self) -> Dict[str, Any]:
        """Customer support automation template"""
        return {
            "user_id": "template-user",
            "workspace_id": "template-workspace",
            "name": "Customer Support Automation",
            "description": "Automated ticket classification and response",
            "state": {
                "blocks": {
                    "starter_1": {
                        "id": "starter_1",
                        "type": "starter",
                        "name": "Ticket Received",
                        "position_x": 100,
                        "position_y": 100,
                        "sub_blocks": {
                            "startWorkflow": "webhook",
                            "webhookPath": "/support-ticket"
                        }
                    },
                    "agent_1": {
                        "id": "agent_1",
                        "type": "agent",
                        "name": "Ticket Classifier",
                        "position_x": 300,
                        "position_y": 100,
                        "sub_blocks": {
                            "model": "gpt-4",
                            "systemPrompt": "Classify support tickets by category and urgency",
                            "temperature": 0.3
                        }
                    },
                    "agent_2": {
                        "id": "agent_2",
                        "type": "agent",
                        "name": "Response Generator",
                        "position_x": 500,
                        "position_y": 100,
                        "sub_blocks": {
                            "model": "gpt-4",
                            "systemPrompt": "Generate helpful responses to customer inquiries",
                            "temperature": 0.5
                        }
                    },
                    "output_1": {
                        "id": "output_1",
                        "type": "output",
                        "name": "Send Response",
                        "position_x": 700,
                        "position_y": 100,
                        "sub_blocks": {
                            "outputType": "email",
                            "template": "support_response"
                        }
                    }
                },
                "edges": [
                    {"from": "starter_1", "to": "agent_1"},
                    {"from": "agent_1", "to": "agent_2"},
                    {"from": "agent_2", "to": "output_1"}
                ],
                "subflows": {},
                "variables": {
                    "ESCALATION_THRESHOLD": 8,
                    "RESPONSE_TIME_SLA": "2h",
                    "SUPPORT_EMAIL": "support@company.com"
                },
                "metadata": {
                    "version": "1.0.0",
                    "createdAt": datetime.utcnow().isoformat() + "Z",
                    "updatedAt": datetime.utcnow().isoformat() + "Z"
                }
            },
            "color": "#3498DB"
        }
    
    def _get_web3_template(self) -> Dict[str, Any]:
        """Web3 automation template"""
        return {
            "user_id": "template-user",
            "workspace_id": "template-workspace",
            "name": "Web3 DeFi Automation",
            "description": "Smart contract monitoring and DeFi operations",
            "state": {
                "blocks": {
                    "starter_1": {
                        "id": "starter_1",
                        "type": "starter",
                        "name": "Blockchain Monitor",
                        "position_x": 100,
                        "position_y": 100,
                        "sub_blocks": {
                            "startWorkflow": "schedule",
                            "scheduleType": "interval",
                            "interval": "5m"
                        }
                    },
                    "api_1": {
                        "id": "api_1",
                        "type": "api",
                        "name": "Check Events",
                        "position_x": 300,
                        "position_y": 100,
                        "sub_blocks": {
                            "url": "https://api.etherscan.io/api",
                            "method": "GET",
                            "params": {"module": "logs", "action": "getLogs"}
                        }
                    },
                    "agent_1": {
                        "id": "agent_1",
                        "type": "agent",
                        "name": "Event Analyzer",
                        "position_x": 500,
                        "position_y": 100,
                        "sub_blocks": {
                            "model": "gpt-4",
                            "systemPrompt": "Analyze blockchain events and determine actions",
                            "temperature": 0.2
                        }
                    },
                    "tool_1": {
                        "id": "tool_1",
                        "type": "tool",
                        "name": "Execute Transaction",
                        "position_x": 700,
                        "position_y": 100,
                        "sub_blocks": {
                            "toolType": "web3",
                            "network": "ethereum"
                        }
                    }
                },
                "edges": [
                    {"from": "starter_1", "to": "api_1"},
                    {"from": "api_1", "to": "agent_1"},
                    {"from": "agent_1", "to": "tool_1"}
                ],
                "subflows": {},
                "variables": {
                    "CONTRACT_ADDRESS": "0x...",
                    "NETWORK": "ethereum",
                    "GAS_LIMIT": 21000
                },
                "metadata": {
                    "version": "1.0.0",
                    "createdAt": datetime.utcnow().isoformat() + "Z",
                    "updatedAt": datetime.utcnow().isoformat() + "Z"
                }
            },
            "color": "#E67E22"
        }
    
    def _get_data_pipeline_template(self) -> Dict[str, Any]:
        """Data processing pipeline template"""
        return {
            "user_id": "template-user",
            "workspace_id": "template-workspace",
            "name": "Data Processing Pipeline",
            "description": "ETL processing and transformation",
            "state": {
                "blocks": {
                    "starter_1": {
                        "id": "starter_1",
                        "type": "starter",
                        "name": "Data Trigger",
                        "position_x": 100,
                        "position_y": 100,
                        "sub_blocks": {
                            "startWorkflow": "schedule",
                            "scheduleType": "daily",
                            "time": "02:00"
                        }
                    },
                    "api_1": {
                        "id": "api_1",
                        "type": "api",
                        "name": "Extract Data",
                        "position_x": 300,
                        "position_y": 100,
                        "sub_blocks": {
                            "url": "https://api.datasource.com/data",
                            "method": "GET"
                        }
                    },
                    "agent_1": {
                        "id": "agent_1",
                        "type": "agent",
                        "name": "Data Transformer",
                        "position_x": 500,
                        "position_y": 100,
                        "sub_blocks": {
                            "model": "gpt-4",
                            "systemPrompt": "Transform and clean data according to schema",
                            "temperature": 0.1
                        }
                    },
                    "api_2": {
                        "id": "api_2",
                        "type": "api",
                        "name": "Load Data",
                        "position_x": 700,
                        "position_y": 100,
                        "sub_blocks": {
                            "url": "https://api.datawarehouse.com/load",
                            "method": "POST"
                        }
                    }
                },
                "edges": [
                    {"from": "starter_1", "to": "api_1"},
                    {"from": "api_1", "to": "agent_1"},
                    {"from": "agent_1", "to": "api_2"}
                ],
                "subflows": {},
                "variables": {
                    "DATA_SOURCE": "api",
                    "OUTPUT_FORMAT": "json",
                    "BATCH_SIZE": 1000
                },
                "metadata": {
                    "version": "1.0.0",
                    "createdAt": datetime.utcnow().isoformat() + "Z",
                    "updatedAt": datetime.utcnow().isoformat() + "Z"
                }
            },
            "color": "#2ECC71"
        }
    
    def _get_content_generation_template(self) -> Dict[str, Any]:
        """Content generation template"""
        return {
            "user_id": "template-user",
            "workspace_id": "template-workspace",
            "name": "Content Generation System",
            "description": "AI-powered writing and publishing",
            "state": {
                "blocks": {
                    "starter_1": {
                        "id": "starter_1",
                        "type": "starter",
                        "name": "Content Request",
                        "position_x": 100,
                        "position_y": 100,
                        "sub_blocks": {
                            "startWorkflow": "manual"
                        }
                    },
                    "agent_1": {
                        "id": "agent_1",
                        "type": "agent",
                        "name": "Content Writer",
                        "position_x": 300,
                        "position_y": 100,
                        "sub_blocks": {
                            "model": "gpt-4",
                            "systemPrompt": "Create engaging content based on requirements",
                            "temperature": 0.7
                        }
                    },
                    "agent_2": {
                        "id": "agent_2",
                        "type": "agent",
                        "name": "Content Editor",
                        "position_x": 500,
                        "position_y": 100,
                        "sub_blocks": {
                            "model": "claude-3-sonnet",
                            "systemPrompt": "Review and improve content quality",
                            "temperature": 0.3
                        }
                    },
                    "api_1": {
                        "id": "api_1",
                        "type": "api",
                        "name": "Publish Content",
                        "position_x": 700,
                        "position_y": 100,
                        "sub_blocks": {
                            "url": "https://api.cms.com/publish",
                            "method": "POST"
                        }
                    }
                },
                "edges": [
                    {"from": "starter_1", "to": "agent_1"},
                    {"from": "agent_1", "to": "agent_2"},
                    {"from": "agent_2", "to": "api_1"}
                ],
                "subflows": {},
                "variables": {
                    "CONTENT_TYPE": "blog_post",
                    "TONE": "professional",
                    "TARGET_LENGTH": 1000
                },
                "metadata": {
                    "version": "1.0.0",
                    "createdAt": datetime.utcnow().isoformat() + "Z",
                    "updatedAt": datetime.utcnow().isoformat() + "Z"
                }
            },
            "color": "#F39C12"
        }
    
    def _get_notification_template(self) -> Dict[str, Any]:
        """Notification system template"""
        return {
            "user_id": "template-user",
            "workspace_id": "template-workspace",
            "name": "Multi-Channel Notification System",
            "description": "Intelligent alerts across multiple channels",
            "state": {
                "blocks": {
                    "starter_1": {
                        "id": "starter_1",
                        "type": "starter",
                        "name": "Alert Trigger",
                        "position_x": 100,
                        "position_y": 100,
                        "sub_blocks": {
                            "startWorkflow": "webhook",
                            "webhookPath": "/alert"
                        }
                    },
                    "agent_1": {
                        "id": "agent_1",
                        "type": "agent",
                        "name": "Alert Processor",
                        "position_x": 300,
                        "position_y": 100,
                        "sub_blocks": {
                            "model": "gpt-4",
                            "systemPrompt": "Process alerts and determine notification priority",
                            "temperature": 0.2
                        }
                    },
                    "output_1": {
                        "id": "output_1",
                        "type": "output",
                        "name": "Email Notification",
                        "position_x": 500,
                        "position_y": 50,
                        "sub_blocks": {
                            "outputType": "email",
                            "channels": ["alerts@company.com"]
                        }
                    },
                    "output_2": {
                        "id": "output_2",
                        "type": "output",
                        "name": "Slack Notification",
                        "position_x": 500,
                        "position_y": 150,
                        "sub_blocks": {
                            "outputType": "webhook",
                            "url": "https://hooks.slack.com/services/..."
                        }
                    }
                },
                "edges": [
                    {"from": "starter_1", "to": "agent_1"},
                    {"from": "agent_1", "to": "output_1"},
                    {"from": "agent_1", "to": "output_2"}
                ],
                "subflows": {},
                "variables": {
                    "ALERT_THRESHOLD": 5,
                    "ESCALATION_TIME": "30m",
                    "CHANNELS": ["email", "slack"]
                },
                "metadata": {
                    "version": "1.0.0",
                    "createdAt": datetime.utcnow().isoformat() + "Z",
                    "updatedAt": datetime.utcnow().isoformat() + "Z"
                }
            },
            "color": "#E74C3C"
        }

# Global instance
def get_all_templates():
    """Get all available templates"""
    service = TemplateService()
    return service.get_all_templates()

def get_template_by_name(name: str):
    """Get template by name"""
    service = TemplateService()
    return service.get_template_by_name(name)

def create_workflow_from_template(template: Dict[str, Any], customization: Dict[str, Any]):
    """Create workflow from template"""
    service = TemplateService()
    return service.create_workflow_from_template(template, customization) 