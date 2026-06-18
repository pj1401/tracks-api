"""
Defines the track paths.
module: src.routers.api.collections.track_router
"""

import jwt
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request, Response, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from models import Track
from models.schemas.tracks import TrackParams, TrackSchema, TrackQueryParams
from models.schemas.users import UserToken
from src.dependencies import get_session, get_settings
from src.repositories.track_repo import TrackRepository
from src.services.track_service import TrackService
from src.controllers.track_controller import TrackController
from src.util.error import InvalidCredentialsError

JWT_ALGORITHM = "ES512"

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


async def get_oauth2_scheme():
    settings = get_settings()
    return OAuth2PasswordBearer(
        tokenUrl=f"{settings.base_url}/tracks-api/auth/api/v1/login"
    )


async def get_public_key():
    settings = get_settings()
    return settings.public_key


async def get_user_id(token: Annotated[str, Depends(get_oauth2_scheme)]):
    try:
        payload = UserToken(
            **jwt.decode(token, get_public_key, algorithms=[JWT_ALGORITHM])  # type: ignore
        )
        user_id = payload.sub
        if user_id is None:
            raise InvalidCredentialsError
    except InvalidTokenError:
        raise InvalidCredentialsError
    return user_id


@track_router.get("", status_code=status.HTTP_200_OK)
async def get_tracks(
    controller: Annotated[TrackController, Depends(get_controller)],
    filter_query: Annotated[TrackQueryParams, Query()],
    response: Response,
) -> dict[str, int | str | list[TrackSchema | None] | None]:
    return await controller.get(filter_query, response)


@track_router.post("", status_code=status.HTTP_201_CREATED)
async def create_item(
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
