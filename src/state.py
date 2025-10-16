from typing import TypedDict, Optional, Dict, Any, List

class CustomerServiceState(TypedDict):
    query: str
    categories: List[str]
    entities: Dict[str, Any]
    sentiment: Optional[str]
    priority: Optional[str]
    response: Optional[str]
    escalation_needed: bool
    attempts: int
    conversation_history: List[str]
    satisfactory: Optional[bool]