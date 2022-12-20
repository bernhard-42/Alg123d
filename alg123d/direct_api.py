from build123d.direct_api import *
from build123d.build_enums import *


def _face_center_location(self):
    origin = self.center()
    x_dir = Vector(self._geom_adaptor().Position().XDirection())
    z_dir = self.normal_at(origin)
    return Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).to_location()


Face.center_location = property(_face_center_location)


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
