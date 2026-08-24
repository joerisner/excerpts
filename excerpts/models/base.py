from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all models.
    For tables that need `id` and `created_at` columns, add mixins below.
    """

    pass


class CreatedAtMixin:
    """
    Mixin for adding the `created_at` column to a table.
    This is used for association tables that do not require an `id` PK.
    """

    # The DB is to be the source of truth when a record was created.
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class IdCreatedAtMixin(CreatedAtMixin):
    """
    Mixin for adding the `id` and `created_at` columns to a table.
    """

    # `id` should always be the first column in a table.
    id: Mapped[int] = mapped_column(primary_key=True, sort_order=-1)
