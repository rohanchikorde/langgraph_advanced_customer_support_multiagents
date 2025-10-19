#!/usr/bin/env python3
"""
Simple HTTP server to serve the frontend.
Run this script to start the frontend server on port 3000.
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 3000
DIRECTORY = Path(__file__).parent / "frontend"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def run_server():
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"🚀 Frontend server running at http://localhost:{PORT}")
        print("📱 Make sure the backend API server is running on http://127.0.0.1:8000")
        print("📋 API Docs: http://127.0.0.1:8000/docs")
        print("🛑 Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")
            httpd.shutdown()

if __name__ == "__main__":
    run_server()