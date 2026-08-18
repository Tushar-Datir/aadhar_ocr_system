from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    String,
    Text
)

from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class OCRDocument(Base):

    __tablename__ = "ocr_documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )

    gender: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    date_of_birth: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    masked_aadhaar_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    is_valid: Mapped[bool] = mapped_column(
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )