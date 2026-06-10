"""
The User model.
module: src/user.py
"""

from sqlalchemy import Column, Integer, String
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    permission_level = Column(Integer, nullable=False, default=0)
