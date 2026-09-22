from pydantic import BaseModel, Field


class CustomerLoginRequest(BaseModel):
    phone: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=1, max_length=128)


class CustomerLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    customer_id: int
    name: str