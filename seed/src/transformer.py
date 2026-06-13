"""
Transformer module for cleaning and joining data.
module: src/transformer.py
"""

from collections.abc import Iterator
import pandas as pd  # type: ignore


class Transformer:
    def __init__(
        self,
        hdf5_lookup: dict[str, dict[str, str]],
        playcount_data: Iterator[pd.DataFrame],
    ) -> None:
        self.hdf5_lookup = hdf5_lookup
        self.playcount_lookup = self._build_playcount_lookup(playcount_data)
        self.seen_artists = set()
        self.seen_albums = set()

    def _build_playcount_lookup(
        self, playcount_data: Iterator[pd.DataFrame]
    ) -> dict[str, int]:
        """
        Build a dictionary with the total playcount values.

        :param playcount_data: The Iterator with the playcount chunks.
        :type playcount_data: Iterator[pd.DataFrame]
        :return: A dictionary with track_id as keys, and the total playcount as values.
        :rtype: dict[str, int]
        """
        totals: dict[str, int] = {}
        for chunk in playcount_data:
            chunk["track_id"] = chunk["track_id"].astype("str").str.strip().str.upper()
            for _, row in chunk.iterrows():
                tid = row["track_id"]

                # Look up if track_id already exists as a key in the totals dictionary, add the track_id if it doesn't exist.
                totals[tid] = totals.get(tid, 0) + int(row["playcount"])
        return totals

    def transform_chunk(
        self, chunk: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame] | None:
        chunk["track_id"] = chunk["track_id"].astype("str").str.strip().str.upper()
        chunk_with_album_names = self.lookup_album_name(chunk)
        merged = self.lookup_playcount(chunk_with_album_names)
        normalized = normalize(merged)
        renamed = rename_columns(normalized)
        cleaned = replace_NaN(renamed)

        # TODO: Make sets of seen artists and albums to avoid duplicates.
        artists_df = transform_artists(cleaned)
        albums_df = transform_albums(cleaned)
        tracks_df = transform_tracks(cleaned)
        tracks_df = replace_ids(artists_df, albums_df, tracks_df)
        return (tracks_df, artists_df, albums_df)

    def lookup_album_name(self, df: pd.DataFrame) -> pd.DataFrame:
        df["album_name"] = df["track_id"].map(self.hdf5_lookup)
        df["old_album_id"] = df["track_id"].map(self.hdf5_lookup)
        return df

    def lookup_playcount(self, df: pd.DataFrame) -> pd.DataFrame:
        df["total_playcount"] = df["track_id"].map(self.playcount_lookup)
        return df


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


# def transform(
#     csv_df: pd.DataFrame, hdf5_df: pd.DataFrame, total_playcount: pd.DataFrame
# ):
#     merged = merge(csv_df, hdf5_df, total_playcount)
#     normalized = normalize(merged)
#     renamed = rename_columns(normalized)
#     cleaned = replace_NaN(renamed)
#     artists_df = transform_artists(cleaned)
#     albums_df = transform_albums(cleaned)
#     tracks_df = transform_tracks(cleaned)
#     tracks_df = replace_ids(artists_df, albums_df, tracks_df)
#     return tracks_df, artists_df, albums_df
