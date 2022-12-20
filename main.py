from alg123d import *
from alg123d.shortcuts import *

import build123d as bd
import cadquery as cq
import time

# %%
def _face_center_location(self):
    origin = self.center()
    x_dir = Vector(self._geom_adaptor().Position().XDirection())
    z_dir = self.normal_at(origin)
    return Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).to_location()


Face.center_location = property(_face_center_location)
# %%

with bd.BuildSketch() as s:
    with bd.Locations(bd.Location((1, 2, 3), (10, 20, 30))):
        bd.Rectangle(1, 2)
show(s)

# %%
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
# %%

from build123d import *
from build123d.joints import JointBox

base: JointBox = JointBox(10, 10, 10, taper=3).locate(
    Location(Vector(1, 1, 1), (1, 1, 1), 30)
)
base_top_edges: ShapeList[Edge] = (
    base.edges().filter_by(Axis.X, tolerance=30).sort_by(Axis.Z)[-2:]
)

show(base, base_top_edges)


# %%
loc = Location(Vector(1, 1, 1), (1, 1, 1), 30)
base: JointBox = JointBox(10, 10, 10, taper=3).locate(loc)

base_top_edges: ShapeList[Edge] = (
    base.edges().group_by(loc.z_axis)[-1].filter_by(loc.x_axis)
)
show(base, base_top_edges)

# %%
class JointBox(AlgCompound):
    def __init__(
        self,
        length: float,
        width: float,
        height: float,
        radius: float = 0.0,
    ):
        # Store the attributes so the object can be copied
        self.length = length
        self.width = width
        self.height = height
        self.joints: dict[str, Joint] = {}

        # Create the object
        obj = Solid.make_box(length, width, height, Plane((-length / 2, -width / 2, 0)))
        if radius != 0.0:
            obj = obj.fillet(radius, obj.edges())
        hole = Solid.make_cylinder(width / 4, length, Plane.YZ.offset(-length / 2))
        obj = obj.cut(hole)

        super().__init__(obj)


# %%
#
# Base Object
#

base = JointBox(10, 10, 10).locate(Location(Vector(1, 1, 1), (1, 1, 1), 30))
base.joints = {}
base_top_edges = group_max(base.edges(), z_axis(base)).filter_by(x_axis(base))

# %%

#
# Rigid Joint
#
fixed_arm = JointBox(1, 1, 5)

j1 = RigidJoint("side", base, max_face(base, x_axis(base)).location)
j2 = RigidJoint("top", fixed_arm, max_face(fixed_arm, Axis.Z).location * Rot(x=180))

j1.connect_to(j2)

show(base, fixed_arm, j1.symbol, j2.symbol)
# %%
#
# Hinge
#
hinge_arm = JointBox(2, 1, 10)
swing_arm_hinge_axis = max_edge(min_face(hinge_arm, Axis.X), Axis.Y).to_axis()
base_hinge_axis = max_edge(max_face(base, x_axis(base)), y_axis(base)).to_axis()

j3 = RevoluteJoint("hinge", base, axis=base_hinge_axis, range=(0, 360))
j4 = RigidJoint("corner", hinge_arm, swing_arm_hinge_axis.to_location())

j3.connect_to(j4, angle=180)

show(base, hinge_arm, j3.symbol, j4.symbol)
# show(base, fixed_arm, hinge_arm, j1.symbol, j2.symbol, j3.symbol, j4.symbol)

# %%
#
# Slider
#
slider_arm = JointBox(4, 1, 2, 0.2)
s1 = LinearJoint(
    "slide",
    base,
    axis=Edge.make_mid_way(*base_top_edges, 0.67).to_axis(),
    range=(0, 10),
)
s2 = RigidJoint("slide", slider_arm, Location(Vector(0, 0, 0)))
s1.connect_to(s2, 8)

#
# Cylindrical
#
hole_axis = Axis(
    base.faces().sort_by(Axis.Y)[0].center(),
    -base.faces().sort_by(Axis.Y)[0].normal_at(),
)
screw_arm = JointBox(1, 1, 10, 0.49)
j5 = CylindricalJoint("hole", base, hole_axis, linear_range=(-10, 10))
j6 = RigidJoint("screw", screw_arm, screw_arm.faces().sort_by(Axis.Z)[-1].location)
j5.connect_to(j6, -1, 90)

