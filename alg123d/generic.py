import copy
from typing import List, Tuple, Union

import build123d as bd

from .algcompound import AlgCompound, create_compound
from .topology import *

__all__ = ["chamfer", "fillet", "mirror", "offset", "scale", "split"]


#
# Patches
#
class Chamfer(Compound):
    """Generic Operation: Chamfer

    Applies to: BuildSketch and BuildPart

    Chamfer the given sequence of edges or vertices.

    Args:
        objects (Union[Edge,Vertex]): sequence of edges or vertices to chamfer
        length (float): chamfer size
        length2 (float, optional): asymmetric chamfer size. Defaults to None.

    Raises:
        ValueError: objects must be Edges
        ValueError: objects must be Vertices
        RuntimeError: Builder not supported
    """

    _applies_to = [bd.BuildPart._tag(), bd.BuildSketch._tag()]

    def __init__(
        self,
        *objects: Union[Edge, Vertex],
        length: float,
        length2: float = None,
        mode=Mode.REPLACE,
    ):
        context: bd.Builder = bd.Builder._get_context(self)
        context.validate_inputs(self, objects)

        if isinstance(context, bd.BuildPart):
            if not all([isinstance(obj, Edge) for obj in objects]):
                raise ValueError("BuildPart Chamfer operation takes only Edges")
            new_part = context.part.chamfer(length, length2, list(objects))
            context._add_to_context(new_part, mode=Mode.REPLACE)
            super().__init__(new_part.wrapped)
        elif isinstance(context, bd.BuildSketch):
            if not all([isinstance(obj, Vertex) for obj in objects]):
                raise ValueError("BuildSketch Chamfer operation takes only Vertices")
            new_faces = []
            for face in context.faces():
                vertices_in_face = [v for v in face.vertices() if v in objects]
                if vertices_in_face:
                    new_faces.append(face.chamfer_2d(length, vertices_in_face))
                else:
                    new_faces.append(face)
            new_sketch = Compound.make_compound(new_faces)
            context._add_to_context(new_sketch, mode=mode)
            super().__init__(new_sketch.wrapped)


class Fillet(Compound):
    """Generic Operation: Fillet

    Applies to: BuildSketch and BuildPart

    Fillet the given sequence of edges or vertices.

    Args:
        objects (Union[Edge,Vertex]): sequence of edges or vertices to fillet
        radius (float): fillet size - must be less than 1/2 local width

    Raises:
        ValueError: objects must be Edges
        ValueError: objects must be Vertices
        RuntimeError: Builder not supported
    """

    _applies_to = [bd.BuildPart._tag(), bd.BuildSketch._tag()]

    def __init__(self, *objects: Union[Edge, Vertex], radius: float, mode=Mode.REPLACE):
        context: bd.Builder = bd.Builder._get_context(self)
        context.validate_inputs(self, objects)

        if isinstance(context, bd.BuildPart):
            if not all([isinstance(obj, Edge) for obj in objects]):
                raise ValueError("BuildPart Fillet operation takes only Edges")
            new_part = context.part.fillet(radius, list(objects))
            context._add_to_context(new_part, mode=Mode.REPLACE)
            super().__init__(new_part.wrapped)
        elif isinstance(context, bd.BuildSketch):
            if not all([isinstance(obj, Vertex) for obj in objects]):
                raise ValueError("BuildSketch Fillet operation takes only Vertices")
            new_faces = []
            for face in context.faces():
                vertices_in_face = [v for v in face.vertices() if v in objects]
                if vertices_in_face:
                    new_faces.append(face.fillet_2d(radius, vertices_in_face))
                else:
                    new_faces.append(face)
            new_sketch = Compound.make_compound(new_faces)
            context._add_to_context(new_sketch, mode=mode)
            super().__init__(new_sketch.wrapped)


#
# Functions
#


def chamfer(
    part: AlgCompound,
    objects: Union[List[Union[Edge, Vertex]], Edge, Vertex],
    length: float,
    length2: float = None,
) -> AlgCompound:
    return create_compound(
        Chamfer,
        objects,
        params=dict(length=length, length2=length2, mode=Mode.PRIVATE),
        part=part,
    )


def fillet(
    part: AlgCompound,
    objects: Union[List[Union[Edge, Vertex]], Edge, Vertex],
    radius: float,
) -> AlgCompound:
    return create_compound(
        Fillet, objects, params=dict(radius=radius, mode=Mode.PRIVATE), part=part
    )


def mirror(
    objects: Union[List[AlgCompound], AlgCompound],
    about: Plane = Plane.XZ,
) -> AlgCompound:
    return create_compound(
        bd.Mirror, objects, params=dict(about=about, mode=Mode.PRIVATE)
    )


def offset(
    objects: Union[List[AlgCompound], AlgCompound],
    amount: float,
    kind: Kind = Kind.ARC,
) -> AlgCompound:
    result = create_compound(
        bd.Offset, objects, params=dict(amount=amount, kind=kind, mode=Mode.PRIVATE)
    )
    if isinstance(objects, AlgCompound) and objects.dim == 3:
        if amount > 0:
            return result + objects
        else:
            return objects - result
    else:
        return result


def scale(objects: Shape, by: Union[float, Tuple[float, float, float]]) -> AlgCompound:
    if isinstance(by, (list, tuple)) and len(by) == 2:
        by = (*by, 1)

    return create_compound(bd.Scale, objects, params=dict(by=by, mode=Mode.PRIVATE))


def split(
    objects: Union[List[AlgCompound], AlgCompound],
    by: Plane = Plane.XZ,
    keep: Keep = Keep.TOP,
) -> AlgCompound:
    return create_compound(
        bd.Split, objects, params=dict(bisect_by=by, keep=keep, mode=Mode.PRIVATE)
    )
