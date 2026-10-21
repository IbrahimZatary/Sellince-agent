
from sqlalchemy.orm import Session

from app.models.conversation import Conversation


def get_open_conversation(
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

    if conversation is None:
        conversation = Conversation(
            customer_id=customer_id,
            company_id=company_id,
            status="open",
        )
        db.add(conversation)
        db.flush()

    return conversation
