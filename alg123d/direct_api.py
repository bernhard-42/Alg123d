from typing import overload, List
from OCP.gp import gp_Pln  # pyright: ignore[reportMissingImports]
import build123d as bd


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


def front_faces(c: bd.Compound) -> bd.ShapeList:
    """Front face"""
    return c.faces().group_by(bd.Axis.Y)[0]


def back_faces(c: bd.Compound) -> bd.ShapeList:
    """Back face"""
    return c.faces().group_by(bd.Axis.Y)[-1]


def left_faces(c: bd.Compound) -> bd.ShapeList:
    """Left face"""
    return c.faces().group_by(bd.Axis.X)[0]


def right_faces(c: bd.Compound) -> bd.ShapeList:
    """Right face"""
    return c.faces().group_by(bd.Axis.X)[-1]


def top_faces(c: bd.Compound) -> bd.ShapeList:
    """Top face"""
    return c.faces().group_by(bd.Axis.Z)[-1]


def bottom_faces(c: bd.Compound) -> bd.Face:
    """Bottom face"""
    return c.faces().group_by(bd.Axis.Z)[0]


def front_face(c: bd.Compound) -> bd.Face:
    """Front face"""
    return c.faces().sort_by(bd.Axis.Y)[0]


def back_face(c: bd.Compound) -> bd.Face:
    """Back face"""
    return c.faces().sort_by(bd.Axis.Y)[-1]


def left_face(c: bd.Compound) -> bd.Face:
    """Left face"""
    return c.faces().sort_by(bd.Axis.X)[0]


def right_face(c: bd.Compound) -> bd.Face:
    """Right face"""
    return c.faces().sort_by(bd.Axis.X)[-1]


def top_face(c: bd.Compound) -> bd.Face:
    """Top face"""
    return c.faces().sort_by(bd.Axis.Z)[-1]


def bottom_face(c: bd.Compound) -> bd.Face:
    """Bottom face"""
    return c.faces().sort_by(bd.Axis.Z)[0]


def front_edges(c: bd.Compound) -> bd.ShapeList:
    """Front edges"""
    return c.edges().group_by(bd.Axis.Y)[0]


def back_edges(c: bd.Compound) -> bd.ShapeList:
    """Back edges"""
    return c.edges().group_by(bd.Axis.Y)[-1]


def left_edges(c: bd.Compound) -> bd.ShapeList:
    """Left edges"""
    return c.edges().group_by(bd.Axis.X)[0]


def right_edges(c: bd.Compound) -> bd.ShapeList:
    """Right edges"""
    return c.edges().group_by(bd.Axis.X)[-1]


def top_edges(c: bd.Compound) -> bd.ShapeList:
    """Top edges"""
    return c.edges().group_by(bd.Axis.Z)[-1]


def bottom_edges(c: bd.Compound) -> bd.ShapeList:
    """Bottom edges"""
    return c.edges().group_by(bd.Axis.Z)[0]


def front_planes(c: bd.Compound) -> List[Workplane]:
    """Front workplanes"""
    return [Workplane(f) for f in front_faces(c)]


def back_planes(c: bd.Compound) -> List[Workplane]:
    """Back workplanes"""
    return [Workplane(f) for f in back_faces(c)]


def left_planes(c: bd.Compound) -> List[Workplane]:
    """Left workplanes"""
    return [Workplane(f) for f in left_faces(c)]


def right_planes(c: bd.Compound) -> List[Workplane]:
    """Right workplanes"""
    return [Workplane(f) for f in right_faces(c)]


def top_planes(c: bd.Compound) -> List[Workplane]:
    """Top workplanes"""
    return [Workplane(f) for f in top_faces(c)]


def bottom_planes(c: bd.Compound) -> List[Workplane]:
    """Bottom workplanes"""
    return [Workplane(f) for f in bottom_faces(c)]


def front_plane(c: bd.Compound) -> Workplane:
    """Front workplanes"""
    return Workplane(front_face(c))


def back_plane(c: bd.Compound) -> Workplane:
    """Back workplanes"""
    return Workplane(back_face(c))


def left_plane(c: bd.Compound) -> Workplane:
    """Left workplanes"""
    return Workplane(left_face(c))


def right_plane(c: bd.Compound) -> Workplane:
    """Right workplanes"""
    return Workplane(right_face(c))


def top_plane(c: bd.Compound) -> Workplane:
    """Top workplanes"""
    return Workplane(top_face(c))


def bottom_plane(c: bd.Compound) -> Workplane:
    """Bottom workplanes"""
    return Workplane(bottom_face(c))
