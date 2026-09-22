from pydantic import BaseModel


class ChatRequest(BaseModel):
    customer_id: int
    message: str


class ChatResponse(BaseModel):
    response: str
    offer: dict | None
    action: str | dict | None = None
    conversation_stage: str | None = None