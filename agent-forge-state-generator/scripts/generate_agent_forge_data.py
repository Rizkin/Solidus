#!/usr/bin/env python3
# scripts/generate_agent_forge_data.py
import json
import random
import sys
import os
from uuid import uuid4
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

class AgentForgeSyntheticData:
    """Generate realistic Agent Forge workflow data for testing and demos"""
    
    def __init__(self):
        self.models = ["gpt-4", "claude-3", "gemini-pro", "custom-byoi", "gpt-3.5-turbo"]
        self.integrations = ["coingecko", "coinmarketcap", "slack", "email", "sms", "discord", "telegram"]
        self.companies = ["TechCorp", "DataFlow Inc", "AI Solutions", "CryptoTrader", "AutoBot Systems"]
        self.colors = ["#3972F6", "#15803D", "#DC2626", "#7C2D12", "#1E40AF", "#BE185D"]
        
    def generate_all_workflows(self) -> list:
        """Generate 15 diverse Agent Forge workflows"""
        workflows = []
        
        print("🚀 Generating Agent Forge synthetic workflows...")
        
        # Simple workflows (5)
        print("📝 Creating simple workflows...")
        workflows.extend([
            self.create_lead_capture_workflow(),
            self.create_scheduled_report_workflow(),
            self.create_webhook_handler_workflow(),
            self.create_data_fetch_workflow(),
            self.create_notification_workflow()
        ])
        
        # Medium complexity (5)
        print("⚙️ Creating medium complexity workflows...")
        workflows.extend([
            self.create_marketing_automation_workflow(),
            self.create_customer_support_workflow(),
            self.create_trading_bot_workflow(),
            self.create_content_generator_workflow(),
            self.create_real_estate_workflow()
        ])
        
        # Complex multi-agent (5)
        print("🤖 Creating complex multi-agent workflows...")
        workflows.extend([
            self.create_multi_agent_research_workflow(),
            self.create_web3_defi_workflow(),
            self.create_enterprise_automation_workflow(),
            self.create_ai_team_workflow(),
            self.create_marketplace_aggregator_workflow()
        ])
        
        print(f"✅ Generated {len(workflows)} workflows successfully!")
        return workflows
    
    def create_trading_bot_workflow(self) -> dict:
        """Create a comprehensive Web3 trading bot workflow"""
        workflow_id = str(uuid4())
        
        blocks = []
        
        # Starter block - Market Monitor
        starter_block = self._create_block(
            workflow_id=workflow_id,
            type="starter",
            name="Market Monitor",
            position=(100, 200),
            sub_blocks={
                "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"},
                "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "minutes"},
                "minutesInterval": {"id": "minutesInterval", "type": "short-input", "value": "5"},
                "timezone": {"id": "timezone", "type": "dropdown", "value": "UTC"}
            }
        )
        blocks.append(starter_block)
        
        # API block - CoinGecko Data
        api_block = self._create_block(
            workflow_id=workflow_id,
            type="api",
            name="CoinGecko Price Data",
            position=(300, 200),
            sub_blocks={
                "url": {"id": "url", "type": "short-input", "value": "https://api.coingecko.com/api/v3/simple/price"},
                "method": {"id": "method", "type": "dropdown", "value": "GET"},
                "params": {"id": "params", "type": "table", "value": [
                    {"id": str(uuid4()), "cells": {"Key": "ids", "Value": "bitcoin,ethereum,solana"}},
                    {"id": str(uuid4()), "cells": {"Key": "vs_currencies", "Value": "usd"}},
                    {"id": str(uuid4()), "cells": {"Key": "include_24hr_change", "Value": "true"}}
                ]},
                "headers": {"id": "headers", "type": "table", "value": [
                    {"id": str(uuid4()), "cells": {"Key": "Accept", "Value": "application/json"}}
                ]}
            }
        )
        blocks.append(api_block)
        
        # Agent block - Trading Decision Agent
        agent_block = self._create_block(
            workflow_id=workflow_id,
            type="agent",
            name="Trading Decision Agent",
            position=(500, 200),
            sub_blocks={
                "model": {"id": "model", "type": "combobox", "value": "gpt-4"},
                "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                               "value": "You are a professional crypto trading agent. Analyze market data and make trading decisions based on: 1) Stop-loss at -5% 2) Take-profit at +10% 3) RSI indicators 4) Volume analysis 5) 24h price change. Respond with clear BUY/SELL/HOLD decisions and reasoning."},
                "temperature": {"id": "temperature", "type": "slider", "value": 0.3},
                "tools": {"id": "tools", "type": "tool-input", "value": [
                    {"type": "market_analysis", "title": "Market Analysis", "enabled": True},
                    {"type": "risk_calculator", "title": "Risk Calculator", "enabled": True},
                    {"type": "technical_indicators", "title": "Technical Indicators", "enabled": True}
                ]}
            }
        )
        blocks.append(agent_block)
        
        # API block - Execute Trade
        execution_block = self._create_block(
            workflow_id=workflow_id,
            type="api",
            name="Execute Trade Order",
            position=(700, 200),
            sub_blocks={
                "url": {"id": "url", "type": "short-input", "value": "https://api.binance.com/api/v3/order"},
                "method": {"id": "method", "type": "dropdown", "value": "POST"},
                "headers": {"id": "headers", "type": "table", "value": [
                    {"id": str(uuid4()), "cells": {"Key": "X-MBX-APIKEY", "Value": "{{BINANCE_API_KEY}}"}},
                    {"id": str(uuid4()), "cells": {"Key": "Content-Type", "Value": "application/json"}}
                ]},
                "body": {"id": "body", "type": "code", "value": '{\n  "symbol": "{{TRADING_PAIR}}",\n  "side": "{{TRADE_SIDE}}",\n  "type": "MARKET",\n  "quantity": "{{TRADE_AMOUNT}}"\n}'}
            }
        )
        blocks.append(execution_block)
        
        # Output block - Trade Notification
        output_block = self._create_block(
            workflow_id=workflow_id,
            type="output",
            name="Trade Notification",
            position=(900, 200),
            sub_blocks={
                "outputType": {"id": "outputType", "type": "dropdown", "value": "multi"},
                "channels": {"id": "channels", "type": "multi-select", "value": ["email", "slack", "discord"]},
                "emailConfig": {"id": "emailConfig", "type": "json", 
                              "value": {"to": "trader@cryptobot.com", "subject": "Trade Executed: {{TRADING_PAIR}}"}},
                "slackConfig": {"id": "slackConfig", "type": "json", 
                              "value": {"webhook": "https://hooks.slack.com/services/...", "channel": "#trading"}},
                "discordConfig": {"id": "discordConfig", "type": "json", 
                                "value": {"webhook": "https://discord.com/api/webhooks/..."}}
            }
        )
        blocks.append(output_block)
        
        # Create edges
        edges = [
            {"source": starter_block["id"], "target": api_block["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": api_block["id"], "target": agent_block["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": agent_block["id"], "target": execution_block["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": execution_block["id"], "target": output_block["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        # Create workflow state
        state = {
            "blocks": {block["id"]: self._block_to_state_format(block) for block in blocks},
            "edges": edges,
            "subflows": {},
            "variables": {
                "BINANCE_API_KEY": {"type": "secret", "value": ""},
                "BINANCE_SECRET_KEY": {"type": "secret", "value": ""},
                "TRADING_PAIR": {"type": "string", "value": "BTCUSDT"},
                "STOP_LOSS_PCT": {"type": "number", "value": -5},
                "TAKE_PROFIT_PCT": {"type": "number", "value": 10},
                "TRADE_AMOUNT": {"type": "number", "value": 0.001}
            },
            "metadata": {
                "version": "1.0.0",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        return {
            "id": workflow_id,
            "user_id": "demo-user-trader",
            "workspace_id": "crypto-trading-workspace",
            "name": "Advanced Crypto Trading Bot",
            "description": "24/7 autonomous crypto trading with advanced risk management, technical analysis, and multi-channel notifications",
            "state": json.dumps(state),
            "color": "#15803D",
            "last_synced": datetime.utcnow().isoformat(),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "is_deployed": True,
            "deployed_state": json.dumps(state),
            "deployed_at": datetime.utcnow().isoformat(),
            "collaborators": json.dumps([]),
            "run_count": random.randint(100, 1000),
            "last_run_at": (datetime.utcnow() - timedelta(minutes=5)).isoformat(),
            "variables": json.dumps({
                "TRADING_PAIR": "BTCUSDT",
                "STOP_LOSS_PCT": -5,
                "TAKE_PROFIT_PCT": 10
            }),
            "is_published": True,
            "marketplace_data": json.dumps({
                "category": "Web3 Trading",
                "tags": ["crypto", "trading", "defi", "automation", "bitcoin", "ethereum"],
                "pricing": "usage-based",
                "rating": 4.8,
                "downloads": 2547,
                "featured": True
            })
        }
    
    def create_multi_agent_research_workflow(self) -> dict:
        """Create a complex multi-agent research team workflow"""
        workflow_id = str(uuid4())
        
        blocks = []
        
        # Starter block
        starter = self._create_block(
            workflow_id=workflow_id,
            type="starter",
            name="Research Request",
            position=(100, 300),
            sub_blocks={
                "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"},
                "webhookPath": {"id": "webhookPath", "type": "short-input", "value": "research-request"},
                "webhookSecret": {"id": "webhookSecret", "type": "short-input", "value": "research-secret-key"}
            }
        )
        blocks.append(starter)
        
        # Coordinator agent
        coordinator = self._create_block(
            workflow_id=workflow_id,
            type="agent",
            name="Research Coordinator",
            position=(300, 300),
            sub_blocks={
                "model": {"id": "model", "type": "combobox", "value": "claude-3"},
                "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                               "value": "You are a research coordinator managing a team of specialist agents. Break down research queries into focused subtasks and assign them to the appropriate specialists: Market Research Agent (trends, consumer behavior), Technical Analysis Agent (technical specs, implementation), and Competitive Intelligence Agent (competitor analysis, market positioning). Provide clear, specific instructions to each agent."},
                "temperature": {"id": "temperature", "type": "slider", "value": 0.5}
            }
        )
        blocks.append(coordinator)
        
        # Specialist agents
        market_agent = self._create_block(
            workflow_id=workflow_id,
            type="agent",
            name="Market Research Agent",
            position=(500, 200),
            sub_blocks={
                "model": {"id": "model", "type": "combobox", "value": "gpt-4"},
                "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                               "value": "You are a market research specialist. Focus on market trends, consumer behavior, demand analysis, market size, growth projections, and customer segments. Provide data-driven insights with sources and confidence levels."},
                "temperature": {"id": "temperature", "type": "slider", "value": 0.7},
                "tools": {"id": "tools", "type": "tool-input", "value": [
                    {"type": "web_search", "title": "Web Search", "enabled": True},
                    {"type": "market_data", "title": "Market Data APIs", "enabled": True}
                ]}
            }
        )
        blocks.append(market_agent)
        
        technical_agent = self._create_block(
            workflow_id=workflow_id,
            type="agent",
            name="Technical Analysis Agent",
            position=(500, 300),
            sub_blocks={
                "model": {"id": "model", "type": "combobox", "value": "gpt-4"},
                "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                               "value": "You are a technical analysis specialist. Focus on technical specifications, implementation details, architecture analysis, technology stack evaluation, performance metrics, and technical feasibility. Provide detailed technical assessments."},
                "temperature": {"id": "temperature", "type": "slider", "value": 0.6},
                "tools": {"id": "tools", "type": "tool-input", "value": [
                    {"type": "code_analysis", "title": "Code Analysis", "enabled": True},
                    {"type": "technical_docs", "title": "Technical Documentation", "enabled": True}
                ]}
            }
        )
        blocks.append(technical_agent)
        
        competitive_agent = self._create_block(
            workflow_id=workflow_id,
            type="agent",
            name="Competitive Intelligence Agent",
            position=(500, 400),
            sub_blocks={
                "model": {"id": "model", "type": "combobox", "value": "claude-3"},
                "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                               "value": "You are a competitive intelligence specialist. Focus on competitor analysis, market positioning, pricing strategies, feature comparisons, SWOT analysis, and competitive advantages. Identify market gaps and opportunities."},
                "temperature": {"id": "temperature", "type": "slider", "value": 0.7},
                "tools": {"id": "tools", "type": "tool-input", "value": [
                    {"type": "competitor_analysis", "title": "Competitor Analysis", "enabled": True},
                    {"type": "pricing_data", "title": "Pricing Intelligence", "enabled": True}
                ]}
            }
        )
        blocks.append(competitive_agent)
        
        # Synthesis agent
        synthesis = self._create_block(
            workflow_id=workflow_id,
            type="agent",
            name="Research Synthesizer",
            position=(700, 300),
            sub_blocks={
                "model": {"id": "model", "type": "combobox", "value": "claude-3"},
                "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                               "value": "You are a research synthesis specialist. Combine insights from market research, technical analysis, and competitive intelligence into a comprehensive report. Create executive summary, key findings, strategic recommendations, and actionable next steps. Ensure consistency and identify cross-functional insights."},
                "temperature": {"id": "temperature", "type": "slider", "value": 0.4}
            }
        )
        blocks.append(synthesis)
        
        # Output block
        output = self._create_block(
            workflow_id=workflow_id,
            type="output",
            name="Research Report Delivery",
            position=(900, 300),
            sub_blocks={
                "outputType": {"id": "outputType", "type": "dropdown", "value": "document"},
                "channels": {"id": "channels", "type": "multi-select", "value": ["email", "google_docs", "slack"]},
                "emailConfig": {"id": "emailConfig", "type": "json", 
                              "value": {"to": "research@company.com", "subject": "Research Report: {{RESEARCH_TOPIC}}"}},
                "docConfig": {"id": "docConfig", "type": "json", 
                            "value": {"format": "pdf", "template": "research_report", "folder": "Research Reports"}},
                "slackConfig": {"id": "slackConfig", "type": "json", 
                              "value": {"channel": "#research", "message": "New research report available"}}
            }
        )
        blocks.append(output)
        
        # Create edges
        edges = [
            {"source": starter["id"], "target": coordinator["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": coordinator["id"], "target": market_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": coordinator["id"], "target": technical_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": coordinator["id"], "target": competitive_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": market_agent["id"], "target": synthesis["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": technical_agent["id"], "target": synthesis["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": competitive_agent["id"], "target": synthesis["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": synthesis["id"], "target": output["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        state = {
            "blocks": {block["id"]: self._block_to_state_format(block) for block in blocks},
            "edges": edges,
            "subflows": {},
            "variables": {
                "RESEARCH_TOPIC": {"type": "string", "value": "AI Market Analysis"},
                "RESEARCH_DEPTH": {"type": "string", "value": "comprehensive"},
                "DEADLINE": {"type": "string", "value": "7 days"}
            },
            "metadata": {
                "version": "1.0.0",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        return {
            "id": workflow_id,
            "user_id": "demo-user-research",
            "workspace_id": "research-team-workspace",
            "name": "Multi-Agent Research Team",
            "description": "Collaborative AI research team with specialized agents for market analysis, technical evaluation, and competitive intelligence",
            "state": json.dumps(state),
            "color": "#7C2D12",
            "last_synced": datetime.utcnow().isoformat(),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "is_deployed": True,
            "deployed_state": json.dumps(state),
            "deployed_at": datetime.utcnow().isoformat(),
            "collaborators": json.dumps(["research-lead@company.com", "analyst@company.com"]),
            "run_count": random.randint(50, 200),
            "last_run_at": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
            "variables": json.dumps({"RESEARCH_TOPIC": "AI Market Analysis"}),
            "is_published": True,
            "marketplace_data": json.dumps({
                "category": "Research & Analysis",
                "tags": ["research", "multi-agent", "analysis", "reports", "intelligence"],
                "pricing": "premium",
                "rating": 4.9,
                "downloads": 1823,
                "featured": True
            })
        }
    
    def create_lead_capture_workflow(self) -> dict:
        """Simple lead capture workflow"""
        workflow_id = str(uuid4())
        
        starter = self._create_block(
            workflow_id, "starter", "Lead Form Submission", (100, 200),
            {
                "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"},
                "webhookPath": {"id": "webhookPath", "type": "short-input", "value": "lead-capture"}
            }
        )
        
        agent = self._create_block(
            workflow_id, "agent", "Lead Qualifier", (300, 200),
            {
                "model": {"id": "model", "type": "combobox", "value": "gpt-4"},
                "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                               "value": "Qualify leads based on company size, budget, and urgency. Score 1-10."},
                "temperature": {"id": "temperature", "type": "slider", "value": 0.3}
            }
        )
        
        output = self._create_block(
            workflow_id, "output", "CRM Update", (500, 200),
            {
                "outputType": {"id": "outputType", "type": "dropdown", "value": "api"},
                "channels": {"id": "channels", "type": "multi-select", "value": ["hubspot", "email"]}
            }
        )
        
        blocks = [starter, agent, output]
        edges = [
            {"source": starter["id"], "target": agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": agent["id"], "target": output["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        return self._create_workflow(workflow_id, "Lead Capture System", 
                                   "Automated lead qualification and CRM integration", 
                                   blocks, edges, "Sales & Marketing")
    
    def create_scheduled_report_workflow(self) -> dict:
        """Scheduled reporting workflow"""
        workflow_id = str(uuid4())
        
        starter = self._create_block(
            workflow_id, "starter", "Daily Report Trigger", (100, 200),
            {
                "startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"},
                "scheduleType": {"id": "scheduleType", "type": "dropdown", "value": "daily"},
                "dailyTime": {"id": "dailyTime", "type": "short-input", "value": "09:00"}
            }
        )
        
        api = self._create_block(
            workflow_id, "api", "Analytics Data", (300, 200),
            {
                "url": {"id": "url", "type": "short-input", "value": "https://api.analytics.com/daily-stats"},
                "method": {"id": "method", "type": "dropdown", "value": "GET"}
            }
        )
        
        agent = self._create_block(
            workflow_id, "agent", "Report Generator", (500, 200),
            {
                "model": {"id": "model", "type": "combobox", "value": "claude-3"},
                "systemPrompt": {"id": "systemPrompt", "type": "long-input", 
                               "value": "Generate daily performance report with insights and recommendations."}
            }
        )
        
        output = self._create_block(
            workflow_id, "output", "Email Report", (700, 200),
            {
                "outputType": {"id": "outputType", "type": "dropdown", "value": "email"},
                "channels": {"id": "channels", "type": "multi-select", "value": ["email"]}
            }
        )
        
        blocks = [starter, api, agent, output]
        edges = [
            {"source": starter["id"], "target": api["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": api["id"], "target": agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": agent["id"], "target": output["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        return self._create_workflow(workflow_id, "Daily Analytics Report", 
                                   "Automated daily performance reporting", 
                                   blocks, edges, "Analytics")
    
    def create_webhook_handler_workflow(self) -> dict:
        """Simple webhook handler"""
        workflow_id = str(uuid4())
        
        starter = self._create_block(
            workflow_id, "starter", "Webhook Receiver", (100, 200),
            {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"}}
        )
        
        agent = self._create_block(
            workflow_id, "agent", "Data Processor", (300, 200),
            {
                "model": {"id": "model", "type": "combobox", "value": "gpt-3.5-turbo"},
                "systemPrompt": {"id": "systemPrompt", "type": "long-input", "value": "Process webhook data and extract key information."}
            }
        )
        
        output = self._create_block(
            workflow_id, "output", "Slack Alert", (500, 200),
            {"outputType": {"id": "outputType", "type": "dropdown", "value": "slack"}}
        )
        
        blocks = [starter, agent, output]
        edges = [
            {"source": starter["id"], "target": agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": agent["id"], "target": output["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        return self._create_workflow(workflow_id, "Webhook Handler", 
                                   "Process incoming webhooks and send alerts", 
                                   blocks, edges, "Integration")
    
    def create_data_fetch_workflow(self) -> dict:
        """Data fetching workflow"""
        workflow_id = str(uuid4())
        
        starter = self._create_block(
            workflow_id, "starter", "Data Sync", (100, 200),
            {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}}
        )
        
        api = self._create_block(
            workflow_id, "api", "External API", (300, 200),
            {"url": {"id": "url", "type": "short-input", "value": "https://api.example.com/data"}}
        )
        
        output = self._create_block(
            workflow_id, "output", "Database Update", (500, 200),
            {"outputType": {"id": "outputType", "type": "dropdown", "value": "database"}}
        )
        
        blocks = [starter, api, output]
        edges = [
            {"source": starter["id"], "target": api["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": api["id"], "target": output["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        return self._create_workflow(workflow_id, "Data Sync Pipeline", 
                                   "Scheduled data synchronization", 
                                   blocks, edges, "Data Processing")
    
    def create_notification_workflow(self) -> dict:
        """Simple notification workflow"""
        workflow_id = str(uuid4())
        
        starter = self._create_block(
            workflow_id, "starter", "Alert Trigger", (100, 200),
            {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"}}
        )
        
        output = self._create_block(
            workflow_id, "output", "Multi-Channel Alert", (300, 200),
            {
                "outputType": {"id": "outputType", "type": "dropdown", "value": "multi"},
                "channels": {"id": "channels", "type": "multi-select", "value": ["email", "sms", "slack"]}
            }
        )
        
        blocks = [starter, output]
        edges = [{"source": starter["id"], "target": output["id"], "sourceHandle": "output", "targetHandle": "input"}]
        
        return self._create_workflow(workflow_id, "Alert System", 
                                   "Multi-channel notification system", 
                                   blocks, edges, "Communication")
    
    # Medium complexity workflows
    def create_marketing_automation_workflow(self) -> dict:
        """Marketing automation workflow"""
        workflow_id = str(uuid4())
        blocks = []
        
        # Create a more complex marketing workflow with multiple agents
        starter = self._create_block(workflow_id, "starter", "Campaign Trigger", (100, 200), 
                                   {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}})
        
        segment_agent = self._create_block(workflow_id, "agent", "Audience Segmentation", (300, 200),
                                         {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}})
        
        content_agent = self._create_block(workflow_id, "agent", "Content Generator", (500, 200),
                                         {"model": {"id": "model", "type": "combobox", "value": "claude-3"}})
        
        email_api = self._create_block(workflow_id, "api", "Email Campaign", (700, 200),
                                     {"url": {"id": "url", "type": "short-input", "value": "https://api.mailchimp.com/3.0/campaigns"}})
        
        blocks = [starter, segment_agent, content_agent, email_api]
        edges = [
            {"source": starter["id"], "target": segment_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": segment_agent["id"], "target": content_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": content_agent["id"], "target": email_api["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        return self._create_workflow(workflow_id, "Marketing Automation", 
                                   "Automated audience segmentation and content generation", 
                                   blocks, edges, "Marketing")
    
    def create_customer_support_workflow(self) -> dict:
        """Customer support workflow"""
        workflow_id = str(uuid4())
        
        starter = self._create_block(workflow_id, "starter", "Support Ticket", (100, 200),
                                   {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"}})
        
        classifier = self._create_block(workflow_id, "agent", "Ticket Classifier", (300, 200),
                                      {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}})
        
        support_agent = self._create_block(workflow_id, "agent", "Support Agent", (500, 200),
                                         {"model": {"id": "model", "type": "combobox", "value": "claude-3"}})
        
        output = self._create_block(workflow_id, "output", "Customer Response", (700, 200),
                                  {"outputType": {"id": "outputType", "type": "dropdown", "value": "email"}})
        
        blocks = [starter, classifier, support_agent, output]
        edges = [
            {"source": starter["id"], "target": classifier["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": classifier["id"], "target": support_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": support_agent["id"], "target": output["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        return self._create_workflow(workflow_id, "Customer Support Automation", 
                                   "Automated ticket classification and response", 
                                   blocks, edges, "Customer Service")
    
    def create_content_generator_workflow(self) -> dict:
        """Content generation workflow"""
        workflow_id = str(uuid4())
        
        starter = self._create_block(workflow_id, "starter", "Content Request", (100, 200),
                                   {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"}})
        
        research_agent = self._create_block(workflow_id, "agent", "Research Agent", (300, 200),
                                          {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}})
        
        writer_agent = self._create_block(workflow_id, "agent", "Content Writer", (500, 200),
                                        {"model": {"id": "model", "type": "combobox", "value": "claude-3"}})
        
        publisher = self._create_block(workflow_id, "api", "Content Publisher", (700, 200),
                                     {"url": {"id": "url", "type": "short-input", "value": "https://api.wordpress.com/wp/v2/posts"}})
        
        blocks = [starter, research_agent, writer_agent, publisher]
        edges = [
            {"source": starter["id"], "target": research_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": research_agent["id"], "target": writer_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": writer_agent["id"], "target": publisher["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        return self._create_workflow(workflow_id, "Content Generation Pipeline", 
                                   "AI-powered content research, writing, and publishing", 
                                   blocks, edges, "Content & Media")
    
    def create_real_estate_workflow(self) -> dict:
        """Real estate workflow"""
        workflow_id = str(uuid4())
        
        starter = self._create_block(workflow_id, "starter", "Property Alert", (100, 200),
                                   {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}})
        
        api = self._create_block(workflow_id, "api", "Property Listings", (300, 200),
                               {"url": {"id": "url", "type": "short-input", "value": "https://api.zillow.com/properties"}})
        
        analyzer = self._create_block(workflow_id, "agent", "Property Analyzer", (500, 200),
                                    {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}})
        
        output = self._create_block(workflow_id, "output", "Investment Alert", (700, 200),
                                  {"outputType": {"id": "outputType", "type": "dropdown", "value": "email"}})
        
        blocks = [starter, api, analyzer, output]
        edges = [
            {"source": starter["id"], "target": api["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": api["id"], "target": analyzer["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": analyzer["id"], "target": output["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        return self._create_workflow(workflow_id, "Real Estate Investment Analyzer", 
                                   "Automated property analysis and investment alerts", 
                                   blocks, edges, "Real Estate")
    
    # Complex workflows
    def create_web3_defi_workflow(self) -> dict:
        """Web3 DeFi workflow"""
        workflow_id = str(uuid4())
        
        # Complex DeFi yield farming workflow
        blocks = []
        
        starter = self._create_block(workflow_id, "starter", "DeFi Monitor", (100, 300),
                                   {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}})
        
        # Multiple APIs for different protocols
        uniswap_api = self._create_block(workflow_id, "api", "Uniswap Data", (300, 200),
                                       {"url": {"id": "url", "type": "short-input", "value": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"}})
        
        aave_api = self._create_block(workflow_id, "api", "Aave Data", (300, 300),
                                    {"url": {"id": "url", "type": "short-input", "value": "https://api.aave.com/data/liquidity/v2"}})
        
        compound_api = self._create_block(workflow_id, "api", "Compound Data", (300, 400),
                                        {"url": {"id": "url", "type": "short-input", "value": "https://api.compound.finance/api/v2/ctoken"}})
        
        # DeFi strategy agent
        strategy_agent = self._create_block(workflow_id, "agent", "DeFi Strategy Agent", (500, 300),
                                          {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}})
        
        # Execution
        execution = self._create_block(workflow_id, "api", "Smart Contract Execution", (700, 300),
                                     {"url": {"id": "url", "type": "short-input", "value": "https://mainnet.infura.io/v3/YOUR-PROJECT-ID"}})
        
        blocks = [starter, uniswap_api, aave_api, compound_api, strategy_agent, execution]
        
        edges = [
            {"source": starter["id"], "target": uniswap_api["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": starter["id"], "target": aave_api["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": starter["id"], "target": compound_api["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": uniswap_api["id"], "target": strategy_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": aave_api["id"], "target": strategy_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": compound_api["id"], "target": strategy_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": strategy_agent["id"], "target": execution["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        return self._create_workflow(workflow_id, "DeFi Yield Optimizer", 
                                   "Multi-protocol DeFi yield farming optimization", 
                                   blocks, edges, "Web3 & DeFi")
    
    def create_enterprise_automation_workflow(self) -> dict:
        """Enterprise automation workflow"""
        workflow_id = str(uuid4())
        
        # Complex enterprise workflow with multiple agents and integrations
        blocks = []
        
        starter = self._create_block(workflow_id, "starter", "Business Process Trigger", (100, 300),
                                   {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "webhook"}})
        
        # Multiple specialist agents
        hr_agent = self._create_block(workflow_id, "agent", "HR Agent", (300, 200),
                                    {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}})
        
        finance_agent = self._create_block(workflow_id, "agent", "Finance Agent", (300, 300),
                                         {"model": {"id": "model", "type": "combobox", "value": "claude-3"}})
        
        legal_agent = self._create_block(workflow_id, "agent", "Legal Agent", (300, 400),
                                       {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}})
        
        coordinator = self._create_block(workflow_id, "agent", "Process Coordinator", (500, 300),
                                       {"model": {"id": "model", "type": "combobox", "value": "claude-3"}})
        
        # Multiple outputs
        erp_integration = self._create_block(workflow_id, "api", "ERP Integration", (700, 250),
                                           {"url": {"id": "url", "type": "short-input", "value": "https://api.sap.com/enterprise"}})
        
        notification = self._create_block(workflow_id, "output", "Stakeholder Notification", (700, 350),
                                        {"outputType": {"id": "outputType", "type": "dropdown", "value": "multi"}})
        
        blocks = [starter, hr_agent, finance_agent, legal_agent, coordinator, erp_integration, notification]
        
        edges = [
            {"source": starter["id"], "target": hr_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": starter["id"], "target": finance_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": starter["id"], "target": legal_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": hr_agent["id"], "target": coordinator["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": finance_agent["id"], "target": coordinator["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": legal_agent["id"], "target": coordinator["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": coordinator["id"], "target": erp_integration["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": coordinator["id"], "target": notification["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        return self._create_workflow(workflow_id, "Enterprise Process Automation", 
                                   "Multi-department business process automation", 
                                   blocks, edges, "Enterprise")
    
    def create_ai_team_workflow(self) -> dict:
        """AI team workflow"""
        workflow_id = str(uuid4())
        
        # AI team with different specialized models
        blocks = []
        
        starter = self._create_block(workflow_id, "starter", "AI Team Request", (100, 400),
                                   {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "manual"}})
        
        # Different AI models for different tasks
        gpt4_agent = self._create_block(workflow_id, "agent", "GPT-4 Analyst", (300, 300),
                                      {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}})
        
        claude_agent = self._create_block(workflow_id, "agent", "Claude Writer", (300, 400),
                                        {"model": {"id": "model", "type": "combobox", "value": "claude-3"}})
        
        gemini_agent = self._create_block(workflow_id, "agent", "Gemini Researcher", (300, 500),
                                        {"model": {"id": "model", "type": "combobox", "value": "gemini-pro"}})
        
        coordinator = self._create_block(workflow_id, "agent", "AI Coordinator", (500, 400),
                                       {"model": {"id": "model", "type": "combobox", "value": "claude-3"}})
        
        output = self._create_block(workflow_id, "output", "Team Output", (700, 400),
                                  {"outputType": {"id": "outputType", "type": "dropdown", "value": "document"}})
        
        blocks = [starter, gpt4_agent, claude_agent, gemini_agent, coordinator, output]
        
        edges = [
            {"source": starter["id"], "target": gpt4_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": starter["id"], "target": claude_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": starter["id"], "target": gemini_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": gpt4_agent["id"], "target": coordinator["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": claude_agent["id"], "target": coordinator["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": gemini_agent["id"], "target": coordinator["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": coordinator["id"], "target": output["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        return self._create_workflow(workflow_id, "Multi-Model AI Team", 
                                   "Collaborative AI team using different models", 
                                   blocks, edges, "AI & ML")
    
    def create_marketplace_aggregator_workflow(self) -> dict:
        """Marketplace aggregator workflow"""
        workflow_id = str(uuid4())
        
        # E-commerce marketplace aggregation
        blocks = []
        
        starter = self._create_block(workflow_id, "starter", "Market Scan", (100, 400),
                                   {"startWorkflow": {"id": "startWorkflow", "type": "dropdown", "value": "schedule"}})
        
        # Multiple marketplace APIs
        amazon_api = self._create_block(workflow_id, "api", "Amazon API", (300, 300),
                                      {"url": {"id": "url", "type": "short-input", "value": "https://webservices.amazon.com/paapi5/searchitems"}})
        
        ebay_api = self._create_block(workflow_id, "api", "eBay API", (300, 400),
                                    {"url": {"id": "url", "type": "short-input", "value": "https://api.ebay.com/buy/browse/v1/item_summary/search"}})
        
        shopify_api = self._create_block(workflow_id, "api", "Shopify API", (300, 500),
                                       {"url": {"id": "url", "type": "short-input", "value": "https://api.shopify.com/admin/api/2023-01/products.json"}})
        
        # Price comparison agent
        price_agent = self._create_block(workflow_id, "agent", "Price Comparison Agent", (500, 400),
                                       {"model": {"id": "model", "type": "combobox", "value": "gpt-4"}})
        
        # Multiple outputs
        database = self._create_block(workflow_id, "api", "Database Update", (700, 350),
                                    {"url": {"id": "url", "type": "short-input", "value": "https://api.database.com/products"}})
        
        alert = self._create_block(workflow_id, "output", "Price Alert", (700, 450),
                                 {"outputType": {"id": "outputType", "type": "dropdown", "value": "email"}})
        
        blocks = [starter, amazon_api, ebay_api, shopify_api, price_agent, database, alert]
        
        edges = [
            {"source": starter["id"], "target": amazon_api["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": starter["id"], "target": ebay_api["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": starter["id"], "target": shopify_api["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": amazon_api["id"], "target": price_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": ebay_api["id"], "target": price_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": shopify_api["id"], "target": price_agent["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": price_agent["id"], "target": database["id"], "sourceHandle": "output", "targetHandle": "input"},
            {"source": price_agent["id"], "target": alert["id"], "sourceHandle": "output", "targetHandle": "input"}
        ]
        
        return self._create_workflow(workflow_id, "E-commerce Price Aggregator", 
                                   "Multi-marketplace price monitoring and comparison", 
                                   blocks, edges, "E-commerce")
    
    def _create_block(self, workflow_id: str, type: str, name: str, 
                     position: tuple, sub_blocks: dict, outputs: dict = None) -> dict:
        """Helper to create Agent Forge block structure"""
        if outputs is None:
            outputs = self._get_default_outputs(type)
        
        return {
            "id": str(uuid4()),
            "workflow_id": workflow_id,
            "type": type,
            "name": name,
            "position_x": position[0],
            "position_y": position[1],
            "enabled": True,
            "horizontal_handles": True,
            "is_wide": type == "agent",
            "advanced_mode": False,
            "height": 120 if type == "agent" else 95,
            "sub_blocks": sub_blocks,
            "outputs": outputs,
            "data": {},
            "parent_id": None,
            "extent": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
    
    def _get_default_outputs(self, block_type: str) -> dict:
        """Get default outputs for block type"""
        defaults = {
            "starter": {"response": {"type": {"input": "any"}}},
            "agent": {"model": "string", "tokens": "any", "content": "string", "toolCalls": "any"},
            "api": {"data": "any", "status": "number", "headers": "json"},
            "output": {"success": "boolean", "message": "string"},
            "tool": {"result": "any", "metadata": "json"}
        }
        return defaults.get(block_type, {"output": "any"})
    
    def _block_to_state_format(self, block: dict) -> dict:
        """Convert block to state format"""
        return {
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
        }
    
    def _create_workflow(self, workflow_id: str, name: str, description: str, 
                        blocks: list, edges: list, category: str) -> dict:
        """Create complete workflow structure"""
        
        state = {
            "blocks": {block["id"]: self._block_to_state_format(block) for block in blocks},
            "edges": edges,
            "subflows": {},
            "variables": {},
            "metadata": {
                "version": "1.0.0",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        return {
            "id": workflow_id,
            "user_id": f"demo-user-{random.randint(1, 100)}",
            "workspace_id": f"workspace-{random.choice(['personal', 'team', 'enterprise'])}",
            "name": name,
            "description": description,
            "state": json.dumps(state),
            "color": random.choice(self.colors),
            "last_synced": datetime.utcnow().isoformat(),
            "created_at": (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat(),
            "updated_at": (datetime.utcnow() - timedelta(hours=random.randint(1, 24))).isoformat(),
            "is_deployed": random.choice([True, False]),
            "deployed_state": json.dumps(state) if random.choice([True, False]) else None,
            "deployed_at": (datetime.utcnow() - timedelta(hours=random.randint(1, 72))).isoformat() if random.choice([True, False]) else None,
            "collaborators": json.dumps([f"user{i}@company.com" for i in range(random.randint(0, 3))]),
            "run_count": random.randint(0, 500),
            "last_run_at": (datetime.utcnow() - timedelta(minutes=random.randint(5, 1440))).isoformat() if random.choice([True, False]) else None,
            "variables": json.dumps({}),
            "is_published": random.choice([True, False]),
            "marketplace_data": json.dumps({
                "category": category,
                "tags": [category.lower().replace(" ", "_"), "automation", "ai"],
                "pricing": random.choice(["free", "usage-based", "premium"]),
                "rating": round(random.uniform(3.5, 5.0), 1),
                "downloads": random.randint(10, 5000)
            })
        }
    
    def generate_sql_inserts(self) -> str:
        """Generate SQL insert statements for all workflows"""
        workflows = self.generate_all_workflows()
        
        sql_statements = []
        
        print("📊 Generating SQL insert statements...")
        
        for i, workflow in enumerate(workflows, 1):
            print(f"  Processing workflow {i}/{len(workflows)}: {workflow['name']}")
            
            # Insert into workflow table - fix f-string backslash issue
            deployed_state_val = 'NULL'
            if workflow.get('deployed_state'):
                deployed_state_val = "'" + workflow['deployed_state'].replace("'", "''") + "'"
            
            deployed_at_val = 'NULL'
            if workflow.get('deployed_at'):
                deployed_at_val = "'" + workflow['deployed_at'] + "'"
            
            last_run_at_val = 'NULL'
            if workflow.get('last_run_at'):
                last_run_at_val = "'" + workflow['last_run_at'] + "'"
            
            workflow_sql = f"""
INSERT INTO workflow (
    id, user_id, workspace_id, folder_id, name, description, state, color,
    last_synced, created_at, updated_at, is_deployed, deployed_state, deployed_at,
    collaborators, run_count, last_run_at, variables, is_published, marketplace_data
) VALUES (
    '{workflow['id']}',
    '{workflow['user_id']}',
    '{workflow['workspace_id']}',
    NULL,
    '{workflow['name'].replace("'", "''")}',
    '{workflow['description'].replace("'", "''")}',
    '{workflow['state'].replace("'", "''")}',
    '{workflow['color']}',
    '{workflow['last_synced']}',
    '{workflow['created_at']}',
    '{workflow['updated_at']}',
    {workflow['is_deployed']},
    {deployed_state_val},
    {deployed_at_val},
    '{workflow['collaborators']}',
    {workflow['run_count']},
    {last_run_at_val},
    '{workflow['variables']}',
    {workflow['is_published']},
    '{workflow['marketplace_data'].replace("'", "''")}'
);"""
            sql_statements.append(workflow_sql)
            
            # Insert blocks
            state = json.loads(workflow['state'])
            for block_id, block in state['blocks'].items():
                # Fix f-string backslash issue for block inserts
                sub_blocks_json = json.dumps(block['subBlocks']).replace("'", "''")
                outputs_json = json.dumps(block['outputs']).replace("'", "''")
                
                block_sql = f"""
INSERT INTO workflow_blocks (
    id, workflow_id, type, name, position_x, position_y,
    enabled, horizontal_handles, is_wide, advanced_mode, height,
    sub_blocks, outputs, data, parent_id, extent,
    created_at, updated_at
) VALUES (
    '{block_id}',
    '{workflow['id']}',
    '{block['type']}',
    '{block['name'].replace("'", "''")}',
    {block['position']['x']},
    {block['position']['y']},
    {block['enabled']},
    {block['horizontalHandles']},
    {block['isWide']},
    FALSE,
    {block['height']},
    '{sub_blocks_json}',
    '{outputs_json}',
    '{{}}',
    NULL,
    NULL,
    NOW(),
    NOW()
);"""
                sql_statements.append(block_sql)
        
        print("✅ SQL generation complete!")
        return '\n'.join(sql_statements)
    
    def generate_json_fixtures(self) -> dict:
        """Generate JSON fixtures for testing"""
        workflows = self.generate_all_workflows()
        
        print("📄 Generating JSON fixtures...")
        
        fixtures = {
            "workflows": workflows,
            "summary": {
                "total_workflows": len(workflows),
                "categories": {},
                "complexity_distribution": {"Simple": 0, "Medium": 0, "Complex": 0},
                "deployment_stats": {"deployed": 0, "not_deployed": 0},
                "model_usage": {}
            }
        }
        
        # Generate summary statistics
        for workflow in workflows:
            marketplace_data = json.loads(workflow['marketplace_data'])
            category = marketplace_data.get('category', 'Unknown')
            
            if category not in fixtures["summary"]["categories"]:
                fixtures["summary"]["categories"][category] = 0
            fixtures["summary"]["categories"][category] += 1
            
            if workflow['is_deployed']:
                fixtures["summary"]["deployment_stats"]["deployed"] += 1
            else:
                fixtures["summary"]["deployment_stats"]["not_deployed"] += 1
            
            # Count model usage
            state = json.loads(workflow['state'])
            for block in state['blocks'].values():
                if block['type'] == 'agent':
                    model = block.get('subBlocks', {}).get('model', {}).get('value', 'unknown')
                    if model not in fixtures["summary"]["model_usage"]:
                        fixtures["summary"]["model_usage"][model] = 0
                    fixtures["summary"]["model_usage"][model] += 1
        
        print("✅ JSON fixtures generated!")
        return fixtures

def main():
    """Main function to generate all data"""
    print("🎯 Agent Forge Synthetic Data Generator")
    print("=" * 50)
    
    generator = AgentForgeSyntheticData()
    
    try:
        # Create data directory
        os.makedirs('data', exist_ok=True)
        
        # Generate SQL file
        print("\n📝 Generating SQL data...")
        sql_content = generator.generate_sql_inserts()
        with open('data/agent_forge_synthetic_data.sql', 'w', encoding='utf-8') as f:
            f.write(sql_content)
        print(f"✅ SQL file saved: data/agent_forge_synthetic_data.sql")
        
        # Generate JSON fixtures
        print("\n📄 Generating JSON fixtures...")
        fixtures = generator.generate_json_fixtures()
        with open('data/agent_forge_workflows.json', 'w', encoding='utf-8') as f:
            json.dump(fixtures, f, indent=2, default=str)
        print(f"✅ JSON file saved: data/agent_forge_workflows.json")
        
        # Print summary
        print("\n📊 Generation Summary:")
        print(f"  • Total workflows: {fixtures['summary']['total_workflows']}")
        print(f"  • Categories: {list(fixtures['summary']['categories'].keys())}")
        print(f"  • Models used: {list(fixtures['summary']['model_usage'].keys())}")
        print(f"  • Deployed workflows: {fixtures['summary']['deployment_stats']['deployed']}")
        
        print("\n🎉 Agent Forge synthetic data generation completed successfully!")
        
    except Exception as e:
        print(f"❌ Error generating data: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
