import numpy as np

from alg123d import *
import alg123d.shortcuts as S


# %%

thickness = 2
height = 40
width = 65
length = 100
diam = 4
tol = 0.05

#
# Base and top
#


class Base:
    def __init__(self):
        x1, x2 = 0.63, 0.87
        self.base_hinges = {
            "right_front": (-x1 * width, -x1 * length),
            "right_middle": (-x2 * width, 0),
            "right_back": (-x1 * width, x1 * length),
            "left_front": (x1 * width, -x1 * length),
            "left_middle": (x2 * width, 0),
            "left_back": (x1 * width, x1 * length),
        }
        self.base_edges = {}

        self.stand_holes = {
            "front_stand": (0, -0.8 * length),
            "back_stand": (0, 0.75 * length),
        }
        self.stand_edges = {}

        self.obj = None

    def create(self):
        base = extrude(Ellipse(width, length), thickness)
        base -= Box(2 * width, 20, 3 * thickness) @ (0, -length + 5, 0)

        for name, pos in self.base_hinges.items():
            last = base.edges()
            base -= (
                Cylinder(diam / 2 + tol, thickness, centered=(True, True, False)) @ pos
            )
            self.base_edges[name] = S.sort_min(S.diff(base.edges(), last))

        for name, pos in self.stand_holes.items():
            last = base.edges()
            base -= Box(width / 2 + 2 * tol, thickness + 2 * tol, 5 * thickness) @ pos
            self.stand_edges[name] = S.group_min(S.diff(base.edges(), last))

        self.obj = base
        return base

    def mates(self):
        m = {
            f"{name}_hole": Mate(edge, name=name)
            for name, edge in self.base_edges.items()
        }
        m2 = {
            f"{name}_hole": Mate(edge, name=name)
            for name, edge in self.stand_edges.items()
        }
        m.update(m2)
        m["base"] = Mate(S.max_face(self.obj), name="base") @ Location(
            (0, 0, height + 2 * tol)
        )
        m["top"] = Mate(S.min_face(self.obj), name="top")
        return m


_base = Base()
base = _base.create()
mates = _base.mates()
show(base, *mates.values(), clear=True, transparent=True)

# %%
#
# Stands
#


class Stand:
    def __init__(self):
        self.h = 5

    def create(self):
        stand = Box(width / 2 + 10, height + 2 * tol, thickness)
        faces = stand.faces().sort_by(Axis.Y)

        t2 = thickness / 2
        w = height / 2 + tol - self.h / 2
        for i in [-1, 1]:
            rect = Rectangle(thickness, self.h) @ (0, i * w, t2)
            block = extrude(rect, self.h)
            stand += block

            m = S.max_edges(block)
            stand = chamfer(
                stand,
                S.sort_min(m, Axis.Y) if i == 1 else S.sort_max(m, Axis.Y),
                length=self.h - 2 * tol,
            )

        for plane in [Plane(faces[0]), Plane(faces[-1])]:
            stand += (
                Box(thickness, width / 2, thickness, centered=(True, True, False))
                @ plane
            )

        self.obj = stand
        return stand

    def mates(self):
        return {"bottom": Mate(S.max_face(self.obj, Axis.Y), name="bottom")}


_stand = Stand()
stand = _stand.create()
mates = _stand.mates()
show(stand, *mates.values(), clear=True, transparent=True)

# %%
#
# Legs
#


class UpperLeg:
    def __init__(self):
        self.l1 = 50
        self.l2 = 80
        self.obj = None

    def create(self):
        points = [(0, 0), (0, height / 2), (self.l1, height / 2 - 5), (self.l2, 0)]
        leg_hole = (self.l2 - 10, 0)

        line = Polyline(points)
        line += mirror(line, Plane.XZ)
        face = make_face(line)
        upper_leg = extrude(face, thickness / 2, both=True)
        upper_leg = fillet(upper_leg, S.max_edge(upper_leg, Axis.X), radius=4)

        last = upper_leg.edges()
        upper_leg -= Bore(upper_leg, diam / 2 + tol) @ leg_hole
        self.knee_hole = (
            S.diff(upper_leg.edges(), last).filter_by(GeomType.CIRCLE).sort_by()
        )

        upper_leg += Cylinder(diam / 2, 2 * (height / 2 + thickness + tol)) @ Rotation(
            90, 0, 0
        )

        self.obj = upper_leg
        return upper_leg

    def mates(self):
        return {
            "knee_bottom": Mate(S.sort_min(self.knee_hole), name="knee_bottom"),
            "knee_top": Mate(S.sort_max(self.knee_hole), name="knee_top"),
            "hinge": Mate(S.min_face(self.obj, Axis.Y), name="hinge"),
        }


