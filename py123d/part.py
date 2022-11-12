from dataclasses import dataclass
from typing import List, Tuple, Union

from .direct_api import (
    Compound,
    Solid,
    Face,
    Wire,
    Edge,
    Vertex,
    Vector,
    Plane,
    Location,
    Rotation,
    VectorLike,
    RotationLike,
    CadObj,
)
from .enums import Mode


@dataclass
class Task:
    obj: CadObj
    mode: Mode


class Part(Compound):
    def __init__(self):
        self.tasks: List[Task] = []
        self.obj: Compound = None

    def _place(self, solid: CadObj, mode: Mode, at: Union[List[Location], None] = None):
        if at is None:
            at = [Location()]

        for loc in at:
            new_solid = solid.obj.located(loc)
            self.tasks.append(Task(new_solid, mode))
            if mode == Mode.ADD:
                if self.obj == None:
                    self.obj = Compound.make_compound([new_solid])
                else:
                    self.obj = self.obj.fuse(new_solid)

            elif mode == Mode.SUBTRACT:
                if self.obj is None:
                    raise RuntimeError("Connect cut solid from None")

                self.obj = self.obj.cut(new_solid)

    def add(self, solid: CadObj, at: Union[List[Location], None] = None):
        self._place(solid, Mode.ADD, at)

    def subtract(self, solid: CadObj, at: Union[List[Location], None] = None):
        self._place(solid, Mode.SUBTRACT, at)

    def intersect(self, solid: CadObj, at: Union[List[Location], None] = None):
        self._place(solid, Mode.INTERSECT, at)


@dataclass
class Box:
    length: float
    width: float
    height: float
    centered: tuple[bool, bool, bool] = (True, True, True)

    def __post_init__(self):

        center_offset = Vector(
            -self.length / 2 if self.centered[0] else 0,
            -self.width / 2 if self.centered[1] else 0,
            -self.height / 2 if self.centered[2] else 0,
        )

        self.obj = Solid.make_box(
            self.length, self.width, self.height, Plane(center_offset)
        )


@dataclass
class Cylinder:
    radius: float
    height: float
    arc_size: float = 360
    centered: tuple[bool, bool, bool] = (True, True, True)

    def __post_init__(self):
        center_offset = Vector(
            0 if self.centered[0] else self.radius,
            0 if self.centered[1] else self.radius,
            -self.height / 2 if self.centered[2] else 0,
        )
        self.obj = Solid.make_cylinder(
            self.radius,
            self.height,
            Plane(center_offset),
            self.arc_size,
        )
