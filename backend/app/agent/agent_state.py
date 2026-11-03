
from typing import Any, Dict, Optional
from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):
    # Core agent context
    customer_id: int
    conversation_id: int
    message: str

    # Customer data
    customer_data: Optional[Dict[str, Any]]

    # Proactive workflow
    entry_type: str
    customer_profile: Optional[Dict[str, Any]]
    active_offer: Optional[Dict[str, Any]]

    # Kareem's 4-stage agent pipeline
    trigger_reason: Optional[str]
    intent: Optional[Dict[str, Any]]
    recommendation: Optional[Dict[str, Any]]

    # Conversation management
    conversation_stage: Optional[str]
    history: list[dict[str, str]]

    # Agent output
    response: Optional[str]
    offer: Optional[Dict[str, Any]]
    action: Optional[Dict[str, Any]]
