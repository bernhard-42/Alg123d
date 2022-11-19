from typing import overload

from build123d.direct_api import *

from build123d import Location as _Location

from OCP.gp import gp_EulerSequence, gp_Trsf
from OCP.TopLoc import TopLoc_Location

__all__ = [
    "Axis",
    "BoundBox",
    "Compound",
    "Edge",
    "Face",
    "Location",
    "Matrix",
    "Mixin1D",
    "Mixin3D",
    "Plane",
    "Rotation",
    "RotationLike",
    "Shape",
    "ShapeList",
    "Shell",
    "Solid",
    "SVG",
    "Vector",
    "VectorLike",
    "Vertex",
    "Wire",
]


class Location(_Location):
    @overload
    def __init__(self) -> None:  # pragma: no cover
        "Empty location with not rotation or translation with respect to the original location."
        ...

    @overload
    def __init__(self, location: "Location") -> None:  # pragma: no cover
        "Location with another given location."
        ...

    @overload
    def __init__(self, translation: VectorLike) -> None:  # pragma: no cover
        "Location with translation with respect to the original location."
        ...

    @overload
    def __init__(self, plane: Plane) -> None:  # pragma: no cover
        "Location corresponding to the location of the Plane."
        ...

    @overload
    def __init__(
        self, plane: Plane, plane_offset: VectorLike
    ) -> None:  # pragma: no cover
        "Location corresponding to the angular location of the Plane with translation plane_offset."
        ...

    @overload
    def __init__(self, top_loc: TopLoc_Location) -> None:  # pragma: no cover
        "Location wrapping the low-level TopLoc_Location object"
        ...

    @overload
    def __init__(self, gp_trsf: gp_Trsf) -> None:  # pragma: no cover
        "Location wrapping the low-level gp_Trsf object"
        ...

    @overload
    def __init__(
        self,
        translation: VectorLike,
        axis: VectorLike = (0, 0, 1),
        angle: float = 0,
    ) -> None:  # pragma: no cover
        """Location with translation and rotation around axis by angle
        with respect to the original location."""
        ...

    @overload
    def __init__(
        self,
        translation: VectorLike,
        rotation: RotationLike,
    ) -> None:  # pragma: no cover
        """Location with translation and rotation
        with respect to the original location."""
        ...

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], Location):
            super().__init__(args[0].wrapped)

        elif len(args) == 1 and kwargs.get("rotation") is not None:
            rot = kwargs["rotation"]
            rot = Rotation(*rot) if isinstance(rot, tuple) else rot
            pos = Location(args[0])
            self.wrapped = (pos * rot).wrapped

        elif len(args) == 1 and kwargs.get("angle") is not None:
            axis = kwargs.get("axis", (0, 0, 1))
            super().__init__(args[0], axis, kwargs["angle"])

        else:
            super().__init__(*args)

    def to_tuple(self) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        transformation = self.wrapped.Transformation()
        trans = transformation.TranslationPart()
        rot = transformation.GetRotation()

        rv_trans = (trans.X(), trans.Y(), trans.Z())
        rv_rot = rot.GetEulerAngles(gp_EulerSequence.gp_Intrinsic_XYZ)

        return rv_trans, rv_rot