#
# PinSlotJoint
#
j7 = LinearJoint(
    "slot",
    base,
    axis=Edge.make_mid_way(*base_top_edges, 0.33).to_axis(),
    range=(0, 10),
)
pin_arm = JointBox(2, 1, 2)
j8 = RevoluteJoint("pin", pin_arm, axis=Axis.Z, range=(0, 360))
j7.connect_to(j8, position=6, angle=60)

if "show_object" in locals():
    show_object(base, name="base", options={"alpha": 0.8}, clear=True)
    show_object(base.joints["side"].symbol, name="side joint")
    show_object(base.joints["hinge"].symbol, name="hinge joint")
    show_object(base.joints["slide"].symbol, name="slot joint")
    show_object(base.joints["slot"].symbol, name="pin slot joint")
    show_object(fixed_arm, name="fixed_arm", options={"alpha": 0.6})
    show_object(hinge_arm, name="hinge_arm", options={"alpha": 0.6})
    show_object(slider_arm, name="slider_arm", options={"alpha": 0.6})
    show_object(pin_arm, name="pin_arm", options={"alpha": 0.6})
    show_object(slider_arm.joints["slide"].symbol, name="slider attachment")
    show_object(pin_arm.joints["pin"].symbol, name="pin axis")
    show_object(screw_arm, name="screw_arm")
    show_object(base.joints["hole"].symbol, name="hole")

# %%
c1 = Circle(10)
c2 = Circle(10) @ Pos(7, 9)
c3 = Circle(10) @ Pos(-7, 9)
show(c1, c2, c3)

# %%
a = extrude(Rectangle(10, 20), 10, both=True)
a.mates["top"] = Mate(max_face(a), name="top")

c = Cone(2, 1, 10)
c.mates["top"] = Mate(max_face(c), name="top") @ Rot(x=180)
show(a, c, *a.mates.values(), *c.mates.values(), transparent=True)

# %%

c2 = c.moved(c.mates["top"].loc * a.mates["top"].loc.inverse())
show(a, c2, transparent=True)

# %%


with bd.BuildPart() as a2:
    with bd.BuildSketch() as s:
        bd.Rectangle(1, 2)
    bd.Extrude(amount=1, both=True)

show(a2.part.wrapped)

# %%
from alg123d.wrappers import create_compound


def extr(
    to_extrude: Compound,
    amount: float = None,
    both: bool = False,
    taper: float = 0.0,
):
    faces = [to_extrude] if isinstance(to_extrude, Face) else to_extrude.faces()
    compound = create_compound(
        bd.Extrude,
        dim=3,
        faces=faces,
        planes=[Plane(face) for face in faces],
        params=dict(amount=amount, both=both, taper=taper),
    )
    return compound


a = extr(Rectangle(1, 2), 0.1, both=True)
show(a)
# %%
r = Rectangle(1, 2)
b = extrude(r, 1, both=True)
# %%

c = cq.Workplane("XZ").circle(1).extrude(1)
s = c.solids()
f = c.faces()
e = c.edges()

a = from_cq(c)
a3 = from_cq(s)
a2 = from_cq(f)
a1 = from_cq(e)

print(a3.dim)
print(a2.dim)
print(a1.dim)
show(a, a1, a2, a3)

# %%


a = Cylinder(1, 1) @ Plane.XZ
s = a.solids()
f = a.faces()
e = a.edges()

c = to_cq(a)
c3 = to_cq(s)
c2 = to_cq(f)
c1 = to_cq(e)

show(c3, c2, c1, show_parent=False)

# %%

with bd.BuildPart() as flange:
    with bd.BuildSketch(Plane.XZ):
        with bd.BuildLine() as l:
            p = bd.Polyline((-2, 5), (-12, 5), (-12, 10), (10, 10))
            bd.Offset(amount=1)
        bd.MakeFace()
    bd.Extrude(amount=10, both=True)

