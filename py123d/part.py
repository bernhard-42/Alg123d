from dataclasses import dataclass
from typing import Union

import build123d as bd

from .common import AlgCompound


@dataclass
class Box(AlgCompound):
    length: float
    width: float
    height: float
    centered: tuple[bool, bool, bool] = (True, True, True)

    def __post_init__(self):
        self.create_context_and_part(bd.Box)


@dataclass
class Cylinder(AlgCompound):
    radius: float
    height: float
    arc_size: float = 360
    centered: tuple[bool, bool, bool] = (True, True, True)

    def __post_init__(self):
        self.create_context_and_part(bd.Cylinder)


@dataclass
class Extrusion(AlgCompound):
    to_extrude: bd.Compound
    amount: float
    until: bd.Until = None
    part: bd.Compound = None
    both: bool = False
    taper: float = 0.0

    def __post_init__(self):
        with bd.BuildPart() as bp:
            # store to_extrude's faces in context
            bp.pending_faces = (
                [self.to_extrude]
                if isinstance(self.to_extrude, bd.Face)
                else self.to_extrude.faces()
            )
            bp.pending_face_planes = [
                bd.Plane(face.to_pln()) for face in bp.pending_faces
            ]

            if len(bp.pending_faces) == 0:
                raise RuntimeError(f"No faces found in {self.to_extrude}")

            # store part's compound for Extrude to derive faces
            if self.part is not None:
                bp.part = self.part

            self.create_part(bd.Extrude, exclude=["to_extrude", "part"])
