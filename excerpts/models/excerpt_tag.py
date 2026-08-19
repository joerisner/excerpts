from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from excerpts.models.base import Base, CreatedAtMixin


class ExcerptTag(CreatedAtMixin, Base):
    """
    Association table for excerpts and tags.
    """

    __tablename__ = "excerpt_tags"

    excerpt_id: Mapped[int] = mapped_column(ForeignKey(column="excerpts.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey(column="tags.id", ondelete="CASCADE"), primary_key=True)
