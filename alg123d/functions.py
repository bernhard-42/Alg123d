from typing import List, Tuple
import build123d as bd
from .wrappers import _function_wrap, AlgCompound, Obj12d, Obj123d

__all__ = [
    "chamfer",
    "fillet",
    "mirror",
    "offset",
    "scale",
    "split",
    "extrude",
]

#
# Generic functions
#


def chamfer(
    part: bd.Compound,
    objects: List[bd.Edge | bd.Vertex] | bd.Edge | bd.Vertex,
    length: float,
    length2: float = None,
):
    return _function_wrap(
        bd.Chamfer, objects, length=length, length2=length2, ctx_add=part, mode=None
    )


def fillet(
    part: bd.Compound,
    objects: List[bd.Edge | bd.Vertex] | bd.Edge | bd.Vertex,
    radius: float,
):
    return _function_wrap(bd.Fillet, objects, radius=radius, ctx_add=part, mode=None)


def mirror(
    objects: List[Obj12d] | Obj12d,
    about: bd.Plane = bd.Plane.XZ,
):
    return _function_wrap(bd.Mirror, objects, about=about)


def offset(
    objects: List[Obj123d] | Obj123d,
    amount: float,
    openings: bd.Face | list[bd.Face] = None,
    kind: bd.Kind = bd.Kind.ARC,
):
    return _function_wrap(
        bd.Offset, objects, amount=amount, openings=openings, kind=kind
    )


def scale(objects: bd.Shape, by: float | Tuple[float, float, float]):
    if isinstance(by, (list, tuple)) and len(by) == 2:
        by = (*by, 1)

    return _function_wrap(bd.Scale, objects, by=by)


def split(
    objects: List[Obj123d] | Obj123d,
    by: bd.Plane = bd.Plane.XZ,
    keep: bd.Keep = bd.Keep.TOP,
):
    return _function_wrap(bd.Split, objects, bisect_by=by, keep=keep)


#
# Part functions
#


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

        # with bd.Locations(bd.Location()):
        compound = bd.Extrude(
            amount=amount,
            until=until,
            both=both,
            taper=taper,
            mode=bd.Mode.PRIVATE,
        )

    steps = []  # part.steps  # TODO

    return AlgCompound(compound, steps, 3)
