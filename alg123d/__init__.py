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
    def top_solid(c: Compound, x=0, y=0, z=0) -> Face:
        """Topsolid"""
        axis = Axis.Z if x == 0 and y == 0 and z == 0 else Axis((0, 0, 0), (x, y, z))
        return c.solids().sort_by(axis)[-1]

    @staticmethod
    def top_solids(c: Compound, x=0, y=0, z=0) -> ShapeList:
        """Top solids"""
        axis = Axis.Z if x == 0 and y == 0 and z == 0 else Axis((0, 0, 0), (x, y, z))
        return c.solids().group_by(axis)[-1]

    @staticmethod
    def top_face(c: Compound, x=0, y=0, z=0) -> Face:
        """Top face"""
        axis = Axis.Z if x == 0 and y == 0 and z == 0 else Axis((0, 0, 0), (x, y, z))
        return c.faces().sort_by(axis)[-1]

    @staticmethod
    def top_faces(c: Compound, x=0, y=0, z=0) -> ShapeList:
        """Top faces"""
        axis = Axis.Z if x == 0 and y == 0 and z == 0 else Axis((0, 0, 0), (x, y, z))
        return c.faces().group_by(axis)[-1]

    @staticmethod
    def top_plane(c: Compound, x=0, y=0, z=0) -> Plane:
        """Top workplanes"""
        return as_plane(Shortcuts.top_face(c, x=x, y=y, z=z))

    @staticmethod
    def top_planes(c: Compound, x=0, y=0, z=0) -> List[Plane]:
        """Top workplanes"""
        return [as_plane(f) for f in Shortcuts.top_faces(c, x=x, y=y, z=z)]

    @staticmethod
    def top_edges(c: Compound, x=0, y=0, z=0) -> ShapeList:
        """Top edges"""
        axis = Axis.Z if x == 0 and y == 0 and z == 0 else Axis((0, 0, 0), (x, y, z))
        return c.edges().group_by(axis)[-1]
