"""
Handle exceptions.
module: src/decorators/exception_handlers.py
"""

from flask import Flask, Response, json, jsonify
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import response
from src.util.errors.error import convert_to_http_error, log_original_error


def setup_exception_handlers(app: Flask):
    @app.errorhandler(HTTPException)
    def handle_http_exception(err: HTTPException) -> response.Response:  # type: ignore[unused-ignore]
        """Turn default error response to JSON"""
        log_original_error(err)
        response = err.get_response()
        response.data = json.dumps(
            {
                "status": err.code,
                "message": err.description
                if err.code != 404
                else "The requested resource was not found.",
            }
        )
        response.content_type = "application/json"
        return response

    @app.errorhandler(Exception)
    def handle_exception(err: Exception) -> tuple[Response, int]:  # type: ignore[unused-ignore]
        """
        Handle exception and return a JSON response.

        :param err: The Exception object.
        :type err: Exception
        :return: A JSON response.
        :rtype: tuple[Response, int]
        """
        log_original_error(err)
        http_err = convert_to_http_error(err)
        return jsonify(http_err.to_dict()), http_err.status
