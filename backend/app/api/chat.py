from typing import Optional
from fastapi import APIRouter, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.customer import Customer
from app.agent.graph import compiled_graph

router = APIRouter(tags=["Chat"])

# Safe schema that accepts the frontend's null value
class SafeChatRequest(BaseModel):
    customer_id: Optional[int] = None
    message: str

@router.post("/chat", status_code=status.HTTP_200_OK)
def chat_endpoint(
    payload: SafeChatRequest,
    db: Session = Depends(get_db)
):
    # If the frontend sends a null ID, safely fall back to the first seeded customer
    real_customer_id = payload.customer_id
    if not real_customer_id:
        customer = db.query(Customer).first()
        real_customer_id = customer.id if customer else 1

    initial_state = {
        "customer_id": real_customer_id,
        "message": payload.message,
    }
    
    result = compiled_graph.invoke(
        initial_state,
        config={"configurable": {"thread_id": str(real_customer_id)}}
    )
    
    return {
        "response": result.get("response"),
        "offer": result.get("offer"),
        "action": result.get("action", "ask_question"),
        "action_payload": result.get("action_payload"),
    }