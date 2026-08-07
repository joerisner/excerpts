"""
Exported types for use throughout the project.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from excerpts.core.db import get_db

type DBDep = Annotated[Session, Depends(get_db)]
