"""
The base router.
module: src/routers/router.py
"""

from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from src.config import Settings
from src.dependencies import get_settings

router = APIRouter()


@router.get("/")
async def get(settings: Annotated[Settings, Depends(get_settings)]):
    return RedirectResponse(f"{settings.base_url}{settings.root_path}/api")


@router.get("/api")
async def api_index(settings: Annotated[Settings, Depends(get_settings)]):
    """
    Returns info about the API. This includes links to the docs and API versions.
    """
    return {
        "message": "Hello from the Tracks API!",
        "docs": f"{settings.base_url}{settings.root_path}/docs",
        "version 1": f"{settings.base_url}{settings.root_path}/api/v1",
    }
