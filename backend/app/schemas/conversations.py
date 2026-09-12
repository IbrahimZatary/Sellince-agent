from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class CustomerBrief(BaseModel):
    id: int
    name: str
    phone: str
    service_type: str | None = None
    plan: str
    segment: str | None = None


class OfferBrief(BaseModel):
    product_name: str
    price: Decimal
    status: str


class MessageRow(BaseModel):
    id: int
    sender: str
    text: str
    sent_at: datetime


class LastMessage(BaseModel):
    id: int
    sender: str
    text: str
    sent_at: datetime


class ConversationSummary(BaseModel):
    id: int
    status: str
    started_at: datetime
    last_activity_at: datetime
    message_count: int
    customer: CustomerBrief
    offer: OfferBrief | None = None
    last_message: LastMessage | None = None


class ConversationDetail(BaseModel):
    id: int
    status: str
    started_at: datetime
    customer: CustomerBrief
    messages: list[MessageRow]
    offer: OfferBrief | None = None