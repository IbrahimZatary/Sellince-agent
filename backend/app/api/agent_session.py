
from decimal import Decimal, InvalidOperation

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
import json

from fastapi.responses import StreamingResponse
from app.agent.runner import (
    has_existing_checkpoint,
    run_proactive_session,
)
from app.core.database import get_db
from app.core.exceptions import AppException
from app.models.customer import Customer
from app.models.message import Message
from app.models.offer import Offer
from app.schemas.agent_session import (
    StartSessionRequest,
    StartSessionResponse,
)
from app.services.conversation_service import get_open_conversation


router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/start-session", response_model=StartSessionResponse)
def start_session(
    req: StartSessionRequest,
    db: Session = Depends(get_db),
):
    try:
        # Phase 1: Create or retrieve the conversation
        customer = (
            db.query(Customer)
            .filter(Customer.id == req.customer_id)
            .first()
        )

        if customer is None:
            raise AppException(
                status_code=404,
                error_code="CUSTOMER_NOT_FOUND",
                message="Customer not found",
            )

        customer_id = customer.id
        company_id = customer.company_id

        conversation = get_open_conversation(
            db=db,
            customer_id=customer_id,
            company_id=company_id,
        )

        conversation_id = conversation.id

        # Persist conversation before using LangGraph
        db.commit()

        # Phase 2: Lock session initialization
        db.execute(
            text("SELECT pg_advisory_xact_lock(:lock_key)"),
            {"lock_key": customer_id},
        )

        # Check while holding the lock
        if has_existing_checkpoint(conversation_id):
            db.commit()

            return StartSessionResponse(
                conversation_id=conversation_id,
                status="existing",
                response=None,
                offer=None,
            )

        # Run the proactive agent
        result = run_proactive_session(
            conversation_id=conversation_id,
            customer_id=customer_id,
        )

        opening_message = result.get("response")
        active_offer = result.get("active_offer")

        # Persist the proactive response
        if opening_message and opening_message.strip():
            db.add(
                Message(
                    conversation_id=conversation_id,
                    sender="agent",
                    text=opening_message,
                )
            )

            if active_offer:
                try:
                    price = Decimal(str(active_offer["price"]))
                except (
                    KeyError,
                    TypeError,
                    ValueError,
                    InvalidOperation,
                ):
                    price = None

                product_name = active_offer.get("product_name")

                if price is not None and product_name:
                    db.add(
                        Offer(
                            customer_id=customer_id,
                            conversation_id=conversation_id,
                            company_id=company_id,
                            product_name=product_name,
                            price=price,
                            status="sent",
                        )
                    )

        # Commit message and offer, then release lock
        db.commit()

        return StartSessionResponse(
            conversation_id=conversation_id,
            status="started",
            response=opening_message,
            offer=active_offer,
        )

    except Exception:
        db.rollback()
        raise

@router.post("/start-session/stream")
def start_session_stream(
    req: StartSessionRequest,
):
    def event_stream():
        # Tell frontend the session is starting
        yield (
            "event: started\n"
            'data: {"status": "processing"}\n\n'
        )

        try:
            # Use a new DB session inside the generator
            from app.core.database import SessionLocal

            with SessionLocal() as db:
                result = start_session(req=req, db=db)

            # Send complete response after agent finishes
            payload = result.model_dump()

            yield (
                "event: completed\n"
                f"data: {json.dumps(payload)}\n\n"
            )

        except Exception:
            yield (
                "event: error\n"
                'data: {"message": "Session initialization failed"}\n\n'
            )

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
