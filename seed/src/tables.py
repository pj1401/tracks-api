"""
SQL queries for creating tables.
module: src/tables.py
"""

from psycopg2 import sql


class TableQuery:
    """
    Queries for creating tables.
    """

    def __init__(self):
        pass

    def get_queries(self) -> list[sql.SQL]:
        """
        Get a list of all the create table queries.

        :param self: This instance.
        :return: A list of create table queries.
        :rtype: list[SQL]
        """
        return [
            self.get_create_tracks_query(),
            self.get_create_artists_query(),
            self.get_create_tracks_artists_query(),
            self.get_create_albums_query(),
            self.get_create_tracks_albums_query(),
            self.get_create_artists_albums_query(),
            self.get_create_users_query(),
        ]

    def get_create_tracks_query(self) -> sql.SQL:
        """
        Get the statement for creating the tracks table.

        :param self: This instance.
        :return: The SQL query.
        :rtype: SQL
        """
        return sql.SQL("""
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

    def get_create_artists_query(self) -> sql.SQL:
        return sql.SQL("""
                    CREATE TABLE IF NOT EXISTS artists (
                        artist_id SERIAL PRIMARY KEY,
                        artist_name VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

    def get_create_tracks_artists_query(self) -> sql.SQL:
        return sql.SQL("""
            CREATE TABLE IF NOT EXISTS tracks_artists (
                track_id INTEGER,
                artist_id INTEGER,
                PRIMARY KEY (track_id, artist_id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (track_id) REFERENCES tracks(track_id),
                FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
            );
        """)

    def get_create_albums_query(self) -> sql.SQL:
        return sql.SQL("""
            CREATE TABLE IF NOT EXISTS albums (
                album_id SERIAL PRIMARY KEY,
                album_name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

    def get_create_tracks_albums_query(self) -> sql.SQL:
        return sql.SQL("""
            CREATE TABLE IF NOT EXISTS tracks_albums (
                track_id INTEGER,
                album_id INTEGER,
                PRIMARY KEY (track_id, album_id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (track_id) REFERENCES tracks(track_id),
                FOREIGN KEY (album_id) REFERENCES albums(album_id)
            );
        """)

    def get_create_artists_albums_query(self) -> sql.SQL:
        return sql.SQL("""
            CREATE TABLE IF NOT EXISTS artists_albums (
                artist_id INTEGER,
                album_id INTEGER,
                PRIMARY KEY (artist_id, album_id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
                FOREIGN KEY (album_id) REFERENCES albums(album_id)
            );
        """)

    def get_create_users_query(self) -> sql.SQL:
        return sql.SQL("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                permission_level INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
