"""
Vercel handler for FastAPI application
Routes requests to the main FastAPI app with full functionality
"""
from src.main import app

# Export the FastAPI app for Vercel
# This allows Vercel to serve the FastAPI application as a serverless function
handler = app 