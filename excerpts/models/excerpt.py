from typing import Any

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column, relationship

from excerpts.models.base import Base


class Excerpt(Base):
    __tablename__ = "excerpts"

    content: Mapped[str] = mapped_column(Text)
    locator: Mapped[str | None] = mapped_column(String(120))
    meta: Mapped[dict[str, Any] | None] = mapped_column(MutableDict.as_mutable(JSONB))
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), index=True)

    source = relationship("Source", back_populates="excerpts")
