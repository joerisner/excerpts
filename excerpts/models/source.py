import enum

from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from excerpts.core.config import config
from excerpts.models.base import Base, IdCreatedAtMixin


class SourceType(enum.StrEnum):
    ARTICLE = "article"
    BOOK = "book"
    ESSAY = "essay"
    PODCAST = "podcast"
    VIDEO = "video"


class Source(IdCreatedAtMixin, Base):
    __tablename__ = "sources"
    __table_args__ = (UniqueConstraint("title", "author_id", name="uq_sources_title_author_id"),)

    title: Mapped[str] = mapped_column(String(160))
    cover_image_file: Mapped[str | None] = mapped_column(String(200))
    type: Mapped[SourceType] = mapped_column(
        Enum(SourceType, name="source_type", values_callable=lambda enum_cls: [member.value for member in enum_cls])
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), index=True)

    author = relationship("Author", back_populates="sources")
    excerpts = relationship("Excerpt", back_populates="source", cascade="all, delete-orphan")

    @property
    def cover_image_path(self) -> str:
        if self.cover_image_file:
            # TODO: Replace with path to S3 object.
            raise NotImplementedError("S3 cover image resolution not yet implemented")

        return f"{config.API_STATIC_ASSETS_DIR}/images/default_cover_image.png"
