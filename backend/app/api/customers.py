from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.customer import Customer
from app.models.user import User
from app.schemas.customers import CustomerListItem

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=list[CustomerListItem])
def list_customers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    customers = (
        db.query(Customer)
        .filter(Customer.company_id == current_user.company_id)
        .order_by(Customer.name.asc())
        .all()
    )
    return [
        CustomerListItem(
            id=customer.id,
            name=customer.name,
            phone=customer.phone,
            current_plan=customer.current_plan,
            service_type=customer.service_type,
            segment=customer.segment,
        )
        for customer in customers
    ]