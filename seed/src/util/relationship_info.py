"""
The RelationshipInfo helper class.
module: src/util/relationship_info.py
"""


class RelationshipInfo:
    """
    Helper class for loading a relationship table.
    """

    def __init__(
        self,
        table_name: str,
        left_col: str,
        right_col: str,
        left_id: int,
        right_id: int,
    ):
        self.table_name = table_name
        self.left_col = left_col
        self.right_col = right_col
        self.left_id = left_id
        self.right_id = right_id
