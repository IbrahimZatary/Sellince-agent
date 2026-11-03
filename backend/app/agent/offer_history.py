
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.offer import Offer


def was_offer_recently_sent(
    db: Session,
    customer_id: int,
    company_id: int,
    product_name: str,
    cooldown_days: int = 30,
) -> bool:

    cutoff = datetime.now(timezone.utc).replace(
        tzinfo=None
    ) - timedelta(days=cooldown_days)

    existing_offer = (
        db.query(Offer)
        .filter(
            Offer.customer_id == customer_id,
            Offer.company_id == company_id,
            Offer.product_name == product_name,
            Offer.status.in_(["sent", "accepted"]),
            Offer.created_at >= cutoff,
        )
        .first()
    )

    return existing_offer is not None
