from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all models.
    Includes definitions for columns common to all models.
    """

    # `id` should always be the first column in a table.
    id: Mapped[int] = mapped_column(primary_key=True, sort_order=-1)
    # Let the DB be the source of truth when a record was created.
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
