#!/usr/bin/env python3
"""
Test script for Agent Memory & Learning functionality
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.memory import agent_memory

def test_memory_system():
    """Test the memory system functionality"""
    print("Testing Agent Memory & Learning System")
    print("=" * 50)

    # Use unique user ID for testing
    import time
    user_id = f"test_user_{int(time.time())}"
    profile = agent_memory.get_user_profile(user_id)
    assert profile is not None, "User profile should be created"
    assert profile["total_interactions"] == 0, "New user should have 0 interactions"
    print("✓ User profile created successfully")

    # Test 2: Conversation saving
    print("2. Testing conversation saving...")
    test_conversation = {
        "query": "I have a billing issue with order 12345",
        "categories": ["billing", "technical"],
        "entities": {"order_id": "12345"},
        "response": "I've checked your order. Here's how to resolve it...",
        "satisfactory": True
    }

    agent_memory.save_conversation(user_id, test_conversation)

    # Verify conversation was saved
    updated_profile = agent_memory.get_user_profile(user_id)
    assert updated_profile["total_interactions"] == 1, "Should have 1 interaction"
    assert len(updated_profile["conversation_history"]) == 1, "Should have 1 conversation"
    assert updated_profile["conversation_history"][0]["query"] == test_conversation["query"], "Query should match"
    print("✓ Conversation saved successfully")

    # Test 3: Similar issues detection
    print("3. Testing similar issues detection...")
    similar_issues = agent_memory.find_similar_past_issues(
        user_id=user_id,
        current_query="billing problem with order 12345",
        categories=["billing"]
    )
    assert len(similar_issues) > 0, "Should find similar issues"
    print(f"✓ Found {len(similar_issues)} similar issues")

    # Test 4: Knowledge base update
    print("4. Testing knowledge base update...")
    agent_memory.update_knowledge_base(
        categories=["billing", "technical"],
        query="billing issue with order",
        resolution="Check payment status and contact support"
    )

    kb_entry = agent_memory.get_knowledge_base_entry(["billing", "technical"])
    assert kb_entry is not None, "Should find knowledge base entry"
    assert "billing_technical" in kb_entry or any("billing" in cat for cat in kb_entry.get("categories", [])), "Should match categories"
    print("✓ Knowledge base updated successfully")

    # Test 5: Memory statistics
    print("5. Testing memory statistics...")
    stats = agent_memory.get_memory_stats()
    assert stats["total_conversations"] >= 1, "Should have at least 1 conversation"
    assert stats["resolved_issues"] >= 1, "Should have at least 1 resolved issue"
    print(f"✓ Memory stats: {stats}")

    print("\n" + "=" * 50)
    print("All tests passed! Agent Memory & Learning system is working correctly.")
    print("=" * 50)

if __name__ == "__main__":
    test_memory_system()