"""
User models.
module: src/util/schemas/user.py
"""

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """User base model."""

    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr


class UserArguments(User):
    """Represents user arguments for creating a user."""

    password: str = Field(..., min_length=8)


class NewUser(User):
    """Represents create user data after going through business logic (service layer)."""

    password_hash: str


class UserLogin(BaseModel):
    """Login arguments."""

    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)


class UserModel(BaseModel):
    """The database User model."""

    __tablename__: str = "users"
    id: int
    username: str
    email: EmailStr
    password_hash: str
    permission_level: int = Field(default=0)
