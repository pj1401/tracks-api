"""
The BaseController class.
module: src/controllers/base_controller.py
"""

from typing import Any, Generic, TypeVar
from flask import Response, jsonify, request
from src.services.base_service import BaseService
from src.util.schemas.query_params import BaseQueryParams
from src.util.errors.error import convert_to_http_error, log_original_error

TService = TypeVar("TService", bound=BaseService[Any, Any])


class BaseController(Generic[TService]):
    """
    BaseController for HTTP routes.
    """

    def __init__(self, service: TService):
        """
        Initialise the controller with its service dependency.

        :param service: The service that performs business logic.
        :type service: TService
        """
        self.service = service

    def get(self) -> tuple[Response, int]:
        """
        Get a list of records using optional query parameters.

        :return: A JSON response.
        :rtype: tuple[Response, Literal[200]] | tuple[Response, int]
        """
        try:
            params = self._get_params(request.args)
            fetched = self.service.get(params)
            return jsonify({"status": 200, "data": fetched}), 200
        except Exception as err:
            return self._error_response(err)

    def _get_params(self, args: dict[str, str]) -> BaseQueryParams:
        """
        Get the parameters object.

        :param request: The arguments from the request.
        :type args: dict[str, str]
        :return: The parameters in the form of BaseQueryParams or similar object.
        :rtype: BaseQueryParams
        """
        # Ignore type error since pydantic validates and coerces the types.
        return BaseQueryParams(**args)  # type: ignore

    def get_by_id(self, id: int | str) -> tuple[Response, int]:
        """
        Fetch one record's data by matching ID.

        :param id: The id of the record.
        :type id: int | str
        :return: A response in JSON.
        :rtype: tuple[Response, Literal[200]] | tuple[Response, int]
        """
        try:
            fetched = self.service.get_by_id(id)
            response: dict[str, int | Any | None] = {
                "status": 200,
                "data": fetched,
            }
            return jsonify(response), 200
        except Exception as err:
            return self._error_response(err)

    def _error_response(self, err: Exception) -> tuple[Response, int]:
        """
        Get the error response.

        :param err: The exception used to determine the response.
        :type err: Exception
        :return: A JSON error response.
        :rtype: tuple[Response, int]
        """
        log_original_error(err)
        http_err = convert_to_http_error(err)
        return jsonify(http_err.to_dict()), http_err.status