with bd.BuildPart() as ex:
    with bd.BuildSketch() as obj_under_test:
        bd.Rectangle(8, 8)
    bd.Extrude(amount=20)  # (1) extrude beyond top face

with bd.BuildPart() as ex2:
    bd.Add(ex.part)
    bd.Add(
        flange.part, mode=bd.Mode.SUBTRACT
    )  # (2) subtract flange from the extruded solid

with bd.BuildPart() as flange2:
    bd.Add(ex2.solids().sort_by()[0])  # and the take the bottom solid and add flange
    bd.Add(flange.part)

show(flange2)


# %%
a = Box(1, 2, 3)
l, f = a.edges(), a.faces()
a -= CounterBore(a, 0.2, 0.3, 0.3) @ Plane(max_face(a))

new_edges = diff(l, a.edges())
new_faces = diff(f, a.faces())
show(a, *new_edges, *new_faces, transparent=True)

# %%

plan = Rectangle(18 * MM, 18 * MM)
key_cap = extrude(plan, amount=10 * MM, taper=15)

# Create a dished top
key_cap -= Sphere(40 * MM) @ Location((0, -3 * MM, 47 * MM), (90, 0, 0))

# Fillet all the edges except the bottom
key_cap = fillet(
    key_cap,
    key_cap.edges().filter_by_position(Axis.Z, 0, 30 * MM, inclusive=(False, True)),
    radius=1 * MM,
)

# Hollow out the key by subtracting a scaled version
key_cap -= scale(key_cap, by=(0.925, 0.925, 0.85))


# Add supporting ribs while leaving room for switch activation
ribs = Rectangle(17.5 * MM, 0.5 * MM)
ribs += Rectangle(0.5 * MM, 17.5 * MM)
ribs += Circle(radius=5.51 * MM / 2)

ribs = extrude(ribs @ (0, 0, 4), 10)
key_cap += min_solid(ribs - key_cap, wrapped=True)

# Find the face on the bottom of the ribs to build onto
rib_bottom = key_cap.faces().filter_by_position(Axis.Z, 4 * MM, 4 * MM)[0]

plane = Plane(rib_bottom)
socket = Circle(radius=5.5 * MM / 2)
socket -= Rectangle(4.1 * MM, 1.17 * MM)
socket -= Rectangle(1.17 * MM, 4.1 * MM)
key_cap += extrude(socket @ plane, amount=3.5 * MM)

show(key_cap, transparent=True)

# %%
pts = [(0, 1), (1, 0), (1, 1), (0, 1)]
show(Polygon(pts))

plane = Plane.ZX
# %%

cyl = Cylinder(1, 0.5)
box = Box(0.3, 0.3, 0.5)

# %%

p = cyl @ plane

for loc in PolarLocations(0.7, 10):
    p -= box @ (plane * loc)

show(p)
# %%

show(p, p.faces().group_by(Axis.Y)[0], transparent=True)

# %%

locs = [Location((0, 0, 0), (0, a, 0)) for a in (0, 45, 90, 135)]

s = Zero()
for i, outer_loc in enumerate(GridLocations(3, 3, 2, 2)):
    c_plane = plane * outer_loc * locs[i]
    s += Circle(1) @ c_plane

    for loc in PolarLocations(0.8, (i + 3) * 2):
        s -= Rectangle(0.1, 0.3) @ (c_plane * loc * Rotation(0, 0, 45))

e = extrude(s, 0.3)
show(e, reset_camera=False)

# %%

show(Zero() + Box(1, 1, 1))
# %%

show(Box(1, 2, 3) + Zero())

# %%

show(Box(2, 3, 1) - Zero())

# %%

show(Box(3, 2, 1) & Zero())

# %%

show(Zero() + Rectangle(1, 1))
# %%

show(Rectangle(1, 2) + Zero())

# %%

show(Rectangle(2, 2) - Zero())

# %%

show(Rectangle(2, 1) & Zero())

# %%

from build123d import *
from cq_vscode import show
import time

