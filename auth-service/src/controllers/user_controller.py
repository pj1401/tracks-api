"""
The UserController class.
module: src/controllers/user_controller.py
"""

from typing import cast
from flask import jsonify, request
from flask_jwt_extended import create_access_token  # type: ignore
from src.controllers.writable_controller import WritableController
from src.util.schemas.user import UserArguments, UserLogin
from src.services.user_service import UserService


class UserController(WritableController[UserService]):
    """
    HTTP controller for user-related routes.

    Translates incoming Flask requests into calls on the user service and
    serializes the resulting domain objects (or errors) back into JSON
    responses with appropriate HTTP status codes.
    """

    def __init__(self, user_service: UserService):
        """
        Initialize the controller with its service dependency.

        :param user_service: The service that performs the actual user
            business logic (creation, authentication, etc.).
        :type user_service: UserService
        """
        super().__init__(user_service)

    def create_user(self):
        """
        Handle a request to register a new user.

        Reads a JSON body matching :class:`UserArguments` from the current
        Flask request, delegates user creation to the service, and returns
        the new user's public fields. Any raised exception is converted to
        a structured HTTP error response.

        :return: A Flask JSON response containing either the created user
            (status 201) or an error payload with the corresponding status
            code.
        :rtype: tuple[flask.Response, int]
        """
        try:
            data = request.get_json()
            user_arguments = UserArguments(**data)
            user = self.service.create_user(user_arguments)
            response: dict[str, int | str] = {
                "id": cast(int, user.id),
                "username": str(user.username),
                "email": str(user.email),
                "status": 201,
            }
            return jsonify(response), 201
        except Exception as err:
            return self._error_response(err)

    def login(self):
        """
        Handle a login request and issue a JWT access token.

        Reads a JSON body matching :class:`UserLogin` from the current
        Flask request, asks the service to verify the credentials, and on
        success returns a signed JWT whose identity claim contains the
        user id, username and permission level.

        :return: A Flask JSON response containing either the access token
            (status 200) or an error payload with the corresponding status
            code.
        :rtype: tuple[flask.Response, int]
        """
        try:
            data = request.get_json()
            user = self.service.login(UserLogin(**data))
            access_token: str = create_access_token(
                identity=str(user.id),
                additional_claims={
                    "username": user.username,
                    "permission_level": user.permission_level,
                },
            )
            response: dict[str, int | str] = {
                "access_token": access_token,
                "status": 200,
            }
            return jsonify(response), 200
        except Exception as err:
            return self._error_response(err)
