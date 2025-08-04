"""
Vercel serverless function entry point for Agent Forge State Generator
This file is required for Vercel deployment and acts as the main entry point.
"""

import sys
import os

# Add the src directory to Python path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.main import app

# Vercel expects the FastAPI app to be available as 'app'
# The main.py file already exports 'app', so we just import it
