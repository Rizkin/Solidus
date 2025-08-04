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
                "complexity": "Medium",
                "estimated_runtime": "24/7",
                "customizable_fields": ["channels", "triggers", "message_templates"],
                "template_data": self._get_notification_template()
            },
            "social_media_automation": {
                "name": "social_media_automation",
                "display_name": "Social Media Automation",
                "description": "Automated posting, engagement, and content scheduling",
                "category": "Social Media",
                "tags": ["social", "automation", "content", "scheduling", "engagement"],
                "complexity": "Medium",
                "estimated_runtime": "24/7",
                "customizable_fields": ["platforms", "posting_schedule", "content_types"],
                "template_data": self._get_social_media_template()
            },
            "ecommerce_automation": {
                "name": "ecommerce_automation",
                "display_name": "E-commerce Order Automation",
                "description": "Order processing, inventory management, and customer notifications",
                "category": "E-commerce",
                "tags": ["ecommerce", "orders", "inventory", "automation", "customers"],
                "complexity": "Complex",
                "estimated_runtime": "24/7",
                "customizable_fields": ["store_platform", "payment_gateway", "fulfillment_service"],
                "template_data": self._get_ecommerce_template()
            },
            "hr_recruitment": {
                "name": "hr_recruitment",
                "display_name": "HR Recruitment Automation",
                "description": "Resume screening, candidate evaluation, and interview scheduling",
                "category": "Human Resources",
                "tags": ["hr", "recruitment", "screening", "interviews", "candidates"],
                "complexity": "Complex",
                "estimated_runtime": "On-demand",
                "customizable_fields": ["job_requirements", "screening_criteria", "interview_types"],
                "template_data": self._get_hr_recruitment_template()
            },
            "financial_analysis": {
                "name": "financial_analysis",
                "display_name": "Financial Analysis & Reporting",
                "description": "Automated financial data analysis and report generation",
                "category": "Finance",
                "tags": ["finance", "analysis", "reporting", "data", "insights"],
                "complexity": "Complex",
                "estimated_runtime": "Scheduled",
                "customizable_fields": ["data_sources", "report_frequency", "analysis_metrics"],
                "template_data": self._get_financial_analysis_template()
            },
            "project_management": {
                "name": "project_management",
                "display_name": "Project Management Automation",
                "description": "Task assignment, progress tracking, and team notifications",
                "category": "Project Management",
                "tags": ["projects", "tasks", "team", "tracking", "notifications"],
                "complexity": "Medium",
                "estimated_runtime": "24/7",
                "customizable_fields": ["project_tools", "team_size", "notification_rules"],
                "template_data": self._get_project_management_template()
            }
        }
    
    def get_all_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get all available templates"""
        return self.templates
    
    def get_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific template by name"""
        return self.templates.get(template_name)
    
    def get_templates_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get templates filtered by category"""
        return [
            template for template in self.templates.values()
            if template.get("category") == category
        ]
    
    def get_templates_by_complexity(self, complexity: str) -> List[Dict[str, Any]]:
        """Get templates filtered by complexity"""
        return [
            template for template in self.templates.values()
            if template.get("complexity") == complexity
        ]
    
    def search_templates(self, query: str) -> List[Dict[str, Any]]:
        """Search templates by name, description, or tags"""
        query_lower = query.lower()
        results = []
        
        for template in self.templates.values():
            # Search in name, description, and tags
            searchable_text = (
                template.get("display_name", "").lower() +
                " " + template.get("description", "").lower() +
                " " + " ".join(template.get("tags", [])).lower()
            )
            
            if query_lower in searchable_text:
                results.append(template)
        
        return results

    def _get_lead_generation_template(self) -> Dict[str, Any]:
        """Lead generation workflow template"""
        return {
            "blocks": {
                "starter_1": {
                    "id": "starter_1",
                    "type": "starter",
                    "name": "Lead Capture",
                    "position_x": 100,
                    "position_y": 100,
                    "sub_blocks": {
                        "startWorkflow": "webhook",
                        "webhookPath": "/lead-capture",
                        "method": "POST"
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
                        "systemPrompt": "You are a lead qualification specialist. Analyze incoming leads and score them based on fit and intent.",
                        "temperature": 0.3
                    }
                },
                "api_1": {
                    "id": "api_1",
                    "type": "api",
                    "name": "CRM Integration",
                    "position_x": 500,
                    "position_y": 100,
                    "sub_blocks": {
                        "endpoint": "{{env.CRM_API_ENDPOINT}}",
                        "method": "POST",
                        "headers": {
                            "Authorization": "Bearer {{env.CRM_API_KEY}}"
                        }
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "agent_1"},
                {"from": "agent_1", "to": "api_1"}
            ],
            "variables": {
                "QUALIFICATION_THRESHOLD": 7,
                "CRM_API_ENDPOINT": "https://api.crm.com/leads",
                "LEAD_SOURCE": "website"
            }
        }

    def _get_trading_bot_template(self) -> Dict[str, Any]:
        """Trading bot workflow template"""
        return {
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
                    "name": "Price Feed",
                    "position_x": 300,
                    "position_y": 100,
                    "sub_blocks": {
                        "endpoint": "https://api.binance.com/api/v3/ticker/price",
                        "method": "GET",
                        "params": {
                            "symbol": "{{variables.TRADING_PAIR}}"
                        }
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
                        "systemPrompt": "You are a cryptocurrency trading expert. Analyze price data and make buy/sell decisions based on technical indicators.",
                        "temperature": 0.1
                    }
                },
                "api_2": {
                    "id": "api_2",
                    "type": "api",
                    "name": "Execute Trade",
                    "position_x": 700,
                    "position_y": 100,
                    "sub_blocks": {
                        "endpoint": "{{env.EXCHANGE_API}}/order",
                        "method": "POST",
                        "headers": {
                            "X-API-Key": "{{env.EXCHANGE_API_KEY}}"
                        }
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "api_1"},
                {"from": "api_1", "to": "agent_1"},
                {"from": "agent_1", "to": "api_2"}
            ],
            "variables": {
                "TRADING_PAIR": "BTCUSDT",
                "STOP_LOSS": -5,
                "TAKE_PROFIT": 10,
                "POSITION_SIZE": 0.01
            }
        }

    def _get_multi_agent_template(self) -> Dict[str, Any]:
        """Multi-agent research team template"""
        return {
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
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are a research coordinator. Break down complex research topics into specific tasks for specialist agents.",
                        "temperature": 0.5
                    }
                },
                "agent_2": {
                    "id": "agent_2",
                    "type": "agent",
                    "name": "Data Researcher",
                    "position_x": 300,
                    "position_y": 200,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are a data research specialist. Find and analyze quantitative data and statistics.",
                        "temperature": 0.3
                    }
                },
                "agent_3": {
                    "id": "agent_3",
                    "type": "agent",
                    "name": "Content Analyst",
                    "position_x": 300,
                    "position_y": 300,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are a content analysis expert. Review and synthesize information from multiple sources.",
                        "temperature": 0.4
                    }
                },
                "agent_4": {
                    "id": "agent_4",
                    "type": "agent",
                    "name": "Report Generator",
                    "position_x": 500,
                    "position_y": 200,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are a report writing specialist. Compile research findings into comprehensive, well-structured reports.",
                        "temperature": 0.6
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
            "variables": {
                "RESEARCH_TOPIC": "AI Market Trends",
                "DEPTH_LEVEL": "comprehensive",
                "OUTPUT_FORMAT": "executive_summary"
            }
        }

    def _get_customer_support_template(self) -> Dict[str, Any]:
        """Customer support automation template"""
        return {
            "blocks": {
                "starter_1": {
                    "id": "starter_1",
                    "type": "starter",
                    "name": "Ticket Received",
                    "position_x": 100,
                    "position_y": 100,
                    "sub_blocks": {
                        "startWorkflow": "webhook",
                        "webhookPath": "/support-ticket",
                        "method": "POST"
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
                        "systemPrompt": "You are a customer support specialist. Classify support tickets by urgency, category, and required expertise.",
                        "temperature": 0.2
                    }
                },
                "agent_2": {
                    "id": "agent_2",
                    "type": "agent",
                    "name": "Auto Responder",
                    "position_x": 500,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are a helpful customer support agent. Provide helpful, empathetic responses to customer inquiries.",
                        "temperature": 0.7
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
            "variables": {
                "ESCALATION_THRESHOLD": "high",
                "AUTO_RESPONSE_ENABLED": True,
                "BUSINESS_HOURS": "9-17"
            }
        }

    def _get_web3_template(self) -> Dict[str, Any]:
        """Web3 DeFi automation template"""
        return {
            "blocks": {
                "starter_1": {
                    "id": "starter_1",
                    "type": "starter",
                    "name": "Contract Monitor",
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
                    "name": "Blockchain Query",
                    "position_x": 300,
                    "position_y": 100,
                    "sub_blocks": {
                        "endpoint": "{{env.WEB3_RPC_URL}}",
                        "method": "POST",
                        "headers": {
                            "Content-Type": "application/json"
                        }
                    }
                },
                "agent_1": {
                    "id": "agent_1",
                    "type": "agent",
                    "name": "DeFi Analyst",
                    "position_x": 500,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are a DeFi protocol expert. Analyze smart contract data and identify opportunities or risks.",
                        "temperature": 0.3
                    }
                },
                "tool_1": {
                    "id": "tool_1",
                    "type": "tool",
                    "name": "Transaction Builder",
                    "position_x": 700,
                    "position_y": 100,
                    "sub_blocks": {
                        "toolType": "web3_transaction",
                        "gasSettings": "auto"
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "api_1"},
                {"from": "api_1", "to": "agent_1"},
                {"from": "agent_1", "to": "tool_1"}
            ],
            "variables": {
                "CONTRACT_ADDRESS": "0x...",
                "CHAIN_ID": 1,
                "GAS_LIMIT": 200000,
                "SLIPPAGE_TOLERANCE": 0.5
            }
        }

    def _get_data_pipeline_template(self) -> Dict[str, Any]:
        """Data processing pipeline template"""
        return {
            "blocks": {
                "starter_1": {
                    "id": "starter_1",
                    "type": "starter",
                    "name": "Data Ingestion",
                    "position_x": 100,
                    "position_y": 100,
                    "sub_blocks": {
                        "startWorkflow": "schedule",
                        "scheduleType": "cron",
                        "cronExpression": "0 0 * * *"
                    }
                },
                "api_1": {
                    "id": "api_1",
                    "type": "api",
                    "name": "Data Source",
                    "position_x": 300,
                    "position_y": 100,
                    "sub_blocks": {
                        "endpoint": "{{variables.DATA_SOURCE_URL}}",
                        "method": "GET",
                        "headers": {
                            "Authorization": "Bearer {{env.DATA_API_KEY}}"
                        }
                    }
                },
                "tool_1": {
                    "id": "tool_1",
                    "type": "tool",
                    "name": "Data Transformer",
                    "position_x": 500,
                    "position_y": 100,
                    "sub_blocks": {
                        "toolType": "data_transform",
                        "transformations": ["clean", "normalize", "aggregate"]
                    }
                },
                "output_1": {
                    "id": "output_1",
                    "type": "output",
                    "name": "Data Export",
                    "position_x": 700,
                    "position_y": 100,
                    "sub_blocks": {
                        "outputType": "database",
                        "destination": "{{env.OUTPUT_DB_URL}}"
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "api_1"},
                {"from": "api_1", "to": "tool_1"},
                {"from": "tool_1", "to": "output_1"}
            ],
            "variables": {
                "DATA_SOURCE_URL": "https://api.example.com/data",
                "BATCH_SIZE": 1000,
                "OUTPUT_FORMAT": "parquet"
            }
        }

    def _get_content_generation_template(self) -> Dict[str, Any]:
        """Content generation system template"""
        return {
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
                    "name": "Content Planner",
                    "position_x": 300,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are a content strategist. Create detailed content plans and outlines based on topics and requirements.",
                        "temperature": 0.7
                    }
                },
                "agent_2": {
                    "id": "agent_2",
                    "type": "agent",
                    "name": "Content Writer",
                    "position_x": 500,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are a professional content writer. Create engaging, well-structured content based on provided outlines.",
                        "temperature": 0.8
                    }
                },
                "agent_3": {
                    "id": "agent_3",
                    "type": "agent",
                    "name": "Content Editor",
                    "position_x": 700,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are an expert editor. Review and refine content for clarity, engagement, and brand consistency.",
                        "temperature": 0.4
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "agent_1"},
                {"from": "agent_1", "to": "agent_2"},
                {"from": "agent_2", "to": "agent_3"}
            ],
            "variables": {
                "CONTENT_TYPE": "blog_post",
                "TARGET_AUDIENCE": "professionals",
                "TONE": "informative",
                "WORD_COUNT": 1500
            }
        }

    def _get_notification_template(self) -> Dict[str, Any]:
        """Multi-channel notification system template"""
        return {
            "blocks": {
                "starter_1": {
                    "id": "starter_1",
                    "type": "starter",
                    "name": "Alert Trigger",
                    "position_x": 100,
                    "position_y": 150,
                    "sub_blocks": {
                        "startWorkflow": "webhook",
                        "webhookPath": "/alert",
                        "method": "POST"
                    }
                },
                "agent_1": {
                    "id": "agent_1",
                    "type": "agent",
                    "name": "Message Composer",
                    "position_x": 300,
                    "position_y": 150,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are a communication specialist. Create appropriate messages for different channels and audiences.",
                        "temperature": 0.6
                    }
                },
                "output_1": {
                    "id": "output_1",
                    "type": "output",
                    "name": "Email Notification",
                    "position_x": 500,
                    "position_y": 100,
                    "sub_blocks": {
                        "outputType": "email",
                        "template": "alert_email"
                    }
                },
                "output_2": {
                    "id": "output_2",
                    "type": "output",
                    "name": "Slack Notification",
                    "position_x": 500,
                    "position_y": 200,
                    "sub_blocks": {
                        "outputType": "slack",
                        "channel": "{{variables.SLACK_CHANNEL}}"
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "agent_1"},
                {"from": "agent_1", "to": "output_1"},
                {"from": "agent_1", "to": "output_2"}
            ],
            "variables": {
                "ALERT_THRESHOLD": "high",
                "SLACK_CHANNEL": "#alerts",
                "EMAIL_RECIPIENTS": ["admin@company.com"]
            }
        }

    def _get_social_media_template(self) -> Dict[str, Any]:
        """Social media automation template"""
        return {
            "blocks": {
                "starter_1": {
                    "id": "starter_1",
                    "type": "starter",
                    "name": "Content Scheduler",
                    "position_x": 100,
                    "position_y": 100,
                    "sub_blocks": {
                        "startWorkflow": "schedule",
                        "scheduleType": "interval",
                        "interval": "2h"
                    }
                },
                "agent_1": {
                    "id": "agent_1",
                    "type": "agent",
                    "name": "Content Creator",
                    "position_x": 300,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are a social media content creator. Create engaging posts for different platforms with appropriate hashtags and timing.",
                        "temperature": 0.8
                    }
                },
                "api_1": {
                    "id": "api_1",
                    "type": "api",
                    "name": "Social Media Publisher",
                    "position_x": 500,
                    "position_y": 100,
                    "sub_blocks": {
                        "endpoint": "{{variables.SOCIAL_API_ENDPOINT}}",
                        "method": "POST",
                        "headers": {
                            "Authorization": "Bearer {{env.SOCIAL_API_KEY}}"
                        }
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "agent_1"},
                {"from": "agent_1", "to": "api_1"}
            ],
            "variables": {
                "PLATFORMS": "twitter,linkedin,instagram",
                "POSTING_SCHEDULE": "morning,afternoon,evening",
                "CONTENT_TYPES": "text,image,video"
            }
        }

    def _get_ecommerce_template(self) -> Dict[str, Any]:
        """E-commerce automation template"""
        return {
            "blocks": {
                "starter_1": {
                    "id": "starter_1",
                    "type": "starter",
                    "name": "Order Webhook",
                    "position_x": 100,
                    "position_y": 100,
                    "sub_blocks": {
                        "startWorkflow": "webhook",
                        "webhookPath": "/order-received",
                        "method": "POST"
                    }
                },
                "agent_1": {
                    "id": "agent_1",
                    "type": "agent",
                    "name": "Order Processor",
                    "position_x": 300,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are an e-commerce order processor. Validate orders, check inventory, and process payments.",
                        "temperature": 0.3
                    }
                },
                "api_1": {
                    "id": "api_1",
                    "type": "api",
                    "name": "Inventory System",
                    "position_x": 500,
                    "position_y": 100,
                    "sub_blocks": {
                        "endpoint": "{{variables.INVENTORY_API}}",
                        "method": "PUT",
                        "headers": {
                            "Authorization": "Bearer {{env.INVENTORY_TOKEN}}"
                        }
                    }
                },
                "output_1": {
                    "id": "output_1",
                    "type": "output",
                    "name": "Customer Notification",
                    "position_x": 700,
                    "position_y": 100,
                    "sub_blocks": {
                        "outputType": "email",
                        "template": "order_confirmation"
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "agent_1"},
                {"from": "agent_1", "to": "api_1"},
                {"from": "api_1", "to": "output_1"}
            ],
            "variables": {
                "STORE_PLATFORM": "shopify",
                "PAYMENT_GATEWAY": "stripe",
                "FULFILLMENT_SERVICE": "auto"
            }
        }

    def _get_hr_recruitment_template(self) -> Dict[str, Any]:
        """HR recruitment template"""
        return {
            "blocks": {
                "starter_1": {
                    "id": "starter_1",
                    "type": "starter",
                    "name": "Resume Upload",
                    "position_x": 100,
                    "position_y": 100,
                    "sub_blocks": {
                        "startWorkflow": "webhook",
                        "webhookPath": "/resume-upload",
                        "method": "POST"
                    }
                },
                "agent_1": {
                    "id": "agent_1",
                    "type": "agent",
                    "name": "Resume Screener",
                    "position_x": 300,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are an expert HR recruiter. Screen resumes for job requirements and rank candidates.",
                        "temperature": 0.4
                    }
                },
                "agent_2": {
                    "id": "agent_2",
                    "type": "agent",
                    "name": "Interview Scheduler",
                    "position_x": 500,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are an interview coordinator. Schedule interviews and send calendar invites.",
                        "temperature": 0.5
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "agent_1"},
                {"from": "agent_1", "to": "agent_2"}
            ],
            "variables": {
                "JOB_REQUIREMENTS": "Python, AI, 3+ years",
                "SCREENING_CRITERIA": "technical_skills,experience,cultural_fit",
                "INTERVIEW_TYPES": "technical,behavioral"
            }
        }

    def _get_financial_analysis_template(self) -> Dict[str, Any]:
        """Financial analysis template"""
        return {
            "blocks": {
                "starter_1": {
                    "id": "starter_1",
                    "type": "starter",
                    "name": "Market Data Monitor",
                    "position_x": 100,
                    "position_y": 100,
                    "sub_blocks": {
                        "startWorkflow": "schedule",
                        "scheduleType": "cron",
                        "cronExpression": "0 9 * * 1-5"
                    }
                },
                "api_1": {
                    "id": "api_1",
                    "type": "api",
                    "name": "Financial Data API",
                    "position_x": 300,
                    "position_y": 100,
                    "sub_blocks": {
                        "endpoint": "{{variables.FINANCIAL_API_URL}}",
                        "method": "GET",
                        "headers": {
                            "X-API-KEY": "{{env.FINANCIAL_API_KEY}}"
                        }
                    }
                },
                "agent_1": {
                    "id": "agent_1",
                    "type": "agent",
                    "name": "Financial Analyst",
                    "position_x": 500,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are a financial analyst. Analyze market data, identify trends, and provide investment insights.",
                        "temperature": 0.3
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "api_1"},
                {"from": "api_1", "to": "agent_1"}
            ],
            "variables": {
                "FINANCIAL_API_URL": "https://api.marketdata.com/v1/stocks",
                "ANALYSIS_METRICS": "revenue,profit,growth,volatility",
                "REPORT_FREQUENCY": "daily"
            }
        }

    def _get_project_management_template(self) -> Dict[str, Any]:
        """Project management template"""
        return {
            "blocks": {
                "starter_1": {
                    "id": "starter_1",
                    "type": "starter",
                    "name": "Task Creation",
                    "position_x": 100,
                    "position_y": 100,
                    "sub_blocks": {
                        "startWorkflow": "webhook",
                        "webhookPath": "/task-created",
                        "method": "POST"
                    }
                },
                "agent_1": {
                    "id": "agent_1",
                    "type": "agent",
                    "name": "Task Manager",
                    "position_x": 300,
                    "position_y": 100,
                    "sub_blocks": {
                        "model": "gpt-4",
                        "systemPrompt": "You are a project manager. Assign tasks, set priorities, and track progress.",
                        "temperature": 0.5
                    }
                },
                "api_1": {
                    "id": "api_1",
                    "type": "api",
                    "name": "Project Management Tool",
                    "position_x": 500,
                    "position_y": 100,
                    "sub_blocks": {
                        "endpoint": "{{variables.PROJECT_API_URL}}",
                        "method": "POST",
                        "headers": {
                            "Authorization": "Bearer {{env.PROJECT_TOKEN}}"
                        }
                    }
                },
                "output_1": {
                    "id": "output_1",
                    "type": "output",
                    "name": "Team Notification",
                    "position_x": 700,
                    "position_y": 100,
                    "sub_blocks": {
                        "outputType": "slack",
                        "channel": "{{variables.TEAM_CHANNEL}}"
                    }
                }
            },
            "edges": [
                {"from": "starter_1", "to": "agent_1"},
                {"from": "agent_1", "to": "api_1"},
                {"from": "api_1", "to": "output_1"}
            ],
            "variables": {
                "PROJECT_TOOLS": "jira",
                "TEAM_CHANNEL": "#development",
                "NOTIFICATION_RULES": "task_assigned,deadline_reminder"
            }
        }

# Create singleton instance
template_service = TemplateService()

# Module-level functions for API compatibility
# Fixed: Template import functions for Vercel deployment
def get_all_templates() -> Dict[str, Dict[str, Any]]:
    """Get all available templates - module-level function for API compatibility"""
    return template_service.get_all_templates()

def get_template_by_name(template_name: str) -> Optional[Dict[str, Any]]:
    """Get a specific template by name - module-level function for API compatibility"""
    return template_service.get_template(template_name)

def create_workflow_from_template(template: Dict[str, Any], customization: Dict[str, Any]) -> Dict[str, Any]:
    """Create a workflow from a template - module-level function for API compatibility"""
    if not template:
        raise ValueError("Template not found")
    
    template_name = template.get("name")
    if not template_name:
        raise ValueError("Template name not specified")
    
    # Generate workflow ID
    workflow_id = str(uuid.uuid4())
    
    # Get template data
    template_data = template.get("template_data", {})
    
    # Merge default variables with customization
    default_variables = template_data.get("variables", {})
    merged_variables = {**default_variables, **customization}
    
    # Create the workflow structure
    workflow = {
        "id": workflow_id,
        "user_id": "template-user",
        "workspace_id": "template-workspace", 
        "name": template.get("display_name", template_name),
        "description": template.get("description", ""),
        "state": {
            "blocks": template_data.get("blocks", {}),
            "edges": template_data.get("edges", []),
            "subflows": {},
            "variables": merged_variables,
            "metadata": {
                "version": "1.0.0",
                "template": template_name,
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z"
            }
        },
        "color": template.get("color", "#3972F6"),
        "is_published": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    return workflow 