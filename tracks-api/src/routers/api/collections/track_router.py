"""
Defines the track paths.
module: src.routers.api.collections.track_router
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from models import Track
from models.schemas.tracks import TrackSchema
from src.dependencies import get_session, get_settings
from src.repositories.track_repo import TrackRepository
from src.services.track_service import TrackService
from src.controllers.track_controller import TrackController

track_router = APIRouter(tags=["tracks"])


async def get_controller(session: AsyncSession = Depends(get_session)):
    settings = get_settings()
    track_repo = TrackRepository(session, Track, settings.base_url)
    track_service = TrackService(track_repo, TrackSchema)
    return TrackController(track_service)


@track_router.get("", status_code=status.HTTP_200_OK)
async def get_tracks(session: AsyncSession = Depends(get_session)):
    pass


@track_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_track_by_id(
    id: int,
    response: Response,
    controller: Annotated[TrackController, Depends(get_controller)],
):
    return await controller.get_by_id(id, response)
