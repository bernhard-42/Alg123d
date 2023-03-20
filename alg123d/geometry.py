from typing import List

from build123d.build_enums import *
from build123d.topology import *

# Classes coverage:
#  - Vector
#  - Axis
#  - BoundBox
#  - Color
#  - Location
#  - Rotation(Location)
#  - Matrix
#  - Plane


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


def _location__mul__(self, other: Union[Location, Shape]) -> Union[Location, Shape]:
    """Combine locations or move shape (premultiply with self)"""
    if isinstance(other, Location):
        return Location(self.wrapped * other.wrapped)

    elif isinstance(other, Shape):
        if other._dim == 3:
            return copy.copy(other).move(self)
        else:
            return other.moved(self)

    else:
        raise TypeError(
            "Locations can only be multiplied with Locations or Shapes to relocate them"
        )


Location.x_axis = property(_location_x_axis)
Location.y_axis = property(_location_y_axis)
Location.z_axis = property(_location_z_axis)
Location.plane = property(_location_plane)
Location.__mul__ = _location__mul__


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


def _plane__mul__(self, other: Union[Location, Shape]) -> Union[Plane, Shape]:
    if isinstance(other, Location):
        return Plane(self.to_location() * other)

    elif isinstance(other, Shape):
        return self.to_location() * other

    else:
        raise TypeError("Planes can only be multiplied with Locations to relocate them")


Plane.location = property(_plane_location)
Plane.__mul__ = _plane__mul__


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
    circle = Edge.make_circle(l * 0.8).locate(loc)
    axes = SVG.axes(axes_scale=l).locate(loc)

    return Compound.make_compound(list(axes) + [circle])


Axis.symbol = axis_symbol
Location.symbol = location_symbol
Plane.symbol = plane_symbol
