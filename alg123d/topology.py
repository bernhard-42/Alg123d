from typing import List

from build123d.build_enums import *
from build123d.topology import *

# Classes coverage:
#  - Mixin1D
#  - Mixin3D
#  - Shape(NodeMixin)
#  - ShapeList(list[T])
#  - Compound(Shape, Mixin3D)
#  - Edge(Shape, Mixin1D)
#  - Face(Shape)
#  - Shell(Shape)
#  - Solid(Shape, Mixin3D)
#  - Vertex(Shape)
#  - Wire(Shape, Mixin1D)
#  - DXF
#  - SVG
#  - Joint(ABC)
#  - RigidJoint(Joint)
#  - RevoluteJoint(Joint)
#  - LinearJoint(Joint)
#  - CylindricalJoint(Joint)
#  - BallJoint(Joint)

#
# World locations
#

# of a face at the center


def _face_center_location(self) -> Location:
    origin = self.center(CenterOf.MASS)
    x_dir = Vector(self._geom_adaptor().Position().XDirection())
    z_dir = self.normal_at(origin)
    return Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).location


Face.center_location = property(_face_center_location)

#  of an edge at its origin


def _edge_origin_location(self) -> Location:
    if self.geom_type() == "LINE":
        return self.to_axis().to_location()
    else:
        origin = self.position_at(0)
        z_dir = self.normal()
        x_dir = self.tangent_at(0)
        return Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).location


def _edge_center_location(self) -> Location:
    if self.is_closed():
        origin = self.center(CenterOf.MASS)
        z_dir = self.normal()
        # Use the vector defined by the single vertex and the origin as x direction
        x_dir = Vector((self.vertices()[0] - origin).to_tuple()).normalized()
        return Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).to_location()

    else:
        raise RuntimeError("center_location only exists for closed edges")


Edge.origin_location = property(_edge_origin_location)
Edge.center_location = property(_edge_center_location)


#
# Shape monkey patching
#


def _filter(
    objs,
    filter_by: Union[Axis, GeomType] = None,
    reverse: bool = False,
    tolerance: float = 1e-5,
):
    if filter_by is None:
        return objs
    else:
        return objs.filter_by(filter_by, reverse, tolerance)


def _shape_vertices(
    self,
    filter_by: Union[Axis, GeomType] = None,
    reverse: bool = False,
    tolerance: float = 1e-5,
):
    vertices = ShapeList([Vertex(downcast(i)) for i in self._entities(Vertex.__name__)])
    return _filter(vertices, filter_by, reverse, tolerance)


def _shape_edges(
    self,
    filter_by: Union[Axis, GeomType] = None,
    reverse: bool = False,
    tolerance: float = 1e-5,
):
    edges = ShapeList(
        [
            Edge(i)
            for i in self._entities(Edge.__name__)
            if not BRep_Tool.Degenerated_s(TopoDS.Edge_s(i))
        ]
    )
    return _filter(edges, filter_by, reverse, tolerance)


def _shape_compounds(
    self,
    filter_by: Union[Axis, GeomType] = None,
    reverse: bool = False,
    tolerance: float = 1e-5,
):
    compounds = ShapeList([Compound(i) for i in self._entities(Compound.__name__)])
    return _filter(compounds, filter_by, reverse, tolerance)


def _shape_wires(
    self,
    filter_by: Union[Axis, GeomType] = None,
    reverse: bool = False,
    tolerance: float = 1e-5,
):
    wires = ShapeList([Wire(i) for i in self._entities(Wire.__name__)])
    return _filter(wires, filter_by, reverse, tolerance)


def _shape_faces(
    self,
    filter_by: Union[Axis, GeomType] = None,
    reverse: bool = False,
    tolerance: float = 1e-5,
):
    faces = ShapeList([Face(i) for i in self._entities(Face.__name__)])
    return _filter(faces, filter_by, reverse, tolerance)


def _shape_shells(
    self,
    filter_by: Union[Axis, GeomType] = None,
    reverse: bool = False,
    tolerance: float = 1e-5,
):
    shells = ShapeList([Shell(i) for i in self._entities(Shell.__name__)])
    return _filter(shells, filter_by, reverse, tolerance)


def _shape_solids(
    self,
    filter_by: Union[Axis, GeomType] = None,
    reverse: bool = False,
    tolerance: float = 1e-5,
):
    solids = ShapeList([Solid(i) for i in self._entities(Solid.__name__)])
    return _filter(solids, filter_by, reverse, tolerance)


Shape.vertices = _shape_vertices
Shape.edges = _shape_edges
Shape.compounds = _shape_compounds
Shape.wires = _shape_wires
Shape.faces = _shape_faces
Shape.shells = _shape_shells
Shape.solids = _shape_solids


#
# ShapeList
#


def _shapelist_sub(self, other: List[Shape]) -> ShapeList:
    d2 = [hash(o) for o in other]
    d1 = {hash(o): o for o in self if hash(o) not in d2}
    return ShapeList(d1.values())


def _shapelist_max(
    self, sort_by: Union[Axis, SortBy] = Axis.Z, wrapped=False
) -> Union[Solid, Face, Wire, Edge, Vertex]:
    return self.sort_by(sort_by)[-1]


def _shapelist_min(
    self, sort_by: Union[Axis, SortBy] = Axis.Z
) -> Union[Solid, Face, Wire, Edge, Vertex]:
    return self.sort_by(sort_by)[0]


def _shapelist_min_group(self, sort_by: Union[Axis, SortBy] = Axis.Z) -> ShapeList:
    return self.group_by(sort_by)[0]


def _shapelist_max_group(self, sort_by: Union[Axis, SortBy] = Axis.Z) -> ShapeList:
    return self.group_by(sort_by)[-1]


ShapeList.__sub__ = _shapelist_sub
ShapeList.min = _shapelist_min
ShapeList.max = _shapelist_max
ShapeList.min_group = _shapelist_min_group
ShapeList.max_group = _shapelist_max_group


#
# Joints
#


def _revolutejoint_symbol(self) -> Compound:
    """A CAD symbol representing the axis of rotation as bound to part"""
    radius = self.parent.bounding_box().diagonal / 30

    return Compound.make_compound(
        [
            Edge.make_line((0, 0, 0), (0, 0, radius * 2)),
            Edge.make_line((0, 0, 0), (self.angle_reference * radius * 2).to_tuple()),
            Edge.make_circle(
                radius,
                start_angle=self.angular_range[0],
                end_angle=self.angular_range[1],
            ),
        ]
    ).move(self.parent.location * self.relative_axis.to_location())


RevoluteJoint.symbol = property(_revolutejoint_symbol)
