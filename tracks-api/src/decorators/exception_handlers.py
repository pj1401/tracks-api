"""
Handle exceptions.
module: src.decorators.exception_handlers
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from src.util.error import (
    convert_to_http_error,
    httpStatusReasonMap,
    log_original_error,
)


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(  # type: ignore[unused-ignore]
        request: Request, exception: StarletteHTTPException
    ):
        """Handle HTTP exceptions."""
        return error_response(exception)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(  # type: ignore[unused-ignore]
        request: Request, exception: RequestValidationError
    ):
        """Handle RequestValidationError"""
        for error in exception.errors():
            log_original_error(error)
        http_status = 400
        response_data = {
            "status": http_status,
            "message": httpStatusReasonMap.get(
                http_status,
                "The server encountered an unexpected condition that prevented it from fulfilling the request.",
            ),
        }
        return JSONResponse(response_data, status_code=http_status)

    @app.exception_handler(Exception)
    async def handle_exception(request: Request, exception: Exception):  # type: ignore[unused-ignore]
        """Handle other exceptions and return a JSON response."""
        return error_response(exception)


def error_response(exception: Exception):
    """Returns an error response."""
    log_original_error(exception)
    http_err = convert_to_http_error(exception)
    return JSONResponse(http_err.to_dict(), status_code=http_err.status)
