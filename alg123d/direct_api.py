from build123d.direct_api import *
from build123d.build_enums import *

#
# The world location of a face at the center
#


def _face_center_location(self) -> Location:
    origin = self.center()
    x_dir = Vector(self._geom_adaptor().Position().XDirection())
    z_dir = self.normal_at(origin)
    return Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).to_location()


Face.center_location = property(_face_center_location)

#
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
