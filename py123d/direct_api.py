from typing import Union

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

CadObj = Union[Solid, Face, Wire, Edge, Edge]


class Location(_Location):
    def __init__(self, *args):
        if (
            len(args) == 2
            and isinstance(args[0], (tuple, Vector))
            and isinstance(args[1], (tuple, Rotation))
        ):
            rot = Rotation(*args[1]) if isinstance(args[1], (tuple, list)) else args[1]
            pos = Location(args[0])
            self.wrapped = (pos * rot).wrapped
        else:
            super().__init__(*args)


def grid_locations(x: int, y: int, dx, dx):
    return [
        Location(((i - x / 2) * dx, (j - y / 2) * dx, 0))
        for i in range(x)
        for j in range(y)
    ]
