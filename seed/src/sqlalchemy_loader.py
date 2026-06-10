"""
DatabaseLoader class.
module: src/sqlalchemy_loader.py
"""

from typing import Dict, List, Type, TypeVar, cast
import bcrypt
import pandas as pd  # type: ignore
from sqlalchemy import Table, create_engine, inspect
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
from src.util.relationship_table import RelationshipTable
from src.util.user import User as UserSchema

from models import (  # type: ignore
    Album,
    Artist,
    Track,
    User,
    artists_albums_table,
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

    def seed_artists(self, data: pd.DataFrame) -> None:
        """Seed the artists table."""
        artists = [
            Artist(name=row["artist_name"], id=row["artist_id"])
            for _, row in data.iterrows()
        ]
        self.load_table("artists", artists, Artist)

    def seed_albums(self, data: pd.DataFrame) -> None:
        """Seed the albums table."""
        albums = [
            Album(name=row["album_name"], id=row["album_id"])
            for _, row in data.iterrows()
        ]
        self.load_table("albums", albums, Album)

    def seed_tracks(self, data: pd.DataFrame) -> None:
        """Seed the tracks table."""
        tracks = [
            Track(
                name=row["name"],
                total_playcount=cast(int, row["total_playcount"]),
                spotify_id=row["spotify_id"],
                tags=row["tags"],
                genre=row["genre"],
                year=row["year"],
                duration_ms=row["duration_ms"],
                danceability=row["danceability"],
                mode=row["mode"],
                valence=row["valence"],
            )
            for _, row in data.iterrows()
        ]
        self.load_table("tracks", tracks, Track)

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

    def seed_artists_albums(self, tracks_data: pd.DataFrame) -> None:
        """Seed the artists_albums relationship table."""
        self.load_relationship_table(
            tracks_data,
            artists_albums_table,
            RelationshipTable("artists_albums", "artist_id", "album_id"),
        )

    def seed_artists_tracks(self, tracks_data: pd.DataFrame) -> None:
        """Seed the artists_tracks relationship table."""
        self.load_relationship_table(
            tracks_data,
            artists_tracks_table,
            RelationshipTable("artists_tracks", "artist_id", "track_id"),
        )

    def seed_tracks_albums(self, tracks_data: pd.DataFrame) -> None:
        """Seed the tracks_albums relationship table."""
        self.load_relationship_table(
            tracks_data,
            tracks_albums_table,
            RelationshipTable("tracks_albums", "track_id", "album_id"),
        )

    def load_relationship_table(
        self, data: pd.DataFrame, table: Table, relationship: RelationshipTable
    ) -> None:
        """Seed a relationship table."""
        relationships = self.get_relationship_data(data, relationship)
        session = self.session_factory()
        try:
            session.query(table).delete()
            session.execute(table.insert(), relationships)
            session.commit()
            print(
                f"Successfully seeded {len(relationships)} {relationship.table_name} relationships."
            )
        except SQLAlchemyError as err:
            session.rollback()
            raise err
        finally:
            session.close()

    def get_relationship_data(
        self, data: pd.DataFrame, relationship: RelationshipTable
    ) -> List[Dict[str, int]]:
        """
        Get a list of dictionaries representing the relationships.

        :param data: The data as a DataFrame
        :type data: pd.DataFrame
        :param relationship: The relationship object that contains the column names and table name.
        :type relationship: RelationshipTable
        :return: A list of dictionaries representing the relationships.
        :rtype: List[Dict[str, int]]
        """
        relationships: List[Dict[str, int]] = []

        # To filter existing relationships
        seen: set[tuple[int, int]] = set()

        for _, row in data.iterrows():
            rel_tuple = (
                cast(int, row[relationship.left_col]),
                cast(int, row[relationship.right_col]),
            )
            if rel_tuple not in seen:
                seen.add(rel_tuple)
                relationships.append(
                    {
                        f"{relationship.left_col}": cast(
                            int, row[relationship.left_col]
                        ),
                        f"{relationship.right_col}": cast(
                            int, row[relationship.right_col]
                        ),
                    }
                )
        return relationships

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
