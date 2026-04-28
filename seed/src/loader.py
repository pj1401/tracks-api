"""
Loader module for seeding the database.
module: src/loader.py
"""

from typing import Any

import bcrypt
from psycopg2 import sql
import pandas as pd
from psycopg2.extensions import connection, cursor
from src.util.relationship_info import RelationshipInfo
from src.util.user import User


class DatabaseLoader:
    def __init__(self, conn: connection) -> None:
        self.conn = conn

    def create_tables(self):
        self.create_tracks_table()
        self.create_artists_table()
        self.create_tracks_artists_table()
        self.create_albums_table()
        self.create_tracks_albums_table()
        self.create_artists_albums_table()
        self.create_users_table()

    def create_tracks_table(self):
        query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS tracks (
                track_id SERIAL PRIMARY KEY,
                name VARCHAR(511),
                total_playcount BIGINT DEFAULT 0,
                spotify_id VARCHAR(255),
                tags VARCHAR(511),
                genre VARCHAR(255),
                year INT,
                duration_ms INT,
                danceability FLOAT,
                mode INT,
                valence FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.run_query(query)
        print("Created table: 'tracks'")

    def create_artists_table(self):
        query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS artists (
                artist_id SERIAL PRIMARY KEY,
                artist_name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.run_query(query)
        print("Created table: 'artists'")

    def create_tracks_artists_table(self):
        query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS tracks_artists (
                track_id INTEGER,
                artist_id INTEGER,
                PRIMARY KEY (track_id, artist_id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (track_id) REFERENCES tracks(track_id),
                FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
            );
        """)
        self.run_query(query)
        print("Created table: 'tracks_artists'")

    def create_albums_table(self):
        query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS albums (
                album_id SERIAL PRIMARY KEY,
                album_name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.run_query(query)
        print("Created table: 'albums'")

    def create_tracks_albums_table(self):
        query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS tracks_albums (
                track_id INTEGER,
                album_id INTEGER,
                PRIMARY KEY (track_id, album_id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (track_id) REFERENCES tracks(track_id),
                FOREIGN KEY (album_id) REFERENCES albums(album_id)
            );
        """)
        self.run_query(query)
        print("Created table: 'tracks_albums'")

    def create_artists_albums_table(self):
        query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS artists_albums (
                artist_id INTEGER,
                album_id INTEGER,
                PRIMARY KEY (artist_id, album_id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
                FOREIGN KEY (album_id) REFERENCES albums(album_id)
            );
        """)
        self.run_query(query)
        print("Created table: 'artists_albums'")

    def create_users_table(self):
        query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                permission_level INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.run_query(query)
        print("Created table: 'users'")

    def run_query(self, query: str | sql.SQL) -> None:
        """Run a query with no value placeholders and no return value."""
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

    def seed_database(self, data: pd.DataFrame):
        """Seed the data into the PostgreSQL database."""
        self.seed_artists(data[["artist_id", "artist_name"]])
        self.seed_albums(data[["album_id", "album_name"]])
        self.seed_tracks(
            data[
                [
                    "track_id",
                    "name",
                    "total_playcount",
                    "spotify_id",
                    "tags",
                    "genre",
                    "year",
                    "duration_ms",
                    "danceability",
                    "mode",
                    "valence",
                ]
            ],
        )

        # Seed relationships
        self.seed_tracks_artists(data[["track_id", "artist_id"]])
        self.seed_tracks_albums(data[["track_id", "album_id"]])
        self.seed_artists_albums(data[["artist_id", "album_id"]])

    def seed_admin_user(self, admin: User):
        cursor = self.conn.cursor()
        query = """
            INSERT INTO users (username, email, password_hash, permission_level)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING;
        """
        admin_password_hash = bcrypt.hashpw(
            admin.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        cursor.execute(query, (admin.username, admin.email, admin_password_hash, 1))
        self.conn.commit()
        cursor.close()
        print("Seeded admin user.")

    def seed_artists(self, artists_data: pd.DataFrame):
        cursor = self.conn.cursor()
        for _, row in artists_data.drop_duplicates(subset=["artist_id"]).iterrows():
            query = """
                INSERT INTO artists (artist_name, artist_id)
                VALUES (%s, %s)
                ON CONFLICT (artist_id) DO NOTHING;
            """
            cursor.execute(query, (row["artist_name"], row["artist_id"]))
        self.conn.commit()
        cursor.close()
        print(
            f"Seeded {len(artists_data.drop_duplicates(subset=['artist_id']))} artists."
        )

    def seed_albums(self, albums_data: pd.DataFrame):
        cursor = self.conn.cursor()
        for _, row in albums_data.drop_duplicates(subset=["album_id"]).iterrows():
            query = """
                INSERT INTO albums (album_name, album_id)
                VALUES (%s, %s)
                ON CONFLICT (album_id) DO NOTHING;
            """
            cursor.execute(
                query,
                (
                    row["album_name"],
                    row["album_id"],
                ),
            )
        self.conn.commit()
        cursor.close()
        print(f"Seeded {len(albums_data.drop_duplicates(subset=['album_id']))} albums.")

    def seed_tracks(self, tracks_data: pd.DataFrame):
        cursor = self.conn.cursor()
        for _, row in tracks_data.iterrows():
            query = """
                INSERT INTO tracks (track_id, name, total_playcount, spotify_id, tags, genre,
                year, duration_ms, danceability, mode, valence)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (track_id) DO NOTHING;;
            """
            cursor.execute(
                query,
                (
                    row["track_id"],
                    row["name"],
                    int(row["total_playcount"]),
                    row["spotify_id"],
                    row["tags"],
                    row["genre"],
                    row["year"],
                    row["duration_ms"],
                    row["danceability"],
                    row["mode"],
                    row["valence"],
                ),
            )
        self.conn.commit()
        cursor.close()
        print(f"Seeded {len(tracks_data)} tracks.")

    def seed_tracks_artists(self, tracks_artists_data: pd.DataFrame):
        cursor = self.conn.cursor()
        for _, row in tracks_artists_data.iterrows():
            self.seed_relationship_table(
                cursor,
                RelationshipInfo(
                    "tracks_artists",
                    "track_id",
                    "artist_id",
                    int(row["track_id"]),
                    int(row["artist_id"]),
                ),
            )
        self.conn.commit()
        cursor.close()
        print(f"Seeded {len(tracks_artists_data)} track-artist relationships.")

    def seed_tracks_albums(self, tracks_albums_data: pd.DataFrame):
        cursor = self.conn.cursor()
        for _, row in tracks_albums_data.iterrows():
            query = """
                INSERT INTO tracks_albums (track_id, album_id)
                VALUES (%s, %s)
                ON CONFLICT (track_id, album_id) DO NOTHING;
            """
            cursor.execute(query, (int(row["track_id"]), int(row["album_id"])))
        self.conn.commit()
        cursor.close()
        print(f"Seeded {len(tracks_albums_data)} track-album relationships.")

    def seed_artists_albums(self, artists_albums_data: pd.DataFrame):
        cursor = self.conn.cursor()
        for _, row in artists_albums_data.iterrows():
            query = """
                INSERT INTO artists_albums (artist_id, album_id)
                VALUES (%s, %s)
                ON CONFLICT (artist_id, album_id) DO NOTHING;
            """
            cursor.execute(query, (int(row["artist_id"]), int(row["album_id"])))
        self.conn.commit()
        cursor.close()
        print(f"Seeded {len(artists_albums_data)} artist-album relationships.")

    def seed_relationship_table(self, cursor: cursor, relationship: RelationshipInfo):
        query = sql.SQL("""
            INSERT INTO {table} ({left_col}, {right_col})
            VALUES (%s, %s)
            ON CONFLICT ({left_col}, {right_col}) DO NOTHING;
        """).format(
            table=sql.Identifier(relationship.table_name),
            left_col=sql.Identifier(relationship.left_col),
            right_col=sql.Identifier(relationship.right_col),
        )
        cursor.execute(query, (relationship.left_id, relationship.right_id))

    def get_max_ids(self) -> dict[str, int]:
        """
        Fetch the current max ids from the database.

        :param self: This instance.
        :return: A dictionary with the max ids.
        :rtype: dict[str, int]
        """
        cursor = self.conn.cursor()
        max_ids: dict[str, int] = {}

        cursor.execute("SELECT MAX(artist_id) FROM artists;")
        fetched = cursor.fetchone()
        max_ids["artist_id"] = self.check_max_id(fetched)

        cursor.execute("SELECT MAX(album_id) FROM albums;")
        fetched = cursor.fetchone()
        max_ids["album_id"] = self.check_max_id(fetched)

        cursor.execute("SELECT MAX(track_id) FROM tracks;")
        fetched = cursor.fetchone()
        max_ids["track_id"] = self.check_max_id(fetched)

        cursor.close()
        return max_ids

    def check_max_id(self, fetched: tuple[Any] | None) -> int:
        """
        Get the max id if the fetched tuple is not None.

        :param self: This instance.
        :param fetched: The fetched tuple to check.
        :type fetched: tuple[Any] | None
        :return: The max id or 0.
        :rtype: int
        """
        max_id = 0
        if fetched is not None:
            max_id = fetched[0]
        return max_id
