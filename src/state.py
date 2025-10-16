from typing import TypedDict, Optional, Dict, Any, List

class CustomerServiceState(TypedDict):
    query: str
    user_id: str  # Added for memory tracking
    categories: List[str]
    entities: Dict[str, Any]
    sentiment: Optional[str]
    priority: Optional[str]
    response: Optional[str]
    escalation_needed: bool
    attempts: int
    conversation_history: List[str]
    satisfactory: Optional[bool]
    # Memory-related fields
    similar_past_issues: List[Dict[str, Any]]
    knowledge_base_entry: Optional[Dict[str, Any]]
    memory_loaded: bool