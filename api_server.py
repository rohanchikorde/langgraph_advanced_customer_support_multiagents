#!/usr/bin/env python3
"""
FastAPI server for the Advanced Customer Support Multi-Agent System.

This server provides REST API endpoints for frontend integration,
allowing web applications to interact with the LangGraph-powered
customer service system.

Usage:
    python api_server.py

The server will start on http://localhost:8000
API documentation available at http://localhost:8000/docs
"""

import uvicorn
from src.api import app

if __name__ == "__main__":
    print("🚀 Starting Advanced Customer Support Multi-Agent API Server")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔗 Redoc Documentation: http://localhost:8000/redoc")
    print("💡 Health Check: http://localhost:8000/health")

    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )