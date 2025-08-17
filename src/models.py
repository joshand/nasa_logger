from sqlalchemy import String, Integer, Date, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.db import Base


class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[str] = mapped_column(String(10), unique=True, index=True)  # 'YYYY-MM-DD'
    title: Mapped[str] = mapped_column(String(255))
    media_type: Mapped[str] = mapped_column(String(50))
    url: Mapped[str] = mapped_column(Text)
    hdurl: Mapped[str | None] = mapped_column(Text, nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    local_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
