from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from excerpts.models.base import Base


class Author(Base):
    __tablename__ = "authors"

    first_name: Mapped[str | None] = mapped_column(String(50))  # Nullable allows for mononyms.
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
