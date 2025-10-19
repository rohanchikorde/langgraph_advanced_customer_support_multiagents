#!/usr/bin/env python3
"""
Combined server script to run both frontend and backend.
This script starts the FastAPI backend and serves the frontend.
"""

import subprocess
import sys
import time
import threading
import os
from pathlib import Path

def run_backend():
    """Run the FastAPI backend server"""
    print("🔧 Starting backend API server...")
    try:
        # Import and run the API server
        sys.path.insert(0, str(Path(__file__).parent))
        from api_server import app
        import uvicorn

        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            workers=1,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        sys.exit(1)

def run_frontend():
    """Run the frontend HTTP server"""
    print("🌐 Starting frontend server...")
    time.sleep(2)  # Wait for backend to start

    try:
        # Run the frontend server
        subprocess.run([
            sys.executable, "frontend_server.py"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting frontend: {e}")
        sys.exit(1)

def main():
    print("🤖 Advanced Customer Support System")
    print("=" * 50)
    print("🚀 Starting both frontend and backend servers...")
    print()

    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()

    # Start frontend (this will block)
    run_frontend()

if __name__ == "__main__":
    main()