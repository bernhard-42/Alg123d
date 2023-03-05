import build123d as bd
from build123d.build_common import CM, FT, IN, MM, M

from .topology import *

__all__ = [
    "LocationList",
    "Locations",
    "PolarLocations",
    "GridLocations",
    "HexLocations",
    "MM",
    "CM",
    "M",
    "IN",
    "FT",
]


class LocationList:
    def __init__(self, loclist):
        bd.Workplanes(Plane.XY).__enter__()
        self.locations = loclist.locations
        self.index = 0

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.locations):
            result = self.locations[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration


class Locations(LocationList):
    def __init__(self, *pts: Union[VectorLike, Vertex, Location]):
        bd.Workplanes(Plane.XY).__enter__()
        super().__init__(bd.Locations(*pts))


class PolarLocations(LocationList):
    def __init__(
        self,
        radius: float,
        count: int,
        start_angle: float = 0.0,
        angular_range: float = 360.0,
        rotate: bool = True,
    ):
        bd.Workplanes(Plane.XY).__enter__()
        super().__init__(
            bd.PolarLocations(radius, count, start_angle, angular_range, rotate)
        )


class GridLocations(LocationList):
    def __init__(
        self,
        x_spacing: float,
        y_spacing: float,
        x_count: int,
        y_count: int,
        align: Union[Align, Tuple[Align, Align]] = (Align.CENTER, Align.CENTER),
    ):
        if isinstance(align, Align):
            align = (align,) * 2

        bd.Workplanes(Plane.XY).__enter__()
        super().__init__(
            bd.GridLocations(x_spacing, y_spacing, x_count, y_count, align)
        )


class HexLocations(LocationList):
    def __init__(
        self,
        apothem: float,
        x_count: int,
        y_count: int,
        align: Union[Align, Tuple[Align, Align]] = (Align.CENTER, Align.CENTER),
    ):
        if isinstance(align, Align):
            align = (align,) * 2

        bd.Workplanes(Plane.XY).__enter__()
        super().__init__(bd.HexLocations(apothem, x_count, y_count, align))
