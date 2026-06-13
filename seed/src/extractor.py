"""
Extractor module for extracting data from files.
"""

from collections.abc import Iterator
import pandas as pd
import h5py


def read_csv_data(file_path: str, chunk_size: int) -> Iterator[pd.DataFrame]:
    return pd.read_csv(
        file_path,
        chunksize=chunk_size,
        usecols=[
            "track_id",
            "name",
            "artist",
            "spotify_id",
            "tags",
            "genre",
            "year",
            "duration_ms",
            "danceability",
            "mode",
            "valence",
        ],
    )


def read_hdf5_data(file_path: str) -> dict[str, tuple]:
    with h5py.File(file_path, "r") as f:
        result = {}
        for a_row, m_row in zip(f["analysis"]["songs"], f["metadata"]["songs"]):
            track_id = a_row["track_id"].decode("utf-8").strip().upper()
            result[track_id] = {
                "album_name": m_row["release"].decode("utf-8").strip(),
                "old_album_id": str(m_row["release_7digitalid"]).strip(),
            }
        return result


def read_playcount_data(file_path: str, chunk_size: int) -> Iterator[pd.DataFrame]:
    return pd.read_csv(
        file_path,
        chunksize=chunk_size,
        usecols=[
            "track_id",
            "playcount",
        ],
    )
