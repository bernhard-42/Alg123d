from build123d.direct_api import *
from build123d.build_enums import *


def tupleize(arg):
    if isinstance(arg, (tuple, list)):
        return tuple(arg)
    else:
        return (arg,)


def as_plane(obj):
    if isinstance(obj, (Face, Location)):
        if isinstance(obj, Face):
            face = obj
            origin = face.center()
        else:
            face = Face.make_rect(1, 1).move(obj)
            origin = obj.position

        x_dir = Vector(face._geom_adaptor().Position().XDirection())
        z_dir = face.normal_at(origin)

        return Plane(origin=origin, x_dir=x_dir, z_dir=z_dir)

    elif isinstance(obj, Compound) and hasattr(obj, "location"):
        return as_plane(obj.location)


def as_planes(objs):
    return [as_plane(obj) for obj in objs]


def __plane_mul__(self, loc) -> Plane:
    if not isinstance(loc, Location):
        raise RuntimeError(
            "Planes can only be multiplied with Locations to relocate them"
        )
    return as_plane(self.to_location() * loc)


def __neg__axis__(self):
    return self.reverse()


Plane.__mul__ = __plane_mul__
Axis.__neg__ = __neg__axis__
