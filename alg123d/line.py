from typing import List
import build123d as bd
from .wrappers import AlgEdge, AlgWire
from .direct_api import *

__all__ = [
    "Empty1",
    "Line",
    "Bezier",
    "PolarLine",
    "Polyline",
    "Spline",
    "Helix",
    "CenterArc",
    "EllipticalCenterArc",
    "RadiusArc",
    "SagittaArc",
    "TangentArc",
    "ThreePointArc",
    "JernArc",
]


class Empty1(AlgEdge):
    def __init__(self):
        super().__init__(dim=1)


class Line(AlgEdge):
    def __init__(self, start: VectorLike, end: VectorLike):
        self.create_line(bd.Line, objects=[start, end])


class Bezier(AlgEdge):
    def __init__(
        self,
        cntl_pts: Iterable[VectorLike],
        weights: list[float] = None,
    ):
        self.create_line(bd.Bezier, objects=cntl_pts, params=dict(weights=weights))


class PolarLine(AlgEdge):
    def __init__(
        self,
        start: VectorLike,
        length: float,
        angle: float = None,
        direction: VectorLike = None,
    ):
        params = dict(start=start, length=length, angle=angle, direction=direction)
        self.create_line(bd.PolarLine, params=params)


class Polyline(AlgWire):
    def __init__(self, pts: List[VectorLike], close: bool = False):
        params = dict(close=close)
        self.create_line(bd.Polyline, objects=pts, params=params)


class Spline(AlgEdge):
    def __init__(
        self,
        pts: Iterable[VectorLike],
        tangents: Iterable[VectorLike] = None,
        tangent_scalars: Iterable[float] = None,
        periodic: bool = False,
    ):
        params = dict(
            tangents=tangents,
            tangent_scalars=tangent_scalars,
            periodic=periodic,
        )
        self.create_line(bd.Spline, objects=pts, params=params)


class Helix(AlgWire):
    def __init__(
        self,
        pitch: float,
        height: float,
        radius: float,
        center: VectorLike = (0, 0, 0),
        direction: VectorLike = (0, 0, 1),
        cone_angle: float = 0,
        lefhand: bool = False,
    ):
        params = dict(
            pitch=pitch,
            height=height,
            radius=radius,
            center=center,
            direction=direction,
            cone_angle=cone_angle,
            lefhand=lefhand,
        )
        self.create_line(bd.Helix, params=params)


class CenterArc(AlgEdge):
    def __init__(
        self,
        center: VectorLike,
        radius: float,
        start_angle: float,
        arc_size: float,
    ):
        params = dict(
            center=center, radius=radius, start_angle=start_angle, arc_size=arc_size
        )
        self.create_line(bd.CenterArc, params=params)


class EllipticalCenterArc(AlgEdge):
    def __init__(
        self,
        center: VectorLike,
        x_radius: float,
        y_radius: float,
        start_angle: float = 0.0,
        end_angle: float = 90.0,
        angular_direction: AngularDirection = AngularDirection.COUNTER_CLOCKWISE,
        plane: Plane = Plane.XY,
    ):
        params = dict(
            center=center,
            x_radius=x_radius,
            y_radius=y_radius,
            start_angle=start_angle,
            end_angle=end_angle,
            angular_direction=angular_direction,
            plane=plane,
        )
        self.create_line(bd.EllipticalCenterArc, params=params)


class RadiusArc(AlgEdge):
    def __init__(
        self,
        start_point: VectorLike,
        end_point: VectorLike,
        radius: float,
    ):
        params = dict(start_point=start_point, end_point=end_point, radius=radius)
        self.create_line(bd.RadiusArc, params=params)


class SagittaArc(AlgEdge):
    def __init__(
        self,
        start_point: VectorLike,
        end_point: VectorLike,
        sagitta: float,
    ):
        params = dict(start_point=start_point, end_point=end_point, sagitta=sagitta)
        self.create_line(bd.SagittaArc, params=params)


class TangentArc(AlgEdge):
    def __init__(
        self,
        *pts: VectorLike,
        tangent: VectorLike,
        tangent_from_first: bool = True,
    ):
        params = dict(
            tangent=tangent,
            tangent_from_first=tangent_from_first,
        )
        self.create_line(bd.TangentArc, objects=pts, params=params)


class ThreePointArc(AlgEdge):
    def __init__(self, pts: Iterable[VectorLike]):
        self.create_line(bd.ThreePointArc, objects=pts)


class JernArc(AlgEdge):
    def __init__(
        self,
        start: VectorLike,
        tangent: VectorLike,
        radius: float,
        arc_size: float,
        plane: Plane = Plane.XY,
    ):
        params = dict(
            start=start,
            tangent=tangent,
            radius=radius,
            arc_size=arc_size,
            plane=plane,
        )
        self.create_line(bd.JernArc, params=params)
