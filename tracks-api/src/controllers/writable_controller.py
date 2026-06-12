"""
The WritableController class.
module: src/controllers/writable_controller.py
"""

from typing import Any, TypeVar
from fastapi import Response
from src.controllers.base_controller import BaseController
from src.services.writable_service import WritableService

TService = TypeVar("TService", bound=WritableService[Any, Any, Any])


class WritableController(BaseController[TService]):
    """
    WritableController for handling read/write endpoints.
    """

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
