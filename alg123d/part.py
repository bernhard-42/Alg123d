from typing import List

import build123d as bd

from .algcompound import AlgCompound, create_compound
from .topology import *
from .utils import to_tuple

__all__ = [
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
    "extrude_until",
    "loft",
    "revolve",
    "sweep",
    "section",
    "shell",
]

#
# Objects
#


class Box(AlgCompound):
    def __init__(
        self,
        length: float,
        width: float,
        height: float,
        align: Union[Align, tuple[Align, Align, Align]] = (
            Align.CENTER,
            Align.CENTER,
            Align.CENTER,
        ),
    ):
        if isinstance(align, Align):
            align = (align,) * 3

        params = dict(
            length=length,
            width=width,
            height=height,
            align=align,
        )
        super().__init__(self.create_part(bd.Box, params=params))


class Cylinder(AlgCompound):
    def __init__(
        self,
        radius: float,
        height: float,
        arc_size: float = 360,
        align: Union[Align, tuple[Align, Align, Align]] = (
            Align.CENTER,
            Align.CENTER,
            Align.CENTER,
        ),
    ):
        if isinstance(align, Align):
            align = (align,) * 3

        params = dict(
            radius=radius,
            height=height,
            arc_size=arc_size,
            align=align,
        )
        super().__init__(self.create_part(bd.Cylinder, params=params))


class Cone(AlgCompound):
    def __init__(
        self,
        bottom_radius: float,
        top_radius: float,
        height: float,
        arc_size: float = 360,
        align: Union[Align, tuple[Align, Align, Align]] = (
            Align.CENTER,
            Align.CENTER,
            Align.CENTER,
        ),
    ):
        if isinstance(align, Align):
            align = (align,) * 3

        params = dict(
            bottom_radius=bottom_radius,
            top_radius=top_radius,
            height=height,
            arc_size=arc_size,
            align=align,
        )
        super().__init__(self.create_part(bd.Cone, params=params))


class Sphere(AlgCompound):
    def __init__(
        self,
        radius: float,
        arc_size1: float = -90,
        arc_size2: float = 90,
        arc_size3: float = 360,
        align: Union[Align, tuple[Align, Align, Align]] = (
            Align.CENTER,
            Align.CENTER,
            Align.CENTER,
        ),
    ):
        if isinstance(align, Align):
            align = (align,) * 3

        params = dict(
            radius=radius,
            arc_size1=arc_size1,
            arc_size2=arc_size2,
            arc_size3=arc_size3,
            align=align,
        )
        super().__init__(self.create_part(bd.Sphere, params=params))


class Torus(AlgCompound):
    def __init__(
        self,
        major_radius: float,
        minor_radius: float,
        minor_start_angle: float = 0,
        minor_end_angle: float = 360,
        major_angle: float = 360,
        align: Union[Align, tuple[Align, Align, Align]] = (
            Align.CENTER,
            Align.CENTER,
            Align.CENTER,
        ),
    ):
        if isinstance(align, Align):
            align = (align,) * 3

        params = dict(
            major_radius=major_radius,
            minor_radius=minor_radius,
            minor_start_angle=minor_start_angle,
            minor_end_angle=minor_end_angle,
            major_angle=major_angle,
            align=align,
        )
        super().__init__(self.create_part(bd.Torus, params=params))


class Wedge(AlgCompound):
    def __init__(
        self,
        xsize: float,
        ysize: float,
        zsize: float,
        xmin: float,
        zmin: float,
        xmax: float,
        zmax: float,
        align: Union[Align, tuple[Align, Align, Align]] = (
            Align.CENTER,
            Align.CENTER,
            Align.CENTER,
        ),
    ):
        params = dict(
            xsize=xsize,
            ysize=ysize,
            zsize=zsize,
            xmin=xmin,
            zmin=zmin,
            xmax=xmax,
            zmax=zmax,
            align=align,
        )
        super().__init__(self.create_part(bd.Wedge, params=params))


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
        super().__init__(self.create_part(bd.CounterBoreHole, part, params=params))


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
        super().__init__(self.create_part(bd.CounterSinkHole, part, params=params))


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
        super().__init__(self.create_part(bd.Hole, part, params=params))


