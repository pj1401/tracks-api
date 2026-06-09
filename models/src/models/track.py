"""
The Track model.
module: src/track.py
"""

from sqlalchemy import Table, Column, ForeignKey, Integer, String, Numeric, BigInteger
from sqlalchemy.orm import relationship
from .base import BaseModel


class Track(BaseModel):
    __tablename__ = "tracks"
    name = Column(String, nullable=False)
    total_playcount = Column(BigInteger, default=0)
    spotify_id = Column(String)
    tags = Column(String)
    genre = Column(String)
    year = Column(Integer)
    duration_ms = Column(Integer)
    danceability = Column(Numeric(precision=4, scale=3))
    mode = Column(Integer)
    valence = Column(Numeric(precision=4, scale=3))
    artists = relationship(
        "Artist", secondary="artists_tracks", back_populates="tracks"
    )
    albums = relationship("Album", secondary="tracks_albums", back_populates="tracks")


tracks_albums_table = Table(
    "tracks_albums",
    BaseModel.metadata,
    Column("track_id", Integer, ForeignKey("tracks.id"), primary_key=True),
    Column("album_id", Integer, ForeignKey("albums.id"), primary_key=True),
)
