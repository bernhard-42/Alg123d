from build123d.direct_api import *
from build123d.build_enums import *


def _face_location(self):
    origin = self.center()
    x_dir = Vector(self._geom_adaptor().Position().XDirection())
    z_dir = self.normal_at(origin)
    return Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).to_location()


Face.location = property(_face_location)
