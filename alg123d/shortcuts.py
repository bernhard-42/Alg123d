from typing import List, Union
from .wrappers import AlgCompound
from .direct_api import *

__all__ = [
    "Pos",
    "Rot",
    "Planes",
    "x_axis",
    "y_axis",
    "z_axis",
    "from_cq",
    "to_cq",
    "from_bd",
    "to_bd",
]


class Pos(Location):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super().__init__((x, y, z))


class Rot(Location):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super().__init__((0, 0, 0), (x, y, z))


class Planes:
    def __init__(self, objs: List[Union[Plane, Location, Face]]) -> List[Plane]:
        self.objects = [Plane(obj) for obj in objs]
        self.index = 0

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.objects):
            plane = self.objects[self.index]
            self.index += 1
            return plane
        else:
            raise StopIteration


#
# Get transformed x-, y- and z-axis of a Compound
#


def x_axis(obj: Union[Location, AlgCompound]) -> Axis:
    loc = obj.location if isinstance(obj, AlgCompound) else obj
    dir = Plane(loc).x_dir
    return Axis(loc.position, dir)


def y_axis(obj: Union[Location, AlgCompound]) -> Axis:
    loc = obj.location if isinstance(obj, AlgCompound) else obj
    dir = Plane(loc).y_dir
    return Axis(loc.position, dir)


def z_axis(obj: Union[Location, AlgCompound]) -> Axis:
    loc = obj.location if isinstance(obj, AlgCompound) else obj
    dir = Plane(loc).z_dir
    return Axis(loc.position, dir)


#
# Conversion functions
#


def from_cq(obj):
    return AlgCompound.make_compound(obj.objects)


def to_cq(obj):
    import cadquery as cq

    return cq.Workplane().newObject([cq.Shape.cast(o.wrapped) for o in obj])


def from_bd(obj):
    if hasattr(obj, "_obj_name"):
        return AlgCompound(getattr(obj, obj._obj_name))
    else:
        return obj


def to_bd(obj):
    import build123d as bd

    if hasattr(obj, "dim"):
        ctx = {1: bd.BuildLine, 2: bd.BuildSketch, 3: bd.BuildPart}
        with ctx[obj.dim]() as c:
            bd.Add(Compound.make_compound(list(obj)))
        return c
    else:
        return bd.ShapeList(
            bd.Compound.make_compound([bd.Shape.cast(o.wrapped) for o in obj])
        )
