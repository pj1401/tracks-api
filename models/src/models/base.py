"""
The Base SQLAlchemy model.
module: src/base.py
"""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class BaseModel(Base):
    """
    An abstract base model.
    see: https://docs.sqlalchemy.org/en/21/orm/inheritance.html#abstract-concrete-classes
    """

    __abstract__: bool = True
    id: Mapped[Column[int]] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[Column[datetime]] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[Column[datetime]] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self) -> dict[str, int | float | str | list[str | int] | Any | None]:
        """
        Get a dictionary that represents the database object.
        see: https://stackoverflow.com/a/11884806

        :return: A dictionary representing the object.
        :rtype: dict[str, int | str]
        """
        # Convert Decimal to float.
        return {
            c.name: getattr(self, c.name)
            if not isinstance(getattr(self, c.name), Decimal)
            else float(getattr(self, c.name))
            for c in self.__table__.columns
        }
