from __future__ import annotations

from collections.abc import Iterable
import copy
from typing import List

import build123d as bd

from .direct_api import *
from .utils import to_list

__all__ = ["SkipClean", "Copy", "LazyAlgCompound", "AlgCompound", "create_compound"]

CTX = [None, bd.BuildLine, bd.BuildSketch, bd.BuildPart]

#
# SkipClean context
#


class SkipClean:
    clean = True

    def __enter__(self):
        SkipClean.clean = False

    def __exit__(self, exception_type, exception_value, traceback):
        SkipClean.clean = True


class Copy:
    shallow = False

    def __enter__(self):
        Copy.shallow = True

    def __exit__(self, exception_type, exception_value, traceback):
        Copy.shallow = False


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
    def __init__(self, obj: Union[Compound, Solid, Face, Edge] = None, label=None):
        if isinstance(obj, Compound):
            objs = list(unwrap(obj))
        elif isinstance(obj, (Solid, Face, Edge)):
            objs = [obj]
        elif obj is not None:
            raise TypeError(f"Unknown type {obj}")

        if obj is None:
            dummy = Solid.make_sphere(1)
            super().__init__(Compound.make_compound([dummy]).wrapped, label=label)
            self.dim = 0
            self.wrapped = None

        elif all([isinstance(obj, (Edge, Wire)) for obj in objs]):
            super().__init__(Compound.make_compound(objs).wrapped, label=label)
            self.dim = 1

        elif all([isinstance(obj, Face) for obj in objs]):
            super().__init__(Compound.make_compound(objs).wrapped, label=label)
            self.dim = 2

        elif all([isinstance(obj, Solid) for obj in objs]):
            super().__init__(Compound.make_compound(objs).wrapped, label=label)
            self.dim = 3
            self.metadata = {}

        else:
            raise RuntimeError(f"{objs} not supported")

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

    def _align(
        self, align: Union[Align, Tuple(Align, Align), Tuple(Align, Align, Align)]
    ) -> AlgCompound:
        if align is not None:
            if isinstance(align, Align):
                align = (align,) * self.dim

            bbox = self.bounding_box()
            align_offset = []
            for i in range(self.dim):
                if align[i] == Align.MIN:
                    align_offset.append(-bbox.min.to_tuple()[i])
                elif align[i] == Align.CENTER:
                    align_offset.append(
                        -(bbox.min.to_tuple()[i] + bbox.max.to_tuple()[i]) / 2
                    )
                elif align[i] == Align.MAX:
                    align_offset.append(-bbox.max.to_tuple()[i])
            self.move(Location(Vector(*align_offset)))

    def create_line(self, cls, objects=None, params=None):
        result = self._create(bd.BuildLine, cls, objects=objects, params=params)
        return Compound.make_compound(result.edges())

    def create_sketch(self, cls, objects=None, params=None):
        return self._create(bd.BuildSketch, cls, objects=objects, params=params)

    def create_part(self, cls, part=None, params=None):
        return self._create(bd.BuildPart, cls, part=part, params=params)

    def _place(self, mode: Mode, *objs: AlgCompound):
        objs = [o if isinstance(o, AlgCompound) else AlgCompound(o) for o in objs]

        if not (objs[0].dim == 0 or self.dim == 0 or self.dim == objs[0].dim):
            raise RuntimeError(
                f"Cannot combine objects of different dimensionality: {self.dim} and {objs[0].dim}"
            )

        if self.dim == 0:  # Cover addition of empty AlgCompound with another object
            if mode == Mode.ADD:
                if len(objs) == 1:
                    compound = copy.deepcopy(objs[0])
                else:
                    compound = copy.deepcopy(objs.pop()).fuse(*objs)
            else:
                raise RuntimeError("Can only add to an empty AlgCompound object")
        elif objs[0].dim == 0:  # Cover operation with empty AlgCompound object
            compound = self
        else:
            if mode == Mode.ADD:
                compound = self.fuse(*objs)

            elif self.dim == 1:
                raise RuntimeError("Lines can only be added")

            else:
                if mode == Mode.SUBTRACT:
                    compound = self.cut(*objs)
                elif mode == Mode.INTERSECT:
                    compound = self.intersect(*objs)

        if SkipClean.clean:
            compound = compound.clean()

        return AlgCompound(compound)

    def __add__(self, other: Union[AlgCompound, List[AlgCompound]]):
        return self._place(Mode.ADD, *to_list(other))

    def __sub__(self, other: Union[AlgCompound, List[AlgCompound]]):
        return self._place(Mode.SUBTRACT, *to_list(other))

    def __and__(self, other: Union[AlgCompound, List[AlgCompound]]):
        return self._place(Mode.INTERSECT, *to_list(other))

    def __mul__(self, loc: Location):
        if self.dim == 3:
            return copy.copy(self).move(loc)
        else:
            return self.moved(loc)

    def __matmul__(self, obj: Union[float, Location]):
        if isinstance(obj, (int, float)):
            if self.dim == 1:
                return Wire.make_wire(self.edges()).position_at(obj)
            else:
                raise TypeError("Only lines can access positions")

        elif isinstance(obj, Location):
            loc = obj

        elif isinstance(obj, Plane):
            loc = obj.location

        else:
            raise ValueError(f"Cannot multiply with {obj}")

        if self.dim == 3:
            return copy.copy(self).locate(loc)
        else:
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

    def edge(self) -> Edge:
        if self.dim == 1:
            if len(self.edges()) == 1:
                return self.edges()[0]
            else:
                raise RuntimeError("Line has more than 1 edge")
        else:
            raise RuntimeError("edge() exists for dim==1 only")

    def wire(self) -> Wire:
        if self.dim == 1:
            return Wire.combine(self.edges())[0]
        else:
            raise RuntimeError("wire() exists for dim==1 only")

    def face(self) -> Face:
        if self.dim == 2:
            if len(self.faces()) == 1:
                return self.faces()[0]
            else:
                raise RuntimeError("Sketch has more than 1 face")
        else:
            raise RuntimeError("face() exists for dim==2 only")

    def solid(self) -> Solid:
        if self.dim == 3:
            if len(self.solids()) == 1:
                return self.solids()[0]
            else:
                raise RuntimeError("Part has more than 1 solid")
        else:
            raise RuntimeError("solid() exists for dim==3 only")


#
# Function wrapper
#


def create_compound(
    cls, objects=None, part=None, dim=None, faces=None, planes=None, params=None
) -> AlgCompound:
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
        result = AlgCompound(solids[0].fuse(*solids[1:]))
    else:
        result = AlgCompound(compound)

    if SkipClean.clean:
        return result.clean()
    else:
        return result


#
# LazyCompound
#


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
