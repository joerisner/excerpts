from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from excerpts.api.schemas.author import AuthorPublic
from excerpts.models.source import SourceType


class SourceBase(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    cover_image_file: str | None = Field(max_length=200, default=None)
    type: SourceType = SourceType.BOOK


class SourceCreate(SourceBase):
    author_id: int


class SourcePublic(SourceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    author: AuthorPublic


class SourceUpdate(BaseModel):
    title: str | None = Field(min_length=1, max_length=160, default=None)
    cover_image_file: str | None = Field(max_length=200, default=None)
    type: SourceType | None = None
    author_id: int | None = None

    # If "title" IS included in the request data, it cannot be null.
    @field_validator("title")
    @classmethod
    def title_not_null(cls, val: str | None) -> str | None:
        if val is None:
            raise ValueError("title cannot be null")
        return val

    # If "type" IS included in the request data, it cannot be null.
    @field_validator("type")
    @classmethod
    def type_not_null(cls, val: str | None) -> str | None:
        if val is None:
            raise ValueError("type cannot be null")
        return val

    # If "author_id" IS included in the request data, it cannot be null.
    @field_validator("author_id")
    @classmethod
    def author_id_not_null(cls, val: int | None) -> int | None:
        if val is None:
            raise ValueError("author_id cannot be null")
        return val


class SourcesPublic(BaseModel):
    data: list[SourcePublic]
    total: int
    skip: int
    limit: int
    has_more: bool