_upper_leg = UpperLeg()
upper_leg = _upper_leg.create()
mates = _upper_leg.mates()
show(upper_leg, *mates.values(), transparent=True, reset_camera=True)

# %%
class LowerLeg:
    def __init__(self):
        self.w = 15
        self.l1 = 20
        self.l2 = 120
        self.obj = None

    def create(self):
        points = [(0, 0), (self.l1, self.w), (self.l2, 0)]
        leg_hole = (self.l1 - 10, 0)

        line = Polyline(points)
        line += mirror(line, Plane.XZ)
        face = make_face(line)
        lower_leg = extrude(face, thickness / 2, both=True)
        lower_leg = fillet(lower_leg, lower_leg.edges().filter_by(Axis.Z), radius=4)

        last = lower_leg.edges()
        lower_leg -= Bore(lower_leg, diam / 2 + tol) @ leg_hole
        self.knee_hole = (
            S.diff(lower_leg.edges(), last).filter_by(GeomType.CIRCLE).sort_by()
        )

        self.obj = lower_leg
        return lower_leg

    def mates(self):
        return {
            "knee_bottom": Mate(S.sort_min(self.knee_hole), name="knee_bottom"),
            "knee_top": Mate(S.sort_max(self.knee_hole), name="knee_top"),
        }


_lower_leg = LowerLeg()
lower_leg = _lower_leg.create()
mates = _lower_leg.mates()
show(lower_leg, *mates.values(), transparent=True, reset_camera=False)

set_defaults(mate_scale=3)


# %%

#
# Assembly
#


hexapod = MAssembly(base, "bottom", color=Color("gray"), loc=Location())
hexapod.add(base, name="top", color=Color(204, 204, 204))

for name, mate in _base.mates().items():
    if name != "top":
        hexapod.mate("bottom", mate, name)
    else:
        hexapod.mate("top", mate, name)

r = {"front_stand": Rotation(180, 0, 90), "back_stand": Rotation(180, 0, -90)}
for name in _base.stand_holes.keys():
    hexapod.add(stand, name=name, color=Color(128, 204, 230))

    hexapod.mate(name, _stand.mates()["bottom"] @ r[name], name)

angles = {
    "right_back": 195,
    "right_middle": 180,
    "right_front": 165,
    "left_back": -15,
    "left_middle": 0,
    "left_front": 15,
}

for name in _base.base_hinges.keys():
    leg = MAssembly(upper_leg, name=f"{name}_leg")
    leg.add(lower_leg, name=f"lower_leg")
    hexapod.add(leg)

    hexapod.mate(
        f"{name}_leg",
        _upper_leg.mates()["hinge"] @ Rotation(180, 0, angles[name]),
        f"{name}_hinge",
        origin=True,
    )
    hexapod.mate(f"{name}_leg", _upper_leg.mates()["knee_top"], f"{name}_knee")

    hexapod.mate(
        f"{name}_leg/lower_leg",
        _lower_leg.mates()["knee_bottom"] @ Rotation(0, 0, -75),
        f"{name}_lower_knee",
        origin=True,
    )

hexapod.relocate()

hexapod.assemble("top", "base")
hexapod.assemble("front_stand", "back_stand_hole")
hexapod.assemble("back_stand", "front_stand_hole")

for name in _base.base_hinges.keys():
    hexapod.assemble(f"{name}_hinge", f"{name}_hole")
    hexapod.assemble(f"{name}_lower_knee", f"{name}_knee")

show(hexapod, render_mates=True, mate_scale=3, reset_camera=True)

show(hexapod, render_mates=True, mate_scale=5, reset_camera=True)

# %%

#
# Animation
#


def time_range(end, count):
    return np.linspace(0, end, count + 1)


def vertical(count, end, offset):
    ints = [min(180, (90 + i * (360 // count)) % 360) for i in range(count)]
    heights = [round(20 * np.sin(np.deg2rad(x) - 15), 1) for x in ints]
    heights.append(heights[0])
    return time_range(end, count), heights[offset:] + heights[1 : offset + 1]


def horizontal(end, reverse):
    horizontal_angle = 25
    angle = horizontal_angle if reverse else -horizontal_angle
    return time_range(end, 4), [0, angle, 0, -angle, 0]


animation = Animation()

leg_group = ("left_front", "right_middle", "left_back")

for name in _base.base_hinges.keys():
    times, values = horizontal(4, "middle" in name)
    animation.add_track(f"/bottom/{name}_leg", "rz", times, values)

    times, values = vertical(8, 4, 0 if name in leg_group else 4)
    animation.add_track(f"/bottom/{name}_leg/lower_leg", "rz", times, values)

animation.animate(2)

# %%
