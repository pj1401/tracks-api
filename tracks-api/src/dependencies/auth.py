"""
The auth dependencies.
module: src.dependencies.auth
"""

import jwt
from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from models.schemas.users import UserToken
from src.dependencies.settings import get_settings
from src.util.error import InvalidCredentialsError

JWT_ALGORITHM = "ES512"

security = HTTPBearer()


async def get_public_key():
    settings = get_settings()
    return settings.public_key


async def get_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    public_key: Annotated[str, Depends(get_public_key)],
):
    """
    Decodes the JWT and returns the user ID.
    """
    try:
        if not hasattr(credentials, "credentials"):
            raise InvalidCredentialsError
        payload = UserToken(
            **jwt.decode(
                credentials.credentials, public_key, algorithms=[JWT_ALGORITHM]
            )  # type: ignore
        )
        user_id = payload.sub
        if user_id is None:
            raise InvalidCredentialsError
    except InvalidTokenError:
        raise InvalidCredentialsError
    return user_id
