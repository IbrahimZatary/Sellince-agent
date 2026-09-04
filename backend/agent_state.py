from typing import TypedDict, Optional, Any


class AgentState(TypedDict):
    customer_id: int
    message: str
    customer_data: Optional[dict]
    trigger_reason: Optional[str]
    intent: Optional[dict]
    recommendation: Optional[dict]
    response: Optional[str]
    action: Optional[str]
    _db: Optional[Any] 