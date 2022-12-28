import numpy as np

from alg123d import *


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
    hinge_x1, hinge_x2 = 0.63, 0.87

    base_hinges = {
        "right_front": Pos(-hinge_x1 * width, -hinge_x1 * length),
        "right_middle": Pos(-hinge_x2 * width, 0),
        "right_back": Pos(-hinge_x1 * width, hinge_x1 * length),
        "left_front": Pos(hinge_x1 * width, -hinge_x1 * length),
        "left_middle": Pos(hinge_x2 * width, 0),
        "left_back": Pos(hinge_x1 * width, hinge_x1 * length),
    }

    stand_holes = {
        "front_stand": Pos(0, -0.8 * length),
        "back_stand": Pos(0, 0.75 * length),
    }

    def __init__(self):
        self.base_edges = {}
        self.stand_edges = {}

    def create(self):
        base = extrude(Ellipse(width, length), thickness)
        base -= Box(2 * width, 20, 3 * thickness) @ Pos(y=-length + 5)

        for name, pos in self.base_hinges.items():
            last = base.edges()
            base -= (
                Cylinder(diam / 2 + tol, thickness, centered=(True, True, False)) @ pos
            )
            self.base_edges[name] = (base.edges() - last).min()

        for name, pos in self.stand_holes.items():
            last = base.edges()
            base -= Box(width / 2 + 2 * tol, thickness + 2 * tol, 5 * thickness) @ pos
            self.stand_edges[name] = (base.edges() - last).min_group()

        base.mates = {
            f"{name}_hole": Mate(edge, name=name)
            for name, edge in self.base_edges.items()
        }
        base.mates.update(
            {
                f"{name}_hole": Mate(edge, name=name)
                for name, edge in self.stand_edges.items()
            }
        )
        base.mates["base"] = Mate(base.faces().max(), name="base") @ Pos(
            z=height + 2 * tol
        )
        base.mates["top"] = Mate(base.faces().min(), name="top")

        return base


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
            rect = Rectangle(thickness, self.h) @ Pos(0, i * w, t2)
            block = extrude(rect, self.h)
            stand += block

            m = block.edges().max_group()
            stand = chamfer(
                stand,
                m.min(Axis.Y) if i == 1 else m.max(Axis.Y),
                length=self.h - 2 * tol,
            )

        for plane in [Plane(faces[0]), Plane(faces[-1])]:
            stand += (
                Box(thickness, width / 2, thickness, centered=(True, True, False))
                @ plane
            )

        stand.mates = {"bottom": Mate(stand.faces().max(Axis.Y), name="bottom")}
        return stand


#
# Legs
#


class UpperLeg:
    def __init__(self):
        self.l1 = 50
        self.l2 = 80

    def create(self):
        points = [(0, 0), (0, height / 2), (self.l1, height / 2 - 5), (self.l2, 0)]
        leg_hole = Pos(self.l2 - 10, 0)

        line = Polyline(points)
        line += mirror(line, Plane.XZ)
        face = make_face(line)
        upper_leg = extrude(face, thickness / 2, both=True)
        upper_leg = fillet(upper_leg, upper_leg.edges().max(Axis.X), radius=4)

        last = upper_leg.edges()
        upper_leg -= Bore(upper_leg, diam / 2 + tol) @ leg_hole
        self.knee_hole = upper_leg.edges(GeomType.CIRCLE) - last

        upper_leg += Cylinder(diam / 2, 2 * (height / 2 + thickness + tol)) @ Rot(
            90, 0, 0
        )

        upper_leg.mates = {
            "knee_bottom": Mate(self.knee_hole.min(), name="knee_bottom"),
            "knee_top": Mate(self.knee_hole.max(), name="knee_top"),
            "hinge": Mate(upper_leg.faces().min(Axis.Y), name="hinge"),
        }

        return upper_leg


# %%
class LowerLeg:
    def __init__(self):
        self.w = 15
        self.l1 = 20
        self.l2 = 120

    def create(self):
        points = [(0, 0), (self.l1, self.w), (self.l2, 0)]
        leg_hole = Pos(self.l1 - 10, 0)

        line = Polyline(points)
        line += mirror(line, Plane.XZ)
        face = make_face(line)
        lower_leg = extrude(face, thickness / 2, both=True)
        lower_leg = fillet(lower_leg, lower_leg.edges(Axis.Z), radius=4)

        last = lower_leg.edges()
        lower_leg -= Bore(lower_leg, diam / 2 + tol) @ leg_hole
        self.knee_hole = (lower_leg.edges(GeomType.CIRCLE) - last).sort_by()

        lower_leg.mates = {
            "knee_bottom": Mate(self.knee_hole.min(), name="knee_bottom"),
            "knee_top": Mate(self.knee_hole.max(), name="knee_top"),
        }
        return lower_leg


base = Base().create()
stand = Stand().create()
upper_leg = UpperLeg().create()
lower_leg = LowerLeg().create()


#
# Assembly
#


hexapod = MAssembly(base, "base", color=Color("gray"), loc=Location())
hexapod.add(base, "top", color=Color(204, 204, 204))

for name, mate in base.mates.items():
    if name != "top":
        hexapod["/base"].mate(name, mate)
    else:
        hexapod["/base/top"].mate(name, mate)

rot = {"front_stand": Rot(180, 0, 90), "back_stand": Rot(180, 0, -90)}
for name in Base.stand_holes.keys():
    hexapod.add(stand, name=name, color=Color(128, 204, 230))

    hexapod[f"/base/{name}"].mate(name, stand.mates["bottom"] @ rot[name])

angles = {
    "right_back": 195,
    "right_middle": 180,
    "right_front": 165,
    "left_back": -15,
    "left_middle": 0,
    "left_front": 15,
}

for name in Base.base_hinges.keys():
    leg = MAssembly(upper_leg, name=f"{name}_leg")
    leg.add(lower_leg, name=f"lower_leg")
    hexapod.add(leg)

    hexapod[f"/base/{name}_leg"].mate(
        f"{name}_hinge",
        upper_leg.mates["hinge"] @ Rot(180, 0, angles[name]),
        origin=True,
    )
    hexapod[f"/base/{name}_leg"].mate(
        f"{name}_knee",
        upper_leg.mates["knee_top" if "right" in name else "knee_bottom"],
    )
    hexapod[f"/base/{name}_leg/lower_leg"].mate(
        f"{name}_lower_knee",
        lower_leg.mates["knee_bottom" if "right" in name else "knee_top"]
        @ Rot(0, 0, -75),
        origin=True,
    )

hexapod.relocate()

hexapod.assemble("top", "base")
hexapod.assemble("front_stand", "back_stand_hole")
hexapod.assemble("back_stand", "front_stand_hole")

for name in Base.base_hinges.keys():
    hexapod.assemble(f"{name}_hinge", f"{name}_hole")
    hexapod.assemble(f"{name}_lower_knee", f"{name}_knee")

if "show_object" in locals():
    show_object(hexapod)


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


animation = Animation(hexapod)

leg_group = ("left_front", "right_middle", "left_back")

for name in Base.base_hinges.keys():
    times, values = horizontal(4, "middle" in name)
    animation.add_track(f"/base/{name}_leg", "rz", times, values)

    times, values = vertical(8, 4, 0 if name in leg_group else 4)
    animation.add_track(f"/base/{name}_leg/lower_leg", "rz", times, values)

animation.animate(2)
