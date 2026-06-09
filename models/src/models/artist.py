"""
The Artist model.
module: src/artist.py
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from .base import BaseModel


class Artist(BaseModel):
    __tablename__ = "artists"
    name = Column(String(255), nullable=False)
    tracks = relationship("Track", secondary="artists_tracks", back_populates="artists")


artists_tracks_table = Table(
    "artists_tracks",
    BaseModel.metadata,
    Column("artist_id", Integer, ForeignKey("artists.id"), primary_key=True),
    Column("track_id", Integer, ForeignKey("tracks.id"), primary_key=True),
)
