from typing import List

from build123d.build_enums import *
from build123d.direct_api import *

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
# Location monkey patching and helpers
#

# Axis of locations


def _location_x_axis(self) -> Axis:
    p = Plane(self)
    return Axis(p.origin, p.x_dir)


def _location_y_axis(self) -> Axis:
    p = Plane(self)
    return Axis(p.origin, p.y_dir)


def _location_z_axis(self) -> Axis:
    p = Plane(self)
    return Axis(p.origin, p.z_dir)


def _location_plane(self) -> Plane:
    return Plane(self)


Location.x_axis = property(_location_x_axis)
Location.y_axis = property(_location_y_axis)
Location.z_axis = property(_location_z_axis)
Location.plane = property(_location_plane)


class Pos(Location):
    def __init__(self, x: Union[float, Vertex, Vector] = 0, y: float = 0, z: float = 0):
        if isinstance(x, (Vertex, Vector)):
            super().__init__(x.to_tuple())
        else:
            super().__init__((x, y, z))


class Rot(Location):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        super().__init__((0, 0, 0), (x, y, z))


#
# Plane monkey patching and helpers
#


def _plane_location(self):
    return Location(self)


Plane.location = property(_plane_location)


class Planes:
    def __init__(self, objs: List[Union[Plane, Location, Face]]) -> List[Plane]:
        self.objects = [Plane(obj) for obj in objs]
        self.index = 0

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.objects):
            plane = self.objects[self.index]
            self.index += 1
            return plane
        else:
            raise StopIteration


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


# def _shapelist_max(self, axis: Axis = Axis.Z, wrapped=False) => algcompound.py
# def _shapelist_min(self, axis: Axis = Axis.Z, wrapped=False) => algcompound.py


def _shapelist_min_group(self, sort_by: Union[Axis, SortBy] = Axis.Z) -> ShapeList:
    return self.group_by(sort_by)[0]


def _shapelist_max_group(self, sort_by: Union[Axis, SortBy] = Axis.Z) -> ShapeList:
    return self.group_by(sort_by)[-1]


ShapeList.__sub__ = _shapelist_sub
ShapeList.min_group = _shapelist_min_group
ShapeList.max_group = _shapelist_max_group

#
# Symbols
#


def axis_symbol(self, l=1) -> Edge:
    edge = Edge.make_line(self.position, self.position + self.direction * 0.95 * l)
    plane = Plane(
        origin=self.position + 0.95 * l * self.direction,
        z_dir=self.direction,
    )
    cone = Solid.make_cone(l / 60, 0, l / 20, plane)
    return Compound.make_compound([edge] + cone.faces())


def location_symbol(self, l=1) -> Compound:
    axes = SVG.axes(axes_scale=l).locate(self)
    return Compound.make_compound(axes)


def plane_symbol(self, l: float = 1) -> Compound:
    loc = self.location
    circle = Edge.make_circle(l * 0.8).located(loc)
    axes = SVG.axes(axes_scale=l).locate(loc)

    return Compound.make_compound(list(axes) + [circle])


Axis.symbol = axis_symbol
Location.symbol = location_symbol
Plane.symbol = plane_symbol


def _revolutejoint_symbol(self) -> Compound:
    """A CAD symbol representing the axis of rotation as bound to part"""
    radius = self.parent.bounding_box().diagonal_length() / 30

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
