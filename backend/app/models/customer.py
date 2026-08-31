from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import String, ForeignKey, Numeric, Date, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, BIGINT_ID


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(BIGINT_ID, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(BIGINT_ID, ForeignKey("companies.id"))
    name: Mapped[str] = mapped_column(String(150))
    phone: Mapped[str] = mapped_column(String(30))
    current_plan: Mapped[str] = mapped_column(String(100))
    usage_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    contract_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    segment: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
