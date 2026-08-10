from datetime import UTC, datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all models.
    Includes definitions for columns common to all models.
    """

    # `id` = first; `created_at` = last.
    id: Mapped[int] = mapped_column(primary_key=True, sort_order=-1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
