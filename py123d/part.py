from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple, Union

from build123d.direct_api import (
    Compound,
    Solid,
    Face,
    Wire,
    Edge,
    Vertex,
    Vector,
    Plane,
    Location as _Location,
    Rotation,
    VectorLike,
    RotationLike,
)

class Location(_Location):
    def __init__(self, *args):
        if len(args) == 2 and isinstance(args[0], (tuple, Vector)) and isinstance(args[1], (tuple, Rotation)):
            rot = Rotation(*args[1]) if isinstance(args[1], (tuple, list)) else args[1]
            pos = Location(args[0])
            self.wrapped = (pos*rot).wrapped
        else:
            super().__init__(*args)

CadObj = Union[Solid, Face, Wire, Edge, Edge]


class Mode(Enum):
    """Combination Mode"""

    ADD = "a"
    SUBTRACT = "s"
    INTERSECT = "i"
    REPLACE = "r"

    def __repr__(self):
        return f'{self.name}("{self.value}")'


@dataclass
class Task:
    obj: CadObj
    mode: Mode


class Part(Compound):
    def __init__(self):
        self.tasks: List[Task] = []
        self.compound: Compound = None

    def add(self, obj: CadObj):
        self.tasks.append(obj, Mode.ADD)

    def subtract(self, obj: CadObj):
        self.tasks.append(obj, Mode.SUBTRACT)

    def intersect(self, obj: CadObj):
        self.tasks.append(obj, Mode.INTERSECT)


@dataclass
class Box:
    length: float
    width: float
    height: float
    rotations: List[RotationLike] = None
    locations: List[Location] = None
    centered: tuple[bool, bool, bool] = (True, True, True)

    def __post_init__(self):
        

        center_offset = Vector(
            -self.length / 2 if self.centered[0] else 0,
            -self.width / 2 if self.centered[1] else 0,
            -self.height / 2 if self.centered[2] else 0,
        )
        rotate = Rotation(*self.rotation) if isinstance(rotation, tuple) else rotation
        if locations is None:
            locations= [Location()]

        if rotations is None:
            rotations = [Rotation((0,0,0))]

        new_solids = []
        for location in self.locations:
            solid = Solid.make_box(self.length, self.width, self.height, Plane(center_offset)).locate(
                location * self.rotate
            )
            for location in self.locations
        ]