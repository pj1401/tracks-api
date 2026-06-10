"""
Set up auth required decorator.
module: src/decorators/auth_required.py
"""

from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar
from flask_jwt_extended import verify_jwt_in_request  # type: ignore
from flask_jwt_extended.exceptions import JWTExtendedException
from src.util.errors.error import InvalidCredentialsError

F = TypeVar("F", bound=Callable[..., Any])


def auth_required() -> Callable[[F], F]:
    def wrapper(fn: F) -> F:
        @wraps(fn)
        def decorator(*args: Any, **kwargs: Any) -> Any:
            """
            A decorator that checks the JWT from the request. Raises an error if the JWT is invalid or missing.
            """
            try:
                verify_jwt_in_request()  # type: ignore[reportUnknownVariableType]
            except JWTExtendedException as err:
                raise InvalidCredentialsError() from err
            return fn(*args, **kwargs)

        return decorator  # type: ignore[return-value]

    return wrapper
