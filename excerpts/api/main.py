from fastapi import APIRouter

from excerpts.api.routes import authors, health

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(authors.router)
