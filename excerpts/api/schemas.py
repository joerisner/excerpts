"""
Pydantic schema definitions.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from excerpts.models.source import SourceType

#######################
##### Healthcheck #####
#######################


class HealthCheck(BaseModel):
    status: str = "UP"


#######################
###### Authors ########
#######################


class AuthorBase(BaseModel):
    first_name: str | None = Field(min_length=1, max_length=50, default=None)
    last_name: str = Field(min_length=1, max_length=50)


class AuthorCreate(AuthorBase):
    pass


class AuthorPublic(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class AuthorUpdate(BaseModel):
    first_name: str | None = Field(min_length=1, max_length=50, default=None)
    last_name: str | None = Field(min_length=1, max_length=50, default=None)

    # If "last_name" is included in the request data, it cannot be null.
    @field_validator("last_name")
    @classmethod
    def last_name_not_null(cls, val: str | None) -> str | None:
        if val is None:
            raise ValueError("last_name cannot be null")
        return val


class AuthorsPublic(BaseModel):
    data: list[AuthorPublic]
    total: int
    skip: int
    limit: int
    has_more: bool


#######################
###### Sources ########
#######################


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


#########################
####### Excerpts ########
#########################


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
