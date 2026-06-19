"""
Defines the artist paths.
module: src.routers.api.collections.artist_router
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from models import Artist
from models.schemas.artists import ArtistSchema, ArtistQueryParams
from src.dependencies import get_session, get_settings
from src.repositories.artist_repo import ArtistRepository
from src.services.artist_service import ArtistService
from src.controllers.artist_controller import ArtistController

artist_router = APIRouter(tags=["artists"])


async def get_controller(
    request: Request, session: AsyncSession = Depends(get_session)
):
    settings = get_settings()
    artist_repo = ArtistRepository(
        session, Artist, f"{settings.base_url}", f"{request.scope.get('root_path')}"
    )
    artist_service = ArtistService(artist_repo, ArtistSchema)
    return ArtistController(
        artist_service,
        f"{settings.base_url}",
        f"{request.scope.get('root_path')}/artists",
    )


@artist_router.get("", status_code=status.HTTP_200_OK)
async def get_artists(
    controller: Annotated[ArtistController, Depends(get_controller)],
    filter_query: Annotated[ArtistQueryParams, Query()],
    response: Response,
) -> dict[str, int | str | list[ArtistSchema | None] | None]:
    return await controller.get(filter_query, response)


@artist_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_artist_by_id(
    controller: Annotated[ArtistController, Depends(get_controller)],
    id: int,
    response: Response,
) -> dict[str, int | ArtistSchema | str]:
    return await controller.get_by_id(id, response)
