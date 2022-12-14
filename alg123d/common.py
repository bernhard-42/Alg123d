import build123d as bd
from build123d.build_common import MM, CM, M, IN, FT
from .direct_api import *

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
        super().__init__(bd.Locations(*pts))


class PolarLocations(LocationList):
    def __init__(
        self,
        radius: float,
        count: int,
        start_angle: float = 0.0,
        stop_angle: float = 360.0,
        rotate: bool = True,
    ):
        super().__init__(
            bd.PolarLocations(radius, count, start_angle, stop_angle, rotate)
        )


class GridLocations(LocationList):
    def __init__(
        self,
        x_spacing: float,
        y_spacing: float,
        x_count: int,
        y_count: int,
        centered: Union[bool, Tuple[bool, bool]] = (True, True),
        offset: VectorLike = (0, 0),
    ):
        if isinstance(centered, bool):
            centered = (centered,) * 2

        super().__init__(
            bd.GridLocations(x_spacing, y_spacing, x_count, y_count, centered, offset)
        )


class HexLocations(LocationList):
    def __init__(
        self,
        diagonal: float,
        x_count: int,
        y_count: int,
        centered: Union[bool, Tuple[bool, bool]] = (True, True),
        offset: VectorLike = (0, 0),
    ):
        if isinstance(centered, bool):
            centered = (centered,) * 2

        super().__init__(bd.HexLocations(diagonal, x_count, y_count, centered, offset))
