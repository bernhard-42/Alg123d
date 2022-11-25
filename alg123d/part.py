from dataclasses import dataclass
import build123d as bd
from .wrappers import AlgCompound

__all__ = [
    "Empty3",
    "Box",
    "Cylinder",
    "Cone",
    "Sphere",
    "Torus",
    "Wedge",
    "CounterBore",
    "CounterSink",
    "Bore",
]


class Empty3(AlgCompound):
    def __init__(self):
        super().__init__(dim=3)


@dataclass(repr=False)
class Box(AlgCompound):
    length: float
    width: float
    height: float
    centered: tuple[bool, bool, bool] = (True, True, True)

    def __post_init__(self):
        self.create_part(bd.Box)


@dataclass(repr=False)
class Cylinder(AlgCompound):
    radius: float
    height: float
    arc_size: float = 360
    centered: tuple[bool, bool, bool] = (True, True, True)

    def __post_init__(self):
        self.create_part(bd.Cylinder)


@dataclass(repr=False)
class Cone(AlgCompound):
    bottom_radius: float
    top_radius: float
    height: float
    arc_size: float = 360
    centered: tuple[bool, bool, bool] = (True, True, True)

    def __post_init__(self):
        self.create_part(bd.Cone)


@dataclass(repr=False)
class Sphere(AlgCompound):
    radius: float
    arc_size1: float = -90
    arc_size2: float = 90
    arc_size3: float = 360
    centered: tuple[bool, bool, bool] = (True, True, True)

    def __post_init__(self):
        self.create_part(bd.Sphere)


@dataclass(repr=False)
class Torus(AlgCompound):
    major_radius: float
    minor_radius: float
    minor_start_angle: float = 0
    minor_end_angle: float = 360
    major_angle: float = 360
    centered: tuple[bool, bool, bool] = (True, True, True)

    def __post_init__(self):
        self.create_part(bd.Torus)


@dataclass(repr=False)
class Wedge(AlgCompound):
    dx: float
    dy: float
    dz: float
    xmin: float
    zmin: float
    xmax: float
    zmax: float

    def __post_init__(self):
        self.create_part(bd.Wedge)


@dataclass(repr=False)
class CounterBore(AlgCompound):
    part: AlgCompound
    radius: float
    counter_bore_radius: float
    counter_bore_depth: float
    depth: float = None

    def __post_init__(self):
        self.create_part(bd.CounterBoreHole, self.part, exclude=["part"])


@dataclass(repr=False)
class CounterSink(AlgCompound):
    part: AlgCompound
    radius: float
    counter_sink_radius: float
    counter_sink_angle: float = 82
    depth: float = None

    def __post_init__(self):
        self.create_part(bd.CounterSinkHole, self.part, exclude=["part"])


@dataclass(repr=False)
class Bore(AlgCompound):
    part: AlgCompound
    radius: float
    depth: float = None

    def __post_init__(self):
        self.create_part(bd.Hole, self.part, exclude=["part"])
