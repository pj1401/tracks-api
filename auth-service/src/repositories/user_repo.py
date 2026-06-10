"""
The UserRepository class.
module: src/repositories/user_repo.py
"""

from sqlalchemy import exc, select
from sqlalchemy.orm import Session
from src.repositories.writable_repo import WritableRepository
from src.util.errors.error import InvalidCredentialsError, UniqueViolationError
from src.util.filters.base_filters import BaseFilters
from models import User
from src.util.schemas.user import NewUser, UserArguments
from src.db.connection_manager import DatabaseConnectionManager


class UserRepository(WritableRepository[User, BaseFilters, UserArguments]):
    """
    Data-access layer for :class:`User` records.

    Encapsulates all SQLAlchemy interactions for users so that the rest
    of the application can work with plain domain objects without dealing
    with sessions, transactions or ORM-specific exceptions.
    """

    def __init__(
        self,
        db_manager: DatabaseConnectionManager,
        user_model: type[User],
        base_url: str,
    ):
        """
        Initialize the repository with a database connection manager.

        :param db_manager: Provides scoped SQLAlchemy sessions backed by
            the application's configured database engine.
        :type db_manager: DatabaseConnectionManager
        """
        super().__init__(db_manager, user_model, base_url)

    def create_user(self, new_user: NewUser) -> User:
        """
        Persist a new user to the database.

        Opens a session, inserts a :class:`User` row built from
        ``new_user``, commits, and returns the refreshed object so the
        caller sees server-generated fields such as the primary key.

        :param new_user: The validated, ready-to-persist user data
            (username, email, and already-hashed password).
        :type new_user: NewUser
        :raises UniqueViolationError: If the username or email collides
            with an existing record.
        :return: The persisted user, refreshed from the database.
        :rtype: User
        """
        session: Session | None = None
        try:
            session = self.db_manager.get_session()
            user = User(
                username=new_user.username,
                email=new_user.email,
                password_hash=new_user.password_hash,
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except exc.IntegrityError as err:
            if session is not None:
                session.rollback()
            raise UniqueViolationError(err)
        except Exception as err:
            if session is not None:
                session.rollback()
            raise err
        finally:
            if session is not None:
                session.close()

    def get_user_by_username(self, username: str) -> User:
        """
        Look up a single user by their unique username.

        :param username: The exact username to match (case-sensitive).
        :type username: str
        :return: The matching user.
        :rtype: User
        :raises: InvalidCredentialsError if the user is not found.
        """
        session: Session | None = None
        try:
            session = self.db_manager.get_session()
            user = session.scalars(
                select(User).where(User.username == username)
            ).first()
            session.commit()
            if user is None:
                raise InvalidCredentialsError()

            # Expire and refresh attributes on the user object.
            session.refresh(user)

            return user
        except Exception as err:
            if session is not None:
                session.rollback()
            raise err
        finally:
            if session is not None:
                session.close()
