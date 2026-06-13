"""
Transformer module for cleaning and joining data.
module: src/transformer.py
"""

from collections.abc import Iterator

import pandas as pd  # type: ignore
import json


def transform_playcount_data(playcount_data: Iterator[pd.DataFrame]) -> pd.DataFrame:
    total_playcount = pd.DataFrame()
    for chunk in playcount_data:
        chunk["track_id"] = chunk["track_id"].astype("str").str.strip().str.upper()
        chunk = chunk.groupby("track_id")["playcount"].sum().reset_index()
        total_playcount = (
            pd.concat([total_playcount, chunk])
            .groupby("track_id")["playcount"]
            .sum()
            .reset_index()
        )
    return total_playcount


def transform_csv_data(
    csv_data: Iterator[pd.DataFrame], no_of_chunks: int
) -> pd.DataFrame:
    csv_df = pd.DataFrame()
    for i, chunk in enumerate(csv_data):
        if i >= no_of_chunks:
            break
        chunk["track_id"] = chunk["track_id"].astype("str").str.strip().str.upper()
        chunk["tags"] = chunk["tags"].astype("str").str.strip()
        chunk["tags"] = chunk["tags"].apply(json.dumps)
        chunk["genre"] = chunk["genre"].astype("str").str.strip()
        chunk["genre"] = chunk["genre"].apply(json.dumps)
        chunk = normalize_columns(chunk)
        csv_df = pd.concat([csv_df, chunk])
    return csv_df


def merge(
    df: pd.DataFrame, hdf5_df: pd.DataFrame, total_playcount: pd.DataFrame
) -> pd.DataFrame:
    """Merge csv, hdf and playcount data."""
    # Normalise track_id
    df["track_id"] = df["track_id"].astype("str").str.strip().str.upper()
    hdf5_df["track_id"] = hdf5_df["track_id"].astype("str").str.strip().str.upper()
    total_playcount["track_id"] = (
        total_playcount["track_id"].astype("str").str.strip().str.upper()
    )

    # Merge
    merged = df.merge(hdf5_df, on="track_id", how="inner")
    merged = merged.merge(total_playcount, on="track_id", how="left")

    return merged


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Normalise values from the hdf5 data.
    df["song_id"] = df["song_id"].astype("str").str.strip()
    df["release"] = df["release"].astype("str").str.strip()
    df["release_7digitalid"] = df["release_7digitalid"].astype("str").str.strip()
    df["artist_id"] = df["artist_id"].astype("str").str.strip()
    return df


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase column names and strip surrounding whitespace."""
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.rename(columns={"track_id": "old_track_id"})
    df = df.rename(columns={"artist": "artist_name"})
    df = df.rename(columns={"artist_id": "old_artist_id"})
    df = df.rename(columns={"release": "album_name"})
    df = df.rename(columns={"release_7digitalid": "old_album_id"})
    df = df.rename(columns={"playcount": "total_playcount"})
    return df


def replace_NaN(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["total_playcount"] = df["total_playcount"].fillna(0)
    df["total_playcount"] = df["total_playcount"].astype("int64")
    return df


def transform_artists(df: pd.DataFrame) -> pd.DataFrame:
    artists_df = pd.DataFrame(
        df[["artist_name"]].drop_duplicates().reset_index(drop=True)
    )
    artists_df["artist_id"] = artists_df.index + 1
    return normalize_columns(artists_df)


def transform_albums(df: pd.DataFrame) -> pd.DataFrame:
    albums_df = pd.DataFrame(df[["album_name", "old_album_id"]].reset_index(drop=True))
    albums_df = albums_df.drop_duplicates(subset=["old_album_id"], keep="first")
    albums_df["album_id"] = albums_df.index + 1
    return normalize_columns(albums_df)


def transform_tracks(df: pd.DataFrame) -> pd.DataFrame:
    """Generate new track_ids and drop duplicates based on old_track_id."""
    df.copy()
    tracks_df = pd.DataFrame(df[["old_track_id", "name"]].reset_index(drop=True))
    tracks_df = tracks_df.drop_duplicates(subset=["old_track_id"], keep="first")
    tracks_df["track_id"] = tracks_df.index + 1
    tracks_df = normalize_columns(tracks_df)
    df = df.drop(columns=["name"])
    return df.merge(tracks_df, on="old_track_id", how="left")


def replace_ids(
    artists_df: pd.DataFrame, albums_df: pd.DataFrame, tracks_df: pd.DataFrame
) -> pd.DataFrame:
    """Replace old artist ids and album ids."""
    # Create a mappings
    artist_mapping = dict(zip(artists_df["artist_name"], artists_df["artist_id"]))
    album_mapping = dict(zip(albums_df["old_album_id"], albums_df["album_id"]))

    # Replace old ids with new ids
    tracks_df["artist_id"] = tracks_df["artist_name"].map(artist_mapping)
    tracks_df["album_id"] = tracks_df["old_album_id"].map(album_mapping)

    return tracks_df


def transform(
    csv_df: pd.DataFrame, hdf5_df: pd.DataFrame, total_playcount: pd.DataFrame
):
    merged = merge(csv_df, hdf5_df, total_playcount)
    normalized = normalize(merged)
    renamed = rename_columns(normalized)
    cleaned = replace_NaN(renamed)
    artists_df = transform_artists(cleaned)
    albums_df = transform_albums(cleaned)
    tracks_df = transform_tracks(cleaned)
    tracks_df = replace_ids(artists_df, albums_df, tracks_df)
    return tracks_df, artists_df, albums_df
