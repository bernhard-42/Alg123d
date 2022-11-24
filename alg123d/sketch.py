from typing import List
from dataclasses import dataclass
import build123d as bd
from .wrappers import AlgCompound
from alg123d import FontStyle, Halign, Valign, Edge, Wire

__all__ = [
    "Empty2",
    "Circle",
    "Ellipse",
    "Rectangle",
    "Polygon",
    "RegularPolygon",
    "Text",
    "Trapezoid",
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
class Ellipse(AlgCompound):
    x_radius: float
    y_radius: float
    rotation: float = 0
    centered: tuple[bool, bool] = (True, True)

    def __post_init__(self):
        self.create_context_and_sketch(bd.Ellipse)


@dataclass
class Rectangle(AlgCompound):
    width: float
    height: float
    centered: tuple[bool, bool] = (True, True)

    def __post_init__(self):
        self.create_context_and_sketch(bd.Rectangle)


@dataclass
class Polygon(AlgCompound):
    pts: List[bd.VectorLike]
    centered: tuple[bool, bool] = (True, True)

    def __post_init__(self):
        self.create_context_and_sketch(bd.Polygon, objects=self.pts, exclude=["pts"])


@dataclass
class RegularPolygon(AlgCompound):
    radius: float
    side_count: int
    centered: tuple[bool, bool] = (True, True)

    def __post_init__(self):
        self.create_context_and_sketch(bd.RegularPolygon)


@dataclass
class Text(AlgCompound):
    txt: str
    fontsize: float
    font: str = "Arial"
    font_path: str = None
    font_style: FontStyle = FontStyle.REGULAR
    halign: Halign = Halign.LEFT
    valign: Valign = Valign.CENTER
    path: Edge | Wire = None
    position_on_path: float = 0.0

    def __post_init__(self):
        self.create_context_and_sketch(bd.Text)


@dataclass
class Trapezoid(AlgCompound):
    width: float
    height: float
    left_side_angle: float
    right_side_angle: float = None
    centered: tuple[bool, bool] = (True, True)

    def __post_init__(self):
        self.create_context_and_sketch(bd.Trapezoid)
