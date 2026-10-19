from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.exceptions import AppException
from app.core.security import create_access_token
from app.models.customer import Customer

router = APIRouter()

class CustomerLoginRequest(BaseModel):
    phone: str
    password: str

@router.post("/login")
def login(
    request: CustomerLoginRequest,
    db: Session = Depends(get_db),
):
    customer = db.query(Customer).filter(Customer.phone == request.phone).first()
    
    # Check if the phone number exists in the seeded database
    if not customer:
        raise AppException(
            status_code=401,
            error_code="INVALID_CREDENTIALS",
            message="Phone number not found in database",
        )
        
    # Enforce the shared demo password since it isn't stored in the database
    if request.password != "Sellince123!":
        raise AppException(
            status_code=401,
            error_code="INVALID_CREDENTIALS",
            message="Invalid password",
        )

    return JSONResponse(
        content={
            "access_token": create_access_token({"sub": str(customer.id), "role": "customer"}),
            "token_type": "bearer",
        }
    )