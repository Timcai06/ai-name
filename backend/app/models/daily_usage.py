"""每日使用记录模型."""
from datetime import datetime, date

from sqlalchemy import Integer, String, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, beijing_now


class DailyUsage(Base):
    __tablename__ = "daily_usage"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    usage_date: Mapped[date] = mapped_column(Date, nullable=False)
    feature_type: Mapped[str] = mapped_column(String(20), nullable=False)  # analyze/compare/premium
    count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=beijing_now, nullable=False)
