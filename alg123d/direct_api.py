from build123d.direct_api import *
from build123d.build_enums import *

LocationLike = Union[
    Location,
    Rotation,
    Tuple[float, float, Optional[float]],
    Tuple[Tuple[float, float, Optional[float]], Tuple[float, float, float]],
]


def tupleize(arg):
    if isinstance(arg, (tuple, list)):
        return tuple(arg)
    else:
        return (arg,)


def __neg__axis__(self):
    return self.reverse()


# Plane.__mul__ = __plane_mul__
Axis.__neg__ = __neg__axis__
