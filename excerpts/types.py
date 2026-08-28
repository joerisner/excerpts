"""
Exported types for use throughout the project.
"""

from typing import Annotated

from fastapi import Depends, Query
from pydantic import StringConstraints
from sqlalchemy.orm import Session

from excerpts.core.db import get_db

type DBDep = Annotated[Session, Depends(get_db)]
type PaginationSkip = Annotated[int, Query(ge=0)]
type PaginationLimit = Annotated[int, Query(ge=1, le=100)]
type TagName = Annotated[str, StringConstraints(min_length=1, max_length=80)]
