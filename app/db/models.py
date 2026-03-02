from datetime import datetime
from typing import Any, Dict

from sqlalchemy import DateTime, Float, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class CandidateStaging(Base):
    """
    ORM model for candidates_staging table.
    """

    __tablename__ = "candidates_staging"

    candidate_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    parse_status: Mapped[str] = mapped_column(String(50), nullable=False)

    confidence_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    structured_profile: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

    candidate_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
