"""
Set up logging decorators.
module: src/decorators/logging.py
"""

from flask import Flask, request, Response


def setup_logging_decorators(app: Flask) -> None:
    """Set up request and response logging decorators."""

    @app.before_request
    def log_request_info() -> None:  # type: ignore[unused-ignore]
        app.logger.info(
            "Request: %s %s %s", request.method, request.path, request.remote_addr
        )

    @app.after_request
    def log_response_info(response: Response) -> Response:  # type: ignore[unused-ignore]
        app.logger.info(
            "Response: %s %s %s", response.status_code, request.method, request.path
        )
        return response
