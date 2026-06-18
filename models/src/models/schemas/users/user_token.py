from __future__ import annotations
from pydantic import BaseModel, Field


class UserToken(BaseModel):
    sub: int | None = Field(..., ge=1, description="The user ID.")
    username: str | None = Field(...)
    permission_level: int | None = Field(...)
