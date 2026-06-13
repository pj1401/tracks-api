"""
The starting point of the seed script.
module: seed.py
"""

import os
from dotenv import load_dotenv
from models import BaseModel

from src.util.user import User
from src.sqlalchemy_loader import DatabaseLoader
from src.extractor import read_csv_data, read_hdf5_data, read_playcount_data
from src.transformer import transform, transform_csv_data, transform_playcount_data

# Load environment variables
load_dotenv()

CSV_PATH = os.getenv("CSV_PATH")
HDF5_PATH = os.getenv("HDF5_PATH")
CSV_LISTENING_HISTORY_PATH = os.getenv("CSV_LISTENING_HISTORY_PATH")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 5000))
NO_OF_CHUNKS = int(os.getenv("NO_OF_CHUNKS", 3))


def main():
    print("Connecting to database...")
    db_loader = DatabaseLoader(get_db_uri(), BaseModel)

    # Check if data already exists.
    if not db_loader.database_is_populated():
        # Read data
        print("Reading data...")
        csv_data = read_csv_data(str(CSV_PATH), CHUNK_SIZE)
        hdf5_data = read_hdf5_data(str(HDF5_PATH))
        playcount_data = read_playcount_data(
            str(CSV_LISTENING_HISTORY_PATH), CHUNK_SIZE
        )

        print("Transforming data...")
        # Transform
        total_playcount = transform_playcount_data(playcount_data)
        csv_df = transform_csv_data(csv_data, NO_OF_CHUNKS)

        # Merge with hdf5
        transoformed_data = transform(csv_df, hdf5_data, total_playcount)

        admin_username = _get_env_or_secret("ADMIN_USERNAME")
        admin_email = _get_env_or_secret("ADMIN_EMAIL")
        admin_password = _get_env_or_secret("ADMIN_PASSWORD")

        print("Seeding database...")
        db_loader.seed_admin_user(User(admin_username, admin_email, admin_password))
        db_loader.seed_database(transoformed_data)

        print("Disconnected")
    else:
        print("Database already populated. Skipping seed.")
    return


def _get_env_or_secret(
    env_var: str, default: str | int | None = None
) -> str | int | None:
    """
    Get the value of an environment variable or read it from a file if it ends with _FILE.

    :param env_var: The variable name.
    :type env_var: str
    :param default: The default value of the variable.
    :type default: str | int | None
    :return: The variable value from the file or environment variable.
    :rtype: str | int | None
    """
    file_var = f"{env_var}_FILE"
    value = None
    if file_var in os.environ:
        # Read from file
        with open(os.environ[file_var], "r") as f:
            value = f.read().strip()
    else:
        # Read from environment variable
        value = os.getenv(env_var, default)
    return value


def get_db_uri() -> str:
    """
    Get the formatted db uri.

    :return: The database URI.
    :rtype: str
    """
    POSTGRES_USER = _get_env_or_secret("POSTGRES_USER")
    POSTGRES_PASSWORD = _get_env_or_secret("POSTGRES_PASSWORD")
    POSTGRES_HOST = _get_env_or_secret("POSTGRES_HOST")
    POSTGRES_PORT = _get_env_or_secret("POSTGRES_PORT", "5432")
    POSTGRES_DB = _get_env_or_secret("POSTGRES_DB")
    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


if __name__ == "__main__":
    main()
