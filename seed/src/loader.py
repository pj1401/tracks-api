"""
Loader module for seeding the database.
module: src/loader.py
"""

import bcrypt
from psycopg2 import sql
import pandas as pd
from psycopg2.extensions import connection, cursor
from src.tables import TableQuery
from src.util.relationship_ids import RelationshipIDs
from src.util.relationship_table import RelationshipTable
from src.util.user import User


class DatabaseLoader:
    def __init__(self, conn: connection) -> None:
        """
        Initialise an instance.

        :param self: This instance.
        :param conn: The database connection object.
        :type conn: connection
        """
        self.conn = conn
        self.tables = TableQuery()

    def create_tables(self):
        """
        Run queries for creating tables.

        :param self: This instance.
        """
        queries = self.tables.get_queries()
        self.execute_queries(queries)

    def execute_queries(self, queries: list[sql.SQL]) -> None:
        """
        Execute a list of queries.

        :param self: This instance.
        :param queries: A list of queries.
        :type queries: list[sql.SQL]
        """
        cursor = self.conn.cursor()
        for query in queries:
            cursor.execute(query)
        self.conn.commit()
        cursor.close()

    def seed_admin_user(self, admin: User):
        cursor = self.conn.cursor()
        query = """
            INSERT INTO users (username, email, password_hash, permission_level)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING;
        """
        # Create a password hash before storing.
        admin_password_hash = bcrypt.hashpw(
            admin.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute(query, (admin.username, admin.email, admin_password_hash, 1))
        self.conn.commit()
        cursor.close()
        print("Seeded admin user.")

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
                (row["album_name"], row["album_id"]),
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
        self.seed_relationship_table(
            tracks_artists_data,
            RelationshipTable("tracks_artists", "track_id", "artist_id"),
        )
        print(f"Seeded {len(tracks_artists_data)} track-artist relationships.")

    def seed_tracks_albums(self, tracks_albums_data: pd.DataFrame):
        self.seed_relationship_table(
            tracks_albums_data,
            RelationshipTable("tracks_albums", "track_id", "album_id"),
        )
        print(f"Seeded {len(tracks_albums_data)} track-album relationships.")

    def seed_artists_albums(self, artists_albums_data: pd.DataFrame):
        self.seed_relationship_table(
            artists_albums_data,
            RelationshipTable("artists_albums", "artist_id", "album_id"),
        )
        print(f"Seeded {len(artists_albums_data)} artist-album relationships.")

    def seed_relationship_table(
        self, data: pd.DataFrame, relationship: RelationshipTable
    ):
        """
        Iterate over relationship data and seed the relationship table.

        :param self: This instance.
        :param data: The DataFrame with the relationship data.
        :type data: pd.DataFrame
        :param relationship: Relationship info for the query string.
        :type relationship: RelationshipQuery
        """
        cursor = self.conn.cursor()
        for _, row in data.iterrows():
            self.execute_relationship_query(
                cursor,
                relationship,
                RelationshipIDs(
                    int(row[relationship.left_col]), int(row[relationship.right_col])
                ),
            )
        self.conn.commit()
        cursor.close()

    def execute_relationship_query(
        self, cursor: cursor, relationship: RelationshipTable, ids: RelationshipIDs
    ):
        """
        Execute a query for seeding a relationship table.

        :param self: This instance.
        :param cursor: The cursor from the connection.
        :type cursor: cursor
        :param relationship: Relationship info for the query string.
        :type relationship: RelationshipQuery
        :param ids: The id values.
        :type ids: RelationshipIDs
        """
        query = sql.SQL("""
            INSERT INTO {table} ({left_col}, {right_col})
            VALUES (%s, %s)
            ON CONFLICT ({left_col}, {right_col}) DO NOTHING;
        """).format(
            table=sql.Identifier(relationship.table_name),
            left_col=sql.Identifier(relationship.left_col),
            right_col=sql.Identifier(relationship.right_col),
        )
        cursor.execute(query, (ids.left_id, ids.right_id))