#
# Functions
#


def extrude(
    to_extrude: Union[Face, Compound, List[Union[Face, Compound]]],
    amount: float = None,
    dir: VectorLike = None,
    both: bool = False,
    taper: float = 0.0,
) -> AlgCompound:
    faces = []
    for obj in to_tuple(to_extrude):
        if isinstance(obj, Compound):
            faces += obj.faces()
        elif isinstance(obj, Face):
            faces.append(obj)
        else:
            raise ValueError(f"Type {type(obj)} not supported for extrude")

    if dir is None:
        planes = [Plane(face) for face in faces]
    else:
        planes = [
            Plane(face.center(), face.center_location.x_axis.direction, Vector(dir))
            for face in faces
        ]

    return create_compound(
        bd.Extrude,
        dim=3,
        faces=faces,
        planes=planes,
        params=dict(amount=amount, both=both, taper=taper, mode=Mode.PRIVATE),
    )


def extrude_until(
    face: Union[Face, AlgCompound],
    limit: AlgCompound,
    dir: VectorLike = None,
    until: Until = Until.NEXT,
) -> AlgCompound:
    if dir is None:
        if isinstance(face, Face):
            f = face
        elif isinstance(face, Compound):
            f = face.faces()[0]

        z_max = limit.bounding_box().diagonal
        axis = Axis(f.center(), f.normal_at(f.center()))

        ex = extrude(f, z_max, dir=dir)
        if until == Until.NEXT:
            return AlgCompound((ex - limit).solids().min(axis))
        else:
            parts = limit & ex
            return AlgCompound((ex - limit).solids().min(axis)) + parts
    else:
        return AlgCompound(Solid.extrude_until(face, limit, dir, until))


def loft(sections: List[Union[AlgCompound, Face]], ruled: bool = False) -> AlgCompound:
    faces = []
    for s in to_tuple(sections):
        if isinstance(s, Compound):
            faces += s.faces()
        else:
            faces.append(s)

    return create_compound(bd.Loft, faces, dim=3, params=dict(ruled=ruled))


def revolve(
    profiles: Union[List[Union[Compound, Face]], Compound, Face],
    axis: Axis,
    arc: float = 360.0,
) -> AlgCompound:
    for p in to_tuple(profiles):
        faces = []
        if isinstance(p, Compound):
            faces += p.faces()
        else:
            faces.append(p)

    return create_compound(
        bd.Revolve,
        faces,
        dim=3,
        params=dict(axis=axis, revolution_arc=arc, mode=Mode.PRIVATE),
    )


def sweep(
    sections: List[Union[Face, Compound]],
    path: Union[Edge, Wire] = None,
    multisection: bool = False,
    is_frenet: bool = False,
    transition: Transition = Transition.TRANSFORMED,
    normal: VectorLike = None,
    binormal: Union[Edge, Wire] = None,
) -> AlgCompound:
    return create_compound(
        bd.Sweep,
        sections,
        dim=3,
        params=dict(
            path=path,
            multisection=multisection,
            is_frenet=is_frenet,
            transition=transition,
            normal=normal,
            binormal=binormal,
            mode=Mode.PRIVATE,
        ),
    )


def section(
    part: AlgCompound,
    by: List[Plane],
    height: float = 0.0,
) -> AlgCompound:
    return create_compound(
        bd.Section, by, part=part, params=dict(height=height, mode=Mode.INTERSECT)
    )


def shell(
    objects: Union[List[AlgCompound], AlgCompound],
    amount: float,
    openings: Union[Face, List[Face]] = None,
    kind: Kind = Kind.ARC,
) -> AlgCompound:
    return create_compound(
        bd.Offset,
        objects,
        params=dict(amount=amount, openings=openings, kind=kind, mode=Mode.PRIVATE),
    )
