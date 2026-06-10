"""
The Track model.
module: src/track.py
"""

from decimal import Decimal
from typing import Any, List
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Numeric, BigInteger
from sqlalchemy.orm import Mapped, relationship
from .base import BaseModel


class Track(BaseModel):
    __tablename__: str = "tracks"
    name: Column[str] = Column(String, nullable=False)
    total_playcount: Column[int] = Column(BigInteger, default=0)
    spotify_id: Column[str] = Column(String)
    tags: Column[str] = Column(String)
    genre: Column[str] = Column(String)
    year: Column[int] = Column(Integer)
    duration_ms: Column[int] = Column(Integer)
    danceability: Column[Decimal] = Column(Numeric(precision=4, scale=3))
    mode: Column[int] = Column(Integer)
    valence: Column[Decimal] = Column(Numeric(precision=4, scale=3))
    artists: Mapped[List[Any]] = relationship(
        "Artist", secondary="artists_tracks", back_populates="tracks"
    )
    albums: Mapped[List[Any]] = relationship(
        "Album", secondary="tracks_albums", back_populates="tracks"
    )


tracks_albums_table: Table = Table(
    "tracks_albums",
    BaseModel.metadata,
    Column("track_id", Integer, ForeignKey("tracks.id"), primary_key=True),
    Column("album_id", Integer, ForeignKey("albums.id"), primary_key=True),
)
