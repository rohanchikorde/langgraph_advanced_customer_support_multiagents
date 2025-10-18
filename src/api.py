from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import uuid
from datetime import datetime

from .graph import create_graph
from .memory import agent_memory

# Pydantic models for API requests/responses
class CustomerQueryRequest(BaseModel):
    query: str = Field(..., description="Customer's question or issue")
    user_id: Optional[str] = Field(None, description="Unique user identifier (auto-generated if not provided)")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context or metadata")

class CustomerQueryResponse(BaseModel):
    conversation_id: str
    user_id: str
    query: str
    response: str
    categories: List[str]
    satisfactory: bool
    escalation_needed: bool
    processing_time: float
    timestamp: datetime

class ConversationHistoryResponse(BaseModel):
    user_id: str
    total_conversations: int
    recent_conversations: List[Dict[str, Any]]
    common_issues: Dict[str, int]

class SystemStatsResponse(BaseModel):
    total_conversations: int
    resolved_issues: int
    active_users: int
    memory_patterns: int
    knowledge_base_entries: int

# FastAPI app
app = FastAPI(
    title="Advanced Customer Support Multi-Agent API",
    description="API for LangGraph-powered multi-agent customer service system with memory and learning capabilities",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global graph instance (in production, consider connection pooling)
graph_app = None

def get_graph():
    """Lazy initialization of the graph to avoid multiprocessing issues."""
    global graph_app
    if graph_app is None:
        graph_app = create_graph()
    return graph_app

@app.post("/api/v1/support/query", response_model=CustomerQueryResponse)
async def process_customer_query(request: CustomerQueryRequest, background_tasks: BackgroundTasks):
    """
    Process a customer support query through the multi-agent system.

    This endpoint:
    - Classifies the query
    - Applies memory and learning
    - Routes to appropriate agents
    - Returns personalized response
    """
    try:
        import time
        start_time = time.time()

        # Generate user_id if not provided
        user_id = request.user_id or f"user_{uuid.uuid4().hex[:8]}"

        # Prepare initial state
        initial_state = {
            "query": request.query,
            "user_id": user_id,
            "categories": [],
            "entities": {},
            "sentiment": None,
            "priority": None,
            "response": None,
            "escalation_needed": False,
            "attempts": 0,  # Start from 0 for API calls
            "conversation_history": [],
            "satisfactory": None,
            "similar_past_issues": [],
            "knowledge_base_entry": None,
            "memory_loaded": False
        }

        # Process through the graph
        result = get_graph().invoke(initial_state)

        processing_time = time.time() - start_time

        # Prepare response
        response = CustomerQueryResponse(
            conversation_id=f"conv_{uuid.uuid4().hex}",
            user_id=user_id,
            query=request.query,
            response=result.get("response", "I'm sorry, I couldn't process your request at this time."),
            categories=result.get("categories", []),
            satisfactory=result.get("satisfactory", False),
            escalation_needed=result.get("escalation_needed", False),
            processing_time=round(processing_time, 2),
            timestamp=datetime.now()
        )

        # Background task to log analytics (optional)
        background_tasks.add_task(log_query_analytics, request, response)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/api/v1/support/history/{user_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(user_id: str, limit: int = 10):
    """
    Get conversation history for a specific user.

    Returns recent conversations and common issues for personalization.
    """
    try:
        profile = agent_memory.get_user_profile(user_id)

        # Get recent conversations (limited)
        recent_conversations = profile.get("conversation_history", [])[-limit:]

        response = ConversationHistoryResponse(
            user_id=user_id,
            total_conversations=profile.get("total_interactions", 0),
            recent_conversations=recent_conversations,
            common_issues=profile.get("common_issues", {})
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

@app.get("/api/v1/support/stats", response_model=SystemStatsResponse)
async def get_system_stats():
    """
    Get system-wide statistics and performance metrics.
    """
    try:
        stats = agent_memory.get_memory_stats()

        # Count unique users
        user_profiles = agent_memory.memory.get("user_profiles", {})
        active_users = len(user_profiles)

        # Count successful patterns
        patterns = agent_memory.memory.get("successful_patterns", {})
        memory_patterns = len(patterns)

        # Count knowledge base entries
        kb = agent_memory.memory.get("knowledge_base", {})
        knowledge_base_entries = len(kb)

        response = SystemStatsResponse(
            total_conversations=stats.get("total_conversations", 0),
            resolved_issues=stats.get("resolved_issues", 0),
            active_users=active_users,
            memory_patterns=memory_patterns,
            knowledge_base_entries=knowledge_base_entries
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")

@app.post("/api/v1/support/feedback")
async def submit_feedback(conversation_id: str, user_id: str, rating: int, feedback: Optional[str] = None):
    """
    Submit user feedback for a conversation.

    This helps improve the learning system.
    """
    try:
        if not (1 <= rating <= 5):
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

        # In a real implementation, you'd store this feedback
        # For now, we'll just acknowledge it
        feedback_data = {
            "conversation_id": conversation_id,
            "user_id": user_id,
            "rating": rating,
            "feedback": feedback,
            "timestamp": datetime.now()
        }

        # TODO: Store feedback for model improvement
        print(f"Feedback received: {feedback_data}")

        return {"message": "Thank you for your feedback!", "feedback_id": f"fb_{uuid.uuid4().hex}"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting feedback: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0"
    }

# Background tasks
def log_query_analytics(request: CustomerQueryRequest, response: CustomerQueryResponse):
    """
    Log query analytics for monitoring and improvement.
    In production, this could send to analytics service, database, etc.
    """
    try:
        analytics_data = {
            "conversation_id": response.conversation_id,
            "user_id": response.user_id,
            "query_length": len(request.query),
            "categories_count": len(response.categories),
            "processing_time": response.processing_time,
            "satisfactory": response.satisfactory,
            "escalation_needed": response.escalation_needed,
            "timestamp": response.timestamp
        }

        # In production, send to logging/monitoring service
        print(f"Analytics: {analytics_data}")

    except Exception as e:
        print(f"Error logging analytics: {e}")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": True,
        "message": exc.detail,
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return {
        "error": True,
        "message": "Internal server error",
        "status_code": 500
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)