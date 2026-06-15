"""
The router that registers the api routes.
module: src/routers/api/api_router.py
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Request
from src.config import Settings
from src.dependencies import get_settings

api_router = APIRouter()


@api_router.get("/")
async def get(settings: Annotated[Settings, Depends(get_settings)], request: Request):
    return {
        "message": "Hello from the Tracks API!",
        "version 1": f"{settings.base_url}{request.scope.get('root_path')}/api/v1",
    }
