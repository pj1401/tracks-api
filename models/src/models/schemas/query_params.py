"""
BaseQueryParams schema.
module: src/util/schemas/query_params.py
"""

from enum import StrEnum
from pydantic import BaseModel, Field, model_validator


class SortOptions(StrEnum):
    """Specifies the column to sort by"""

    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    ID = "id"


class BaseQueryParams(BaseModel):
    """
    Common query parameters for all collections.

    :var limit: Specifies the maximum number of items to return.
    :vartype limit: int
    :var offset: Specifies the starting index of the data.
    :vartype offset: int
    :var sort: The column to sort by.
    :vartype sort: SortOptions
    """

    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)
    sort: SortOptions = Field(default=SortOptions("id"))

    @model_validator(mode="before")
    @classmethod
    def strip_strings(
        cls, values: dict[str, str | int | float]
    ) -> dict[str, str | int | float]:
        """
        Remove whitespaces from field values.

        :param values: The key, value pair as a dict.
        :type values: dict[str, str | int | float]
        :return: The key, value pair. If value is a string, whitespaces are removed.
        :rtype: dict[str, str | int | float]
        """
        return {k: v.strip() if isinstance(v, str) else v for k, v in values.items()}
