from __future__ import annotations
from typing import List

import build123d as bd
from .direct_api import *
from .utils import to_list

__all__ = ["DelayClean", "Empty", "AlgCompound", "create_compound"]

CTX = [None, bd.BuildLine, bd.BuildSketch, bd.BuildPart]


#
# Algebra operations enhanced Compound
#
class DelayClean:
    clean = True

    def __init__(self, callback):
        self.callback = callback

    def __enter__(self):
        DelayClean.clean = False

    def __exit__(self, exception_type, exception_value, traceback):
        objs = self.callback()
        if not isinstance(objs, (tuple, list)):
            objs = [objs]
        for obj in objs:
            obj.clean()
        DelayClean.clean = True


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

        self.mates = {}

    @classmethod
    def make_compound(cls, objs: Shape, dim=None):
        compound = Compound.make_compound(objs)
        if dim is None:
            dims = {"Solid": 3, "Face": 2, "Wire": 1, "Edge": 1}
            if hasattr(objs[0], "ShapeType"):
                dim = dims[objs[0].ShapeType()]
            else:
                dim = dims[objs[0].shape_type()]
        return cls(compound, dim)

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
        self.mates = {}

    def _place(self, mode: Mode, *objs: AlgCompound):
        if len(objs) == 1:
            obj = objs[0]
            if not (obj.dim == 0 or self.dim == 0 or self.dim == obj.dim):
                raise RuntimeError(
                    f"Cannot combine obercts of different dimensionality: {self.dim} and {obj.dim}"
                )
        else:
            objs = list(objs)
            if not (self.dim == 0 or all([obj.dim == self.dim for obj in objs])):
                raise RuntimeError(
                    f"Cannot combine obercts of different dimensionalities"
                )

        if self.dim == 0:  # Cover addition of Empty with another object
            if mode == Mode.ADD:
                if len(objs) == 1:
                    compound = obj
                else:
                    compound = objs.pop().fuse(*objs).clean()
                dim = objs[0].dim  # take over dimensionality of other operand
            else:
                raise RuntimeError("Can only add to empty object")
        elif objs[0].dim == 0:  # Cover operation with Empty object
            compound = self
        else:
            dim = self.dim
            if dim == 1:
                if mode == Mode.ADD:
                    compound = self.fuse(*objs)
                    if DelayClean.clean:
                        compound.clean()
                else:
                    raise RuntimeError("Lines can only be added")
            else:
                if mode == Mode.ADD:
                    compound = self.fuse(*objs)
                    if DelayClean.clean:
                        compound.clean()
                elif mode == Mode.SUBTRACT:
                    compound = self.cut(*objs)
                    if DelayClean.clean:
                        compound.clean()
                elif mode == Mode.INTERSECT:
                    compound = self.intersect(*objs)
                    if DelayClean.clean:
                        compound.clean()

        return AlgCompound(compound, dim)

    def __add__(self, other: Union[AlgCompound, List[AlgCompound]]):
        return self._place(Mode.ADD, *to_list(other))

    def __sub__(self, other: Union[AlgCompound, List[AlgCompound]]):
        return self._place(Mode.SUBTRACT, *to_list(other))

    def __and__(self, other: Union[AlgCompound, List[AlgCompound]]):
        return self._place(Mode.INTERSECT, *to_list(other))

    def __matmul__(self, obj: Union[float, Location]):
        if isinstance(obj, (int, float)):
            if self.dim == 1:
                return Wire.make_wire(self.edges()).position_at(obj)
            else:
                raise TypeError("Only lines can access positions")

        elif isinstance(obj, Location):
            loc = obj

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

    solids = compound.solids()
    if len(solids) > 1:
        return AlgCompound(solids[0].fuse(*solids[1:]).clean(), 3)
    else:
        return AlgCompound(compound, dim)
