from typing import Union, List, overload
from dataclasses import dataclass

import build123d as bd
from OCP.gp import gp_Pln

CadObj1d = Union[bd.Wire, bd.Edge, bd.Compound]
CadObj2d = Union[bd.Face, bd.Compound]
CadObj3d = Union[bd.Solid, bd.Compound]
CadObj23d = Union[bd.Solid, bd.Face, bd.Compound]


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


class Workplane(bd.Plane):
    @classmethod
    @property
    def XY(cls) -> "Workplane":
        """XY Plane"""
        return cls((0, 0, 0), (1, 0, 0), (0, 0, 1))

    @classmethod
    @property
    def YZ(cls) -> "Workplane":
        """YZ Plane"""
        return cls((0, 0, 0), (0, 1, 0), (1, 0, 0))

    @classmethod
    @property
    def ZX(cls) -> "Workplane":
        """ZX Plane"""
        return cls((0, 0, 0), (0, 0, 1), (0, 1, 0))

    @classmethod
    @property
    def XZ(cls) -> "Workplane":
        """XZ Plane"""
        return cls((0, 0, 0), (1, 0, 0), (0, -1, 0))

    @classmethod
    @property
    def YX(cls) -> "Workplane":
        """YX Plane"""
        return cls((0, 0, 0), (0, 1, 0), (0, 0, -1))

    @classmethod
    @property
    def ZY(cls) -> "Workplane":
        """ZY Plane"""
        return cls((0, 0, 0), (0, 0, 1), (-1, 0, 0))

    @classmethod
    @property
    def front(cls) -> "Workplane":
        """Front Plane"""
        return cls((0, 0, 0), (1, 0, 0), (0, 0, 1))

    @classmethod
    @property
    def back(cls) -> "Workplane":
        """Back Plane"""
        return cls((0, 0, 0), (-1, 0, 0), (0, 0, -1))

    @classmethod
    @property
    def left(cls) -> "Workplane":
        """Left Plane"""
        return cls((0, 0, 0), (0, 0, 1), (-1, 0, 0))

    @classmethod
    @property
    def right(cls) -> "Workplane":
        """Right Plane"""
        return cls((0, 0, 0), (0, 0, -1), (1, 0, 0))

    @classmethod
    @property
    def top(cls) -> "Workplane":
        """Top Plane"""
        return cls((0, 0, 0), (1, 0, 0), (0, 1, 0))

    @classmethod
    @property
    def bottom(cls) -> "Workplane":
        """Bottom Plane"""
        return cls((0, 0, 0), (1, 0, 0), (0, -1, 0))

    @overload
    def __init__(self, gp_pln: gp_Pln):  # pragma: no cover
        ...

    @overload
    def __init__(self, face: bd.Face):  # pragma: no cover
        ...

    @overload
    def __init__(self, plane: bd.Plane):  # pragma: no cover
        ...

    @overload
    def __init__(self, plane: bd.Plane):  # pragma: no cover
        ...

    def __init__(self, *args, **kwargs):
        """Create a plane from either an OCCT gp_pln or coordinates"""
        if isinstance(args[0], bd.Plane):
            p = args[0]
            super().__init__(p.origin, p.x_dir, p.y_dir)

        elif isinstance(args[0], (bd.Face, bd.Location)):
            if isinstance(args[0], bd.Face):
                face = args[0]
                origin = face.center()
            else:
                face = bd.Face.make_rect(1, 1).move(args[0])
                origin = args[0].position

            x_dir = bd.Vector(face._geom_adaptor().Position().XDirection())
            z_dir = face.normal_at(origin)

            super().__init__(origin=origin, x_dir=x_dir, z_dir=z_dir)

        else:
            super().__init__(*args, **kwargs)

    def __repr__(self):
        """To String

        Convert Plane to String for display

        Returns:
            Plane as String
        """
        origin_str = ", ".join((f"{v:.2f}" for v in self._origin.to_tuple()))
        x_dir_str = ", ".join((f"{v:.2f}" for v in self.x_dir.to_tuple()))
        z_dir_str = ", ".join((f"{v:.2f}" for v in self.z_dir.to_tuple()))
        return f"Workplane(o=({origin_str}), x=({x_dir_str}), z=({z_dir_str}))"

    def __mul__(self, loc) -> "Workplane":
        if not isinstance(loc, bd.Location):
            raise RuntimeError(
                "Planes can only be multiplied with Locations to relocate them"
            )
        return Workplane(self.to_location() * loc)


