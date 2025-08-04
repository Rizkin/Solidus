# src/api/workflows.py
from fastapi import APIRouter, HTTPException, Body
from typing import Optional
import logging
from src.services.state_generator import state_generator
from src.services.validation import validator
from src.utils.database_hybrid import db_service
from src.models.schemas import StateGenerationOptions

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["workflows"])

@router.post("/workflows/{workflow_id}/generate-state")
async def generate_workflow_state(
    workflow_id: str,
    options: Optional[StateGenerationOptions] = Body(default=None)
):
    """Generate Agent Forge-compatible workflow state using AI"""
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
        
        return {
            "workflow_id": workflow_id,
            "generated_state": generated_state,
            "validation_report": validation_report.dict(),
            "agent_forge_pattern": pattern,
            "generation_metadata": {
                "model": "claude-3-opus",
                "platform": "agent-forge",
                "options": options.dict()
            }
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating state: {e}")
        raise HTTPException(status_code=500, detail=f"State generation failed: {str(e)}")

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
