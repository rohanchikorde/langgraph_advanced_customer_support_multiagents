import os
from dotenv import load_dotenv

load_dotenv()

# Set OpenRouter API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")

from src.graph import graph

def main():
    # topic = input("Enter the essay topic: ")
    topic = "The Impact of Artificial Intelligence on Society"  # Test topic
    
    initial_state = {
        "topic": topic,
        "current_essay": None,
        "feedback": None,
        "iteration": 0,
        "max_iterations": 5,
        "approved": False
    }
    
    config = {"configurable": {"thread_id": "essay_thread"}}
    
    for event in graph.stream(initial_state, config):
        for node, state in event.items():
            print(f"Node: {node}")
            if node == "write_essay":
                print("Essay written.")
            elif node == "critique_essay":
                print(f"Feedback: {state.get('feedback')}")
                if state.get("approved"):
                    print("Essay approved!")
                    break
    
    final_state = graph.get_state(config).values
    print("\nFinal Essay:")
    print(final_state["current_essay"])

if __name__ == "__main__":
    main()