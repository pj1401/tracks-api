"""
The RelationshipIDs helper class.
module: src/util/relationship_ids.py
"""


class RelationshipIDs:
    """
    Relationship id values.
    """

    def __init__(
        self,
        left_id: int,
        right_id: int,
    ):
        """
        Initialise an instance.

        :param self: This instance.
        :param left_id: The value of the id in the left column.
        :type left_id: int
        :param right_id: The value of the id in the right column.
        :type right_id: int
        """
        self.left_id = left_id
        self.right_id = right_id
