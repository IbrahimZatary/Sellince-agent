from typing import TypedDict, Optional


class AgentState(TypedDict):
    customer_id: int
    message: str
    customer_data: Optional[dict]
    trigger_reason: Optional[str]
    intent: Optional[dict]
    recommendation: Optional[dict]

    # Multi-turn conversation
    conversation_stage: Optional[str]

    response: Optional[str]
    action: Optional[str]