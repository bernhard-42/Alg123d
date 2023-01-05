from typing import List, Tuple, Union

import build123d as bd

from .algcompound import AlgCompound
from .direct_api import *

__all__ = [
    "Circle",
    "Ellipse",
    "Rectangle",
    "Polygon",
    "RegularPolygon",
    "Text",
    "Trapezoid",
    "SlotArc",
    "SlotCenterPoint",
    "SlotCenterToCenter",
    "SlotOverall",
    "make_face",
]


#
# Objects
#


class Circle(AlgCompound):
    def __init__(
        self,
        radius: float,
        centered: Union[bool, Tuple[bool, bool]] = (True, True),
    ):
        if isinstance(centered, bool):
            centered = (centered,) * 2

        params = dict(
            radius=radius,
            centered=centered,
        )
        super().__init__(self.create_sketch(bd.Circle, params=params))


class Ellipse(AlgCompound):
    def __init__(
        self,
        x_radius: float,
        y_radius: float,
        centered: Union[bool, Tuple[bool, bool]] = (True, True),
    ):
        if isinstance(centered, bool):
            centered = (centered,) * 2

        params = dict(
            x_radius=x_radius,
            y_radius=y_radius,
            centered=centered,
        )
        super().__init__(self.create_sketch(bd.Ellipse, params=params))


class Rectangle(AlgCompound):
    def __init__(
        self,
        width: float,
        height: float,
        centered: Union[bool, Tuple[bool, bool]] = (True, True),
    ):
        if isinstance(centered, bool):
            centered = (centered,) * 2

        params = dict(
            width=width,
            height=height,
            centered=centered,
        )
        super().__init__(self.create_sketch(bd.Rectangle, params=params))


class Polygon(AlgCompound):
    def __init__(
        self,
        pts: List[VectorLike],
        # centered: Union[bool, Tuple[bool, bool]] = (True, True),
    ):
        # if isinstance(centered, bool):
        #     centered = (centered,) * 2

        # params = dict(
        #     centered=centered,
        # )
        params = {}
        super().__init__(self.create_sketch(bd.Polygon, objects=pts, params=params))


class RegularPolygon(AlgCompound):
    def __init__(
        self,
        radius: float,
        side_count: int,
        centered: Union[bool, Tuple[bool, bool]] = (True, True),
    ):
        if isinstance(centered, bool):
            centered = (centered,) * 2

        params = dict(
            radius=radius,
            side_count=side_count,
            centered=centered,
        )
        super().__init__(self.create_sketch(bd.RegularPolygon, params=params))


class Text(AlgCompound):
    def __init__(
        self,
        txt: str,
        fontsize: float,
        font: str = "Arial",
        font_path: str = None,
        font_style: FontStyle = FontStyle.REGULAR,
        halign: Halign = Halign.LEFT,
        valign: Valign = Valign.CENTER,
        path: Union[Edge, Wire] = None,
        position_on_path: float = 0.0,
    ):
        params = dict(
            txt=txt,
            fontsize=fontsize,
            font=font,
            font_path=font_path,
            font_style=font_style,
            halign=halign,
            valign=valign,
            path=path,
            position_on_path=position_on_path,
        )
        super().__init__(self.create_sketch(bd.Text, params=params))


class Trapezoid(AlgCompound):
    def __init__(
        self,
        width: float,
        height: float,
        left_side_angle: float,
        right_side_angle: float = None,
        centered: Union[bool, Tuple[bool, bool]] = (True, True),
    ):
        if isinstance(centered, bool):
            centered = (centered,) * 2

        params = dict(
            width=width,
            height=height,
            left_side_angle=left_side_angle,
            right_side_angle=right_side_angle,
            centered=centered,
        )
        super().__init__(self.create_sketch(bd.Trapezoid, params=params))


class SlotArc(AlgCompound):
    def __init__(
        self,
        arc: Union[Edge, Wire],
        height: float,
    ):
        params = dict(
            arc=arc,
            height=height,
        )
        super().__init__(self.create_sketch(bd.SlotArc, params=params))


class SlotCenterPoint(AlgCompound):
    def __init__(
        self,
        center: VectorLike,
        point: VectorLike,
        height: float,
    ):
        params = dict(
            center=center,
            point=point,
            height=height,
        )
        super().__init__(self.create_sketch(bd.SlotCenterPoint, params=params))


class SlotCenterToCenter(AlgCompound):
    def __init__(
        self,
        center_separation: float,
        height: float,
    ):
        params = dict(
            center_separation=center_separation,
            height=height,
        )
        super().__init__(self.create_sketch(bd.SlotCenterToCenter, params=params))


class SlotOverall(AlgCompound):
    def __init__(
        self,
        width: float,
        height: float,
    ):
        params = dict(
            width=width,
            height=height,
        )
        super().__init__(self.create_sketch(bd.SlotOverall, params=params))


#
# Functions
#


def make_face(objs: Union[AlgCompound, List[Edge]]):
    if isinstance(objs, AlgCompound) and objs.dim == 1:
        edges = objs.edges()
    elif isinstance(objs, (tuple, list)):
        edges = objs
    else:
        edges = [objs]

    return AlgCompound.make_compound([Face.make_from_wires(*Wire.combine(edges))])
