from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from excerpts.api.schemas.source import SourcePublic


class ExcerptBase(BaseModel):
    content: str = Field(min_length=1)
    locator: str | None = Field(min_length=1, max_length=120, default=None)
    meta: dict[str, Any] | None = None


class ExcerptCreate(ExcerptBase):
    source_id: int


class ExcerptPublic(ExcerptBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    source: SourcePublic


class ExcerptUpdate(BaseModel):
    content: str | None = Field(min_length=1, default=None)
    locator: str | None = Field(min_length=1, max_length=120, default=None)
    meta: dict[str, Any] | None = None
    source_id: int | None = None

    @field_validator("content")
    @classmethod
    def content_not_null(cls, val: str | None) -> str | None:
        if val is None:
            raise ValueError("content cannot be null")
        return val

    @field_validator("source_id")
    @classmethod
    def source_id_not_null(cls, val: int | None) -> int | None:
        if val is None:
            raise ValueError("source_id cannot be null")
        return val


class ExcerptsPublic(BaseModel):
    data: list[ExcerptPublic]
    total: int
    skip: int
    limit: int
    has_more: bool
