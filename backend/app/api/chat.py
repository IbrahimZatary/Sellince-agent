
from decimal import Decimal, InvalidOperation

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agent.runner import run_agent_turn
from app.core.database import get_db
from app.core.exceptions import AppException
from app.models.customer import Customer
from app.models.attribution import Attribution
from app.models.message import Message
from app.models.offer import Offer
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.conversation_service import get_open_conversation


router = APIRouter(prefix="/chat", tags=["chat"])


def _to_decimal(value) -> Decimal | None:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


@router.post("", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    db: Session = Depends(get_db),
):
    customer = db.query(Customer).filter(
        Customer.id == req.customer_id
    ).first()

    if not customer:
        raise AppException(
            status_code=404,
            error_code="CUSTOMER_NOT_FOUND",
            message="Customer not found",
        )

    conversation = get_open_conversation(
        db,
        customer_id=req.customer_id,
        company_id=customer.company_id,
    )

    result = run_agent_turn(
        conversation_id=conversation.id,
        state={
            "customer_id": req.customer_id,
            "conversation_id": conversation.id,
            "message": req.message,
            "entry_type": "message",
        },
    )

    # Save customer and agent messages
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

    # Save offer only if it does not already exist
    # in this conversation
    offer = result.get("offer")

    if offer:
        price = _to_decimal(offer.get("price"))
        product_name = (
            offer.get("product")
            or offer.get("product_name")
        )

        if price is not None and product_name:
            existing_offer = (
                db.query(Offer)
                .filter(
                    Offer.conversation_id == conversation.id,
                    Offer.customer_id == req.customer_id,
                    Offer.product_name == product_name,
                )
                .first()
            )

            if existing_offer is None:
                db.add(
                    Offer(
                        customer_id=req.customer_id,
                        conversation_id=conversation.id,
                        company_id=customer.company_id,
                        product_name=product_name,
                        price=price,
                        status="sent",
                    )
                )

    # Handle purchase action
    action = result.get("action")

    if isinstance(action, dict) and action.get("type") == "purchase":
        primary_offer = (
            (result.get("recommendation") or {}).get("primary") or {}
        )

        product_id = str(
            primary_offer.get("product_id")
            or "checkout-default-product"
        )

        product_name = str(
            primary_offer.get("product_name")
            or (offer or {}).get("product")
            or "Selected plan"
        )

        price = _to_decimal(
            primary_offer.get("price")
            or (offer or {}).get("price")
        )

        if price is not None:
            attribution = (
                db.query(Attribution)
                .filter(
                    Attribution.conversation_id == conversation.id,
                    Attribution.customer_id == req.customer_id,
                    Attribution.product_id == product_id,
                    Attribution.status == "pending",
                )
                .order_by(Attribution.created_at.desc())
                .first()
            )

            if attribution is None:
                attribution = Attribution(
                    conversation_id=conversation.id,
                    customer_id=req.customer_id,
                    product_id=product_id,
                    product_name=product_name,
                    price=price,
                    status="pending",
                )
                db.add(attribution)
                db.flush()

            action["url"] = (
                f"{action['url']}&attribution_id={attribution.id}"
            )

    db.commit()

    return ChatResponse(
        response=result["response"],
        offer=result.get("offer"),
        action=action,
        conversation_stage=result.get("conversation_stage"),
    )
