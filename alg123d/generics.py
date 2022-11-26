from typing import List, Tuple
import build123d as bd
from .wrappers import create_compound, AlgCompound, Obj12d, Obj123d

__all__ = [
    "tupleize",
    "chamfer",
    "fillet",
    "mirror",
    "offset",
    "scale",
    "split",
]


def tupleize(arg):
    if isinstance(arg, (tuple, list)):
        return tuple(arg)
    else:
        return (arg,)


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
        bd.Chamfer,
        objects,
        params=dict(length=length, length2=length2),
        part=part,
    )


def fillet(
    part: AlgCompound,
    objects: List[bd.Edge | bd.Vertex] | bd.Edge | bd.Vertex,
    radius: float,
):
    return create_compound(bd.Fillet, objects, params=dict(radius=radius), part=part)


def mirror(
    objects: List[Obj12d] | Obj12d,
    about: bd.Plane = bd.Plane.XZ,
):
    return create_compound(bd.Mirror, objects, params=dict(about=about))


def offset(
    objects: List[Obj123d] | Obj123d,
    amount: float,
    openings: bd.Face | list[bd.Face] = None,
    kind: bd.Kind = bd.Kind.ARC,
):
    return create_compound(
        bd.Offset, objects, params=dict(amount=amount, openings=openings, kind=kind)
    )


def scale(objects: bd.Shape, by: float | Tuple[float, float, float]):
    if isinstance(by, (list, tuple)) and len(by) == 2:
        by = (*by, 1)

    return create_compound(bd.Scale, objects, params=dict(by=by))


def split(
    objects: List[Obj123d] | Obj123d,
    by: bd.Plane = bd.Plane.XZ,
    keep: bd.Keep = bd.Keep.TOP,
):
    return create_compound(bd.Split, objects, params=dict(bisect_by=by, keep=keep))
