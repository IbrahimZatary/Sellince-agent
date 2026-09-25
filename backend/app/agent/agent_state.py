from typing import Optional, List, Dict, Any
from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):
    customer_id: int
    message: str
    customer_data: Optional[Dict[str, Any]]
    trigger_reason: Optional[str]
    intent: Optional[Dict[str, Any]]
    recommendation: Optional[Dict[str, Any]]
    response: Optional[str]
    offer: Optional[Dict[str, Any]]
    action: Optional[str]
    stage: Optional[str]
    history: List[Dict[str, str]]
    action_payload: dict
