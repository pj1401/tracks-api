"""
The base router.
module: src/routers/router.py
"""

from typing import Annotated
from fastapi import APIRouter, Depends
from src.config import Settings
from src.dependencies import get_settings

router = APIRouter()


@router.get("/")
async def get(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "message": "Hello from the Tracks API!",
        "docs": f"{settings.base_url}{settings.root_path}/docs",
        "version 1": f"{settings.base_url}{settings.root_path}/api/v1",
    }


@router.get("/health")
async def health():
    return {"status": 200, "message": "OK"}
