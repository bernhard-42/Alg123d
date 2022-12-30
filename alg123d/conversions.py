from typing import List, Union
from .algcompound import AlgCompound
from .direct_api import *

__all__ = [
    "from_cq",
    "to_cq",
    "from_bd",
    "to_bd",
]


def from_cq(obj):
    return AlgCompound.make_compound(obj.objects)


def to_cq(obj):
    import cadquery as cq

    return cq.Workplane().newObject([cq.Shape.cast(o.wrapped) for o in obj])


def from_bd(obj):
    if hasattr(obj, "_obj_name"):
        return AlgCompound(getattr(obj, obj._obj_name))
    else:
        return obj


def to_bd(obj):
    import build123d as bd

    if hasattr(obj, "dim"):
        ctx = {1: bd.BuildLine, 2: bd.BuildSketch, 3: bd.BuildPart}
        with ctx[obj.dim]() as c:
            bd.Add(Compound.make_compound(list(obj)))
        return c
    else:
        return bd.ShapeList(
            bd.Compound.make_compound([bd.Shape.cast(o.wrapped) for o in obj])
        )
