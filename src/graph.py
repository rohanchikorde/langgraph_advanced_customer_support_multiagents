from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.state import EssayState
from src.agents import create_essay_agent, create_critique_agent

# Agents
essay_agent = create_essay_agent()
critique_agent = create_critique_agent()

# Nodes
def write_essay(state: EssayState) -> EssayState:
    essay = essay_agent.invoke({
        "topic": state["topic"],
        "current_essay": state.get("current_essay", ""),
        "feedback": state.get("feedback", "")
    })
    return {"current_essay": essay, "iteration": state["iteration"] + 1}

def critique_essay(state: EssayState) -> EssayState:
    feedback = critique_agent.invoke({
        "topic": state["topic"],
        "essay": state["current_essay"]
    })
    # Parse feedback: if contains "OK", approved
    approved = "OK" in feedback.upper()
    return {"feedback": feedback, "approved": approved}

# Graph
workflow = StateGraph(EssayState)

workflow.add_node("write_essay", write_essay)
workflow.add_node("critique_essay", critique_essay)

workflow.set_entry_point("write_essay")

workflow.add_edge("write_essay", "critique_essay")

def should_continue(state: EssayState) -> str:
    if state["approved"] or state["iteration"] >= state["max_iterations"]:
        return END
    else:
        return "write_essay"

workflow.add_conditional_edges("critique_essay", should_continue)

# Memory
memory = MemorySaver()

graph = workflow.compile(checkpointer=memory)