s = time.time()
with BuildPart() as key_cap:
    # Start with the plan of the key cap and extrude it
    with BuildSketch() as plan:
        Rectangle(18 * MM, 18 * MM)
    Extrude(amount=10 * MM, taper=15)
    # Create a dished top
    with Locations((0, -3 * MM, 47 * MM)):
        Sphere(40 * MM, mode=Mode.SUBTRACT, rotation=(90, 0, 0))
    # Fillet all the edges except the bottom
    Fillet(
        *key_cap.edges().filter_by_position(
            Axis.Z, 0, 30 * MM, inclusive=(False, True)
        ),
        radius=1 * MM,
    )
    # Hollow out the key by subtracting a scaled version
    Scale(by=(0.925, 0.925, 0.85), mode=Mode.SUBTRACT)

with BuildPart() as ribs:
    # Add supporting ribs while leaving room for switch activation
    with Workplanes(Plane(origin=(0, 0, 4 * MM))):
        with BuildSketch():
            Rectangle(17.5 * MM, 0.5 * MM)
            Rectangle(0.5 * MM, 17.5 * MM)
            Circle(radius=5.51 * MM / 2)
    # Extrude the mount and ribs to the key cap underside
    # Extrude(until=Until.NEXT)
    Extrude(amount=10)
    Add(key_cap.part, mode=Mode.SUBTRACT)

with BuildPart() as key_cap2:
    Add(ribs.solids().sort_by()[0])
    Add(key_cap.part)

    # Find the face on the bottom of the ribs to build onto
    rib_bottom = key_cap2.faces().filter_by_position(Axis.Z, 4 * MM, 4 * MM)[0]
    # Add the switch socket
    with Workplanes(rib_bottom):
        with BuildSketch() as cruciform:
            Circle(radius=5.5 * MM / 2)
            Rectangle(4.1 * MM, 1.17 * MM, mode=Mode.SUBTRACT)
            Rectangle(1.17 * MM, 4.1 * MM, mode=Mode.SUBTRACT)
    Extrude(amount=3.5 * MM, mode=Mode.ADD)
print(time.time() - s)

show(key_cap2, transparent=True, reset_camera=False)

# %%

s = time.time()

with BuildPart() as key_cap:
    # Start with the plan of the key cap and extrude it
    with BuildSketch() as plan:
        Rectangle(18 * MM, 18 * MM)
    Extrude(amount=10 * MM, taper=15)
    # Create a dished top
    with Locations((0, -3 * MM, 47 * MM)):
        Sphere(40 * MM, mode=Mode.SUBTRACT, rotation=(90, 0, 0))
    # Fillet all the edges except the bottom
    Fillet(
        *key_cap.edges().filter_by_position(
            Axis.Z, 0, 30 * MM, inclusive=(False, True)
        ),
        radius=1 * MM,
    )
    # Hollow out the key by subtracting a scaled version
    Scale(by=(0.925, 0.925, 0.85), mode=Mode.SUBTRACT)

    # Add supporting ribs while leaving room for switch activation
    with Workplanes(Plane(origin=(0, 0, 4 * MM))):
        with BuildSketch():
            Rectangle(17.5 * MM, 0.5 * MM)
            Rectangle(0.5 * MM, 17.5 * MM)
            Circle(radius=5.51 * MM / 2)
    # Extrude the mount and ribs to the key cap underside
    t2 = time.time()
    Extrude(until=Until.NEXT)
    print(time.time() - t2)
    # Find the face on the bottom of the ribs to build onto
    rib_bottom = key_cap.faces().filter_by_position(Axis.Z, 4 * MM, 4 * MM)[0]
    # Add the switch socket
    with Workplanes(rib_bottom):
        with BuildSketch() as cruciform:
            Circle(radius=5.5 * MM / 2)
            Rectangle(4.1 * MM, 1.17 * MM, mode=Mode.SUBTRACT)
            Rectangle(1.17 * MM, 4.1 * MM, mode=Mode.SUBTRACT)
    Extrude(amount=3.5 * MM, mode=Mode.ADD)
print(time.time() - s)

show(key_cap, transparent=True, reset_camera=False)
# %%
def __neg__axis__(self):
    return self.reverse()


Axis.__neg__ = __neg__axis__

# %%

