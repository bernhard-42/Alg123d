from enum import Enum


class Mode(Enum):
    """Combination Mode"""

    ADD = "a"
    SUBTRACT = "s"
    INTERSECT = "i"
    REPLACE = "r"

    def __repr__(self):
        return f'{self.name}")'
