from typing import overload, List, Optional
from OCP.gp import gp_Pln  # pyright: ignore[reportMissingImports]
from build123d.direct_api import *
from build123d.build_enums import *


class Workplane(Plane):
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
    def __init__(self, face: Face):  # pragma: no cover
        ...

    @overload
    def __init__(self, plane: Plane):  # pragma: no cover
        ...

    @overload
    def __init__(self, plane: Plane):  # pragma: no cover
        ...

    def __init__(self, *args, **kwargs):
        """Create a plane from either an OCCT gp_pln or coordinates"""
        if isinstance(args[0], Plane):
            p = args[0]
            super().__init__(p.origin, p.x_dir, p.y_dir)

        elif isinstance(args[0], (Face, Location)):
            if isinstance(args[0], Face):
                face = args[0]
                origin = face.center()
            else:
                face = Face.make_rect(1, 1).move(args[0])
                origin = args[0].position

            x_dir = Vector(face._geom_adaptor().Position().XDirection())
            z_dir = face.normal_at(origin)

            super().__init__(origin=origin, x_dir=x_dir, z_dir=z_dir)

        elif isinstance(args[0], Compound) and hasattr(args[0], "location"):
            self.__init__(args[0].location)

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
        if not isinstance(loc, Location):
            raise RuntimeError(
                "Planes can only be multiplied with Locations to relocate them"
            )
        return Workplane(self.to_location() * loc)


def front_faces(c: Compound) -> ShapeList:
    """Front face"""
    return c.faces().group_by(Axis.Y)[0]


def back_faces(c: Compound) -> ShapeList:
    """Back face"""
    return c.faces().group_by(Axis.Y)[-1]


def left_faces(c: Compound) -> ShapeList:
    """Left face"""
    return c.faces().group_by(Axis.X)[0]


def right_faces(c: Compound) -> ShapeList:
    """Right face"""
    return c.faces().group_by(Axis.X)[-1]


def top_faces(c: Compound) -> ShapeList:
    """Top face"""
    return c.faces().group_by(Axis.Z)[-1]


def bottom_faces(c: Compound) -> Face:
    """Bottom face"""
    return c.faces().group_by(Axis.Z)[0]


def front_face(c: Compound) -> Face:
    """Front face"""
    return c.faces().sort_by(Axis.Y)[0]


def back_face(c: Compound) -> Face:
    """Back face"""
    return c.faces().sort_by(Axis.Y)[-1]


def left_face(c: Compound) -> Face:
    """Left face"""
    return c.faces().sort_by(Axis.X)[0]


def right_face(c: Compound) -> Face:
    """Right face"""
    return c.faces().sort_by(Axis.X)[-1]


def top_face(c: Compound) -> Face:
    """Top face"""
    return c.faces().sort_by(Axis.Z)[-1]


def bottom_face(c: Compound) -> Face:
    """Bottom face"""
    return c.faces().sort_by(Axis.Z)[0]


def front_edges(c: Compound) -> ShapeList:
    """Front edges"""
    return c.edges().group_by(Axis.Y)[0]


def back_edges(c: Compound) -> ShapeList:
    """Back edges"""
    return c.edges().group_by(Axis.Y)[-1]


def left_edges(c: Compound) -> ShapeList:
    """Left edges"""
    return c.edges().group_by(Axis.X)[0]


def right_edges(c: Compound) -> ShapeList:
    """Right edges"""
    return c.edges().group_by(Axis.X)[-1]


def top_edges(c: Compound) -> ShapeList:
    """Top edges"""
    return c.edges().group_by(Axis.Z)[-1]


def bottom_edges(c: Compound) -> ShapeList:
    """Bottom edges"""
    return c.edges().group_by(Axis.Z)[0]


def front_planes(c: Compound) -> List[Workplane]:
    """Front workplanes"""
    return [Workplane(f) for f in front_faces(c)]


def back_planes(c: Compound) -> List[Workplane]:
    """Back workplanes"""
    return [Workplane(f) for f in back_faces(c)]


def left_planes(c: Compound) -> List[Workplane]:
    """Left workplanes"""
    return [Workplane(f) for f in left_faces(c)]


def right_planes(c: Compound) -> List[Workplane]:
    """Right workplanes"""
    return [Workplane(f) for f in right_faces(c)]


def top_planes(c: Compound) -> List[Workplane]:
    """Top workplanes"""
    return [Workplane(f) for f in top_faces(c)]


def bottom_planes(c: Compound) -> List[Workplane]:
    """Bottom workplanes"""
    return [Workplane(f) for f in bottom_faces(c)]


def front_plane(c: Compound) -> Workplane:
    """Front workplanes"""
    return Workplane(front_face(c))


