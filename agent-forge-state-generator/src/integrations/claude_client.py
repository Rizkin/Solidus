# src/integrations/claude_client.py
import os
from typing import Dict, Any, Optional
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
import json
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class ClaudeClient:
    """Claude API client for generating workflow states"""
    
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = "claude-3-opus-20240229"  # Latest Claude model
    
    async def generate_workflow_state(self, prompt: str) -> Dict[str, Any]:
        """Generate workflow state using Claude"""
        try:
            logger.info("Sending request to Claude API...")
            
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.3,  # Lower temperature for more consistent JSON
                system="You are an expert at generating Agent Forge workflow states. Always respond with valid JSON only, no explanations or markdown.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract the text content
            content = response.content[0].text
            logger.info(f"Claude response received: {len(content)} characters")
            
            # Parse JSON response
            try:
                # Clean up the response (remove markdown if any)
                content = content.strip()
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                
                state = json.loads(content.strip())
                return state
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Claude response as JSON: {e}")
                logger.error(f"Response was: {content[:500]}...")
                return None
                
        except Exception as e:
            logger.error(f"Error calling Claude API: {e}")
            return None
    
    async def analyze_workflow_pattern(self, workflow_data: Dict[str, Any]) -> str:
        """Analyze workflow to identify Agent Forge patterns"""
        prompt = f"""
        Analyze this workflow data and identify the Agent Forge pattern:
        {json.dumps(workflow_data, indent=2)}
        
        Respond with one of these patterns:
        - lead_generation
        - trading_bot
        - multi_agent_research
        - customer_support
        - web3_automation
        - data_pipeline
        - content_generation
        
        Just respond with the pattern name, nothing else.
        """
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=50,
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text.strip().lower()
        except Exception as e:
            logger.error(f"Error analyzing pattern: {e}")
            return "unknown"

# Create singleton instance
claude_client = ClaudeClient()
