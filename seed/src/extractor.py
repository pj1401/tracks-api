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


# def read_hdf5_data(file_path: str) -> pd.DataFrame:
#     with h5py.File(file_path, "r") as f:
#         # Read analysis group
#         analysis_data = f["analysis"]["songs"][:]
#         analysis_df = pd.DataFrame(analysis_data, columns=["track_id"])

#         # Read metadata group
#         metadata_data = f["metadata"]["songs"][:]
#         metadata_df = pd.DataFrame(
#             metadata_data,
#             columns=["song_id", "release", "release_7digitalid", "artist_id"],
#         )

#         # Align by index
#         hdf5_df = pd.concat([analysis_df, metadata_df], axis=1)

#         return hdf5_df


def read_hdf5_data(file_path: str) -> dict[str, tuple]:
    with h5py.File(file_path, "r") as f:
        analysis_data = f["analysis"]["songs"][:]
        metadata_data = f["metadata"]["songs"][:]
        result = {}
        for a_row, m_row in zip(analysis_data, metadata_data):
            track_id = str(a_row[0]).strip().upper()
            result[track_id] = (
                str(m_row[0]).strip(),
                str(m_row[1]).strip(),
                str(m_row[2]).strip(),
                str(m_row[3]).strip(),
            )
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
