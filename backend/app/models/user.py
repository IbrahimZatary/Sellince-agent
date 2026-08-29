from datetime import datetime

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, BIGINT_ID


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT_ID, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(BIGINT_ID, ForeignKey("companies.id"))
    full_name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="admin")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
