"""
Defines the track paths.
module: src.routers.api.collections.track_router
"""

from typing import Annotated, Mapping
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from models import Track
from models.schemas.tracks import TrackSchema, TrackQueryParams
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
async def get_tracks(
    controller: Annotated[TrackController, Depends(get_controller)],
    filter_query: Annotated[TrackQueryParams, Query()],
    response: Response,
) -> Mapping[str, int | list[TrackSchema] | str]:
    return await controller.get(filter_query, response)


@track_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_track_by_id(
    controller: Annotated[TrackController, Depends(get_controller)],
    id: int,
    response: Response,
) -> dict[str, int | TrackSchema | str]:
    return await controller.get_by_id(id, response)
