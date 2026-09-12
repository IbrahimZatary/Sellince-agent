from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.core.exceptions import AppException
from app.models.conversation import Conversation
from app.models.customer import Customer
from app.models.message import Message
from app.models.offer import Offer
from app.models.user import User
from app.schemas.conversations import (
    ConversationDetail,
    ConversationSummary,
    CustomerBrief,
    LastMessage,
    MessageRow,
    OfferBrief,
)

router = APIRouter(prefix="/conversations", tags=["conversations"])


def _customer_brief(customer: Customer) -> CustomerBrief:
    return CustomerBrief(
        id=customer.id,
        name=customer.name,
        phone=customer.phone,
        service_type=customer.service_type,
        plan=customer.current_plan,
        segment=customer.segment,
    )


def _offer_brief(offer: Offer) -> OfferBrief:
    return OfferBrief(
        product_name=offer.product_name,
        price=offer.price,
        status=offer.status,
    )


@router.get("", response_model=list[ConversationSummary])
def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    company_id = current_user.company_id

    rows = (
        db.query(Conversation, Customer)
        .join(Customer, Conversation.customer_id == Customer.id)
        .filter(Conversation.company_id == company_id)
        .order_by(Conversation.started_at.desc())
        .all()
    )

    conversation_ids = [conversation.id for conversation, _ in rows]
    if not conversation_ids:
        return []

    messages = (
        db.query(Message)
        .filter(Message.conversation_id.in_(conversation_ids))
        .order_by(Message.sent_at.asc())
        .all()
    )
    messages_by_conversation: dict[int, list[Message]] = defaultdict(list)
    for message in messages:
        messages_by_conversation[message.conversation_id].append(message)

    offers = (
        db.query(Offer)
        .filter(Offer.conversation_id.in_(conversation_ids))
        .all()
    )
    offer_by_conversation: dict[int, Offer] = {}
    for offer in offers:
        offer_by_conversation.setdefault(offer.conversation_id, offer)

    summaries = []
    for conversation, customer in rows:
        thread = messages_by_conversation.get(conversation.id, [])
        last_message = thread[-1] if thread else None
        last_activity_at = conversation.started_at
        for source in (
            last_message.sent_at if last_message else None,
            conversation.closed_at,
        ):
            if source and source > last_activity_at:
                last_activity_at = source

        offer = offer_by_conversation.get(conversation.id)
        summaries.append(
            ConversationSummary(
                id=conversation.id,
                status=conversation.status,
                started_at=conversation.started_at,
                last_activity_at=last_activity_at,
                message_count=len(thread),
                customer=_customer_brief(customer),
                offer=_offer_brief(offer) if offer else None,
                last_message=(
                    LastMessage(
                        id=last_message.id,
                        sender=last_message.sender,
                        text=last_message.text,
                        sent_at=last_message.sent_at,
                    )
                    if last_message
                    else None
                ),
            )
        )

    summaries.sort(key=lambda s: s.last_activity_at, reverse=True)
    return summaries


@router.get("/{conversation_id}", response_model=ConversationDetail)
def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    company_id = current_user.company_id

    row = (
        db.query(Conversation, Customer)
        .join(Customer, Conversation.customer_id == Customer.id)
        .filter(
            Conversation.id == conversation_id,
            Conversation.company_id == company_id,
        )
        .first()
    )
    if not row:
        raise AppException(
            status_code=404,
            error_code="CONVERSATION_NOT_FOUND",
            message="Conversation not found",
        )

    conversation, customer = row
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation.id)
        .order_by(Message.sent_at.asc())
        .all()
    )
    offer = (
        db.query(Offer)
        .filter(Offer.conversation_id == conversation.id)
        .first()
    )

    return ConversationDetail(
        id=conversation.id,
        status=conversation.status,
        started_at=conversation.started_at,
        customer=_customer_brief(customer),
        messages=[
            MessageRow(
                id=message.id,
                sender=message.sender,
                text=message.text,
                sent_at=message.sent_at,
            )
            for message in messages
        ],
        offer=_offer_brief(offer) if offer else None,
    )