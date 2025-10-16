from langgraph.graph import StateGraph, END
from state import CustomerServiceState
from nodes import (
    classify_query, analyze_sentiment, handle_billing, handle_technical,
    handle_returns, handle_general, escalate, generate_response, validate_response, collaborate
)

# Router functions
def route_after_classify(state: CustomerServiceState) -> str:
    categories = state['categories']
    if len(categories) > 1:
        return "collaboration"
    elif categories[0] == "technical":
        return "technical_handler"
    elif categories[0] == "billing":
        return "billing_handler"
    elif categories[0] == "returns":
        return "returns_handler"
    else:
        return "general_handler"

def route_after_sentiment(state: CustomerServiceState) -> str:
    # Always try to handle first, regardless of sentiment
    return route_after_classify(state)

def route_after_validate(state: CustomerServiceState) -> str:
    if state.get('satisfactory'):
        return END
    elif state['attempts'] >= 3:
        return "escalate"
    else:
        return "generate_response"

# Build graph
def create_graph():
    graph = StateGraph(CustomerServiceState)

    # Add nodes
    graph.add_node("classify", classify_query)
    graph.add_node("sentiment", analyze_sentiment)
    graph.add_node("technical_handler", handle_technical)
    graph.add_node("billing_handler", handle_billing)
    graph.add_node("returns_handler", handle_returns)
    graph.add_node("general_handler", handle_general)
    graph.add_node("collaboration", collaborate)
    graph.add_node("escalate", escalate)
    graph.add_node("generate_response", generate_response)
    graph.add_node("validate", validate_response)

    # Add edges
    graph.set_entry_point("classify")
    graph.add_edge("classify", "sentiment")
    graph.add_conditional_edges("sentiment", route_after_sentiment)
    graph.add_edge("technical_handler", "generate_response")
    graph.add_edge("billing_handler", "generate_response")
    graph.add_edge("returns_handler", "generate_response")
    graph.add_edge("general_handler", "generate_response")
    graph.add_edge("collaboration", "generate_response")
    graph.add_edge("generate_response", "validate")
    graph.add_conditional_edges("validate", route_after_validate)
    graph.add_edge("escalate", END)

    # Compile
    return graph.compile()