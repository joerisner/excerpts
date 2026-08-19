from typing import Any

from fastapi import APIRouter

from excerpts.api.schemas.health import HealthCheck

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthCheck)
def get_health() -> Any:
    """Perform a health check of the application."""
    return HealthCheck()
