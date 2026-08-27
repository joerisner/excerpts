from datetime import datetime

from pydantic import BaseModel, ConfigDict, computed_field

from excerpts.types import TagName
from excerpts.utils.string import slugify


class TagBase(BaseModel):
    name: TagName

    @computed_field
    @property
    def slug(self) -> str:
        return slugify(self.name)


class TagCreate(TagBase):
    # Disallow setting computed field `slug` manually.
    model_config = ConfigDict(extra="forbid")


class TagPublic(TagBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class TagUpdate(TagBase):
    # Disallow setting computed field `slug` manually.
    model_config = ConfigDict(extra="forbid")


class TagsPublic(BaseModel):
    data: list[TagPublic]
    total: int
    skip: int
    limit: int
    has_more: bool
