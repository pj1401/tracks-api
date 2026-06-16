"""
The BaseController class.
module: src/controllers/base_controller.py
"""

from typing import Any, Generic, Mapping, TypeVar
from fastapi import Response
from models.schemas.query_params import BaseQueryParams
from src.services.base_service import BaseService
from src.util.error import convert_to_http_error, log_original_error

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

    async def get(
        self, query_params: BaseQueryParams, response: Response
    ) -> Mapping[str, int | list[Any] | str]:
        """
        Get a list of records using optional query parameters.

        :param query_params: A Pydantic model containing the query parameter data.
        :type query_params: BaseQueryParams
        :param response: The FastAPI response object.
        :type response: Response
        :return: A JSON response.
        :rtype: dict[str, int | list[Any | None] | str]
        """
        try:
            fetched = await self.service.get(query_params)
            result: Mapping[str, int | Any] = {
                "status": 200,
                "data": fetched,
            }
            return result
        except Exception as err:
            return self._error_response(err, response)

    async def get_by_id(
        self, id: int | str, response: Response
    ) -> dict[str, int | Any | str]:
        """
        Fetch one record's data by matching ID.

        :param id: The id of the record.
        :type id: int | str
        :return: A response in JSON.
        :rtype: dict[str, int | Any | None]
        """
        try:
            fetched = await self.service.get_by_id(id)
            result: dict[str, int | Any | None] = {
                "status": 200,
                "data": fetched,
            }
            return result
        except Exception as err:
            return self._error_response(err, response)

    def _error_response(
        self, err: Exception, response: Response
    ) -> dict[str, int | str]:
        """
        Get the error response.

        :param err: The exception used to determine the response.
        :type err: Exception
        :param response: The Response object.
        :type response: Response
        :return: A JSON error response.
        :rtype: dict[str, int | str]
        """
        log_original_error(err)
        http_err = convert_to_http_error(err)
        response.status_code = http_err.status
        return http_err.to_dict()
