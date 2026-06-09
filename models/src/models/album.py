"""
The Album model.
module: src/album.py
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import BaseModel


class Album(BaseModel):
    __tablename__ = "albums"
    name = Column(String(255), nullable=False)
    tracks = relationship("Track", secondary="tracks_albums", back_populates="albums")
    artists = relationship(
        "Artist", secondary="artists_albums", back_populates="albums"
    )
