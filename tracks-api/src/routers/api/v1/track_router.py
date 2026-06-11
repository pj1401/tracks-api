"""
Defines the track paths.
module: src.routers.api.v1.track_router
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_session

track_router = APIRouter(tags=["tracks"])


@track_router.get("")
async def get_tracks(session: AsyncSession = Depends(get_session)):
    pass
