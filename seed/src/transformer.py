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
        self.seen_artists = {}
        self.max_artist_id = 1
        self.seen_albums = {}
        self.max_album_id = 1

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
        chunk_with_album_info = self.lookup_album(chunk)
        merged = self.lookup_playcount(chunk_with_album_info)
        renamed = self.rename_columns(merged)
        cleaned = self.replace_NaN(renamed)

        # TODO: Make sets of seen artists and albums to avoid duplicates.
        # albums_df = self.transform_albums(cleaned)
        artists_df = self.transform_artists(cleaned)
        albums_df = self.transform_albums(cleaned)
        tracks_df = self.transform_tracks(cleaned)
        # tracks_df = replace_ids(artists_df, albums_df, tracks_df)
        return (tracks_df, artists_df, albums_df)

    def lookup_album(self, df: pd.DataFrame) -> pd.DataFrame:
        # https://stackoverflow.com/a/23974523
        # Look up track_id in the hdf5 dictionary, and add the album info to the album column.
        df["album"] = df["track_id"].map(self.hdf5_lookup)

        # https://stackoverflow.com/a/41970572
        # Map album column into new columns from the album dictionary.
        df = pd.concat(
            [df.drop(["album"], axis=1), df["album"].apply(pd.Series)], axis=1
        )
        return df

    def lookup_playcount(self, df: pd.DataFrame) -> pd.DataFrame:
        df["total_playcount"] = df["track_id"].map(self.playcount_lookup)
        return df

    def rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df = df.rename(columns={"track_id": "old_track_id"})
        df = df.rename(columns={"artist": "artist_name"})
        df = df.rename(columns={"playcount": "total_playcount"})
        return df

    def replace_NaN(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["total_playcount"] = df["total_playcount"].fillna(0)
        df["total_playcount"] = df["total_playcount"].astype("int64")
        return df

    def transform_artists(self, df: pd.DataFrame) -> pd.DataFrame:
        artists_df = pd.DataFrame(
            df[["artist_name"]].drop_duplicates().reset_index(drop=True)
        )

        # Use integers as IDs
        # Add artist_name to seen_artists if they don't exist, and increment max_artist_id. Otherwise reuse artist_id from seen_artists.
        artists_df["artist_id"] = artists_df["artist_name"].map(self.seen_artists)
        artists_df["artist_id"] = artists_df["artist_id"].fillna(self.max_artist_id)
        self.max_artist_id += 1
        return self.normalize_columns(artists_df)

    def transform_albums(self, df: pd.DataFrame) -> pd.DataFrame:
        albums_df = pd.DataFrame(
            df[["album_name", "old_album_id"]].reset_index(drop=True)
        )
        albums_df = albums_df.drop_duplicates(subset=["old_album_id"], keep="first")

        self.seen_albums.update(albums_df["old_album_id"].to_numpy())
        albums_df["album_id"] = albums_df.index + 1
        return self.normalize_columns(albums_df)

    def transform_tracks(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate new track_ids and drop duplicates based on old_track_id."""
        df.copy()
        tracks_df = pd.DataFrame(df[["old_track_id", "name"]].reset_index(drop=True))
        tracks_df = tracks_df.drop_duplicates(subset=["old_track_id"], keep="first")
        tracks_df["track_id"] = tracks_df.index + 1
        tracks_df = self.normalize_columns(tracks_df)
        df = df.drop(columns=["name"])
        return df.merge(tracks_df, on="old_track_id", how="left")

    def normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Lowercase column names and strip surrounding whitespace."""
        df = df.copy()
        df.columns = [col.strip().lower() for col in df.columns]
        return df

    def replace_ids(
        self, artists_df: pd.DataFrame, albums_df: pd.DataFrame, tracks_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Replace old artist ids and album ids."""
        # Create a mappings
        artist_mapping = dict(zip(artists_df["artist_name"], artists_df["artist_id"]))
        album_mapping = dict(zip(albums_df["old_album_id"], albums_df["album_id"]))

        # Replace old ids with new ids
        tracks_df["artist_id"] = tracks_df["artist_name"].map(artist_mapping)
        tracks_df["album_id"] = tracks_df["old_album_id"].map(album_mapping)

        return tracks_df
