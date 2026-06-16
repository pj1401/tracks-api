"""
Handle exceptions.
module: src.decorators.exception_handlers
"""

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from src.util.error import httpStatusReasonMap, log_original_error


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(  # type: ignore[unused-ignore]
        request: Request,
        exc: RequestValidationError,
        response: Response,
    ):
        for error in exc.errors():
            log_original_error(error)
        http_status = 400
        response_data = {
            "status": http_status,
            "message": httpStatusReasonMap.get(
                http_status,
                "The server encountered an unexpected condition that prevented it from fulfilling the request.",
            ),
        }
        response.status_code = http_status
        return response_data
