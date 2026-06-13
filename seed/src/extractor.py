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

        # Only save columns that are going to be used.
        df = pd.DataFrame(
            {
                "track_id": analysis_songs["track_id"][:],
                "release": metadata_songs["release"][:],
                "release_7digitalid": metadata_songs["release_7digitalid"][:],
            }
        )

    # Decode values.
    df["track_id"] = df["track_id"].str.decode("utf-8").str.strip().str.upper()
    df["release"] = df["release"].str.decode("utf-8").str.strip()
    df["release_7digitalid"] = df["release_7digitalid"].astype(str).str.strip()

    df = df.set_index("track_id")
    return df.rename(
        columns={"release": "album_name", "release_7digitalid": "old_album_id"}
    ).to_dict("index")


def read_playcount_data(file_path: str, chunk_size: int) -> Iterator[pd.DataFrame]:
    return pd.read_csv(
        file_path,
        chunksize=chunk_size,
        usecols=[
            "track_id",
            "playcount",
        ],
    )
