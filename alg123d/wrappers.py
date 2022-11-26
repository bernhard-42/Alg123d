import copy

import build123d as bd
from .direct_api import *

from OCP.BRepBuilderAPI import (  # pyright: ignore[reportMissingImports]
    BRepBuilderAPI_Copy,
)

Obj1d = Compound | Wire | Edge
Obj2d = Compound | Face
Obj3d = Compound | Solid
Obj12d = Obj1d | Obj2d
Obj23d = Obj2d | Obj3d
Obj123d = Obj1d | Obj2d | Obj3d

CTX = [None, bd.BuildLine, bd.BuildSketch, bd.BuildPart]

__all__ = [
    "AlgCompound",
    "AlgEdge",
    "AlgWire",
    "create_compound",
]

#
# Algebra operations enhanced Compound
#


class Mixin:
    def create_line(self, cls, objects=None, params=None):
        if params is None:
            params = {}

        with bd.BuildLine() as ctx:
            if objects is None:
                obj = cls(**params, mode=Mode.PRIVATE)
            else:
                obj = cls(*objects, **params, mode=Mode.PRIVATE)

        self.wrapped = obj.wrapped
        self._params = params
        self.dim = 1

    def create_part(
        self,
        cls,
        part=None,
        params=None,
    ):
        if params is None:
            params = {}

        with bd.BuildPart() as ctx:
            if part is not None:
                ctx._add_to_context(part)

            self.wrapped = cls(**params, mode=Mode.PRIVATE).wrapped

        self._params = params
        self.dim = 3

    def create_sketch(self, cls, objects=None, params=None):
        if params is None:
            params = {}

        with bd.BuildSketch():
            if objects is None:
                self.wrapped = cls(**params, mode=Mode.PRIVATE).wrapped
            else:
                self.wrapped = cls(*objects, **params, mode=Mode.PRIVATE).wrapped

        self._params = params
        self.dim = 2

    def _place(
        self,
        mode: Mode,
        obj: Obj23d,
        at: Location = None,
    ):
        if at is None:
            located_obj = obj
            loc = obj.location
        else:
            if isinstance(at, Location):
                loc = at
            elif isinstance(at, Workplane):
                loc = at.to_location()
            elif isinstance(at, tuple):
                loc = Location(at)
            else:
                raise ValueError(f"{at } is no location or plane")

            located_obj = obj.located(loc)

        if self.wrapped is None:
            if mode == Mode.ADD:
                compound = located_obj
            else:
                raise RuntimeError("Can only add to empty object")
        else:
            compound = self
            if mode == Mode.ADD:
                compound = compound.fuse(located_obj).clean()
            elif mode == Mode.SUBTRACT:
                compound = compound.cut(located_obj).clean()
            elif mode == Mode.INTERSECT:
                compound = compound.intersect(located_obj).clean()

        return AlgCompound(compound, {}, self.dim)

    def __add__(self, other: Obj23d):
        return self._place(Mode.ADD, other)

    def __sub__(self, other: Obj23d):
        return self._place(Mode.SUBTRACT, other)

    def __and__(self, other: Obj23d):
        return self._place(Mode.INTERSECT, other)

    def __matmul__(self, obj):
        if isinstance(obj, Location):
            loc = obj
        elif isinstance(obj, tuple):
            loc = Location(obj)
        elif isinstance(obj, Workplane):
            loc = obj.to_location()
        else:
            raise ValueError(f"Cannot multiply with {obj}")

        return self.located(loc)

    def __repr__(self):
        def r2(v):
            return tuple([round(e, 2) for e in v])

        p = ""
        for k, v in self._params.items():
            p += f"{k}={v},"

        loc_str = f"position={r2(self.location.position)}, rotation={r2(self.location.orientation)}"
        return f"{self.__class__.__name__}({p}); loc=({loc_str}); dim={self.dim}"

    def copy(self):
        memo = {}
        memo[id(self.wrapped)] = bd.downcast(BRepBuilderAPI_Copy(self.wrapped).Shape())

        return copy.deepcopy(self, memo)


class AlgEdge(Mixin, Edge):  # keep order to overwrite __matmul__
    def __init__(self, edge=None, params=None, dim: int = None):
        self.wrapped = None if edge is None else edge.wrapped
        self.dim = dim
        self._params = [] if params is None else params

    def __and__(self, position):
        return self.position_at(position)


class AlgWire(Mixin, Wire):  # keep order to overwrite __matmul__
    def __init__(self, wire=None, params=None, dim: int = None):
        self.wrapped = None if wire is None else wire.wrapped
        self.dim = dim
        self._params = [] if params is None else params

    def __and__(self, position):
        return self.position_at(position)


class AlgCompound(Compound, Mixin):
    def __init__(self, compound=None, params=None, dim: int = None):
        self.wrapped = None if compound is None else compound.wrapped
        self.dim = dim
        self._params = [] if params is None else params


#
# Function wrapper
#


def create_compound(
    cls,
    objects,
    part=None,
    dim=None,
    faces=None,
    planes=None,
    params=None,
):
    objs = objects if isinstance(objects, (list, tuple)) else [objects]

    if dim is None:
        if part is None:
            dim = max([o.dim for o in objs])
        else:
            dim = part.dim

    with CTX[dim]() as ctx:
        if part is not None:
            ctx._add_to_context(Compound(part.wrapped))

        if faces is not None:
            ctx.pending_faces = faces

        if planes is not None:
            ctx.pending_face_planes = planes

        compound = cls(*objs, **params)

        if part is not None:
            compound = ctx._obj

    return AlgCompound(compound, {}, dim)
