from dataclasses import dataclass
import build123d as bd
from .common import AlgCompound


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