class OperatorCompound(bd.Compound):
    def __init__(self, compound=None, tasks=None):
        self.tasks: List[Task] = [] if tasks is None else tasks
        self.wrapped = None if compound is None else compound.wrapped

    def _params(self, exclude):
        # get the paramter dict from the data class
        params = {
            k: v for k, v in self.__dict__.items() if k in self.__dataclass_fields__
        }
        for ex in exclude:
            del params[ex]
        return params

    def create_context_and_part(self, cls, exclude=[]):
        with bd.BuildPart():
            self.create_part(cls, exclude)

    def create_part(self, cls, exclude=[]):
        with bd.Locations(bd.Location()):
            self.wrapped = cls(**self._params(exclude), mode=bd.Mode.PRIVATE).wrapped

        self._applies_to = cls._applies_to
        self.tasks = [Task(self, self.location, bd.Mode.ADD)]

    def create_context_and_sketch(self, cls, exclude=[]):
        with bd.BuildSketch():
            self.wrapped = cls(**self._params(exclude), mode=bd.Mode.PRIVATE).wrapped

        self._applies_to = bd.Circle._applies_to
        self.tasks = [Task(self, self.location, bd.Mode.ADD)]

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
        elif isinstance(at, Workplane):
            loc = at.to_location()
        elif isinstance(at, tuple):
            loc = bd.Location(at)
        else:
            raise ValueError(f"{at } is no location orm plane")

        located_obj = obj.located(loc)

        if self.wrapped is None:
            if mode == bd.Mode.ADD:
                compound = located_obj
            else:
                raise RuntimeError("Can only add to empty object")
        else:
            compound = self.copy()
            if mode == bd.Mode.ADD:
                compound = compound.fuse(located_obj)
            elif mode == bd.Mode.SUBTRACT:
                compound = compound.cut(located_obj)
            elif mode == bd.Mode.INTERSECT:
                compound = compound.intersect(located_obj)

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
        elif isinstance(obj, Workplane):
            loc = obj.to_location()
        else:
            raise ValueError(f"Cannot multiply with {obj}")

        return self.located(loc)

    def __repr__(self):
        return "Sketch(\n" + "\n".join(["    " + str(t) for t in self.tasks]) + "\n)"


class Empty(OperatorCompound):
    def __init__(self):
        self.wrapped = None
        self.tasks = []


class Locations(bd.Locations):
    def __init__(self, *pts: Union[bd.VectorLike, bd.Vertex, bd.Location]):
        super().__init__(*pts)
        del self.plane_index

    def __enter__(self):
        raise RuntimeError("No context!")

    def __exit__(self):
        raise RuntimeError("No context!")


class PolarLocations(bd.PolarLocations):
    def __init__(
        self,
        radius: float,
        count: int,
        start_angle: float = 0.0,
        stop_angle: float = 360.0,
        rotate: bool = True,
    ):
        super().__init__(radius, count, start_angle, stop_angle, rotate)
        del self.plane_index

    def __enter__(self):
        raise RuntimeError("No context!")

    def __exit__(self):
        raise RuntimeError("No context!")


class GridLocations(bd.GridLocations):
    def __init__(
        self,
        x_spacing: float,
        y_spacing: float,
        x_count: int,
        y_count: int,
        centered: tuple[bool, bool] = (True, True),
    ):
        super().__init__(x_spacing, y_spacing, x_count, y_count, centered)
        del self.plane_index

    def __enter__(self):
        raise RuntimeError("No context!")

    def __exit__(self):
        raise RuntimeError("No context!")
