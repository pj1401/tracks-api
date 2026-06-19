"""
Defines the track paths.
module: src.routers.api.collections.track_router
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from models import Track
from models.schemas.tracks import TrackParams, TrackSchema, TrackQueryParams
from src.dependencies import get_session, get_settings, get_user_id
from src.repositories.track_repo import TrackRepository
from src.services.track_service import TrackService
from src.controllers.track_controller import TrackController

track_router = APIRouter(tags=["tracks"])


async def get_controller(
    request: Request, session: AsyncSession = Depends(get_session)
):
    settings = get_settings()
    track_repo = TrackRepository(
        session, Track, f"{settings.base_url}", f"{request.scope.get('root_path')}"
    )
    track_service = TrackService(track_repo, TrackSchema)
    return TrackController(
        track_service,
        f"{settings.base_url}",
        f"{request.scope.get('root_path')}/tracks",
    )


@track_router.get("", status_code=status.HTTP_200_OK)
async def get_tracks(
    controller: Annotated[TrackController, Depends(get_controller)],
    filter_query: Annotated[TrackQueryParams, Query()],
    response: Response,
) -> dict[str, int | str | list[TrackSchema | None] | None]:
    return await controller.get(filter_query, response)


@track_router.post("", status_code=status.HTTP_201_CREATED)
async def post(
    controller: Annotated[TrackController, Depends(get_controller)],
    user_id: Annotated[int, Depends(get_user_id)],
    track: TrackParams,
    response: Response,
):
    return await controller.post(track, response)


@track_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_track_by_id(
    controller: Annotated[TrackController, Depends(get_controller)],
    id: int,
    response: Response,
) -> dict[str, int | TrackSchema | str]:
    return await controller.get_by_id(id, response)


@track_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    controller: Annotated[TrackController, Depends(get_controller)],
    user_id: Annotated[int, Depends(get_user_id)],
    id: int,
    response: Response,
):
    return await controller.delete(id, response)
