"""
Custom errors and helper functions.
module: src/util/errors/error.py
"""

import logging


class CustomError(Exception):
    """Base class for custom errors."""

    def __init__(
        self, err: Exception | None = None, message: str = "An error occurred."
    ):
        self.err = err
        self.message = message


class UniqueViolationError(CustomError):
    def __init__(
        self,
        err: Exception,
        message: str = "Duplicate key value violates unique constraint.",
    ):
        super().__init__(err, message)


class InvalidCredentialsError(CustomError):
    def __init__(
        self,
        err: Exception | None = None,
        message: str = "Credentials invalid or not provided.",
    ):
        super().__init__(err, message)


class ForbiddenError(CustomError):
    def __init__(
        self,
        err: Exception | None = None,
        message: str = "The request contained valid data and was understood by the server, but the server is refusing action due to the authenticated user not having the necessary permissions for the resource.",
    ):
        super().__init__(err, message)


class NotFoundError(CustomError):
    def __init__(
        self,
        err: Exception | None = None,
        message: str = "The requested resource was not found.",
    ):
        super().__init__(err, message)


class HttpError(CustomError):
    """An error with an HTTP status and message."""

    def __init__(
        self,
        err: Exception,
        status: int,
        message: str = "The server encountered an unexpected condition that prevented it from fulfilling the request.",
    ):
        super().__init__(err, message)
        self.status = status

    def to_dict(self) -> dict[str, int | str]:
        return {
            "status": self.status,
            "message": self.message,
        }


def convert_to_http_error(err: Exception) -> HttpError:
    error_name = type(err).__name__
    status = errorHttpStatusMap.get(error_name, 500)
    message = httpStatusReasonMap.get(
        status,
        "The server encountered an unexpected condition that prevented it from fulfilling the request.",
    )
    return HttpError(err, status, message)


errorHttpStatusMap = {
    "BadRequest": 400,
    "UniqueViolationError": 400,
    "ValidationError": 400,
    "InvalidCredentialsError": 401,
    "ForbiddenError": 404,  # Don't leak information.
    "NotFoundError": 404,
}

httpStatusReasonMap = {
    400: "The request cannot or will not be processed due to something that is perceived to be a client error (for example validation error).",
    401: "Credentials invalid or not provided.",
    404: "The requested resource was not found.",
    500: "The server encountered an unexpected condition that prevented it from fulfilling the request.",
}


def log_original_error(err: Exception):
    logging.error(f"Error occurred: {type(err).__name__}, Original exception: {err}")
