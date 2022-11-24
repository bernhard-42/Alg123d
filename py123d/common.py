import copy
from typing import Union, List, overload
from dataclasses import dataclass

import build123d as bd
from .direct_api import Workplane

from OCP.BRepBuilderAPI import (  # pyright: ignore[reportMissingImports]
    BRepBuilderAPI_Copy,
)

Obj1d = bd.Compound | bd.Wire | bd.Edge
Obj2d = bd.Compound | bd.Face
Obj3d = bd.Compound | bd.Solid
Obj12d = Obj1d | Obj2d
Obj23d = Obj2d | Obj3d
Obj123d = Obj1d | Obj2d | Obj3d


@dataclass
class Step:
    obj: Obj23d
    loc: bd.Location
    mode: bd.Mode

    def __init__(self, obj: Obj2d | Obj3d, loc: bd.Location, mode: bd.Mode):
        self.obj = {"name": obj.__class__.__name__}
        if hasattr(obj, "__dataclass_fields__"):
            for name in obj.__dataclass_fields__:
                self.obj[name] = getattr(obj, name)
        self.loc = loc.to_tuple()
        self.mode = "" if mode is None else mode.name


class AlgCompound(bd.Compound):
    def __init__(self, compound=None, objects=None, dim: int = None):
        self.objects: List[Obj123d] = [] if objects is None else objects
        self.wrapped = None if compound is None else compound.wrapped
        self.dim = dim

    def _params(self, exclude):
        # get the paramter dict from the data class
        params = {
            k: v for k, v in self.__dict__.items() if k in self.__dataclass_fields__
        }
        for ex in exclude:
            del params[ex]
        return params

    def create_context_and_part(self, cls, exclude=[]):
        with bd.BuildPart():
            self.create_part(cls, exclude)

    def create_part(self, cls, exclude=[]):
        with bd.Locations(bd.Location()):
            self.wrapped = cls(**self._params(exclude), mode=bd.Mode.PRIVATE).wrapped

        # self._applies_to = cls._applies_to
        self.objects = [Step(self, self.location, bd.Mode.ADD)]
        self.dim = 3

    def create_context_and_sketch(self, cls, exclude=[]):
        with bd.BuildSketch():
            self.wrapped = cls(**self._params(exclude), mode=bd.Mode.PRIVATE).wrapped

        # self._applies_to = cls._applies_to
        self.objects = [Step(self, self.location, bd.Mode.ADD)]
        self.dim = 2

    def _place(
        self,
        mode: bd.Mode,
        obj: Obj23d,
        at: bd.Location = None,
    ):
        if at is None:
            located_obj = obj
            loc = obj.location
        else:
            if isinstance(at, bd.Location):
                loc = at
            elif isinstance(at, Workplane):
                loc = at.to_location()
            elif isinstance(at, tuple):
                loc = bd.Location(at)
            else:
                raise ValueError(f"{at } is no location or plane")

            located_obj = obj.located(loc)

        if self.wrapped is None:
            if mode == bd.Mode.ADD:
                compound = located_obj
            else:
                raise RuntimeError("Can only add to empty object")
        else:
            compound = self
            if mode == bd.Mode.ADD:
                compound = compound.fuse(located_obj)
            elif mode == bd.Mode.SUBTRACT:
                compound = compound.cut(located_obj)
            elif mode == bd.Mode.INTERSECT:
                compound = compound.intersect(located_obj)

        steps = self.objects.copy()
        steps.append(Step(obj, loc, mode))

        return AlgCompound(compound, steps, self.dim)

    def __add__(self, other: Obj23d):
        return self._place(bd.Mode.ADD, other)

    def __sub__(self, other: Obj23d):
        return self._place(bd.Mode.SUBTRACT, other)

    def __and__(self, other: Obj23d):
        return self._place(bd.Mode.INTERSECT, other)

    def __matmul__(self, obj):
        if isinstance(obj, bd.Location):
            loc = obj
        elif isinstance(obj, tuple):
            loc = bd.Location(obj)
        elif isinstance(obj, Workplane):
            loc = obj.to_location()
        else:
            raise ValueError(f"Cannot multiply with {obj}")

        return self.located(loc)

    def __repr__(self):
        repr = "{\n"
        repr += f'  "dim": {self.dim},\n'
        repr += '  "objects": [\n    '
        repr += "\n    ".join([str(task) for task in self.objects])
        repr += "\n  ]\n"
        repr += "}"
        return repr

    def copy(self):
        memo = {}
        memo[id(self.wrapped)] = bd.downcast(BRepBuilderAPI_Copy(self.wrapped).Shape())
        if hasattr(self, "part"):
            memo[id(self.part.wrapped)] = (
                bd.downcast(BRepBuilderAPI_Copy(self.part.wrapped).Shape()),
            )

        return copy.deepcopy(self, memo)


class Empty2d(AlgCompound):
    def __init__(self):
        self.wrapped = None
        self.objects = []
        self.dim = 2


class Empty3d(AlgCompound):
    def __init__(self):
        self.wrapped = None
        self.objects = []
        self.dim = 3


class Locations(bd.Locations):
    def __init__(self, *pts: Union[bd.VectorLike, bd.Vertex, bd.Location]):
        bd.Workplanes(bd.Plane.XY).__enter__()
        super().__init__(*pts)
        del self.plane_index


class PolarLocations(bd.PolarLocations):
    def __init__(
        self,
        radius: float,
        count: int,
        start_angle: float = 0.0,
        stop_angle: float = 360.0,
        rotate: bool = True,
    ):
        bd.Workplanes(bd.Plane.XY).__enter__()
        super().__init__(radius, count, start_angle, stop_angle, rotate)
        del self.plane_index


class GridLocations(bd.GridLocations):
    def __init__(
        self,
        x_spacing: float,
        y_spacing: float,
        x_count: int,
        y_count: int,
        centered: tuple[bool, bool] = (True, True),
    ):
        bd.Workplanes(bd.Plane.XY).__enter__()
        super().__init__(x_spacing, y_spacing, x_count, y_count, centered)
        del self.plane_index
