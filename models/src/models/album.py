"""
The Album model.
module: src/album.py
"""

from typing import Any, List
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship
from .base import BaseModel


class Album(BaseModel):
    """
    The Album SQLAlchemy model.

    :var __tablename__: The name of the table.
    :vartype __tablename__: str
    """

    __tablename__: str = "albums"
    name: Column[str] = Column(String(255), nullable=False)
    tracks: Mapped[List[Any]] = relationship(
        "Track", secondary="tracks_albums", back_populates="albums"
    )
    artists: Mapped[List[Any]] = relationship(
        "Artist", secondary="artists_albums", back_populates="albums"
    )
