from sqlalchemy.orm import Session

from app.models.customer import Customer


def search_customer_by_name(
    db: Session,
    query: str,
) -> list[Customer]:
    if not query or not query.strip():
        return []

    search_term = f"%{query.strip()}%"

    return (
        db.query(Customer)
        .filter(Customer.name.ilike(search_term))
        .all()
    )