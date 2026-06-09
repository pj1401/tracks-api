"""
The starting point of the seed script.
module: seed.py
"""

import os
import psycopg2
from dotenv import load_dotenv
from models import BaseModel

from src.util.user import User
from src.sqlalchemy_loader import DatabaseLoader
from src.extractor import read_csv_data, read_hdf5_data, read_playcount_data
from src.transformer import transform, transform_csv_data, transform_playcount_data

# Load environment variables
load_dotenv()

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")

SQL_TABLE = os.getenv("SQL_TABLE")

CSV_PATH = os.getenv("CSV_PATH")
HDF5_PATH = os.getenv("HDF5_PATH")
CSV_LISTENING_HISTORY_PATH = os.getenv("CSV_LISTENING_HISTORY_PATH")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 5000))
NO_OF_CHUNKS = int(os.getenv("NO_OF_CHUNKS", 3))

admin_username = str(os.getenv("ADMIN_USERNAME"))
admin_email = str(os.getenv("ADMIN_EMAIL"))
admin_password = str(os.getenv("ADMIN_PASSWORD"))

# Read secrets from files
ENVIRONMENT = str(os.getenv("ENVIRONMENT", "production"))
if ENVIRONMENT == "production":
    admin_username = open("/run/secrets/admin_username", "r").read().strip()
    admin_email = open("/run/secrets/admin_email", "r").read().strip()
    admin_password = open("/run/secrets/admin_password", "r").read().strip()


def connect_to_db():
    """Connect to PostgreSQL database."""
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )
    print("Connected to database")
    return conn


def main():
    db_loader = DatabaseLoader(get_db_uri(), BaseModel)

    # Check if data already exists.
    if not db_loader.database_is_populated():
        # Read data
        csv_data = read_csv_data(str(CSV_PATH), CHUNK_SIZE)
        hdf5_data = read_hdf5_data(str(HDF5_PATH))
        playcount_data = read_playcount_data(
            str(CSV_LISTENING_HISTORY_PATH), CHUNK_SIZE
        )

        # Transform
        total_playcount = transform_playcount_data(playcount_data)
        csv_df = transform_csv_data(csv_data, NO_OF_CHUNKS)

        # Merge with hdf5
        combined_data = transform(csv_df, hdf5_data, total_playcount)

        db_loader.seed_admin_user(User(admin_username, admin_email, admin_password))
        db_loader.seed_database(combined_data)

        print("Disconnected")
    else:
        print("Database already populated. Skipping seed.")
    return


def get_db_uri() -> str:
    """
    Get the formatted db uri.

    :return: The database URI.
    :rtype: str
    """
    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


if __name__ == "__main__":
    main()
