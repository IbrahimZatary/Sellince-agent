from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import AppException
from app.core.security import create_access_token, verify_password
from app.models.customer import Customer
from app.schemas.customer_auth import CustomerLoginRequest, CustomerLoginResponse

router = APIRouter(prefix="/customer-auth", tags=["customer-auth"])


@router.post("/login", response_model=CustomerLoginResponse)
def customer_login(request: CustomerLoginRequest, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.phone == request.phone.strip()).first()
    if not customer or not customer.password_hash or not verify_password(request.password, customer.password_hash):
        raise AppException(
            status_code=401,
            error_code="INVALID_CUSTOMER_CREDENTIALS",
            message="Invalid phone number or password",
        )

    return CustomerLoginResponse(
        access_token=create_access_token({"sub": str(customer.id), "token_type": "customer"}),
        customer_id=customer.id,
        name=customer.name,
    )