from typing import List
from build123d.direct_api import *
from build123d.build_enums import *

from .direct_api import *
from .wrappers import AlgCompound, Empty
from .common import *
from .generic import *
from .part import *
from .sketch import *
from .line import *

try:
    from cq_vscode import show, show_object, set_defaults, reset_show

    print("Loaded show, show_object, set_defaults, reset_show")
except:
    ...


class Shortcuts:
    @staticmethod
    def planes(objs: List[Union[Plane, Location, Face]]) -> List[Plane]:
        return [Plane(obj) for obj in objs]

    @staticmethod
    def min_solid(a: Compound, axis=Axis.Z, wrapped=False) -> Union[Compound, Solid]:
        obj = a.solids().sort_by(axis)[0]
        return AlgCompound(obj) if wrapped else obj

    @staticmethod
    def max_solid(a: Compound, axis=Axis.Z, wrapped=False) -> Union[Compound, Solid]:
        obj = a.solids().sort_by(axis)[-1]
        return AlgCompound(obj) if wrapped else obj

    @staticmethod
    def min_solids(a: Compound, axis=Axis.Z) -> ShapeList:
        return a.solids().group_by(axis)[0]

    @staticmethod
    def max_solids(a: Compound, axis=Axis.Z) -> ShapeList:
        return a.solids().group_by(axis)[-1]

    @staticmethod
    def min_face(a: Compound, axis=Axis.Z, wrapped=False) -> Union[Compound, Face]:
        obj = a.faces().sort_by(axis)[0]
        return AlgCompound(obj) if wrapped else obj

    @staticmethod
    def max_face(a: Compound, axis=Axis.Z, wrapped=False) -> Union[Compound, Face]:
        obj = a.faces().sort_by(axis)[-1]
        return AlgCompound(obj) if wrapped else obj

    @staticmethod
    def min_faces(a: Compound, axis=Axis.Z) -> ShapeList:
        return a.faces().group_by(axis)[0]

    @staticmethod
    def max_faces(a: Compound, axis=Axis.Z) -> ShapeList:
        return a.faces().group_by(axis)[-1]

    @staticmethod
    def min_edge(a: Compound, axis=Axis.Z, wrapped=False) -> Union[Compound, Edge]:
        obj = a.edges().sort_by(axis)[0]
        return AlgCompound(obj) if wrapped else obj

    @staticmethod
    def max_edge(a: Compound, axis=Axis.Z, wrapped=False) -> Union[Compound, Edge]:
        obj = a.edges().sort_by(axis)[-1]
        return AlgCompound(obj) if wrapped else obj

    @staticmethod
    def min_edges(a: Compound, axis=Axis.Z) -> ShapeList:
        return a.edges().group_by(axis)[0]

    @staticmethod
    def max_edges(a: Compound, axis=Axis.Z) -> ShapeList:
        return a.edges().group_by(axis)[-1]
