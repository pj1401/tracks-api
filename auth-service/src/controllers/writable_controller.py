"""
The WritableController class.
module: src/controllers/writable_controller.py
"""

from typing import Any, Dict, TypeVar
from flask import Response, jsonify, request
from flask_jwt_extended import get_jwt_identity
from pydantic import BaseModel as PydanticBaseModel
from src.controllers.base_controller import BaseController
from src.services.writable_service import WritableService

TService = TypeVar("TService", bound=WritableService[Any, Any, Any])


class WritableController(BaseController[TService]):
    """
    WritableController for handling read/write endpoints.
    """

    def post(self) -> tuple[Response, int]:
        """
        Create a new resource.

        :return: The JSON response and the HTTP status code.
        :rtype: tuple[Response, int]
        """
        try:
            arguments = self.get_validated_arguments(
                request.get_json(), get_jwt_identity()
            )
            resource = self.service.post(arguments)
            response = self.get_post_response(resource)
            return jsonify(response), 201
        except Exception as err:
            return self._error_response(err)

    def get_validated_arguments(
        self, data: dict[str, str], user_id: str
    ) -> PydanticBaseModel:
        """
        Validates the arguments from the request body and returns them as a pydantic model.

        :param data: The arguments from the request body.
        :type data: dict[str, str]
        :param user_id: The ID of the user.
        :type user_id: int
        :return: The arguments as a validated pydantic model.
        :rtype: BaseModel
        """
        return PydanticBaseModel(**data)

    def get_post_response(self, resource: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get the response data for POST requests.

        :param resource: A dictionary representing the resource.
        :type resource: Dict[str, Any]
        :return: The response data in the form of a dictionary.
        :rtype: Dict[str, Any]
        """
        return resource | {
            "status": 201,
        }

    def update(self, id: int):
        """
        Update by using the PUT method.

        :param id: The id of the resource.
        :type id: int
        :return: Only the status code if the operation was successful. Returns the error response otherwise.
        :rtype: Response | tuple[Response, int]
        """
        try:
            arguments = self.get_validated_arguments(
                request.get_json(), get_jwt_identity()
            )
            self.service.update(id, arguments)
            return Response(None, 204)
        except Exception as err:
            return self._error_response(err)

    def delete(self, id: int):
        """
        Delete a resource.

        :param id: The id of the resource.
        :type id: int
        :return: Only the status code if the operation was successful. Returns the error response otherwise.
        :rtype: Response | tuple[Response, int]
        """
        try:
            self.service.delete(id)
            return Response(None, 204)
        except Exception as err:
            return self._error_response(err)
