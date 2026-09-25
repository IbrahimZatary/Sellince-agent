from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    customer_id: int = Field(..., gt=0)
    message: str = Field(..., min_length=1)

class ActionPayload(BaseModel):
    label: str
    url: str

class ChatResponse(BaseModel):
    response: str
    offer: Optional[Dict[str, Any]] = None
    action: str = Field(..., description="Action: show_offer, route_checkout, ask_question")
    action_payload: Optional[ActionPayload] = None
