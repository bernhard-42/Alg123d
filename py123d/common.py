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


class Build:
    def __init__(self, obj=None, tasks=None):
        self.tasks: List[Task] = [] if tasks is None else tasks
        self.obj: bd.Compound = obj

    def _place(
        self,
        mode: bd.Mode,
        obj: CadObj23d,
        on: bd.Plane = None,
        at: bd.Location = None,
        combine=True,
    ):
        if at is None:
            loc = obj.location
        elif isinstance(at, bd.Location):
            loc = at
        else:
            loc = bd.Location(at)

        if on is not None:
            loc = on.to_location() * loc

        new_obj = obj.located(loc)

        if combine:
            new_build = self
        else:
            new_build = Build(
                None if self.obj is None else self.obj.copy(), self.tasks.copy()
            )

        new_build.tasks.append(Task(obj, loc, mode))

        if mode == bd.Mode.ADD:
            if new_build.obj == None:
                new_build.obj = bd.Compound.make_compound([new_obj])
            else:
                new_build.obj = new_build.obj.fuse(new_obj)

        elif mode == bd.Mode.SUBTRACT:
            if new_build.obj is None:
                raise RuntimeError("Connect cut obj from None")

            new_build.obj = new_build.obj.cut(new_obj)

        return new_build

    def add(
        self, obj: CadObj23d, on: bd.Plane = None, at: bd.Location = None, combine=True
    ):
        return self._place(bd.Mode.ADD, obj, on=on, at=at, combine=combine)

    def subtract(
        self, obj: CadObj23d, on: bd.Plane = None, at: bd.Location = None, combine=True
    ):
        return self._place(bd.Mode.SUBTRACT, obj, on=on, at=at, combine=combine)

    def intersect(
        self, obj: CadObj23d, on: bd.Plane = None, at: bd.Location = None, combine=True
    ):
        return self._place(bd.Mode.INTERSECT, obj, on=on, at=at, combine=combine)

    def __add__(self, other: CadObj23d):
        return self.add(other, combine=False)

    def __sub__(self, other: CadObj23d):
        return self.subtract(other, combine=False)

    def __and__(self, other: CadObj23d):
        return self.intersect(other, combine=False)


class Mixin:
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
