"""
DatabaseLoader class.
module: src/sqlalchemy_loader.py
"""

from typing import Dict, Iterator, List, Optional, Type, TypeVar, cast
import bcrypt
import numpy as np
import pandas as pd
from sqlalchemy import Table, create_engine, inspect
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
from src.util.user import User as UserSchema

from models import (
    Album,
    Artist,
    Track,
    User,
    artists_tracks_table,
    tracks_albums_table,
)

# Use generic type model
M = TypeVar("M", bound=DeclarativeBase)


class DatabaseLoader:
    def __init__(self, uri: str, base_model: Type[M]) -> None:
        self.engine = create_engine(uri, pool_pre_ping=True)
        base_model.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)

    def database_is_populated(self) -> bool:
        """
        Check if the database already has data.

        :return: True if there is data in the database.
        :rtype: bool
        """
        session = self.session_factory()
        try:
            track_count = session.query(Track).count()
            return track_count > 0
        except Exception:
            return False
        finally:
            session.close()

    def seed_database(
        self, data: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]
    ) -> None:
        """Seed the database."""
        tracks_df, artists_df, albums_df = data
        self.seed_artists(artists_df)
        self.seed_albums(albums_df)
        self.seed_tracks(tracks_df)
        self.seed_artists_albums(tracks_df)
        self.seed_artists_tracks(tracks_df)
        self.seed_tracks_albums(tracks_df)

    def load_table(self, table_name: str, data: List[M], model: Type[M]) -> None:
        """Load seed data from a DataFrame into a table."""
        session = self.session_factory()
        try:
            if inspect(self.engine).has_table(table_name):
                session.query(model).delete()
            session.add_all(data)
            session.commit()
            print(f"Successfully loaded {len(data)} {table_name}.")
        except SQLAlchemyError as err:
            session.rollback()
            raise err
        finally:
            session.close()

    def seed_relationship_table(
        self, relationships: List[Dict[str, int]], table: Table, relationship_name: str
    ) -> None:
        """Seed a relationship table."""
        session = self.session_factory()
        try:
            session.query(table).delete()
            session.execute(table.insert(), relationships)
            session.commit()
            print(
                f"Successfully seeded {len(relationships)} {relationship_name} relationships."
            )
        except SQLAlchemyError as err:
            session.rollback()
            raise err
        finally:
            session.close()

    def seed_admin_user(self, admin: UserSchema):
        session = self.session_factory()

        # Create a password hash before storing.
        admin_password_hash = bcrypt.hashpw(
            admin.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        try:
            if inspect(self.engine).has_table("users"):
                session.query(User).delete()
            user = User(
                username=admin.username,
                email=admin.email,
                password_hash=admin_password_hash,
                permission_level=1,
            )
            session.add(user)
            session.commit()
            print("Seeded admin user.")
        except SQLAlchemyError as err:
            session.rollback()
            raise err
        finally:
            session.close()
