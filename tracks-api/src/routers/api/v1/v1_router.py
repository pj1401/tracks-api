"""
API version 1 router. Registers API paths for version 1 of the API.
module: src/routers/api/v1/v1_router.py
"""

from typing import Annotated
from fastapi import APIRouter, Depends, status
from ..collections import artist_router, track_router
from src.config import Settings
from src.dependencies import get_settings, get_user_id

v1_router = APIRouter()
v1_router.include_router(track_router, prefix="/tracks")
v1_router.include_router(artist_router, prefix="/artists")


@v1_router.get("/")
async def get(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "message": "Welcome to version 1 of the Tracks API!",
        "docs": f"{settings.base_url}{settings.root_path}/api/v1/docs",
    }


@v1_router.get("/health")
async def health():
    return {"status": 200, "message": "OK"}


@v1_router.get("/auth-required", status_code=status.HTTP_200_OK)
async def auth_test(
    user_id: Annotated[int, Depends(get_user_id)],
) -> dict[str, int | str]:
    return {"status": 200, "message": "JWT was decoded!"}
