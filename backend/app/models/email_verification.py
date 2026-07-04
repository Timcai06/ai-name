"""邮箱验证码模型."""
from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, beijing_now


class EmailVerification(Base):
    __tablename__ = "email_verifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(6), nullable=False)
    purpose: Mapped[str] = mapped_column(String(20), nullable=False, default="bind")  # bind / reset_password
    used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    expire_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=beijing_now, nullable=False
    )
