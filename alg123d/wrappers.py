import copy
from typing import List
from dataclasses import dataclass

import build123d as bd
from .direct_api import Workplane

from OCP.BRepBuilderAPI import (  # pyright: ignore[reportMissingImports]
    BRepBuilderAPI_Copy,
)

Obj1d = bd.Compound | bd.Wire | bd.Edge
Obj2d = bd.Compound | bd.Face
Obj3d = bd.Compound | bd.Solid
Obj12d = Obj1d | Obj2d
Obj23d = Obj2d | Obj3d
Obj123d = Obj1d | Obj2d | Obj3d

CTX = [None, bd.BuildLine, bd.BuildSketch, bd.BuildPart]

__all__ = [
    "AlgCompound",
    "_function_wrap",
]

#
# Tracking class
#


@dataclass
class Step:
    obj: Obj23d
    loc: bd.Location
    mode: bd.Mode

    def __init__(self, obj: Obj2d | Obj3d, loc: bd.Location, mode: bd.Mode):
        self.obj = {"name": obj.__class__.__name__}
        if hasattr(obj, "__dataclass_fields__"):
            for name in obj.__dataclass_fields__:
                self.obj[name] = getattr(obj, name)
        self.loc = loc.to_tuple()
        self.mode = "" if mode is None else mode.name


#
# Algebra operations enhanced Compound
#


class AlgCompound(bd.Compound):
    def __init__(self, compound=None, steps=None, dim: int = None):
        self.steps: List[Obj123d] = [] if steps is None else steps
        self.wrapped = None if compound is None else compound.wrapped
        self.dim = dim

    def _params(self, exclude):
        # get the paramter dict from the data class
        params = {
            k: v for k, v in self.__dict__.items() if k in self.__dataclass_fields__
        }
        for ex in exclude:
            del params[ex]
        return params

    def create_part(self, cls, part=None, faces=None, planes=None, exclude=[]):
        with bd.BuildPart() as ctx:
            if part is not None:
                ctx._add_to_context(part)

            if faces is not None:
                ctx.pending_faces = faces

            if planes is not None:
                ctx.pending_face_planes = planes

            self.wrapped = cls(**self._params(exclude), mode=bd.Mode.PRIVATE).wrapped

        # self.steps = []  # [Step(self, self.location, bd.Mode.ADD)]
        # self.dim = 3

    def create_sketch(self, cls, objects=None, exclude=[]):
        with bd.BuildSketch():
            if objects is None:
                self.wrapped = cls(
                    **self._params(exclude), mode=bd.Mode.PRIVATE
                ).wrapped
            else:
                self.wrapped = cls(
                    *objects, **self._params(exclude), mode=bd.Mode.PRIVATE
                ).wrapped

        self.steps = []  # [Step(self, self.location, bd.Mode.ADD)]
        self.dim = 2

    def _place(
        self,
        mode: bd.Mode,
        obj: Obj23d,
        at: bd.Location = None,
    ):
        if at is None:
            located_obj = obj
            loc = obj.location
        else:
            if isinstance(at, bd.Location):
                loc = at
            elif isinstance(at, Workplane):
                loc = at.to_location()
            elif isinstance(at, tuple):
                loc = bd.Location(at)
            else:
                raise ValueError(f"{at } is no location or plane")

            located_obj = obj.located(loc)

        if self.wrapped is None:
            if mode == bd.Mode.ADD:
                compound = located_obj
            else:
                raise RuntimeError("Can only add to empty object")
        else:
            compound = self
            if mode == bd.Mode.ADD:
                compound = compound.fuse(located_obj).clean()
            elif mode == bd.Mode.SUBTRACT:
                compound = compound.cut(located_obj).clean()
            elif mode == bd.Mode.INTERSECT:
                compound = compound.intersect(located_obj).clean()

        # steps = self.steps.copy()
        # steps.append(Step(obj, loc, mode))

        return AlgCompound(compound, [], self.dim)

    def __add__(self, other: Obj23d):
        return self._place(bd.Mode.ADD, other)

    def __sub__(self, other: Obj23d):
        return self._place(bd.Mode.SUBTRACT, other)

    def __and__(self, other: Obj23d):
        return self._place(bd.Mode.INTERSECT, other)

    def __matmul__(self, obj):
        if isinstance(obj, bd.Location):
            loc = obj
        elif isinstance(obj, tuple):
            loc = bd.Location(obj)
        elif isinstance(obj, Workplane):
            loc = obj.to_location()
        else:
            raise ValueError(f"Cannot multiply with {obj}")

        return self.located(loc)

    def __repr__(self):
        repr = "{\n"
        repr += f'  "dim": {self.dim},\n'
        repr += '  "steps": ['
        if len(self.steps) > 0:
            repr += "\n    "
            repr += "\n    ".join([str(task) for task in self.steps])
            repr += "\n  "
        repr += "]\n}"
        return repr

    def copy(self):
        memo = {}
        memo[id(self.wrapped)] = bd.downcast(BRepBuilderAPI_Copy(self.wrapped).Shape())
        for _, value in self.__dict__.items():
            if hasattr(value, "wrapped"):
                memo[id(value.wrapped)] = (
                    bd.downcast(BRepBuilderAPI_Copy(value.wrapped).Shape()),
                )

        return copy.deepcopy(self, memo)


#
# Function wrapper
#


def _function_wrap(cls, objects, ctx_add=None, mode=bd.Mode.PRIVATE, **kwargs):
    objs = objects if isinstance(objects, (list, tuple)) else [objects]

    if ctx_add is None:
        dim = max([o.dim for o in objs])
    else:
        dim = ctx_add.dim

    if mode is not None:
        kwargs["mode"] = mode

    with CTX[dim]() as ctx:
        if ctx_add is not None:
            ctx._add_to_context(bd.Compound(ctx_add.wrapped))
        compound = cls(*objs, **kwargs)

    steps = []  # [Step(compound, compound.location, None)]  # TODO

    return AlgCompound(compound, steps, dim)
