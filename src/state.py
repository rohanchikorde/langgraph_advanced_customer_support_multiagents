from typing import TypedDict, Optional

class EssayState(TypedDict):
    topic: str
    current_essay: Optional[str]
    feedback: Optional[str]
    iteration: int
    max_iterations: int
    approved: bool