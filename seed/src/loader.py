"""
Loader module for seeding the database.
module: src/loader.py
"""

from typing import Any
import bcrypt
from psycopg2 import sql
import pandas as pd
from psycopg2.extensions import connection, cursor
from src.tables import TableQuery
from src.util.relationship_ids import RelationshipIDs
from src.util.relationship_query import RelationshipQuery
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
        self.seed_albums(data[["album_id", "album_name", "old_album_id"]])
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
                INSERT INTO albums (album_name, album_id, old_album_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (album_id) DO NOTHING;
            """
            cursor.execute(
                query,
                (row["album_name"], row["album_id"], row["old_album_id"]),
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
            RelationshipQuery("tracks_artists", "track_id", "artist_id"),
        )
        print(f"Seeded {len(tracks_artists_data)} track-artist relationships.")

    def seed_tracks_albums(self, tracks_albums_data: pd.DataFrame):
        self.seed_relationship_table(
            tracks_albums_data,
            RelationshipQuery("tracks_albums", "track_id", "album_id"),
        )
        print(f"Seeded {len(tracks_albums_data)} track-album relationships.")

    def seed_artists_albums(self, artists_albums_data: pd.DataFrame):
        self.seed_relationship_table(
            artists_albums_data,
            RelationshipQuery("artists_albums", "artist_id", "album_id"),
        )
        print(f"Seeded {len(artists_albums_data)} artist-album relationships.")

    def seed_relationship_table(
        self, data: pd.DataFrame, relationship: RelationshipQuery
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
        self, cursor: cursor, relationship: RelationshipQuery, ids: RelationshipIDs
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

    def create_indexes(self) -> None:
        """Create indexes for artists and albums."""
        queries = [
            sql.SQL(
                "CREATE INDEX IF NOT EXISTS idx_artist_name ON artists(artist_name);"
            ),
            sql.SQL(
                "CREATE INDEX IF NOT EXISTS idx_album_old_id ON albums(old_album_id);"
            ),
        ]
        self.execute_queries(queries)
        print("Created indexes for artists and albums.")

    def update_relationships(self) -> None:
        queries = self.get_update_relationship_queries()
        self.execute_queries(queries)
        print("Updated relationships.")

    def get_update_relationship_queries(self) -> list[sql.SQL]:
        return (
            self.get_update_artists_relationships()
            + self.get_update_albums_relationships()
        )

    def get_update_artists_relationships(self) -> list[sql.SQL]:
        queries = [
            sql.SQL("""
            UPDATE tracks_artists ta_table
            SET artist_id = a.new_artist_id
            FROM (
                SELECT artist_name, MIN(artist_id) AS new_artist_id
                FROM artists
                GROUP BY artist_name
            ) a
            WHERE EXISTS (
                SELECT 1
                FROM artists a2
                WHERE a2.artist_name = a.artist_name
                AND a2.artist_id = ta_table.artist_id
            )
            AND ta_table.artist_id != a.new_artist_id;
        """)
        ]

        queries.append(
            sql.SQL("""
            UPDATE artists_albums aa_table
            SET artist_id = a.new_artist_id
            FROM (
                SELECT artist_name, MIN(artist_id) AS new_artist_id
                FROM artists
                GROUP BY artist_name
            ) a
            WHERE EXISTS (
                SELECT 1
                FROM artists a2
                WHERE a2.artist_name = a.artist_name
                AND a2.artist_id = aa_table.artist_id
            )
            AND aa_table.artist_id != a.new_artist_id;
        """)
        )
        return queries

    def get_update_albums_relationships(self) -> list[sql.SQL]:
        queries = [
            sql.SQL("""
            UPDATE tracks_albums ta_table
            SET album_id = a.new_album_id
            FROM (
                SELECT old_album_id, MIN(album_id) AS new_album_id
                FROM albums
                GROUP BY old_album_id
            ) a
            WHERE EXISTS (
                SELECT 1
                FROM albums a2
                WHERE a2.old_album_id = a.old_album_id
                AND a2.album_id = ta_table.album_id
            )
            AND ta_table.album_id != a.new_album_id;
        """)
        ]

        queries.append(
            sql.SQL("""
            UPDATE artists_albums aa_table
            SET album_id = a.new_album_id
            FROM (
                SELECT old_album_id, MIN(album_id) AS new_album_id
                FROM albums
                GROUP BY old_album_id
            ) a
            WHERE EXISTS (
                SELECT 1
                FROM albums a2
                WHERE a2.old_album_id = a.old_album_id
                AND a2.album_id = aa_table.album_id
            )
            AND aa_table.album_id != a.new_album_id;
        """)
        )
        return queries

    def drop_duplicates(self) -> None:
        queries = self.get_drop_duplicates_queries()
        self.execute_queries(queries)
        print("Dropped duplicates.")

    def get_drop_duplicates_queries(self) -> list[sql.SQL]:
        queries = [
            sql.SQL("""
                DELETE FROM artists
                WHERE artist_id NOT IN (
                    SELECT MIN(artist_id)
                    FROM artists
                    GROUP BY artist_name
                );
            """)
        ]
        queries.append(
            sql.SQL("""
                DELETE FROM albums
                WHERE album_id NOT IN (
                    SELECT MIN(album_id)
                    FROM albums
                    GROUP BY old_album_id
                );
            """)
        )
        return queries

    def remove_temp_cols(self):
        query = sql.SQL("""
                        ALTER TABLE albums
                        DROP COLUMN old_album_id;
                        """)
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()