with BuildPart() as bp:
    with BuildSketch() as sk:
        with Locations((20, 0, 0)):
            Circle(2)
    Revolve(axis=-Axis.Y, revolution_arc=180)
    with BuildSketch():
        Rectangle(20, 4)
    Extrude(until=Until.NEXT)

# %%

# %%

import build123d as bd

with bd.BuildPart() as bp:
    with bd.BuildSketch() as sk:
        with bd.Locations((20, 0, 0)):
            bd.Circle(2)
    bd.Revolve(axis=-bd.Axis.Y, revolution_arc=180)

with bd.BuildPart() as ex:
    with bd.BuildSketch():
        bd.Rectangle(20, 4)
    bd.Extrude(amount=30)
    bd.Add(bp.part, mode=bd.Mode.SUBTRACT)

with bd.BuildPart() as result:
    bd.Add(ex.solids().sort_by()[0])
    bd.Add(bp.part)

show(result)

# %%
set_defaults(reset_camera=False)
with bd.BuildSketch() as s:
    r = bd.Rectangle(1, 2)
    bd.Offset(amount=0.1, mode=bd.Mode.SUBTRACT)  # Fails with s.sketch.faces == []
# show(s, r.located(Location((1.5, 0, 0))))
print(list(s.sketch) == [])

# %%

with bd.BuildSketch() as s:
    r = bd.Rectangle(1, 2)
    bd.Offset(amount=-0.1, mode=bd.Mode.SUBTRACT)  # ok, face with holoe
show(s, r.located(Location((1.5, 0, 0))))

# %%

with bd.BuildSketch() as s:
    r = bd.Rectangle(1, 2)
    bd.Offset(amount=0.1, mode=bd.Mode.ADD)  # ok, larger face, same as mode=REPLACE
show(s, r.located(Location((1.5, 0, 0))))

# %%
with bd.BuildSketch() as s:
    r = bd.Rectangle(1, 2)
    bd.Offset(amount=-0.1, mode=bd.Mode.ADD)  # useless
show(s, r.located(Location((1.5, 0, 0))))

# %%
with bd.BuildSketch() as s:
    r = bd.Rectangle(1, 2)
    bd.Offset(amount=0.1, mode=bd.Mode.REPLACE)  # ok, larger face, same as mode=ADD
show(s, r.located(Location((1.5, 0, 0))))

# %%
with bd.BuildSketch() as s:
    r = bd.Rectangle(1, 2)
    bd.Offset(amount=-0.1, mode=bd.Mode.REPLACE)  # ok, smaller face
show(s, r.located(Location((1.5, 0, 0))))

# %%


# %%

with bd.BuildPart() as p:
    b = bd.Box(1, 2, 3)
    bd.Offset(amount=0.1, mode=bd.Mode.SUBTRACT)  # useless
b.locate(Location((1.5, 0, 0)))
show(p, b)

# %%

with bd.BuildPart() as p:
    b = bd.Box(1, 2, 3)
    bd.Offset(amount=-0.1, mode=bd.Mode.SUBTRACT)  # ok, smaller box
b.locate(Location((1.5, 0, 0)))
show(p, b)

# %%

with bd.BuildPart() as p:
    b = bd.Box(1, 2, 3)
    bd.Offset(amount=0.1, mode=bd.Mode.ADD)  # ok, larger box
b.locate(Location((1.5, 0, 0)))
show(p, b)

# %%
with bd.BuildPart() as p:
    b = bd.Box(1, 2, 3)
    bd.Offset(amount=-0.1, mode=bd.Mode.ADD)  # useless
b.locate(Location((1.5, 0, 0)))
show(p, b)

# %%
with bd.BuildPart() as p:
    b = bd.Box(1, 2, 3)
    bd.Offset(amount=0.1, mode=bd.Mode.REPLACE)  # ok, larger hollow box
b.locate(Location((1.5, 0, 0)))
show(p, b)

# %%
with bd.BuildPart() as p:
    b = bd.Box(1, 2, 3)
    bd.Offset(amount=-0.1, mode=bd.Mode.REPLACE)  # ok, same box, but hollow
b.locate(Location((1.5, 0, 0)))
show(p, b)

# %%
