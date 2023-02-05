import copy
from typing import List, Tuple, Union

import build123d as bd

from .algcompound import AlgCompound, create_compound
from .direct_api import *

__all__ = ["chamfer", "fillet", "mirror", "offset", "scale", "split"]


#
# Functions
#


def chamfer(
    part: AlgCompound,
    objects: Union[List[Union[Edge, Vertex]], Edge, Vertex],
    length: float,
    length2: float = None,
) -> AlgCompound:
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
) -> AlgCompound:
    return create_compound(bd.Fillet, objects, params=dict(radius=radius), part=part)


def mirror(
    objects: Union[List[AlgCompound], AlgCompound],
    about: Plane = Plane.XZ,
) -> AlgCompound:
    return create_compound(bd.Mirror, objects, params=dict(about=about))


def offset(
    objects: Union[List[AlgCompound], AlgCompound],
    amount: float,
    kind: Kind = Kind.ARC,
) -> AlgCompound:
    result = create_compound(bd.Offset, objects, params=dict(amount=amount, kind=kind))
    if isinstance(objects, AlgCompound) and objects.dim == 3:
        if amount > 0:
            return result + objects
        else:
            return objects - result
    else:
        return result


def scale(objects: Shape, by: Union[float, Tuple[float, float, float]]) -> AlgCompound:
    if isinstance(by, (list, tuple)) and len(by) == 2:
        by = (*by, 1)

    return create_compound(bd.Scale, objects, params=dict(by=by))


def split(
    objects: Union[List[AlgCompound], AlgCompound],
    by: Plane = Plane.XZ,
    keep: Keep = Keep.TOP,
) -> AlgCompound:
    return create_compound(bd.Split, objects, params=dict(bisect_by=by, keep=keep))
