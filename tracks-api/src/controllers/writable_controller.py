"""
The WritableController class.
module: src/controllers/writable_controller.py
"""

from typing import Any, TypeVar
from fastapi import Response
from pydantic import BaseModel
from src.controllers.base_controller import BaseController
from src.services.writable_service import WritableService

TService = TypeVar("TService", bound=WritableService[Any, Any, Any])


class WritableController(BaseController[TService]):
    """
    WritableController for handling read/write endpoints.
    """

    async def post(
        self, body_params: BaseModel, response: Response
    ) -> dict[str, int | str | Any]:
        """
        Create a new resource.

        :return: The JSON response with the HTTP status code and created resource.
        :rtype: dict[str, int | str | Any]
        """
        try:
            resource = await self.service.post(body_params)
            result: dict[str, int | Any | None] = {
                "status": 200,
                "data": resource,
            }
            return result
        except Exception as err:
            return self._error_response(err, response)

    async def update(self, id: int, body_params: BaseModel, response: Response):
        """
        Update by using the PUT method.

        :return: Only the status code if the operation was successful. Returns the error response otherwise.
        :rtype: Response | tuple[Response, int]
        """
        try:
            await self.service.update(id, body_params)
        except Exception as err:
            return self._error_response(err, response)

    async def delete(self, id: int, response: Response):
        """
        Delete a resource.

        :param id: The id of the resource.
        :type id: int
        :return: Only the status code if the operation was successful. Returns the error response otherwise.
        :rtype: Response | tuple[Response, int]
        """
        try:
            await self.service.delete(id)
        except Exception as err:
            return self._error_response(err, response)
