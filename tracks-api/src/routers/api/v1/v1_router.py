"""
API version 1 router. Registers API paths for version 1 of the API.
module: src/routers/api/v1/v1_router.py
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Request
from ..collections.track_router import track_router
from src.config import Settings
from src.dependencies import get_settings

v1_router = APIRouter()
v1_router.include_router(track_router, prefix="/tracks")


@v1_router.get("/")
async def get(settings: Annotated[Settings, Depends(get_settings)], request: Request):
    return {
        "message": "Welcome to version 1 of the Tracks API!",
        "docs": f"{settings.base_url}{request.scope.get('root_path')}/docs",
    }


@v1_router.get("/health")
async def health():
    return {"status": 200, "message": "OK"}
