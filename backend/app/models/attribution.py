from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, BIGINT_ID


class Attribution(Base):
    """A sale our AI agent closed.

    A row is created the moment the agent decides the deal is done
    (status=pending, the checkout URL is handed to the customer). It
    moves to completed when the customer actually pays, or expired if
    the checkout URL is never used.

    Counting rows where status='completed' == how many sales our agent
    actually closed. No agent_id needed: we're a single-agent product.
    """

    __tablename__ = "attributions"

    id: Mapped[int] = mapped_column(BIGINT_ID, primary_key=True, autoincrement=True)
    conversation_id: Mapped[int] = mapped_column(
        BIGINT_ID, ForeignKey("conversations.id"), nullable=False
    )
    customer_id: Mapped[int] = mapped_column(
        BIGINT_ID, ForeignKey("customers.id"), nullable=False
    )
    # Product is a plain catalog id (no products table) — model owns just a name.
    product_id: Mapped[str] = mapped_column(String(50), nullable=False)
    product_name: Mapped[str] = mapped_column(String(150), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )
