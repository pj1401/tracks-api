"""
The BaseFilters dataclass.
module: src/util/filters/base_filters.py
"""

from dataclasses import dataclass


@dataclass
class BaseFilters:
    """
    Common filters for all collections.

    :var limit: Specifies the maximum number of items to return.
    :vartype limit: int
    :var offset: Specifies the starting index of the data.
    :vartype offset: int
    """

    limit: int = 20
    offset: int = 0
