"""
The Artist model.
module: src/artist.py
"""

from typing import Any, List
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, relationship
from .base import BaseModel


class Artist(BaseModel):
    __tablename__: str = "artists"
    name: Column[str] = Column(String(255), nullable=False)
    tracks: Mapped[List[Any]] = relationship(
        "Track", secondary="artists_tracks", back_populates="artists"
    )
    albums: Mapped[List[Any]] = relationship(
        "Album", secondary="artists_albums", back_populates="artists"
    )


artists_tracks_table: Table = Table(
    "artists_tracks",
    BaseModel.metadata,
    Column("artist_id", Integer, ForeignKey("artists.id"), primary_key=True),
    Column("track_id", Integer, ForeignKey("tracks.id"), primary_key=True),
)

artists_albums_table: Table = Table(
    "artists_albums",
    BaseModel.metadata,
    Column("artist_id", Integer, ForeignKey("artists.id"), primary_key=True),
    Column("album_id", Integer, ForeignKey("albums.id"), primary_key=True),
)
