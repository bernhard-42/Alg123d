from typing import Union, List
from dataclasses import dataclass

import build123d as bd
from .common import AlgCompound, Obj123d

TYPES = [None, bd.BuildLine, bd.BuildSketch, bd.BuildPart]


def chamfer(
    part: bd.Compound,
    objects: List[Union[bd.Edge, bd.Vertex]],
    length: float,
    length2: float = None,
):
    with TYPES[part.dim]() as ctx:
        ctx.part = bd.Compound(part.wrapped)
        compound = bd.Chamfer(*objects, length=length, length2=length2)

    objects = part.objects  # TODO

    return AlgCompound(compound, objects, part.dim)


def fillet(
    part: bd.Compound,
    objects: List[Union[bd.Edge, bd.Vertex]],
    radius: float,
):
    with TYPES[part.dim]() as ctx:
        ctx.part = bd.Compound(part.wrapped)
        compound = bd.Fillet(*objects, radius=radius)

    objects = [Obj123d(compound, compound.location, None)]  # TODO

    return AlgCompound(compound, objects, part.dim)
