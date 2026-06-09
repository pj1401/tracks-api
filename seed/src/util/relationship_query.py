"""
The RelationshipQuery helper class.
module: src/util/relationship_query.py
"""


class RelationshipQuery:
    """
    Helper class for loading a relationship table.
    """

    def __init__(self, table_name: str, left_col: str, right_col: str):
        """
        Initialise an instance.

        :param self: This instance.
        :param table_name: The name of the relationship table.
        :type table_name: str
        :param left_col: The name of the left column in the relationship table.
        :type left_col: str
        :param right_col: The name of the right column in the relationship table.
        :type right_col: str
        """
        self.table_name = table_name
        self.left_col = left_col
        self.right_col = right_col
