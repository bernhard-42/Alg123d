from dataclasses import dataclass
import build123d as bd
from .wrappers import AlgCompound

__all__ = [
    "Empty3",
    "Box",
    "Cylinder",
]


class Empty3(AlgCompound):
    def __init__(self):
        super().__init__(dim=3)


@dataclass(repr=False)
class Box(AlgCompound):
    length: float
    width: float
    height: float
    centered: tuple[bool, bool, bool] = (True, True, True)

    def __post_init__(self):
        self.create_context_and_part(bd.Box)


@dataclass(repr=False)
class Cylinder(AlgCompound):
    radius: float
    height: float
    arc_size: float = 360
    centered: tuple[bool, bool, bool] = (True, True, True)

    def __post_init__(self):
        self.create_context_and_part(bd.Cylinder)
