from datetime import datetime

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, BIGINT_ID


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(BIGINT_ID, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(BIGINT_ID, ForeignKey("customers.id"))
    company_id: Mapped[int] = mapped_column(BIGINT_ID, ForeignKey("companies.id"))
    status: Mapped[str] = mapped_column(String(30), server_default="open")
    started_at: Mapped[datetime] = mapped_column(server_default=func.now())
    closed_at: Mapped[datetime | None] = mapped_column(nullable=True)
