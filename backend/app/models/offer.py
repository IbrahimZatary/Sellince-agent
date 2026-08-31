from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, BIGINT_ID


class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(BIGINT_ID, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(BIGINT_ID, ForeignKey("customers.id"))
    conversation_id: Mapped[int | None] = mapped_column(BIGINT_ID, ForeignKey("conversations.id"), nullable=True)
    company_id: Mapped[int] = mapped_column(BIGINT_ID, ForeignKey("companies.id"))
    product_name: Mapped[str] = mapped_column(String(150))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[str] = mapped_column(String(30), default="sent")
    confirmed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
