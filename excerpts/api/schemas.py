"""
Pydantic schema definitions.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

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
