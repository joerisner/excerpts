from fastapi import APIRouter

from excerpts.api.routes import authors, excerpts, health, sources

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(authors.router)
api_router.include_router(sources.router)
api_router.include_router(excerpts.router)
