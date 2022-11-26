from typing import List, Tuple
import build123d as bd
from .wrappers import create_compound, AlgCompound, Obj12d, Obj123d

__all__ = [
    "chamfer",
    "fillet",
    "mirror",
    "offset",
    "scale",
    "split",
]

#
# Functions
#


def chamfer(
    part: AlgCompound,
    objects: List[bd.Edge | bd.Vertex] | bd.Edge | bd.Vertex,
    length: float,
    length2: float = None,
):
    return create_compound(
        bd.Chamfer, objects, length=length, length2=length2, ctx_add=part, mode=None
    )


def fillet(
    part: AlgCompound,
    objects: List[bd.Edge | bd.Vertex] | bd.Edge | bd.Vertex,
    radius: float,
):
    return create_compound(bd.Fillet, objects, radius=radius, ctx_add=part, mode=None)


def mirror(
    objects: List[Obj12d] | Obj12d,
    about: bd.Plane = bd.Plane.XZ,
):
    return create_compound(bd.Mirror, objects, about=about)


def offset(
    objects: List[Obj123d] | Obj123d,
    amount: float,
    openings: bd.Face | list[bd.Face] = None,
    kind: bd.Kind = bd.Kind.ARC,
):
    return create_compound(
        bd.Offset, objects, amount=amount, openings=openings, kind=kind
    )


def scale(objects: bd.Shape, by: float | Tuple[float, float, float]):
    if isinstance(by, (list, tuple)) and len(by) == 2:
        by = (*by, 1)

    return create_compound(bd.Scale, objects, by=by)


def split(
    objects: List[Obj123d] | Obj123d,
    by: bd.Plane = bd.Plane.XZ,
    keep: bd.Keep = bd.Keep.TOP,
):
    return create_compound(bd.Split, objects, bisect_by=by, keep=keep)
