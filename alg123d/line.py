from typing import List
import build123d as bd
from .wrappers import AlgCompound
from .direct_api import *

__all__ = [
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

#
# Objects
#


class Line(AlgCompound):
    def __init__(self, start: VectorLike, end: VectorLike):
        super().__init__(self.create_line(bd.Line, objects=[start, end]))


class Bezier(AlgCompound):
    def __init__(
        self,
        cntl_pts: Iterable[VectorLike],
        weights: List[float] = None,
    ):
        super().__init__(
            self.create_line(bd.Bezier, objects=cntl_pts, params=dict(weights=weights))
        )


class PolarLine(AlgCompound):
    def __init__(
        self,
        start: VectorLike,
        length: float,
        angle: float = None,
        direction: VectorLike = None,
    ):
        params = dict(start=start, length=length, angle=angle, direction=direction)
        super().__init__(self.create_line(bd.PolarLine, params=params))


class Polyline(AlgCompound):
    def __init__(self, pts: List[VectorLike], close: bool = False):
        params = dict(close=close)
        super().__init__(self.create_line(bd.Polyline, objects=pts, params=params))


class Spline(AlgCompound):
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
        super().__init__(self.create_line(bd.Spline, objects=pts, params=params))


class Helix(AlgCompound):
    def __init__(
        self,
        pitch: float,
        height: float,
        radius: float,
        direction: VectorLike = (0, 0, 1),
        cone_angle: float = 0,
        lefthand: bool = False,
    ):
        params = dict(
            pitch=pitch,
            height=height,
            radius=radius,
            direction=direction,
            cone_angle=cone_angle,
            lefhand=lefthand,
        )
        super().__init__(self.create_line(bd.Helix, params=params))


class CenterArc(AlgCompound):
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
        super().__init__(self.create_line(bd.CenterArc, params=params))


class EllipticalCenterArc(AlgCompound):
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
        super().__init__(self.create_line(bd.EllipticalCenterArc, params=params))


class RadiusArc(AlgCompound):
    def __init__(
        self,
        start_point: VectorLike,
        end_point: VectorLike,
        radius: float,
    ):
        params = dict(start_point=start_point, end_point=end_point, radius=radius)
        super().__init__(self.create_line(bd.RadiusArc, params=params))


class SagittaArc(AlgCompound):
    def __init__(
        self,
        start_point: VectorLike,
        end_point: VectorLike,
        sagitta: float,
    ):
        params = dict(start_point=start_point, end_point=end_point, sagitta=sagitta)
        super().__init__(self.create_line(bd.SagittaArc, params=params))


class TangentArc(AlgCompound):
    def __init__(
        self,
        start_point: VectorLike,
        end_point: VectorLike,
        tangent: VectorLike,
        tangent_from_first: bool = True,
    ):
        params = dict(
            tangent=tangent,
            tangent_from_first=tangent_from_first,
        )
        super().__init__(
            self.create_line(
                bd.TangentArc, objects=[start_point, end_point], params=params
            )
        )


class ThreePointArc(AlgCompound):
    def __init__(self, p1: VectorLike, p2: VectorLike, p3: VectorLike):
        super().__init__(self.create_line(bd.ThreePointArc, objects=(p1, p2, p3)))


class JernArc(AlgCompound):
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
        super().__init__(self.create_line(bd.JernArc, params=params))
