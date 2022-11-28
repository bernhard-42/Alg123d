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
    def front_faces(c: Compound) -> ShapeList:
        """Front face"""
        return c.faces().group_by(Axis.Y)[0]

    @staticmethod
    def back_faces(c: Compound) -> ShapeList:
        """Back face"""
        return c.faces().group_by(Axis.Y)[-1]

    @staticmethod
    def left_faces(c: Compound) -> ShapeList:
        """Left face"""
        return c.faces().group_by(Axis.X)[0]

    @staticmethod
    def right_faces(c: Compound) -> ShapeList:
        """Right face"""
        return c.faces().group_by(Axis.X)[-1]

    @staticmethod
    def top_faces(c: Compound) -> ShapeList:
        """Top face"""
        return c.faces().group_by(Axis.Z)[-1]

    @staticmethod
    def bottom_faces(c: Compound) -> Face:
        """Bottom face"""
        return c.faces().group_by(Axis.Z)[0]

    @staticmethod
    def front_face(c: Compound) -> Face:
        """Front face"""
        return c.faces().sort_by(Axis.Y)[0]

    @staticmethod
    def back_face(c: Compound) -> Face:
        """Back face"""
        return c.faces().sort_by(Axis.Y)[-1]

    @staticmethod
    def left_face(c: Compound) -> Face:
        """Left face"""
        return c.faces().sort_by(Axis.X)[0]

    @staticmethod
    def right_face(c: Compound) -> Face:
        """Right face"""
        return c.faces().sort_by(Axis.X)[-1]

    @staticmethod
    def top_face(c: Compound) -> Face:
        """Top face"""
        return c.faces().sort_by(Axis.Z)[-1]

    @staticmethod
    def bottom_face(c: Compound) -> Face:
        """Bottom face"""
        return c.faces().sort_by(Axis.Z)[0]

    @staticmethod
    def front_edges(c: Compound) -> ShapeList:
        """Front edges"""
        return c.edges().group_by(Axis.Y)[0]

    @staticmethod
    def back_edges(c: Compound) -> ShapeList:
        """Back edges"""
        return c.edges().group_by(Axis.Y)[-1]

    @staticmethod
    def left_edges(c: Compound) -> ShapeList:
        """Left edges"""
        return c.edges().group_by(Axis.X)[0]

    @staticmethod
    def right_edges(c: Compound) -> ShapeList:
        """Right edges"""
        return c.edges().group_by(Axis.X)[-1]

    @staticmethod
    def top_edges(c: Compound) -> ShapeList:
        """Top edges"""
        return c.edges().group_by(Axis.Z)[-1]

    @staticmethod
    def bottom_edges(c: Compound) -> ShapeList:
        """Bottom edges"""
        return c.edges().group_by(Axis.Z)[0]

    @staticmethod
    def front_planes(c: Compound) -> List[Workplane]:
        """Front workplanes"""
        return [Workplane(f) for f in Shortcuts.front_faces(c)]

    @staticmethod
    def back_planes(c: Compound) -> List[Workplane]:
        """Back workplanes"""
        return [Workplane(f) for f in Shortcuts.back_faces(c)]

    @staticmethod
    def left_planes(c: Compound) -> List[Workplane]:
        """Left workplanes"""
        return [Workplane(f) for f in Shortcuts.left_faces(c)]

    @staticmethod
    def right_planes(c: Compound) -> List[Workplane]:
        """Right workplanes"""
        return [Workplane(f) for f in Shortcuts.right_faces(c)]

    @staticmethod
    def top_planes(c: Compound) -> List[Workplane]:
        """Top workplanes"""
        return [Workplane(f) for f in Shortcuts.top_faces(c)]

    @staticmethod
    def bottom_planes(c: Compound) -> List[Workplane]:
        """Bottom workplanes"""
        return [Workplane(f) for f in Shortcuts.bottom_faces(c)]

    @staticmethod
    def front_plane(c: Compound) -> Workplane:
        """Front workplanes"""
        return Workplane(Shortcuts.front_face(c))

    @staticmethod
    def back_plane(c: Compound) -> Workplane:
        """Back workplanes"""
        return Workplane(Shortcuts.back_face(c))

    @staticmethod
    def left_plane(c: Compound) -> Workplane:
        """Left workplanes"""
        return Workplane(Shortcuts.left_face(c))

    @staticmethod
    def right_plane(c: Compound) -> Workplane:
        """Right workplanes"""
        return Workplane(Shortcuts.right_face(c))

    @staticmethod
    def top_plane(c: Compound) -> Workplane:
        """Top workplanes"""
        return Workplane(Shortcuts.top_face(c))

    @staticmethod
    def bottom_plane(c: Compound) -> Workplane:
        """Bottom workplanes"""
        return Workplane(Shortcuts.bottom_face(c))

    @staticmethod
    def workplanes(faces: List[Face]):
        return [Workplane(f) for f in faces]
