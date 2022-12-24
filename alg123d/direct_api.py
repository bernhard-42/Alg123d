from typing import List

from build123d.direct_api import *
from build123d.build_enums import *

#
# The world location of a face at the center
#


def _face_origin_location(self) -> Location:
    origin = self.center()
    x_dir = Vector(self._geom_adaptor().Position().XDirection())
    z_dir = self.normal_at(origin)
    return Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).to_location()


Face.origin_location = property(_face_origin_location)


def _edge_origin_location(self) -> Location:
    z_dir = self.normal()

    vertices = self.vertices()
    if len(vertices) == 1:  # e.g. a single closed spline
        origin = self.center(CenterOf.BOUNDING_BOX)
        # Use the vector defined by the vertex and the origin as x direction
        x_dir = Vector((vertices[0] - origin).to_tuple()).normalized()
    else:
        origin = Vector(vertices[0].to_tuple())
        # Use the vector defined by the first and the last vertex as x direction
        x_dir = Vector((vertices[0] - vertices[-1]).to_tuple()).normalized()

    return Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).to_location()


Edge.origin_location = property(_edge_origin_location)

#
# Location monkey patching
# Axis of locations
#


def _location_x_axis(self) -> Axis:
    p = Plane(self)
    return Axis(p.origin, p.x_dir)


def _location_y_axis(self) -> Axis:
    p = Plane(self)
    return Axis(p.origin, p.y_dir)


def _location_z_axis(self) -> Axis:
    p = Plane(self)
    return Axis(p.origin, p.z_dir)


Location.x_axis = property(_location_x_axis)
Location.y_axis = property(_location_y_axis)
Location.z_axis = property(_location_z_axis)

#
# Shape monkey patching
#

_shape_vertices_orig = Shape.vertices
_shape_edges_orig = Shape.edges
_shape_compounds_orig = Shape.compounds
_shape_wires_orig = Shape.wires
_shape_faces_orig = Shape.faces
_shape_shells_orig = Shape.shells
_shape_solids_orig = Shape.solids


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
    return _filter(_shape_vertices_orig(self), filter_by, reverse, tolerance)


def _shape_edges(
    self,
    filter_by: Union[Axis, GeomType] = None,
    reverse: bool = False,
    tolerance: float = 1e-5,
):
    return _filter(_shape_edges_orig(self), filter_by, reverse, tolerance)


def _shape_compounds(
    self,
    filter_by: Union[Axis, GeomType] = None,
    reverse: bool = False,
    tolerance: float = 1e-5,
):
    return _filter(_shape_compounds_orig(self), filter_by, reverse, tolerance)


def _shape_wires(
    self,
    filter_by: Union[Axis, GeomType] = None,
    reverse: bool = False,
    tolerance: float = 1e-5,
):
    return _filter(_shape_wires_orig(self), filter_by, reverse, tolerance)


def _shape_faces(
    self,
    filter_by: Union[Axis, GeomType] = None,
    reverse: bool = False,
    tolerance: float = 1e-5,
):
    return _filter(_shape_faces_orig(self), filter_by, reverse, tolerance)


def _shape_shells(
    self,
    filter_by: Union[Axis, GeomType] = None,
    reverse: bool = False,
    tolerance: float = 1e-5,
):
    return _filter(_shape_shells_orig(self), filter_by, reverse, tolerance)


def _shape_solids(
    self,
    filter_by: Union[Axis, GeomType] = None,
    reverse: bool = False,
    tolerance: float = 1e-5,
):
    return _filter(_shape_solids_orig(self), filter_by, reverse, tolerance)


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


# def _shapelist_max(self, axis: Axis = Axis.Z, wrapped=False) => wrappers.py
# def _shapelist_min(self, axis: Axis = Axis.Z, wrapped=False) => wrappers.py


def _shapelist_min_group(self, axis: Axis = Axis.Z) -> ShapeList:
    return self.group_by(axis)[0]


def _shapelist_max_group(self, axis: Axis = Axis.Z) -> ShapeList:
    return self.group_by(axis)[-1]


ShapeList.__sub__ = _shapelist_sub
ShapeList.min_group = _shapelist_min_group
ShapeList.max_group = _shapelist_max_group

#
# Symbols
#


def axis_symbol(axis: Axis, l=1) -> Edge:
    return Edge.make_line(axis.position, axis.position + axis.direction * l)


def location_symbol(location: Location, l=1) -> Compound:
    plane = Plane(location)
    x = Edge.make_line(plane.origin, plane.origin + plane.x_dir * l)
    y = Edge.make_line(plane.origin, plane.origin + plane.y_dir * l)
    z = Edge.make_line(plane.origin, plane.origin + plane.z_dir * l)
    return Compound.make_compound([x, y, z])


def plane_symbol(plane: Axis, l: float = 1) -> Compound:
    c = Edge.make_circle(l).located(plane.to_location())
    x = Edge.make_line(plane.origin, plane.origin + plane.x_dir * l / 2)
    y = Edge.make_line(plane.origin, plane.origin + plane.y_dir * l / 2)
    z = Edge.make_line(plane.origin, plane.origin + plane.z_dir * l)
    return Compound.make_compound([c, x, y, z])


Axis.symbol = property(axis_symbol)
Location.symbol = property(location_symbol)
Plane.symbol = property(plane_symbol)
