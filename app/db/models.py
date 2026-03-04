from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import DateTime, Float, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class CandidateStaging(Base):
    """
    ORM model for candidates_staging table.
    """

    __tablename__ = "candidates_staging"

    candidate_id: Mapped[str] = mapped_column(String(36), primary_key=True)

    parse_status: Mapped[str] = mapped_column(String(50), nullable=False)

    processing_stage: Mapped[str] = mapped_column(String(50), nullable=False)

    raw_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    confidence_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    structured_profile: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)

    candidate_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
