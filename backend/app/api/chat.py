from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agent.graph import compiled_graph
from app.api.auth import get_current_user
from app.core.database import get_db
from app.core.exceptions import AppException
from app.models.customer import Customer
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    customer = db.query(Customer).filter(Customer.id == req.customer_id).first()
    if not customer or customer.company_id != current_user.company_id:
        raise AppException(
            status_code=404,
            error_code="CUSTOMER_NOT_FOUND",
            message="Customer not found",
        )

    result = compiled_graph.invoke(
        {
            "customer_id": req.customer_id,
            "message": req.message,
            "_db": db,
        }
    )
    return ChatResponse(
        response=result["response"],
        offer=result["recommendation"]["primary"]
        if result["recommendation"]
        else None,
        action=result["action"],
    )
