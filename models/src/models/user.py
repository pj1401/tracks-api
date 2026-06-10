"""
The User model.
module: src/user.py
"""

from sqlalchemy import Column, Integer, String
from .base import BaseModel


class User(BaseModel):
    __tablename__: str = "users"
    username: Column[str] = Column(String(255), nullable=False, unique=True)
    email: Column[str] = Column(String(255), nullable=False, unique=True)
    password_hash: Column[str] = Column(String(255), nullable=False)
    permission_level: Column[int] = Column(Integer, nullable=False, default=0)
