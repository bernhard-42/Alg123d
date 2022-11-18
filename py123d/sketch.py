from dataclasses import dataclass
import build123d as bd
from .common import Build, Mixin


class Sketch(Build):
    def __repr__(self):
        return "Sketch(\n" + "\n".join(["    " + str(t) for t in self.tasks]) + "\n)"


@dataclass
class Circle(bd.Circle, Mixin):
    __module__ = "build123d.build_sketch"

    radius: float
    centered: tuple[bool, bool]

    def __init__(self, radius: float, centered: tuple[bool, bool] = (True, True)):
        with bd.BuildSketch():
            super().__init__(radius, centered=centered, mode=bd.Mode.PRIVATE)

        del self.mode


@dataclass
class Rectangle(bd.Rectangle, Mixin):
    __module__ = "build123d.build_sketch"

    width: float
    height: float
    centered: tuple[bool, bool]

    def __init__(
        self, width: float, height: float, centered: tuple[bool, bool] = (True, True)
    ):
        with bd.BuildSketch():
            super().__init__(
                width, height, rotation=0, centered=centered, mode=bd.Mode.PRIVATE
            )

        del self.rotation
        del self.mode
