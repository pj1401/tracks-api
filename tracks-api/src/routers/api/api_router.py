"""
The router that registers the api routes.
module: src/routers/api/api_router.py
"""

from typing import Annotated
from fastapi import APIRouter, Depends
from .v1.v1_router import v1_router
from src.config import Settings
from src.dependencies import get_settings

api_router = APIRouter()

api_router.include_router(v1_router, prefix="/v1")


@api_router.get("")
async def get(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "message": "Hello from the Tracks API!",
        "version 1": f"{settings.base_url}/api/v1",
    }
