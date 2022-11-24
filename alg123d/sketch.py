from dataclasses import dataclass
import build123d as bd
from .wrappers import AlgCompound

__all__ = [
    "Empty2",
    "Circle",
    "Rectangle",
]


class Empty2(AlgCompound):
    def __init__(self):
        super().__init__(dim=2)


@dataclass
class Circle(AlgCompound):
    radius: float
    centered: tuple[bool, bool] = (True, True)

    def __post_init__(self):
        self.create_context_and_sketch(bd.Circle)


@dataclass
class Rectangle(AlgCompound):
    width: float
    height: float
    centered: tuple[bool, bool] = (True, True)

    def __post_init__(self):
        self.create_context_and_sketch(bd.Rectangle)
