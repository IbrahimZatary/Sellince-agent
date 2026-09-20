from decimal import Decimal, InvalidOperation

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agent.runner import run_agent_turn
from app.core.database import get_db
from app.core.exceptions import AppException
from app.models.conversation import Conversation
from app.models.customer import Customer
from app.models.message import Message
from app.models.offer import Offer
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])


def _to_decimal(value) -> Decimal | None:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


def _get_open_conversation(
    db: Session,
    customer_id: int,
    company_id: int,
) -> Conversation:
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.customer_id == customer_id,
            Conversation.company_id == company_id,
            Conversation.status == "open",
        )
        .order_by(Conversation.started_at.desc())
        .first()
    )
    if not conversation:
        conversation = Conversation(
            customer_id=customer_id,
            company_id=company_id,
            status="open",
        )
        db.add(conversation)
        db.flush()
    return conversation


@router.post("", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    db: Session = Depends(get_db),
):
    customer = db.query(Customer).filter(Customer.id == req.customer_id).first()
    if not customer:
        raise AppException(
            status_code=404,
            error_code="CUSTOMER_NOT_FOUND",
            message="Customer not found",
        )

    conversation = _get_open_conversation(
        db,
        customer_id=req.customer_id,
        company_id=customer.company_id,
    )

    result = run_agent_turn(
        conversation_id=conversation.id,
        state={
            "customer_id": req.customer_id,
            "message": req.message,
        },
    )

    db.add_all(
        [
            Message(
                conversation_id=conversation.id,
                sender="customer",
                text=req.message,
            ),
            Message(
                conversation_id=conversation.id,
                sender="agent",
                text=result["response"],
            ),
        ]
    )

    offer = result.get("offer")
    if offer:
        price = _to_decimal(offer.get("price"))
        if price is not None:
            db.add(
                Offer(
                    customer_id=req.customer_id,
                    conversation_id=conversation.id,
                    company_id=customer.company_id,
                    product_name=str(offer.get("product") or "Special Offer"),
                    price=price,
                    status="sent",
                )
            )

    db.commit()

    return ChatResponse(
        response=result["response"],
        offer=result["offer"],
        action=result["action"],
        conversation_stage=result.get("conversation_stage"),
    )