from typing import List
import build123d as bd
from .wrappers import AlgCompound, create_compound
from .direct_api import *
from .generic import tupleize

__all__ = [
    "Empty3",
    "Box",
    "Cylinder",
    "Cone",
    "Sphere",
    "Torus",
    "Wedge",
    "CounterBore",
    "CounterSink",
    "Bore",
    "extrude",
    "loft",
    "revolve",
    "sweep",
    "section",
]


class Empty3(AlgCompound):
    def __init__(self):
        super().__init__(dim=3)


class Box(AlgCompound):
    def __init__(
        self,
        length: float,
        width: float,
        height: float,
        centered: tuple[bool, bool, bool] = (True, True, True),
    ):
        params = dict(
            length=length,
            width=width,
            height=height,
            centered=centered,
        )
        self.create_part(bd.Box, params=params)


class Cylinder(AlgCompound):
    def __init__(
        self,
        radius: float,
        height: float,
        arc_size: float = 360,
        centered: tuple[bool, bool, bool] = (True, True, True),
    ):
        params = dict(
            radius=radius,
            height=height,
            arc_size=arc_size,
            centered=centered,
        )
        self.create_part(bd.Cylinder, params=params)


class Cone(AlgCompound):
    def __init__(
        self,
        bottom_radius: float,
        top_radius: float,
        height: float,
        arc_size: float = 360,
        centered: tuple[bool, bool, bool] = (True, True, True),
    ):
        params = dict(
            bottom_radius=bottom_radius,
            top_radius=top_radius,
            height=height,
            arc_size=arc_size,
            centered=centered,
        )
        self.create_part(bd.Cone, params=params)


class Sphere(AlgCompound):
    def __init__(
        self,
        radius: float,
        arc_size1: float = -90,
        arc_size2: float = 90,
        arc_size3: float = 360,
        centered: tuple[bool, bool, bool] = (True, True, True),
    ):
        params = dict(
            radius=radius,
            arc_size1=arc_size1,
            arc_size2=arc_size2,
            arc_size3=arc_size3,
            centered=centered,
        )
        self.create_part(bd.Sphere, params=params)


class Torus(AlgCompound):
    def __init__(
        self,
        major_radius: float,
        minor_radius: float,
        minor_start_angle: float = 0,
        minor_end_angle: float = 360,
        major_angle: float = 360,
        centered: tuple[bool, bool, bool] = (True, True, True),
    ):
        params = dict(
            major_radius=major_radius,
            minor_radius=minor_radius,
            minor_start_angle=minor_start_angle,
            minor_end_angle=minor_end_angle,
            major_angle=major_angle,
            centered=centered,
        )
        self.create_part(bd.Torus, params=params)


class Wedge(AlgCompound):
    def __init__(
        self,
        dx: float,
        dy: float,
        dz: float,
        xmin: float,
        zmin: float,
        xmax: float,
        zmax: float,
    ):
        params = dict(
            dx=dx,
            dy=dy,
            dz=dz,
            xmin=xmin,
            zmin=zmin,
            xmax=xmax,
            zmax=zmax,
        )
        self.create_part(bd.Wedge, params=params)


class CounterBore(AlgCompound):
    def __init__(
        self,
        part: AlgCompound,
        radius: float,
        counter_bore_radius: float,
        counter_bore_depth: float,
        depth: float = None,
    ):
        params = dict(
            radius=radius,
            counter_bore_radius=counter_bore_radius,
            counter_bore_depth=counter_bore_depth,
            depth=depth,
        )
        self.create_part(bd.CounterBoreHole, part, params=params)


class CounterSink(AlgCompound):
    def __init__(
        self,
        part: AlgCompound,
        radius: float,
        counter_sink_radius: float,
        counter_sink_angle: float = 82,
        depth: float = None,
    ):
        params = dict(
            radius=radius,
            counter_sink_radius=counter_sink_radius,
            counter_sink_angle=counter_sink_angle,
            depth=depth,
        )
        self.create_part(bd.CounterSinkHole, part, params=params)


class Bore(AlgCompound):
    def __init__(
        self,
        part: AlgCompound,
        radius: float,
        depth: float = None,
    ):
        params = dict(
            radius=radius,
            depth=depth,
        )
        self.create_part(bd.Hole, part, params=params)


#
# Functions
#


def extrude(
    to_extrude: Compound,
    amount: float = None,
    until: Until = None,
    until_part: Compound = None,
    both: bool = False,
    taper: float = 0.0,
):
    with bd.BuildPart() as ctx:
        # store to_extrude's faces in context
        ctx.pending_faces = (
            [to_extrude] if isinstance(to_extrude, Face) else to_extrude.faces()
        )
        ctx.pending_face_planes = [Plane(face.to_pln()) for face in ctx.pending_faces]

        if len(ctx.pending_faces) == 0:
            raise RuntimeError(f"No faces found in {to_extrude}")

        if until_part is not None:
            ctx._add_to_context(until_part)

        compound = bd.Extrude(
            amount=amount,
            until=until,
            both=both,
            taper=taper,
            mode=Mode.PRIVATE,
        )

    return AlgCompound(compound, {}, 3)


def loft(sections: List[AlgCompound | Face], ruled: bool = False):
    faces = []
    for s in tupleize(sections):
        if isinstance(s, Compound):
            faces += s.faces()
        else:
            faces.append(s)

    return create_compound(bd.Loft, faces, dim=3, params=dict(ruled=ruled))


def revolve(
    profiles: List[Compound | Face] | Compound | Face,
    axis: Axis,
    arc: float = 360.0,
):
    for p in tupleize(profiles):
        faces = []
        if isinstance(p, Compound):
            faces += p.faces()
        else:
            faces.append(p)

    return create_compound(
        bd.Revolve, faces, dim=3, params=dict(axis=axis, revolution_arc=arc)
    )


def sweep(
    sections: List[Face | Compound],
    path: Edge | Wire = None,
    multisection: bool = False,
    is_frenet: bool = False,
    transition: Transition = Transition.TRANSFORMED,
    normal: VectorLike = None,
    binormal: Edge | Wire = None,
):
    return create_compound(
        bd.Sweep,
        sections,
        params=dict(
            path=path,
            multisection=multisection,
            is_frenet=is_frenet,
            transition=transition,
            normal=normal,
            binormal=binormal,
        ),
    )


def section(
    part: AlgCompound,
    by: List[Workplane],
    height: float = 0.0,
):
    return create_compound(
        bd.Section, by, part=part, params=dict(height=height, mode=Mode.INTERSECT)
    )
