"""mst_user テーブルの ORM モデル."""

from __future__ import annotations

# Ruff の型チェックを無視しないと SQLAlchemy がエラーを出してしまう
from datetime import date, datetime  # noqa: TC003

from sqlalchemy import Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


class MstUser(Base):
    """ユーザーマスタ."""

    __tablename__ = "mst_user"

    user_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    user_name: Mapped[str] = mapped_column(String(100))
    user_name_kana: Mapped[str] = mapped_column(String(100))
    ignition_key: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150))
    gender: Mapped[str] = mapped_column(String(10))
    age: Mapped[int] = mapped_column(Integer)
    birth_day: Mapped[date] = mapped_column(Date)
    blood_type: Mapped[str] = mapped_column(String(10))
    prefecture: Mapped[str] = mapped_column(String(10))
    curry: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
