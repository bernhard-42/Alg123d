from typing import Union, List, overload
from dataclasses import dataclass

import build123d as bd
from cq_vscode import show

# from .common import Workplane

CadObj1d = Union[bd.Wire, bd.Edge, bd.Compound]
CadObj2d = Union[bd.Face, bd.Compound]
CadObj3d = Union[bd.Solid, bd.Compound]
CadObj23d = Union[bd.Solid, bd.Face, bd.Compound]

# %%


@dataclass
class Task:
    obj: Union[CadObj2d, CadObj3d]
    loc: bd.Location
    mode: bd.Mode

    def __init__(self, obj: Union[CadObj2d, CadObj3d], loc: bd.Location, mode: bd.Mode):
        self.obj = {"name": obj.__class__.__name__}
        for name in obj.__dataclass_fields__:
            self.obj[name] = getattr(obj, name)
        self.loc = loc.to_tuple()
        self.mode = mode


# %%


class OperatorCompound(bd.Compound):
    def __init__(self, compound=None, tasks=None):
        self.tasks: List[Task] = [] if tasks is None else tasks
        self.wrapped = compound.wrapped

    def _place(
        self,
        mode: bd.Mode,
        obj: CadObj23d,
        at: bd.Location = None,
    ):
        if at is None:
            loc = obj.location
        elif isinstance(at, bd.Location):
            loc = at
        # elif isinstance(at, Workplane):
        #     loc = at.to_location()
        elif isinstance(at, tuple):
            loc = bd.Location(at)
        else:
            raise ValueError(f"{at } is no location orm plane")

        located_obj = obj.located(loc)

        compound = self.copy()

        if mode == bd.Mode.ADD:
            compound = compound.fuse(located_obj)
        elif mode == bd.Mode.SUBTRACT:
            compound = compound.cut(located_obj)

        tasks = self.tasks.copy()
        tasks.append(Task(obj, loc, mode))

        return OperatorCompound(compound, tasks)

    def __add__(self, other: CadObj23d):
        return self._place(bd.Mode.ADD, other)

    def __sub__(self, other: CadObj23d):
        return self._place(bd.Mode.SUBTRACT, other)

    def __and__(self, other: CadObj23d):
        return self._place(bd.Mode.INTERSECT, other)

    def __matmul__(self, obj):
        if isinstance(obj, bd.Location):
            loc = obj
        elif isinstance(obj, tuple):
            loc = bd.Location(obj)
        # elif isinstance(obj, Workplane):
        #     loc = obj.to_location()
        else:
            raise ValueError(f"Cannot multiply with {obj}")

        return self.located(loc)

    def __repr__(self):
        return "Sketch(\n" + "\n".join(["    " + str(t) for t in self.tasks]) + "\n)"

# %%


@dataclass
class Box(OperatorCompound):
    length: float
    width: float
    height: float
    centered: tuple[bool, bool, bool]

    def __init__(
        self,
        length: float,
        width: float,
        height: float,
        centered: tuple[bool, bool, bool] = (True, True, True),
    ):
        self.length = length
        self.width = width
        self.height = height
        self.centered = centered

        with bd.BuildPart():
            with bd.Locations(bd.Location()):
                self.wrapped = bd.Box(
                    length, width, height, centered=centered, mode=bd.Mode.PRIVATE
                ).wrapped

        self.tasks = [Task(self, self.location, bd.Mode.ADD)]


@dataclass
class Cylinder(OperatorCompound):
    radius: float
    height: float
    arc_size: float
    centered: tuple[bool, bool, bool]

    def __init__(
        self,
        radius: float,
        height: float,
        arc_size: float = 360,
        centered: tuple[bool, bool, bool] = (True, True, True),
    ):
        self.radius = radius
        self.height = height
        self.arc_size = arc_size
        self.centered = centered

        with bd.BuildPart():
            with bd.Locations(bd.Location()):
                self.wrapped = bd.Cylinder(
                    radius, height, arc_size, centered=centered, mode=bd.Mode.PRIVATE
                ).wrapped

        self.tasks = [Task(self, self.location, bd.Mode.ADD)]



# %%

b1 = Box(1, 1, 1) 
c = Cylinder(0.1, 3) 
b2 = Box(0.1, 2, 0.1)

d = b1 + c - b2

# %%
