from alg123d import *

set_defaults(transparent=True, axes=False, axes0=True)


class JointBox(AlgCompound):
    def __init__(
        self,
        length: float,
        width: float,
        height: float,
        radius: float = 0.0,
        taper: float = 0.0,
    ):
        # Store the attributes so the object can be copied
        self.length = length
        self.width = width
        self.height = height

        # Create the object
        rect = Rectangle(length, width)
        obj = extrude(rect, amount=height, taper=taper)
        if radius != 0.0:
            obj = fillet(obj, obj.edges(), radius)
        obj -= Cylinder(width / 4, length) @ Rot(y=90)

        super().__init__(obj)


# %%
loc = Location(Vector(1, 1, 1), (1, 0.1, 1), 30)

base = JointBox(10, 10, 10, taper=3).locate(loc)
# base_top_edges = base.edges().filter_by(Axis.X, tolerance=30).sort_by(Axis.Z)[-2:]
base_top_edges = base.edges(loc.x_axis).max_group(loc.z_axis)

show(base, base_top_edges)
# %%
#
# Rigid Joint
#
fixed_arm = JointBox(1, 1, 5, 0.2)
j1 = RigidJoint("side", base, base.faces().max(loc.x_axis).center_location)
# j2 = RigidJoint("top", fixed_arm, (-Plane(fixed_arm.faces().sort_by(Axis.Z)[-1])).to_location())
j2 = RigidJoint("top", fixed_arm, fixed_arm.faces().max().center_location * Rot(x=180))
base.joints["side"].connect_to(fixed_arm.joints["top"])
j1.connect_to(j2)

show(base, fixed_arm, j1.symbol, j2.symbol)
# %%
#
# Hinge
#
hinge_arm = JointBox(2, 1, 10, taper=1)
# swing_arm_hinge_edge: Edge = hinge_arm.edges().group_by(SortBy.LENGTH)[-1].sort_by(Axis.X)[-2:].sort_by(Axis.Y)[0]
swing_arm_hinge_edge: Edge = hinge_arm.faces().max(Axis.Y).edges().max(Axis.X)
swing_arm_hinge_axis = swing_arm_hinge_edge.to_axis()
# base_corner_edge = base.edges().sort_by(Axis((0, 0, 0), (1, 1, 0)))[-1]
base_corner_edge = base.faces().max(loc.x_axis).edges().max(loc.y_axis)
base_hinge_axis = base_corner_edge.to_axis()
j3 = RevoluteJoint("hinge", base, axis=base_hinge_axis, range=(0, 180))
j4 = RigidJoint("corner", hinge_arm, swing_arm_hinge_axis.to_location())
j3.connect_to(j4, angle=90)

show(base, hinge_arm, j3.symbol, j4.symbol)
# %%
#
# Slider
#
slider_arm = JointBox(4, 1, 2, 0.2)
s1 = LinearJoint(
    "slide",
    base,
    axis=Edge.make_mid_way(*base_top_edges, 0.67).to_axis(),
    range=(0, base_top_edges[0].length),
)
s2 = RigidJoint("slide", slider_arm, Location(Vector(0, 0, 0)))
s1.connect_to(s2, 7)

show(base, slider_arm, s1.symbol, s2.symbol)
# %%
#
# Cylindrical
#
hole_axis = Axis(
    base.faces().min(Axis.Y).center(),
    base.faces().min(Axis.Y).normal_at(),
)
screw_arm = JointBox(1, 1, 10, 0.49)
j5 = CylindricalJoint("hole", base, hole_axis, linear_range=(-10, 10))
j6 = RigidJoint("screw", screw_arm, screw_arm.faces().max().center_location)
j5.connect_to(j6, position=-4, angle=90)

show(base, screw_arm, j5.symbol, j6.symbol)

# %%
#
# PinSlotJoint
#
j7 = LinearJoint(
    "slot",
    base,
    axis=Edge.make_mid_way(*base_top_edges, 0.33).to_axis(),
    range=(0, base_top_edges[0].length),
)
pin_arm = JointBox(2, 1, 2)
j8 = RevoluteJoint("pin", pin_arm, axis=Axis.Z, range=(0, 360))
j7.connect_to(j8, position=6, angle=60)

show(base, pin_arm, j7.symbol, j8.symbol)

# %%
#
# BallJoint
#
j9 = BallJoint("socket", base, base.faces().min(Axis.X).center_location)
ball = JointBox(2, 2, 2, 0.99)
j10 = RigidJoint("ball", ball, Location(Vector(0, 0, 1)))
j9.connect_to(j10, angles=(10, 20, 30))

show(base, ball, j9.symbol, j10.symbol)

# %%
