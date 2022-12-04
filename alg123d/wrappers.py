from __future__ import annotations

import build123d as bd
from .direct_api import *

__all__ = ["Empty", "AlgCompound", "create_compound"]

CTX = [None, bd.BuildLine, bd.BuildSketch, bd.BuildPart]


#
# Algebra operations enhanced Compound
#


class AlgCompound(Compound):
    def __init__(self, obj: Union[Compound, Solid, Face, Edge] = None, dim: int = None):
        if isinstance(obj, Solid):
            self.dim = 3
            self.wrapped = Compound.make_compound([obj]).wrapped
        elif isinstance(obj, Face):
            self.dim = 2
            self.wrapped = Compound.make_compound([obj]).wrapped
        elif isinstance(obj, Edge):
            self.dim = 1
            self.wrapped = Compound.make_compound([obj]).wrapped
        else:
            self.dim = dim
            self.wrapped = None if obj is None else obj.wrapped

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

    def _place(self, mode: Mode, obj: AlgCompound):
        if not (obj.dim == 0 or self.dim == 0 or self.dim == obj.dim):
            raise RuntimeError(
                f"Cannot combine obercts of different dimensionality: {self.dim} and {obj.dim} "
            )

        if self.dim == 0:  # Cover addition of Empty with another object
            if mode == Mode.ADD:
                compound = obj
                self.dim = obj.dim  # take over dimensionality of other operand
            else:
                raise RuntimeError("Can only add to empty object")
        elif obj.dim == 0:  # Cover operation with Empty object
            compound = self
        else:
            if self.dim == 1:
                if mode == Mode.ADD:
                    compound = self.fuse(obj).clean()
                else:
                    raise RuntimeError("Lines can only be added")
            else:
                if mode == Mode.ADD:
                    compound = self.fuse(obj).clean()
                elif mode == Mode.SUBTRACT:
                    compound = self.cut(obj).clean()
                elif mode == Mode.INTERSECT:
                    compound = self.intersect(obj).clean()

        return AlgCompound(compound, self.dim)

    def __add__(self, other: AlgCompound):
        return self._place(Mode.ADD, other)

    def __sub__(self, other: AlgCompound):
        return self._place(Mode.SUBTRACT, other)

    def __and__(self, other: AlgCompound):
        return self._place(Mode.INTERSECT, other)

    def __matmul__(self, obj: Union[float, LocationLike]):
        if isinstance(obj, (int, float)):
            if self.dim == 1:
                return Wire.make_wire(self.edges()).position_at(obj)
            else:
                raise TypeError("Only lines can access positions")

        elif isinstance(obj, Location):
            loc = obj

        elif isinstance(obj, tuple) and all([isinstance(o, (int, float)) for o in obj]):
            loc = Location(obj)

        elif isinstance(obj, Plane):
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

        if self.dim == 0:
            loc_str = "None"
        else:
            loc_str = f"(position={r2(self.location.position)}, rotation={r2(self.location.orientation)})"
        return f"obj={self.__class__.__name__}; loc={loc_str}; dim={self.dim}"


class Empty(AlgCompound):
    def __init__(self):
        super().__init__(dim=0)


#
# Function wrapper
#


def create_compound(
    cls, objects=None, part=None, dim=None, faces=None, planes=None, params=None
):
    if objects is None:
        objs = None
    else:
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

        compound = cls(**params) if objs is None else cls(*objs, **params)

        if part is not None:
            if len(list(ctx._obj)) == 1 and isinstance(ctx._obj, Compound):
                compound = list(ctx._obj)[0]
            else:
                compound = ctx._obj

    return AlgCompound(compound, dim)
