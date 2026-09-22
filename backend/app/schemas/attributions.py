from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

class AttributionCreate(BaseModel):
    """Body the AI agent sends the moment it decides the deal is done."""

    model_config = ConfigDict(from_attributes=True)

    conversation_id: int = Field(gt=0)
    customer_id: int = Field(gt=0)

    # Catalog ids are plain strings (no products table) — e.g. p002.
    product_id: str = Field(min_length=1, max_length=50)
    product_name: str = Field(min_length=1, max_length=150)

    # Freeze the agreed price at POST time the same way the model already
    # snapshots it (price column exists on the model). There is no products
    # table to re-fetch price from — so our attribution row must own it.
    # Without this field the POST body can never supply price and every
    # insert violates the model's NOT NULL constraint.
    price: Decimal = Field(gt=0)


class AttributionUpdate(BaseModel):
    """AI/frontend moves a pending sale forward.

    status='pending' → 'completed' (customer paid) or 'expired'
    (checkout URL never used). Only pending rows may be updated.
    """

    model_config = ConfigDict(from_attributes=True)

    status: str = Field(pattern="^(pending|completed|expired)$")


class CheckoutComplete(BaseModel):
    customer_id: int = Field(gt=0)
    conversation_id: int = Field(gt=0)
    product_id: str = Field(min_length=1, max_length=50)


class AttributionRead(BaseModel):
    """A single sale attributed to our AI agent."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    conversation_id: int
    customer_id: int
    product_id: str
    product_name: str
    price: Decimal
    status: str
    created_at: datetime
    confirmed_at: datetime | None
