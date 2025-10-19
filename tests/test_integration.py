#!/usr/bin/env python3
"""
Test script for the frontend-backend integration.
This script tests the complete system end-to-end.
"""

import requests
import time
import subprocess
import sys
from pathlib import Path

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_frontend_available():
    """Test if frontend is accessible"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_chat_endpoint():
    """Test the chat functionality"""
    try:
        payload = {
            "query": "Hello, I need help with my order",
            "user_id": "test_user_frontend"
        }
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/support/query",
            json=payload,
            timeout=30
        )
        return response.status_code == 200 and 'response' in response.json()
    except:
        return False

def test_frontend_files():
    """Test if frontend files are accessible"""
    files_to_test = ['index.html', 'styles.css', 'script.js']
    for file in files_to_test:
        try:
            response = requests.get(f"http://localhost:3000/{file}", timeout=5)
            if response.status_code != 200:
                return False
        except:
            return False
    return True

def run_integration_test():
    """Run complete integration test"""
    print("🧪 Testing Frontend-Backend Integration")
    print("=" * 50)

    # Test backend
    print("1. 🔍 Testing backend health...")
    if test_backend_health():
        print("   ✅ Backend is running")
    else:
        print("   ❌ Backend is not running")
        return False

    # Test frontend
    print("2. 🌐 Testing frontend availability...")
    if test_frontend_available():
        print("   ✅ Frontend is accessible")
    else:
        print("   ❌ Frontend is not accessible")
        return False

    # Test frontend files
    print("3. 📁 Testing frontend files...")
    if test_frontend_files():
        print("   ✅ All frontend files are accessible")
    else:
        print("   ❌ Some frontend files are missing")
        return False

    # Test chat functionality
    print("4. 💬 Testing chat endpoint...")
    if test_chat_endpoint():
        print("   ✅ Chat functionality working")
    else:
        print("   ❌ Chat functionality failed")
        return False

    print()
    print("🎉 All integration tests passed!")
    print("🌐 Frontend URL: http://localhost:3000")
    print("🔧 Backend API: http://127.0.0.1:8000")
    print("📚 API Docs: http://127.0.0.1:8000/docs")
    return True

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--start-servers":
        # Start both servers
        print("🚀 Starting servers for testing...")
        try:
            subprocess.run([
                sys.executable, "run_servers.py"
            ], check=True)
        except KeyboardInterrupt:
            print("\n👋 Servers stopped")
    else:
        # Just run tests
        success = run_integration_test()
        if not success:
            print("\n❌ Integration test failed")
            print("💡 Make sure both servers are running:")
            print("   python run_servers.py")
            sys.exit(1)

if __name__ == "__main__":
    main()