from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AttributionCreate(BaseModel):
    """Body the AI agent sends the moment it decides the deal is done."""

    model_config = ConfigDict(from_attributes=True)

    conversation_id: int = Field(gt=0)
    customer_id: int = Field(gt=0)
    # Catalog ids are plain strings (no products table) — e.g. p002.
    product_id: str = Field(min_length=1, max_length=50)
    product_name: str = Field(min_length=1, max_length=150)


class AttributionUpdate(BaseModel):
    """AI/frontend moves a pending sale forward.

    status='pending' → 'completed' (customer paid) or 'expired'
    (checkout URL never used). Only pending rows may be updated.
    """

    model_config = ConfigDict(from_attributes=True)

    status: str = Field(pattern="^(pending|completed|expired)$")


class AttributionRead(BaseModel):
    """A single sale attributed to our AI agent."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    conversation_id: int
    customer_id: int
    product_id: str
    product_name: str
    status: str
    created_at: datetime
    updated_at: datetime
