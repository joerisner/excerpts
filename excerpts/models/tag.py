from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from excerpts.models.base import Base, IdCreatedAtMixin


class Tag(IdCreatedAtMixin, Base):
    __tablename__ = "tags"
    # Enforce lowercase values for `slug` on write.
    __table_args__ = (CheckConstraint("slug = lower(slug)", name="ck_tags_slug_lowercase"),)

    name: Mapped[str] = mapped_column(String(80))
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)

    excerpts = relationship("Excerpt", secondary="excerpt_tags", back_populates="tags", order_by="Excerpt.id")
