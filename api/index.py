"""
Vercel serverless function entry point for Agent Forge State Generator
"""
import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import app

# Export for Vercel
application = app
