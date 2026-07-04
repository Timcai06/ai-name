"""取名历史模型."""
from datetime import datetime

from sqlalchemy import Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, beijing_now


class NamingHistory(Base):
    __tablename__ = "naming_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    surname: Mapped[str] = mapped_column(String(5), nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    birthday: Mapped[str | None] = mapped_column(String(20), nullable=True)
    birth_time: Mapped[str | None] = mapped_column(String(10), nullable=True)
    style: Mapped[str | None] = mapped_column(String(50), nullable=True)
    expectations: Mapped[str | None] = mapped_column(String(200), nullable=True)
    result_json: Mapped[str] = mapped_column(Text, nullable=False)  # 名字结果 JSON
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)  # 微调对话 JSON
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)  # 软删除
    record_type: Mapped[str] = mapped_column(String(20), default="naming", nullable=False)  # naming / analyze
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=beijing_now, nullable=False
    )
