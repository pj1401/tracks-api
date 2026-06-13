"""
Extractor module for extracting data from files.
"""

from collections.abc import Iterator
import pandas as pd  # type: ignore
import h5py  # type: ignore


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


def read_hdf5_data(file_path: str) -> dict[str, dict[str, str]]:
    with h5py.File(file_path, "r") as f:
        analysis_songs: h5py.Dataset = f["analysis"]["songs"]
        metadata_songs: h5py.Dataset = f["metadata"]["songs"]

        # Slice only the columns that are going to be used.
        track_ids = analysis_songs["track_id"][:]
        releases = metadata_songs["release"][:]
        release_ids = metadata_songs["release_7digitalid"][:]

        result = {}
        for track_id, release, release_id in zip(track_ids, releases, release_ids):
            key = track_id.decode("utf-8").strip().upper()
            result[key] = {
                "album_name": release.decode("utf-8").strip(),
                "old_album_id": str(release_id).strip(),
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
