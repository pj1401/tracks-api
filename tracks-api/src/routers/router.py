"""
The base router.
module: src/routers/router.py
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from .api.api_router import api_router
from src.config import Settings
from src.dependencies import get_settings

router = APIRouter()

router.include_router(api_router, prefix="/api")


@router.get("/")
async def get(settings: Annotated[Settings, Depends(get_settings)], request: Request):
    return RedirectResponse(f"{settings.base_url}{request.scope.get('root_path')}/api")
