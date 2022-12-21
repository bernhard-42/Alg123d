from __future__ import annotations
from collections.abc import Iterable
from typing import List

import build123d as bd
from .direct_api import *
from .utils import to_list

__all__ = ["DelayClean", "LazyAlgCompound", "AlgCompound", "create_compound"]

CTX = [None, bd.BuildLine, bd.BuildSketch, bd.BuildPart]


#
# Algebra operations enhanced Compound
#


def unwrap(compound: Compound) -> Compound:
    """remove enclosing Compound if it only holds one other Compund"""
    if (
        isinstance(compound, Compound)
        and isinstance(compound, Iterable)
        and len(list(compound)) == 1
        and isinstance(list(compound)[0], Compound)
    ):
        return list(compound)[0]
    else:
        return compound


class AlgCompound(Compound):
    def __init__(self, obj: Union[Compound, Solid, Face, Edge] = None):
        if isinstance(obj, Compound):
            objs = list(unwrap(obj))
        elif isinstance(obj, (Solid, Face, Edge)):
            objs = [obj]
        elif obj is not None:
            raise TypeError(f"Unknown type {obj}")

        if obj is None:
            self.dim = 0
            self.wrapped = None

        elif all([isinstance(obj, (Edge, Wire)) for obj in objs]):
            self.dim = 1
            self.wrapped = Compound.make_compound(objs).wrapped

        elif all([isinstance(obj, Face) for obj in objs]):
            self.dim = 2
            self.wrapped = Compound.make_compound(objs).wrapped

        elif all([isinstance(obj, Solid) for obj in objs]):
            self.dim = 3
            self.wrapped = Compound.make_compound(objs).wrapped

        else:
            raise RuntimeError(f"{objs} not supported")

        self.mates = {}
        self.joints = {}
        # Don't call super().__init__() since we don't need .for_construction

    @classmethod
    def make_compound(cls, objs: Shape):
        compound = Compound.make_compound(objs)
        return cls(compound)

    def _create(self, ctx, cls, objects=None, part=None, params=None):
        if params is None:
            params = {}

        with ctx() as c:
            if part is not None:
                c._add_to_context(part)

            if objects is None:
                result = cls(**params, mode=Mode.PRIVATE)
            else:
                result = cls(*list(objects), **params, mode=Mode.PRIVATE)

        return result

    def create_line(self, cls, objects=None, params=None):
        result = self._create(bd.BuildLine, cls, objects=objects, params=params)
        return Compound.make_compound(result.edges())

    def create_sketch(self, cls, objects=None, params=None):
        return self._create(bd.BuildSketch, cls, objects=objects, params=params)

    def create_part(self, cls, part=None, params=None):
        return self._create(bd.BuildPart, cls, part=part, params=params)

    def _place(self, mode: Mode, *objs: AlgCompound):
        if not (objs[0].dim == 0 or self.dim == 0 or self.dim == objs[0].dim):
            raise RuntimeError(
                f"Cannot combine objects of different dimensionality: {self.dim} and {objs[0].dim}"
            )

        if self.dim == 0:  # Cover addition of empty AlgCompound with another object
            if mode == Mode.ADD:
                if len(objs) == 1:
                    compound = objs[0]
                else:
                    compound = objs.pop().fuse(*objs).clean()
            else:
                raise RuntimeError("Can only add to an empty AlgCompound object")
        elif objs[0].dim == 0:  # Cover operation with empty AlgCompound object
            compound = self
        else:
            if mode == Mode.ADD:
                compound = self.fuse(*objs).clean()

            elif self.dim == 1:
                raise RuntimeError("Lines can only be added")

            else:
                if mode == Mode.SUBTRACT:
                    compound = self.cut(*objs).clean()
                elif mode == Mode.INTERSECT:
                    compound = self.intersect(*objs).clean()

        return AlgCompound(compound)

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

        compound = unwrap(cls(**params) if objs is None else cls(*objs, **params))

        if part is not None:
            compound = unwrap(ctx._obj)

    solids = compound.solids()
    if len(solids) > 1:
        return AlgCompound(solids[0].fuse(*solids[1:]).clean())
    else:
        return AlgCompound(compound)


class LazyAlgCompound(AlgCompound):
    def __init__(self):
        super().__init__()

    def __enter__(self):
        self._collected_objects = []
        return self

    def __add__(self, other):
        if hasattr(self, "_collected_objects"):
            if other.solids():
                dim = 3
            elif other.faces():
                dim = 2
            else:
                dim = 1

            if self.dim == 0:
                self.dim = dim
            else:
                if dim != self.dim:
                    raise RuntimeError("Cannot add objects with different dimensions")

            self._collected_objects.append(other)
            return self

        else:
            return super().__add__(other)

    def __exit__(self, exception_type, exception_value, traceback):
        self.wrapped = (
            self._collected_objects.pop().fuse(*self._collected_objects).clean().wrapped
        )
        del self._collected_objects
