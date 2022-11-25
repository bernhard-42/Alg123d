import build123d as bd
from .wrappers import AlgCompound

__all__ = [
    "LocationList",
    "Locations",
    "PolarLocations",
    "GridLocations",
    "HexLocations",
]


#
# Location generators
#


class LocationList:
    def __init__(self, generator):
        bd.Workplanes(bd.Plane.XY).__enter__()
        self.generator = generator

    def __iter__(self):
        return self.generator.__iter__()

    def __next__(self):
        return self.generator.__next__()


class Locations(LocationList):
    def __init__(self, *pts: bd.VectorLike | bd.Vertex | bd.Location):
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
        centered: tuple[bool, bool] = (True, True),
    ):
        super().__init__(
            bd.GridLocations(x_spacing, y_spacing, x_count, y_count, centered)
        )


class HexLocations(LocationList):
    def __init__(
        self,
        diagonal: float,
        x_count: int,
        y_count: int,
        centered: tuple[bool, bool] = (True, True),
    ):
        super().__init__(bd.HexLocations(diagonal, x_count, y_count, centered))
