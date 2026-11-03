from decimal import Decimal, InvalidOperation
from sqlalchemy.orm import Session

from app.agent.runner import run_agent_turn
from app.core.exceptions import AppException
from app.models.attribution import Attribution
from app.models.customer import Customer
from app.models.message import Message
from app.models.offer import Offer
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.conversation_service import get_open_conversation


def _to_decimal(value) -> Decimal | None:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


def handle_chat_turn(db: Session, req: ChatRequest) -> ChatResponse:
    # 1. Fetch customer
    customer = (
        db.query(Customer)
        .filter(Customer.id == req.customer_id)
        .first()
    )
    if not customer:
        raise AppException(
            status_code=404,
            error_code="CUSTOMER_NOT_FOUND",
            message="Customer not found",
        )

    # 2. Get or create active open conversation
    conversation = get_open_conversation(
        db,
        customer_id=req.customer_id,
        company_id=customer.company_id,
    )

    # 3. Execute LangGraph agent turn
    result = run_agent_turn(
        conversation_id=conversation.id,
        state={
            "customer_id": req.customer_id,
            "conversation_id": conversation.id,
            "message": req.message,
            "entry_type": "message",
        },
    )

    # 4. Save messages
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

    # 5. Persist offer if newly presented
    offer = result.get("offer")
    if isinstance(offer, dict) and offer:
        price = _to_decimal(offer.get("price"))
        product_name = (
            offer.get("product")
            or offer.get("product_name")
            or offer.get("name")
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

    # 6. Process purchase action & attribution linking
    action = result.get("action")
    if isinstance(action, dict) and action.get("type") == "purchase":
        recommendation = result.get("recommendation") or {}

        if isinstance(recommendation, dict):
            primary_offer = (
                recommendation.get("primary")
                if "primary" in recommendation
                else recommendation
            )
        else:
            primary_offer = None

        if not primary_offer:
            primary_offer = result.get("active_offer") or {}

        if not primary_offer and isinstance(offer, dict):
            primary_offer = offer

        if not isinstance(primary_offer, dict):
            primary_offer = {}

        product_id = (
            primary_offer.get("product_id")
            or primary_offer.get("id")
        )

        product_name = (
            primary_offer.get("product_name")
            or primary_offer.get("product")
            or primary_offer.get("name")
            or (
                offer.get("product")
                or offer.get("product_name")
                or offer.get("name")
                if isinstance(offer, dict)
                else None
            )
        )

        raw_price = primary_offer.get("price")
        if raw_price is None and isinstance(offer, dict):
            raw_price = offer.get("price")

        price = _to_decimal(raw_price)

        if (
            product_id is not None
            and product_name
            and price is not None
        ):
            product_id = str(product_id)

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
        else:
            action = "chat"

    db.commit()

    return ChatResponse(
        response=result["response"],
        offer=offer,
        action=action,
        conversation_stage=result.get("conversation_stage"),
    )
