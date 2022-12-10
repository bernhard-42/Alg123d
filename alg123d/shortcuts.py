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


def min_shape(
    s: ShapeList, axis: Axis = Axis.Z
) -> Union[Solid, Face, Wire, Edge, Vertex]:
    return s.sort_by(axis)[0]


def max_shape(
    s: ShapeList, axis: Axis = Axis.Z
) -> Union[Solid, Face, Wire, Edge, Vertex]:
    return s.sort_by(axis)[-1]


def min_solid(
    a: Compound, axis: Axis = Axis.Z, wrapped: bool = False
) -> Union[Compound, Solid]:
    obj = a.solids().sort_by(axis)[0]
    return AlgCompound(obj) if wrapped else obj


def max_solid(
    a: Compound, axis: Axis = Axis.Z, wrapped: bool = False
) -> Union[Compound, Solid]:
    obj = a.solids().sort_by(axis)[-1]
    return AlgCompound(obj) if wrapped else obj


def min_solids(a: Compound, axis: Axis = Axis.Z) -> ShapeList:
    return a.solids().group_by(axis)[0]


def max_solids(a: Compound, axis: Axis = Axis.Z) -> ShapeList:
    return a.solids().group_by(axis)[-1]


def min_face(a: Compound, axis: Axis = Axis.Z, wrapped=False) -> Union[Compound, Face]:
    obj = a.faces().sort_by(axis)[0]
    return AlgCompound(obj) if wrapped else obj


def max_face(a: Compound, axis: Axis = Axis.Z, wrapped=False) -> Union[Compound, Face]:
    obj = a.faces().sort_by(axis)[-1]
    return AlgCompound(obj) if wrapped else obj


def min_faces(a: Compound, axis: Axis = Axis.Z) -> ShapeList:
    return a.faces().group_by(axis)[0]


def max_faces(a: Compound, axis: Axis = Axis.Z) -> ShapeList:
    return a.faces().group_by(axis)[-1]


def min_edge(a: Compound, axis: Axis = Axis.Z, wrapped=False) -> Union[Compound, Edge]:
    obj = a.edges().sort_by(axis)[0]
    return AlgCompound(obj) if wrapped else obj


def max_edge(a: Compound, axis: Axis = Axis.Z, wrapped=False) -> Union[Compound, Edge]:
    obj = a.edges().sort_by(axis)[-1]
    return AlgCompound(obj) if wrapped else obj


def min_edges(a: Compound, axis: Axis = Axis.Z) -> ShapeList:
    return a.edges().group_by(axis)[0]


def max_edges(a: Compound, axis: Axis = Axis.Z) -> ShapeList:
    return a.edges().group_by(axis)[-1]


def min_vertex(
    a: Compound, axis: Axis = Axis.Z, wrapped=False
) -> Union[Compound, Vertex]:
    obj = a.vertices().sort_by(axis)[0]
    return AlgCompound(obj) if wrapped else obj


def max_vertex(
    a: Compound, axis: Axis = Axis.Z, wrapped=False
) -> Union[Compound, Vertex]:
    obj = a.vertices().sort_by(axis)[-1]
    return AlgCompound(obj) if wrapped else obj


def min_vertices(a: Compound, axis: Axis = Axis.Z) -> ShapeList:
    return a.vertices().group_by(axis)[0]


def max_vertices(a: Compound, axis: Axis = Axis.Z) -> ShapeList:
    return a.vertices().group_by(axis)[-1]
