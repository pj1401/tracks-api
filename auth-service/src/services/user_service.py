"""
The UserService class.
module: src/services/user_service.py
"""

from typing import Type
import bcrypt
from flask_jwt_extended import get_jwt_identity
from src.services.writable_service import WritableService
from models import User
from src.util.errors.error import InvalidCredentialsError
from src.util.schemas.query_params import BaseQueryParams
from src.util.schemas.user import NewUser, UserArguments, UserLogin, UserModel
from src.repositories.user_repo import UserRepository


class UserService(WritableService[UserRepository, BaseQueryParams, UserArguments]):
    """
    Business logic for user registration and authentication.

    Sits between the controllers and the repository: handles password
    hashing on registration and credential verification on login, so
    neither the HTTP layer nor the data layer needs to know about
    bcrypt.
    """

    def __init__(
        self,
        user_repo: UserRepository,
        user_schema: Type[UserModel],
    ):
        """
        Initialize the service with its repository dependency.

        :param user_repo: Repository used to persist and retrieve users.
        :type user_repo: UserRepository
        """
        super().__init__(user_repo, user_schema)

    def create_user(self, user_arguments: UserArguments):
        """
        Register a new user, hashing the supplied plaintext password.

        :param user_arguments: Validated registration input containing a
            plaintext password that has not yet been hashed.
        :type user_arguments: UserArguments
        :return: The persisted user as returned by the repository.
        :rtype: User
        """
        try:
            password_hash = bcrypt.hashpw(
                user_arguments.password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            return self.repository.create_user(
                NewUser(
                    username=user_arguments.username,
                    email=user_arguments.email,
                    password_hash=password_hash,
                )
            )
        except Exception as err:
            raise err

    def login(self, user_login: UserLogin) -> User:
        """
        Verify a username/password pair and return the matching user.

        Looks up the user by username and uses bcrypt to compare the
        supplied password against the stored hash. The same
        :class:`InvalidCredentialsError` is raised whether the user is
        missing or the password is wrong, so callers cannot use the
        error to probe which usernames exist.

        :param user_login: The submitted login credentials.
        :type user_login: UserLogin
        :raises InvalidCredentialsError: If no such user exists or the
            password does not match.
        :return: The authenticated user.
        :rtype: User
        """
        try:
            user = self.repository.get_user_by_username(user_login.username)
            password_matches = bcrypt.checkpw(
                user_login.password.encode("utf-8"), user.password_hash.encode("utf-8")
            )
            if not password_matches:
                raise InvalidCredentialsError()
            return user
        except Exception as err:
            raise err

    def delete(self, id: int):
        try:
            self.authorize(id, int(get_jwt_identity()))
            self.repository.delete(id)
        except Exception as err:
            raise err
