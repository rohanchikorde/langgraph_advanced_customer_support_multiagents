from src.graph import create_graph

if __name__ == "__main__":
    app = create_graph()
    initial_state = {
        "query": "I have a billing issue with order 12345",
        "user_id": "user123",  # Added user identification
        "categories": [],
        "entities": {},
        "sentiment": None,
        "priority": None,
        "response": None,
        "escalation_needed": False,
        "attempts": 2,
        "conversation_history": [],
        "satisfactory": None,
        "similar_past_issues": [],
        "knowledge_base_entry": None,
        "memory_loaded": False
    }
    try:
        result = app.invoke(initial_state)
        print("Final state:", result)
    except Exception as e:
        print("Error:", e)