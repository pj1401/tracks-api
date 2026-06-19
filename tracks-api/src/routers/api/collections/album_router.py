"""
Defines the album paths.
module: src.routers.api.collections.album_router
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from models import Album
from models.schemas.albums import AlbumSchema, AlbumQueryParams
from src.dependencies import get_session, get_settings
from src.repositories.album_repo import AlbumRepository
from src.services.album_service import AlbumService
from src.controllers.album_controller import AlbumController

album_router = APIRouter(tags=["albums"])


async def get_controller(
    request: Request, session: AsyncSession = Depends(get_session)
):
    settings = get_settings()
    album_repo = AlbumRepository(
        session, Album, f"{settings.base_url}", f"{request.scope.get('root_path')}"
    )
    album_service = AlbumService(album_repo, AlbumSchema)
    return AlbumController(
        album_service,
        f"{settings.base_url}",
        f"{request.scope.get('root_path')}/albums",
    )


@album_router.get("", status_code=status.HTTP_200_OK)
async def get_albums(
    controller: Annotated[AlbumController, Depends(get_controller)],
    filter_query: Annotated[AlbumQueryParams, Query()],
    response: Response,
) -> dict[str, int | str | list[AlbumSchema | None] | None]:
    return await controller.get(filter_query, response)


@album_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_album_by_id(
    controller: Annotated[AlbumController, Depends(get_controller)],
    id: int,
    response: Response,
) -> dict[str, int | AlbumSchema | str]:
    return await controller.get_by_id(id, response)
