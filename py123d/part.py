from dataclasses import dataclass
import build123d as bd
from .common import Build, Mixin


class Part(Build):
    def __repr__(self):
        return "Part(\n" + "\n".join(["    " + str(t) for t in self.tasks]) + "\n)"


@dataclass
class Box(bd.Box, Mixin):
    __module__ = "build123d.build_part"

    length: float
    width: float
    height: float
    centered: tuple[bool, bool, bool]

    def __init__(
        self,
        length: float,
        width: float,
        height: float,
        centered: tuple[bool, bool, bool] = (True, True, True),
    ):
        with bd.BuildPart():
            with bd.Locations(bd.Location()):
                super().__init__(
                    length, width, height, centered=centered, mode=bd.Mode.PRIVATE
                )

        del self.rotation
        del self.mode


@dataclass
class Cylinder(bd.Cylinder, Mixin):
    __module__ = "build123d.build_part"

    radius: float
    height: float
    arc_size: float
    centered: tuple[bool, bool, bool]

    def __init__(
        self,
        radius: float,
        height: float,
        arc_size: float = 360,
        centered: tuple[bool, bool, bool] = (True, True, True),
    ):
        with bd.BuildPart():
            with bd.Locations(bd.Location()):
                super().__init__(
                    radius, height, arc_size, centered=centered, mode=bd.Mode.PRIVATE
                )

        del self.rotation
        del self.mode


# Operations


class Extrusion(bd.Extrude):
    def __init__(
        self,
        to_extrude: bd.Face = None,
        amount: float = None,
        until: bd.Until = None,
        both: bool = False,
        taper: float = 0.0,
    ):
        with bd.BuildPart() as bp:

            with bd.Locations():
                self.__init__(to_extrude, amount, until=until, both=both, taper=taper)
