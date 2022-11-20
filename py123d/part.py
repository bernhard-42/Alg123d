from dataclasses import dataclass
from typing import Union

import build123d as bd


def validate(c, b, s=None):
    print("validate", c, b, s)
    return True


from .common import Build, Mixin
from .sketch import Sketch


bd.validate_inputs = validate


class Part(Build):
    def __repr__(self):
        return "Part(\n" + "\n".join(["    " + str(t) for t in self.tasks]) + "\n)"


@dataclass
class Box(bd.Box, Mixin):
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


@dataclass
class Extrusion(bd.Extrude, Mixin):
    def __init__(
        self,
        to_extrude: Union[bd.Face, Sketch],
        amount: float,
        until: bd.Until = None,
        part: Part = None,
        both: bool = False,
        taper: float = 0.0,
    ):
        with bd.BuildPart() as bp:
            # store to_extrude's faces in context
            bp.pending_faces = (
                [to_extrude]
                if isinstance(to_extrude, bd.Face)
                else to_extrude.obj.faces()
            )
            bp.pending_face_planes = [
                bd.Plane(face.to_pln()) for face in bp.pending_faces
            ]

            # store part's compound for Extrude to derive faces
            if part is not None:
                bp.part = part.obj

            with bd.Locations(bd.Location()):
                print(to_extrude, amount, until, both, taper)
                super().__init__(None, amount, until=until, both=both, taper=taper)

        del self.mode
