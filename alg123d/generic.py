from typing import List, Tuple, Union
import build123d as bd
from .direct_api import *
from .wrappers import create_compound, AlgCompound

__all__ = ["chamfer", "fillet", "mirror", "offset", "scale", "split"]


#
# Functions
#


def chamfer(
    part: AlgCompound,
    objects: Union[List[Union[Edge, Vertex]], Edge, Vertex],
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
    objects: Union[List[Union[Edge, Vertex]], Edge, Vertex],
    radius: float,
):
    return create_compound(bd.Fillet, objects, params=dict(radius=radius), part=part)


def mirror(
    objects: Union[List[AlgCompound], AlgCompound],
    about: Plane = Plane.XZ,
):
    return create_compound(bd.Mirror, objects, params=dict(about=about))


def offset(
    objects: Union[List[AlgCompound], AlgCompound],
    amount: float,
    openings: Union[Face, List[Face]] = None,
    kind: Kind = Kind.ARC,
):
    return create_compound(
        bd.Offset, objects, params=dict(amount=amount, openings=openings, kind=kind)
    )


def scale(objects: Shape, by: Union[float, Tuple[float, float, float]]):
    if isinstance(by, (list, tuple)) and len(by) == 2:
        by = (*by, 1)

    return create_compound(bd.Scale, objects, params=dict(by=by))


def split(
    objects: Union[List[AlgCompound], AlgCompound],
    by: Plane = Plane.XZ,
    keep: Keep = Keep.TOP,
):
    return create_compound(bd.Split, objects, params=dict(bisect_by=by, keep=keep))
