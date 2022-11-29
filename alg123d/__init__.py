from typing import List
from build123d.direct_api import *
from build123d.build_enums import *

from .direct_api import *
from .common import *
from .generic import *
from .part import *
from .sketch import *
from .line import *

MM = 1
CM = 10 * MM
M = 1000 * MM
IN = 25.4 * MM
FT = 12 * IN

try:
    from cq_vscode import show, show_object, set_defaults, reset_show

    print("Loaded show, show_object, set_defaults, reset_show")
except:
    ...


class Shortcuts:
    @staticmethod
    def top_solid(c: Compound, axis=Axis.Z) -> Face:
        """Topsolid"""
        return c.solids().sort_by(axis)[-1]

    @staticmethod
    def top_solids(c: Compound, axis=Axis.Z) -> ShapeList:
        """Top solids"""
        return c.solids().group_by(axis)[-1]

    @staticmethod
    def top_face(c: Compound, axis=Axis.Z) -> Face:
        """Top face"""
        return c.faces().sort_by(axis)[-1]

    @staticmethod
    def top_faces(c: Compound, axis=Axis.Z) -> ShapeList:
        """Top faces"""
        return c.faces().group_by(axis)[-1]

    @staticmethod
    def top_plane(c: Compound, axis=Axis.Z) -> Plane:
        """Top workplanes"""
        return as_plane(Shortcuts.top_face(c, axis))

    @staticmethod
    def top_planes(c: Compound, axis=Axis.Z) -> List[Plane]:
        """Top workplanes"""
        return [as_plane(f) for f in Shortcuts.top_faces(c, axis)]

    @staticmethod
    def top_edges(c: Compound, axis=Axis.Z) -> ShapeList:
        """Top edges"""
        return c.edges().group_by(axis)[-1]
