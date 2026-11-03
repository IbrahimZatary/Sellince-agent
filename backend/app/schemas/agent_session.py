
from pydantic import BaseModel, Field


class StartSessionRequest(BaseModel):
    customer_id: int = Field(gt=0)


class StartSessionResponse(BaseModel):
    conversation_id: int
    status: str
    response: str | None = None
    offer: dict | None = None
