from alg123d import *
from typing import Union, Tuple

set_defaults(axes=True, axes0=True)

# %%

s = 2


class Club(AlgCompound):
    def __init__(
        self,
        height: float,
        align: Union[Align, Tuple[Align, Align]] = None,
    ):
        l0 = Line((0, -188), (76, -188))
        b0 = Bezier((l0 @ 1, (61, -185), (33, -173), (17, -81)))
        b1 = Bezier((b0 @ 1, (49, -128), (146, -145), (167, -67)))
        b2 = Bezier((b1 @ 1, (187, 9), (94, 52), (32, 18)))
        b3 = Bezier((b2 @ 1, (92, 57), (113, 188), (0, 188)))
        club = l0 + b0 + b1 + b2 + b3
        club += mirror(club, about=Plane.YZ)
        club = make_face(club)
        club = scale(club, by=height / club.bounding_box().size.Y)

        super().__init__(club)
        self._align(align)


class Spade(AlgCompound):
    def __init__(
        self,
        height: float,
        align: Union[Align, Tuple[Align, Align]] = None,
    ):
        b0 = Bezier(((0, 198), (6, 190), (41, 127), (112, 61)))
        b1 = Bezier((b0 @ 1, (242, -72), (114, -168), (11, -105)))
        b2 = Bezier((b1 @ 1, (31, -174), (42, -179), (53, -198)))
        l0 = Line(b2 @ 1, (0, -198))
        spade = l0 + b0 + b1 + b2
        spade += mirror(spade, about=Plane.YZ)
        spade = make_face(spade)
        spade = scale(spade, by=height / spade.bounding_box().size.Y)

        super().__init__(spade)
        self._align(align)


class Heart(AlgCompound):
    def __init__(
        self,
        height: float,
        align: Union[Align, Tuple[Align, Align]] = None,
    ):
        b1 = Bezier(((0, 146), (20, 169), (67, 198), (97, 198)))
        b2 = Bezier((b1 @ 1, (125, 198), (151, 186), (168, 167)))
        b3 = Bezier((b2 @ 1, (197, 133), (194, 88), (158, 31)))
        b4 = Bezier((b3 @ 1, (126, -13), (94, -48), (62, -95)))
        b5 = Bezier((b4 @ 1, (40, -128), (0, -198)))
        heart = b1 + b2 + b3 + b4 + b5
        heart += mirror(heart, about=Plane.YZ)
        heart = make_face(heart)
        heart = scale(heart, by=height / heart.bounding_box().size.Y)

        super().__init__(heart)
        self._align(align)


class Diamond(AlgCompound):
    def __init__(
        self,
        height: float,
        align: Union[Align, Tuple[Align, Align]] = None,
    ):
        diamond = Bezier(((135, 0), (94, 69), (47, 134), (0, 198)))
        diamond += mirror(diamond, about=Plane.XZ)
        diamond += mirror(diamond, about=Plane.YZ)
        diamond = make_face(diamond)
        diamond = scale(diamond, by=height / diamond.bounding_box().size.Y)

        super().__init__(diamond)
        self._align(align)


# %%

club = Club(s, align=Align.MAX)
spade = Spade(s, align=Align.MAX)
heart = Heart(s, align=Align.MAX)
diamond = Diamond(s, align=Align.MAX)

faces = [
    Pos(-s, -s) * club,
    Pos(-s, s) * spade,
    Pos(s, -s) * heart,
    Pos(s, s) * diamond,
]

show(faces, extrude(faces, 1, dir=(0, 0, -1)), alphas=[0.9, 0.3])

# %%
