from typing import List, Tuple

import build123d as bd
from .common import AlgCompound, Step, Obj12d, Obj123d

CTX = [None, bd.BuildLine, bd.BuildSketch, bd.BuildPart]


def extrude(
    to_extrude: bd.Compound,
    amount: float,
    until: bd.Until = None,
    until_part: bd.Compound = None,
    both: bool = False,
    taper: float = 0.0,
):
    with bd.BuildPart() as ctx:
        # store to_extrude's faces in context
        ctx.pending_faces = (
            [to_extrude] if isinstance(to_extrude, bd.Face) else to_extrude.faces()
        )
        ctx.pending_face_planes = [
            bd.Plane(face.to_pln()) for face in ctx.pending_faces
        ]

        if len(ctx.pending_faces) == 0:
            raise RuntimeError(f"No faces found in {to_extrude}")

        if until_part is not None:
            ctx._add_to_context(until_part)

        with bd.Locations(bd.Location()):
            compound = bd.Extrude(
                amount=amount,
                until=until,
                both=both,
                taper=taper,
                mode=bd.Mode.PRIVATE,
            )

    steps = []  # part.steps  # TODO

    return AlgCompound(compound, steps, 3)


def chamfer(
    part: bd.Compound,
    objects: List[bd.Edge | bd.Vertex] | bd.Edge | bd.Vertex,
    length: float,
    length2: float = None,
):
    with CTX[part.dim]() as ctx:
        ctx._add_to_context(bd.Compound(part.wrapped))
        compound = bd.Chamfer(*objects, length=length, length2=length2)

    objects = part.objects  # TODO

    return AlgCompound(compound, objects, part.dim)


def fillet(
    part: bd.Compound,
    objects: List[bd.Edge | bd.Vertex] | bd.Edge | bd.Vertex,
    radius: float,
):
    with CTX[part.dim]() as ctx:
        ctx._add_to_context(bd.Compound(part.wrapped))
        compound = bd.Fillet(*objects, radius=radius)

    steps = [Step(compound, compound.location, None)]  # TODO

    return AlgCompound(compound, steps, part.dim)


def mirror(
    objects: List[Obj12d] | Obj12d,
    about: bd.Plane = bd.Plane.XZ,
):
    objs = objects if isinstance(objects, (list, tuple)) else [objects]

    dim = max([o.dim for o in objs])
    with CTX[dim]():
        compound = bd.Mirror(*objs, about=about, mode=bd.Mode.PRIVATE)

    steps = [Step(compound, compound.location, None)]  # TODO

    return AlgCompound(compound, steps, dim)


def offset(
    objects: List[Obj123d] | Obj123d,
    amount: float,
    openings: bd.Face | list[bd.Face] = None,
    kind: bd.Kind = bd.Kind.ARC,
):
    objs = objects if isinstance(objects, (list, tuple)) else [objects]

    dim = max([o.dim for o in objs])
    with CTX[dim]():
        compound = bd.Offset(
            *objs, amount=amount, openings=openings, kind=kind, mode=bd.Mode.PRIVATE
        )

    steps = [Step(compound, compound.location, None)]  # TODO

    return AlgCompound(compound, steps, dim)


def scale(objects: bd.Shape, by: float | Tuple[float, float, float]):
    objs = objects if isinstance(objects, (list, tuple)) else [objects]

    dim = max([o.dim for o in objs])

    if dim == 2 and isinstance(by, (list, tuple)) and len(by) == 2:
        by = (by[0], by[1], 1)

    with CTX[dim]():
        compound = bd.Scale(*objs, by=by, mode=bd.Mode.PRIVATE)

    steps = [Step(compound, compound.location, None)]  # TODO

    return AlgCompound(compound, steps, dim)


def split(
    objects: List[Obj123d] | Obj123d,
    by: bd.Plane = bd.Plane.XZ,
    keep: bd.Keep = bd.Keep.TOP,
):
    objs = objects if isinstance(objects, (list, tuple)) else [objects]

    dim = max([o.dim for o in objs])

    with CTX[dim]():
        compound = bd.Split(*objs, bisect_by=by, keep=keep, mode=bd.Mode.PRIVATE)

    steps = [Step(compound, compound.location, None)]  # TODO

    return AlgCompound(compound, steps, dim)
