from typing import TypedDict, Optional , NotRequired


class AgentState(TypedDict):
    customer_id: int
    conversation_id: int
    message: str

    #Existing customer information 
    customer_data: Optional[dict]


    ## Determines which workflow starts
    entry_type: NotRequired[str]

    # Proactive Agent
    customer_profile: NotRequired[dict | None]
    active_offer: NotRequired[dict | None]


    trigger_reason: Optional[str]
    intent: Optional[dict]
    recommendation: Optional[dict]

    # Multi-turn conversation
    conversation_stage: Optional[str]

    response: Optional[str]
    offer: Optional[dict]
    action: Optional[dict]