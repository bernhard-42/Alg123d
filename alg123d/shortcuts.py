from typing import List, Union
from .wrappers import AlgCompound
from .direct_api import *


def tupleize(arg):
    if isinstance(arg, (tuple, list)):
        return tuple(arg)
    else:
        return (arg,)


def planes(objs: List[Union[Plane, Location, Face]]) -> List[Plane]:
    return [Plane(obj) for obj in objs]


def diff(l1: List[Shape], l2: List[Shape]) -> ShapeList:
    d2 = [hash(o) for o in l2]
    d1 = {hash(o): o for o in l1 if hash(o) not in d2}
    return ShapeList(d1.values())


#
# min/max handling of ShapeLists
#


def sort_min(
    s: ShapeList, axis: Axis = Axis.Z
) -> Union[Solid, Face, Wire, Edge, Vertex]:
    return s.sort_by(axis)[0]


def sort_max(
    s: ShapeList, axis: Axis = Axis.Z
) -> Union[Solid, Face, Wire, Edge, Vertex]:
    return s.sort_by(axis)[-1]


def group_min(s: ShapeList, axis: Axis = Axis.Z) -> ShapeList:
    return s.group_by(axis)[0]


def group_max(s: ShapeList, axis: Axis = Axis.Z) -> ShapeList:
    return s.group_by(axis)[-1]


def min_solid(
    a: Compound, axis: Axis = Axis.Z, wrapped: bool = False
) -> Union[Compound, Solid]:
    obj = sort_min(a.solids(), axis)
    return AlgCompound(obj) if wrapped else obj


def max_solid(
    a: Compound, axis: Axis = Axis.Z, wrapped: bool = False
) -> Union[Compound, Solid]:
    obj = sort_max(a.solids(), axis)
    return AlgCompound(obj) if wrapped else obj


def min_solids(a: Compound, axis: Axis = Axis.Z) -> ShapeList:
    return group_min(a.solids(), axis)


def max_solids(a: Compound, axis: Axis = Axis.Z) -> ShapeList:
    return group_max(a.solids(), axis)


def min_face(a: Compound, axis: Axis = Axis.Z, wrapped=False) -> Union[Compound, Face]:
    obj = sort_min(a.faces(), axis)
    return AlgCompound(obj) if wrapped else obj


def max_face(a: Compound, axis: Axis = Axis.Z, wrapped=False) -> Union[Compound, Face]:
    obj = sort_max(a.faces(), axis)
    return AlgCompound(obj) if wrapped else obj


def min_faces(a: Compound, axis: Axis = Axis.Z) -> ShapeList:
    return group_min(a.faces(), axis)


def max_faces(a: Compound, axis: Axis = Axis.Z) -> ShapeList:
    return group_max(a.faces(), axis)


def min_edge(a: Compound, axis: Axis = Axis.Z, wrapped=False) -> Union[Compound, Edge]:
    obj = sort_min(a.edges(), axis)
    return AlgCompound(obj) if wrapped else obj


def max_edge(a: Compound, axis: Axis = Axis.Z, wrapped=False) -> Union[Compound, Edge]:
    obj = sort_max(a.edges(), axis)
    return AlgCompound(obj) if wrapped else obj


def min_edges(a: Compound, axis: Axis = Axis.Z) -> ShapeList:
    return group_min(a.edges(), axis)


def max_edges(a: Compound, axis: Axis = Axis.Z) -> ShapeList:
    return group_max(a.edges(), axis)


def min_vertex(
    a: Compound, axis: Axis = Axis.Z, wrapped=False
) -> Union[Compound, Vertex]:
    obj = sort_min(a.vertices(), axis)
    return AlgCompound(obj) if wrapped else obj


def max_vertex(
    a: Compound, axis: Axis = Axis.Z, wrapped=False
) -> Union[Compound, Vertex]:
    obj = sort_max(a.vertices(), axis)
    return AlgCompound(obj) if wrapped else obj


def min_vertices(a: Compound, axis: Axis = Axis.Z) -> ShapeList:
    return group_min(a.vertices(), axis)


def max_vertices(a: Compound, axis: Axis = Axis.Z) -> ShapeList:
    return group_max(a.vertices(), axis)


def from_cq(obj):
    return AlgCompound.make_compound(obj.objects)


#
# Conversion functions
#


def to_cq(obj):
    import cadquery as cq

    return cq.Workplane().newObject([cq.Shape.cast(o.wrapped) for o in obj])


def from_bd(obj):
    if hasattr(obj, "_obj_name"):
        return AlgCompound(getattr(obj, obj._obj_name))
    else:
        return obj


def to_bd(obj):
    import build123d as bd

    if hasattr(obj, "dim"):
        ctx = {1: bd.BuildLine, 2: bd.BuildSketch, 3: bd.BuildPart}
        with ctx[obj.dim]() as c:
            bd.Add(Compound.make_compound(list(obj)))
        return c
    else:
        return bd.ShapeList(
            bd.Compound.make_compound([bd.Shape.cast(o.wrapped) for o in obj])
        )