def back_plane(c: Compound) -> Workplane:
    """Back workplanes"""
    return Workplane(back_face(c))


def left_plane(c: Compound) -> Workplane:
    """Left workplanes"""
    return Workplane(left_face(c))


def right_plane(c: Compound) -> Workplane:
    """Right workplanes"""
    return Workplane(right_face(c))


def top_plane(c: Compound) -> Workplane:
    """Top workplanes"""
    return Workplane(top_face(c))


def bottom_plane(c: Compound) -> Workplane:
    """Bottom workplanes"""
    return Workplane(bottom_face(c))


def _extrude(
    faces: List[Face],
    amount: Optional[float] = None,
    z_dir: Vector = None,
    both: bool = False,
    taper: Optional[float] = None,
    up_to: Optional[Compound | Face] = None,
    up_to_index: Optional[int] = None,
) -> Solid | Compound:
    def get_faces(face, eDir, direction, both=False):
        """
        Utility function to make the code further below more clean and tidy
        Performs some test and raise appropriate error when no Faces are found for extrusion
        """
        facesList = self.findSolid().facesIntersectedByLine(
            face.Center(), eDir, direction=direction
        )
        if len(facesList) == 0 and both:
            raise ValueError(
                "Couldn't find a face to extrude/cut to for at least one of the two required directions of extrusion/cut."
            )

        if len(facesList) == 0:
            # if we don't find faces in the workplane normal direction we try the other
            # direction (as the user might have created a workplane with wrong orientation)
            facesList = self.findSolid().facesIntersectedByLine(
                face.Center(), eDir.multiply(-1.0), direction=direction
            )
            if len(facesList) == 0:
                raise ValueError(
                    "Couldn't find a face to extrude/cut to. Check your workplane orientation."
                )
        return facesList

    # check for nested geometry and tapered extrusion
    for face in faces:
        if taper and face.inner_wires():
            raise ValueError("Inner wires not allowed with tapered extrusion")

    taper = 0.0 if taper is None else taper

    # compute extrusion vector and extrude
    if z_dir is None:
        if isinstance(up_to, Face):
            e_dir = Workplane(up_to).z_dir
        else:
            e_dir = Workplane(up_to.location).z_dir
    else:
        e_dir = z_dir.normalized()

    if amount is not None:
        e_dir = e_dir.multiply(amount)

    to_fuse = []

    if up_to is not None:
        res: Solid = up_to.solids()[0]
        for face in faces:
            if isinstance(up_to, Compound):
                face_list = get_faces(face, e_dir, "AlongAxis", both=both)
                if res.isInside(face.outer_wire().center()) and up_to_index == 0:
                    up_to_index = 1  # extrude until next face outside the solid

                limit_face = face_list[up_to_index]
            else:
                limit_face = up_to

            res = res.dprism(None, [face], taper=taper, up_to_face=limit_face)

            if both:
                face_list2 = get_faces(
                    face, e_dir.multiply(-1.0), "AlongAxis", both=both
                )
                if res.isInside(face.outer_wire().center()) and up_to_index == 0:
                    up_to_index = 1  # extrude until next face outside the solid

                limit_face2 = face_list2[up_to_index]
                res = res.dprism(
                    None,
                    [face],
                    taper=taper,
                    up_to_face=limit_face2,
                )

    else:
        for face in faces:
            res = Solid.extrude_linear(face, e_dir, taper=taper)
            to_fuse.append(res)

            if both:
                res = Solid.extrude_linear(face, e_dir.multiply(-1.0), taper=taper)
                to_fuse.append(res)

    return res if up_to is not None else Compound.makeCompound(to_fuse)


def extrude(
    objs: List[Face | Compound] | Face | Compound,
    until: int | float | Until,
    up_to: Face | Compound = None,
    both: bool = False,
    taper: Optional[float] = None,
    z_dir: Vector = None,
) -> Compound:

    faces = objs.faces() if isinstance(objs, Compound) else objs

    if isinstance(until, Until) and isinstance(up_to, Compound):
        face_index = 0 if until == Until.NEXT else 1
        r = _extrude(
            faces,
            None,
            z_dir=z_dir,
            both=both,
            taper=taper,
            up_to=up_to,
            up_to_index=face_index,
        )

    elif isinstance(up_to, Face):
        r = _extrude(faces, None, z_dir=z_dir, both=both, taper=taper, up_to=up_to)

    elif isinstance(until, (int, float)):
        r = _extrude(faces, until, both=both, taper=taper)

    else:
        raise ValueError(
            f"Do not know how to handle combination of until type {type(until)} and up_to {type(up_to)}"
        )

    return Compound(r, 3)
