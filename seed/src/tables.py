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

    def get_create_tracks_query(self):
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
