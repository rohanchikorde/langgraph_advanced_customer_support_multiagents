#!/usr/bin/env python3
"""
Test script for the FastAPI endpoints.

This script tests the API endpoints to ensure they work correctly.
Run this after starting the API server with: python api_server.py
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        print("✓ Health check passed")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_customer_query():
    """Test the customer query endpoint"""
    print("Testing customer query endpoint...")
    try:
        payload = {
            "query": "I have a billing issue with order 12345",
            "user_id": "test_user_api"
        }

        response = requests.post(
            f"{API_BASE_URL}/api/v1/support/query",
            json=payload,
            timeout=30
        )

        assert response.status_code == 200
        data = response.json()

        # Check required fields
        required_fields = ["conversation_id", "user_id", "query", "response",
                          "categories", "satisfactory", "processing_time", "timestamp"]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

        assert data["user_id"] == "test_user_api"
        assert data["query"] == payload["query"]
        assert isinstance(data["categories"], list)
        assert isinstance(data["processing_time"], (int, float))

        print(f"✓ Customer query processed in {data['processing_time']} seconds")
        print(f"  Response: {data['response'][:100]}...")
        return data

    except Exception as e:
        print(f"✗ Customer query test failed: {e}")
        return None

def test_conversation_history(query_data):
    """Test the conversation history endpoint"""
    print("Testing conversation history endpoint...")
    try:
        user_id = query_data["user_id"]
        response = requests.get(f"{API_BASE_URL}/api/v1/support/history/{user_id}")

        assert response.status_code == 200
        data = response.json()

        required_fields = ["user_id", "total_conversations", "recent_conversations", "common_issues"]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

        assert data["user_id"] == user_id
        assert data["total_conversations"] >= 1

        print(f"✓ Retrieved history for user {user_id}: {data['total_conversations']} conversations")
        return data

    except Exception as e:
        print(f"✗ Conversation history test failed: {e}")
        return None

def test_system_stats():
    """Test the system statistics endpoint"""
    print("Testing system statistics endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/support/stats")

        assert response.status_code == 200
        data = response.json()

        required_fields = ["total_conversations", "resolved_issues", "active_users",
                          "memory_patterns", "knowledge_base_entries"]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

        print(f"✓ System stats: {data['total_conversations']} conversations, "
              f"{data['active_users']} active users")
        return data

    except Exception as e:
        print(f"✗ System stats test failed: {e}")
        return None

def test_feedback():
    """Test the feedback submission endpoint"""
    print("Testing feedback submission endpoint...")
    try:
        payload = {
            "conversation_id": "test_conv_123",
            "user_id": "test_user_api",
            "rating": 5,
            "feedback": "Great API!"
        }

        response = requests.post(
            f"{API_BASE_URL}/api/v1/support/feedback",
            json=payload
        )

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "feedback_id" in data

        print("✓ Feedback submitted successfully")
        return data

    except Exception as e:
        print(f"✗ Feedback test failed: {e}")
        return None

def run_api_tests():
    """Run all API tests"""
    print("🧪 Starting API Endpoint Tests")
    print("=" * 50)

    # Test health check first
    if not test_health_check():
        print("❌ API server not running. Please start with: python api_server.py")
        return

    # Test customer query
    query_result = test_customer_query()
    if not query_result:
        print("❌ Cannot continue tests without successful query")
        return

    # Test other endpoints
    test_conversation_history(query_result)
    test_system_stats()
    test_feedback()

    print("=" * 50)
    print("✅ All API tests completed!")

if __name__ == "__main__":
    run_api_tests()