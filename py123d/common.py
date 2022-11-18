from typing import Union, List
from dataclasses import dataclass

import build123d as bd

from .direct_api import Location

CadObj1d = Union[bd.Wire, bd.Edge, bd.Compound]
CadObj2d = Union[bd.Face, bd.Compound]
CadObj3d = Union[bd.Solid, bd.Compound]
CadObj23d = Union[bd.Solid, bd.Face, bd.Compound]


@dataclass
class Task:
    obj: Union[CadObj2d, CadObj3d]
    loc: bd.Location
    mode: bd.Mode


class Build:
    def __init__(self):
        self.tasks: List[Task] = []
        self.obj: bd.Compound = None

    def _place(self, mode: bd.Mode, obj: CadObj23d, at: Location = None):
        if at is None:
            loc = obj.location
        elif isinstance(at, bd.Location):
            loc = at
        else:
            loc = Location(at)

        new_obj = obj.located(loc)

        self.tasks.append(Task(obj, loc, mode))

        if mode == bd.Mode.ADD:
            if self.obj == None:
                self.obj = bd.Compound.make_compound([new_obj])
            else:
                self.obj = self.obj.fuse(new_obj)

        elif mode == bd.Mode.SUBTRACT:
            if self.obj is None:
                raise RuntimeError("Connect cut obj from None")

            self.obj = self.obj.cut(new_obj)

    def add(self, obj: CadObj23d, at: Location = None):
        self._place(bd.Mode.ADD, obj, at=at)
        return self

    def subtract(self, obj: CadObj23d, at: Location = None):
        self._place(bd.Mode.SUBTRACT, obj, at=at)
        return self

    def intersect(self, obj: CadObj23d, at: Location = None):
        self._place(bd.Mode.INTERSECT, obj, at=at)
        return self

    def __add__(self, other: CadObj23d):
        self.add(other)
        return self

    def __sub__(self, other: CadObj23d):
        self.subtract(other)
        return self


class Mixin:
    def __matmul__(self, location):
        if isinstance(location, bd.Location):
            loc = location
        else:
            loc = Location(location)

        return self.located(loc)


class Locations(bd.Locations):
    def __init__(self, *pts: Union[bd.VectorLike, bd.Vertex, bd.Location]):
        super().__init__(*pts)
        del self.plane_index

    def __enter__(self):
        raise RuntimeError("No context!")

    def __exit__(self):
        raise RuntimeError("No context!")


class PolarLocations(bd.PolarLocations):
    def __init__(
        self,
        radius: float,
        count: int,
        start_angle: float = 0.0,
        stop_angle: float = 360.0,
        rotate: bool = True,
    ):
        super().__init__(radius, count, start_angle, stop_angle, rotate)
        del self.plane_index

    def __enter__(self):
        raise RuntimeError("No context!")

    def __exit__(self):
        raise RuntimeError("No context!")


class GridLocations(bd.GridLocations):
    def __init__(
        self,
        x_spacing: float,
        y_spacing: float,
        x_count: int,
        y_count: int,
        centered: tuple[bool, bool] = (True, True),
    ):
        super().__init__(x_spacing, y_spacing, x_count, y_count, centered)
        del self.plane_index

    def __enter__(self):
        raise RuntimeError("No context!")

    def __exit__(self):
        raise RuntimeError("No context!")
