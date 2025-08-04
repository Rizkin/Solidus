# src/api/workflows.py
from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
import uuid
from src.services.state_generator import state_generator
from src.services.validation import validator
from src.utils.database_hybrid import db_service
from src.models.schemas import StateGenerationOptions
from src.models.connection import get_db, AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["workflows"])

@router.post("/workflows/{workflow_id}/generate-state")
async def generate_workflow_state(
    workflow_id: str,
    options: Optional[StateGenerationOptions] = Body(default=None)
):
    """
    Generate Agent Forge-compatible workflow state using AI.
    Supports drag-and-drop workflow patterns and multi-agent teams.
    """
    try:
        logger.info(f"Generating state for workflow {workflow_id}")
        
        # Use default options if none provided
        if not options:
            options = StateGenerationOptions()
        
        # Generate state
        generated_state = await state_generator.generate_workflow_state(workflow_id)
        
        # Validate the generated state
        validation_report = await validator.validate_state(generated_state, workflow_id)
        
        # Save to database if valid and requested
        if validation_report.overall_valid and options.include_suggestions:
            await db_service.update_workflow_state(workflow_id, generated_state)
            logger.info(f"State saved for workflow {workflow_id}")
        
        # Analyze pattern
        pattern = await state_generator.analyze_workflow_pattern(workflow_id)
        
        # Extract detected patterns from validation metadata
        detected_patterns = []
        for result in validation_report.validation_results:
            if result.validator_name == "validate_workflow_patterns" and result.metadata:
                detected_patterns = result.metadata.get('detected_patterns', [])
        
        return {
            "workflow_id": workflow_id,
            "generated_state": generated_state,
            "validation_report": validation_report.dict(),
            "agent_forge_pattern": pattern,
            "agent_forge_patterns": detected_patterns,
            "generation_metadata": {
                "model": "claude-3-opus",
                "platform": "agent-forge",
                "timestamp": datetime.utcnow().isoformat(),
                "options": options.dict()
            }
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating state: {e}")
        raise HTTPException(status_code=500, detail=f"State generation failed: {str(e)}")

@router.get("/workflows/{workflow_id}/marketplace-preview")
async def get_marketplace_preview(workflow_id: str):
    """
    Preview how workflow would appear in Agent Forge marketplace
    """
    try:
        # Get workflow data
        workflow = await db_service.get_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        blocks = await db_service.get_workflow_blocks(workflow_id)
        state = workflow.get('state', {})
        
        if isinstance(state, str):
            try:
                state = json.loads(state)
            except json.JSONDecodeError:
                state = {}
        
        # Analyze workflow for marketplace categorization
        categories = []
        tags = []
        
        # Count different block types
        agent_count = sum(1 for b in blocks if b.get('type') == 'agent')
        api_count = sum(1 for b in blocks if b.get('type') == 'api')
        starter_count = sum(1 for b in blocks if b.get('type') == 'starter')
        
        # Categorize based on content
        workflow_content = str(workflow).lower() + str(state).lower()
        
        if agent_count > 0:
            categories.append("AI Agents")
            tags.append("ai")
        
        if agent_count >= 3:
            categories.append("Multi-Agent Teams")
            tags.append("multi-agent")
        
        if "web3" in workflow_content or "crypto" in workflow_content or "defi" in workflow_content:
            categories.append("Web3 Automation")
            tags.extend(["web3", "crypto"])
        
        if "trading" in workflow_content or "market" in workflow_content:
            categories.append("Trading Bots")
            tags.extend(["trading", "finance"])
        
        if "email" in workflow_content or "notification" in workflow_content:
            categories.append("Communication")
            tags.append("notifications")
        
        if api_count > 0:
            categories.append("API Integration")
            tags.append("integration")
        
        # Default category if none detected
        if not categories:
            categories.append("Automation")
            tags.append("automation")
        
        # Estimate complexity
        complexity = "Simple"
        if agent_count >= 2 or api_count >= 2:
            complexity = "Medium"
        if agent_count >= 3 or (agent_count >= 1 and api_count >= 3):
            complexity = "Complex"
        
        return {
            "workflow_id": workflow_id,
            "name": workflow['name'],
            "description": workflow.get('description', 'No description provided'),
            "categories": categories,
            "tags": tags,
            "complexity": complexity,
            "stats": {
                "agent_count": agent_count,
                "api_count": api_count,
                "total_blocks": len(blocks),
                "estimated_runtime": "24/7" if starter_count > 0 else "On-demand"
            },
            "marketplace_ready": workflow.get('is_published', False),
            "pricing_model": "usage-based" if agent_count > 0 else "free"
        }
        
    except Exception as e:
        logger.error(f"Error getting marketplace preview: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/workflows/templates/{template_name}")
async def create_from_template(
    template_name: str,
    customization: Dict[str, Any] = Body(default={})
):
    """
    Create workflow from Agent Forge marketplace templates
    """
    try:
        # Import template functions
        from src.services.templates import get_template_by_name, create_workflow_from_template
        
        # Get template
        template = get_template_by_name(template_name)
        if not template:
            available_templates = [
                "lead_generation", "trading_bot", "multi_agent_research", 
                "customer_support", "web3_automation", "data_pipeline",
                "content_generation", "notification_system"
            ]
            raise HTTPException(
                status_code=404, 
                detail=f"Template '{template_name}' not found. Available: {available_templates}"
            )
        
        # Create workflow from template
        workflow_data = create_workflow_from_template(template, customization)
        
        # Save to database
        workflow_id = await db_service.create_workflow(workflow_data)
        
        if not workflow_id:
            raise HTTPException(status_code=500, detail="Failed to create workflow")
        
        return {
            "workflow_id": workflow_id,
            "name": workflow_data['name'],
            "template_used": template_name,
            "customizations_applied": list(customization.keys()),
            "message": f"Successfully created workflow from {template_name} template"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating from template: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workflows/{workflow_id}/export")
async def export_workflow(workflow_id: str, format: str = "json"):
    """
    Export workflow in various formats for sharing or backup
    """
    try:
        workflow = await db_service.get_workflow_with_blocks(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        if format == "json":
            # Export as Agent Forge JSON
            export_data = {
                "format": "agent-forge-workflow",
                "version": "1.0.0",
                "exported_at": datetime.utcnow().isoformat(),
                "workflow": {
                    "id": workflow['id'],
                    "name": workflow['name'],
                    "description": workflow.get('description'),
                    "state": workflow.get('state'),
                    "blocks": workflow.get('blocks', []),
                    "metadata": {
                        "block_count": len(workflow.get('blocks', [])),
                        "agent_count": sum(1 for b in workflow.get('blocks', []) if b.get('type') == 'agent'),
                        "created_at": workflow.get('created_at'),
                        "updated_at": workflow.get('updated_at')
                    }
                }
            }
            return export_data
        
        elif format == "yaml":
            # Convert to YAML-friendly format
            import yaml
            yaml_data = {
                "name": workflow['name'],
                "description": workflow.get('description'),
                "blocks": [
                    {
                        "id": block['id'],
                        "type": block['type'],
                        "name": block['name'],
                        "config": block.get('sub_blocks', {})
                    }
                    for block in workflow.get('blocks', [])
                ]
            }
            return {"format": "yaml", "data": yaml.dump(yaml_data)}
        
        else:
            raise HTTPException(status_code=400, detail="Unsupported format. Use 'json' or 'yaml'")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates")
async def list_templates():
    """
    List all available Agent Forge workflow templates
    """
    try:
        from src.services.templates import get_all_templates
        
        templates = get_all_templates()
        
        return {
            "templates": templates,
            "total_count": len(templates),
            "categories": list(set(t.get('category', 'General') for t in templates))
        }
        
    except Exception as e:
        logger.error(f"Error listing templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/workflows/{workflow_id}/validate")
async def validate_workflow_state(workflow_id: str):
    """Validate existing workflow state"""
    try:
        # Get workflow
        workflow = await db_service.get_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Get current state
        state = workflow.get('state')
        if not state:
            raise HTTPException(status_code=400, detail="Workflow has no state")
        
        # Parse state if it's a string
        if isinstance(state, str):
            try:
                state = json.loads(state)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid state format")
        
        # Validate
        validation_report = await validator.validate_state(state, workflow_id)
        
        return {
            "workflow_id": workflow_id,
            "validation_report": validation_report.dict(),
            "summary": {
                "valid": validation_report.overall_valid,
                "agent_forge_compliant": validation_report.agent_forge_compliance,
                "error_count": sum(len(r.errors) for r in validation_report.validation_results),
                "warning_count": sum(len(r.warnings) for r in validation_report.validation_results)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating state: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workflows/{workflow_id}/state")
async def get_workflow_state(workflow_id: str):
    """Get current workflow state"""
    try:
        workflow = await db_service.get_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        blocks = await db_service.get_workflow_blocks(workflow_id)
        
        return {
            "workflow_id": workflow_id,
            "name": workflow['name'],
            "description": workflow.get('description'),
            "state": workflow.get('state'),
            "block_count": len(blocks),
            "block_types": list(set(b['type'] for b in blocks))
        }
        
    except Exception as e:
        logger.error(f"Error getting workflow state: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/block-types")
async def get_block_types():
    """Get available Agent Forge block types with schemas"""
    return {
        "block_types": {
            "starter": {
                "description": "Entry point for workflows",
                "sub_blocks": {
                    "startWorkflow": "How the workflow is triggered (manual, webhook, schedule)",
                    "webhookPath": "Path for webhook triggers",
                    "scheduleType": "Type of schedule (daily, hourly, etc.)",
                    "timezone": "Timezone for scheduled runs"
                }
            },
            "agent": {
                "description": "AI agent for processing and decision-making",
                "sub_blocks": {
                    "model": "AI model to use (gpt-4, claude-3, gemini-pro)",
                    "systemPrompt": "Instructions for the agent",
                    "temperature": "Creativity level (0-1)",
                    "tools": "Available tools for the agent"
                }
            },
            "api": {
                "description": "External API integration",
                "sub_blocks": {
                    "url": "API endpoint URL",
                    "method": "HTTP method (GET, POST, etc.)",
                    "headers": "Request headers",
                    "params": "Query parameters",
                    "body": "Request body"
                }
            },
            "output": {
                "description": "Output destination for results",
                "sub_blocks": {
                    "outputType": "Type of output (email, sms, webhook)",
                    "channels": "Output channels to use",
                    "configuration": "Channel-specific settings"
                }
            },
            "tool": {
                "description": "Specialized tools (web scraper, BYOI models)",
                "sub_blocks": {
                    "toolType": "Type of tool",
                    "configuration": "Tool-specific settings"
                }
            }
        }
    }

# Template creation functions
def create_trading_bot_template(customization: Dict[str, Any]) -> Dict[str, Any]:
    """Create a trading bot workflow template"""
    workflow_id = str(uuid.uuid4())
    trading_pair = customization.get('trading_pair', 'BTC/USD')
    stop_loss = customization.get('stop_loss', -5)
    take_profit = customization.get('take_profit', 10)
    
    return {
        "id": workflow_id,
        "user_id": "template-user",
        "workspace_id": "template-workspace",
        "name": f"Trading Bot - {trading_pair}",
        "description": f"Automated trading bot for {trading_pair} with {stop_loss}% stop-loss",
        "state": {
            "blocks": {},
            "edges": [],
            "subflows": {},
            "variables": {
                "TRADING_PAIR": trading_pair,
                "STOP_LOSS": stop_loss,
                "TAKE_PROFIT": take_profit
            },
            "metadata": {
                "version": "1.0.0",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z"
            }
        },
        "color": "#FF6B6B",
        "last_synced": datetime.utcnow(),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

def create_lead_gen_template(customization: Dict[str, Any]) -> Dict[str, Any]:
    """Create a lead generation workflow template"""
    workflow_id = str(uuid.uuid4())
    source = customization.get('source', 'website')
    
    return {
        "id": workflow_id,
        "user_id": "template-user",
        "workspace_id": "template-workspace",
        "name": f"Lead Generation - {source}",
        "description": f"Automated lead capture and qualification from {source}",
        "state": {
            "blocks": {},
            "edges": [],
            "subflows": {},
            "variables": {},
            "metadata": {
                "version": "1.0.0",
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "updatedAt": datetime.utcnow().isoformat() + "Z"
            }
        },
        "color": "#4ECDC4",
        "last_synced": datetime.utcnow(),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

# Template endpoints
@router.post("/workflows/templates/{template_name}")
async def create_from_template(
    template_name: str,
    customization: Dict[str, Any] = Body(default={})
):
    """Create workflow from Agent Forge marketplace templates"""
    
    # Template mapping
    templates = {
        "trading_bot": create_trading_bot_template,
        "lead_generation": create_lead_gen_template,
        "multi_agent_research": lambda c: create_lead_gen_template(c),  # Reuse for now
        "web3_automation": lambda c: create_trading_bot_template(c)     # Reuse for now
    }
    
    if template_name not in templates:
        raise HTTPException(
            status_code=404, 
            detail=f"Template '{template_name}' not found. Available templates: {list(templates.keys())}"
        )
    
    # Generate workflow from template
    workflow_data = templates[template_name](customization)
    
    # In a real implementation, you would save this to the database
    # For now, we'll just return the generated workflow
    
    return {
        "workflow_id": workflow_data["id"],
        "name": workflow_data["name"],
        "description": workflow_data["description"],
        "template": template_name,
        "customization": customization,
        "message": f"Created from {template_name} template",
        "next_steps": [
            f"POST /api/workflows/{workflow_data['id']}/generate-state to generate AI state",
            f"GET /api/workflows/{workflow_data['id']}/state to view the workflow"
        ]
    }

@router.get("/templates")
async def list_templates():
    """List all available workflow templates"""
    return {
        "templates": [
            {
                "name": "trading_bot",
                "display_name": "Crypto Trading Bot",
                "description": "Automated trading with stop-loss and take-profit",
                "category": "Web3 Trading",
                "customizable_fields": ["trading_pair", "stop_loss", "take_profit"]
            },
            {
                "name": "lead_generation",
                "display_name": "Lead Generation System",
                "description": "Capture and qualify leads from multiple sources",
                "category": "Sales & Marketing",
                "customizable_fields": ["source", "crm_integration"]
            },
            {
                "name": "multi_agent_research",
                "display_name": "Multi-Agent Research Team",
                "description": "Collaborative AI agents for research tasks",
                "category": "AI Automation",
                "customizable_fields": ["research_topic", "agent_count"]
            },
            {
                "name": "web3_automation",
                "display_name": "Web3 DeFi Automation",
                "description": "Smart contract monitoring and DeFi operations",
                "category": "Blockchain",
                "customizable_fields": ["chain", "contract_address"]
            }
        ]
    } 