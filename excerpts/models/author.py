from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from excerpts.models.base import Base


class Author(Base):
    __tablename__ = "authors"

    first_name: Mapped[str | None] = mapped_column(String(50))  # Nullable allows for mononyms.
    last_name: Mapped[str] = mapped_column(String(50))

    sources = relationship("Source", back_populates="author", cascade="all, delete-orphan")
