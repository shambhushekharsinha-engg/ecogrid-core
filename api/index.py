"""
Vercel Serverless Entrypoint for EcoGrid Core Enterprise REST API
Exposes FastAPI application instance for Vercel Python Runtime deployment.
"""

import os
import sys

# Add project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.server import app

# Vercel serverless function handler
handler = app
