from __future__ import annotations

import build123d as bd
from .direct_api import *


CTX = [None, bd.BuildLine, bd.BuildSketch, bd.BuildPart]

__all__ = [
    "AlgCompound",
    "create_compound",
]

#
# Algebra operations enhanced Compound
#


class AlgCompound(Compound):
    def __init__(self, compound=None, dim: int = None):
        self.wrapped = None if compound is None else compound.wrapped
        self.dim = dim

    @classmethod
    def make_compound(cls, objs: Shape, dim):
        return cls(Compound.make_compound(objs), dim)

    def create_line(self, cls, objects=None, params=None):
        if params is None:
            params = {}

        with bd.BuildLine():
            if objects is None:
                obj = cls(**params, mode=Mode.PRIVATE)
            else:
                obj = cls(*list(objects), **params, mode=Mode.PRIVATE)

        self.wrapped = Compound.make_compound(obj.edges()).wrapped
        self.dim = 1

    def create_sketch(self, cls, objects=None, params=None):
        if params is None:
            params = {}

        with bd.BuildSketch():
            if objects is None:
                self.wrapped = cls(**params, mode=Mode.PRIVATE).wrapped
            else:
                self.wrapped = cls(*list(objects), **params, mode=Mode.PRIVATE).wrapped
        self.dim = 2

    def create_part(self, cls, part=None, params=None):
        if params is None:
            params = {}

        with bd.BuildPart() as ctx:
            if part is not None:
                ctx._add_to_context(part)

            self.wrapped = cls(**params, mode=Mode.PRIVATE).wrapped
        self.dim = 3

    def _place(self, mode: Mode, obj: AlgCompound, at: Location = None):
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
            if self.dim == 1:
                if mode == Mode.ADD:
                    compound = self.fuse(located_obj).clean()
                else:
                    raise RuntimeError("Lines can only be added")
            else:
                if mode == Mode.ADD:
                    compound = self.fuse(located_obj).clean()
                elif mode == Mode.SUBTRACT:
                    compound = self.cut(located_obj).clean()
                elif mode == Mode.INTERSECT:
                    compound = self.intersect(located_obj).clean()

        return AlgCompound(compound, self.dim)

    def __add__(self, other: AlgCompound):
        return self._place(Mode.ADD, other)

    def __sub__(self, other: AlgCompound):
        return self._place(Mode.SUBTRACT, other)

    def __and__(self, other: AlgCompound):
        return self._place(Mode.INTERSECT, other)

    def __matmul__(self, obj: Union[float, AlgCompound]):
        if isinstance(obj, (int, float)):
            if self.dim == 1:
                return Wire.make_wire(self.edges()).position_at(obj)
            else:
                raise TypeError("Only lines can access positions")

        elif isinstance(obj, Location):
            loc = obj

        elif isinstance(obj, tuple):
            loc = Location(obj)

        elif isinstance(obj, Workplane):
            loc = obj.to_location()

        else:
            raise ValueError(f"Cannot multiply with {obj}")

        return self.located(loc)

    def __mod__(self, position):
        if self.dim == 1:
            return Wire.make_wire(self.edges()).tangent_at(position)
        else:
            raise TypeError(f"unsupported operand type(s)")

    def __repr__(self):
        def r2(v):
            return tuple([round(e, 2) for e in v])

        loc_str = f"position={r2(self.location.position)}, rotation={r2(self.location.orientation)}"
        return f"obj={self.__class__.__name__}; loc=({loc_str}); dim={self.dim}"


#
# Function wrapper
#


def create_compound(
    cls, objects, part=None, dim=None, faces=None, planes=None, params=None
):
    if isinstance(objects, AlgCompound) and objects.dim == 1:
        objs = objects.edges()
        dim = 1
    else:
        if isinstance(objects, (list, tuple)):
            objs = objects
        elif isinstance(objects, filter):
            objs = list(objects)
        else:
            objs = [objects]

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

    return AlgCompound(compound, dim)
