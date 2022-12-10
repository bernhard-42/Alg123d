from alg123d import *
import alg123d.shortcuts as S
import build123d as bd
import cadquery as cq

# %%
r = Rectangle(1, 2)
b = extrude(r, 1, both=True)
# %%

c = cq.Workplane("XZ").circle(1).extrude(1)
s = c.solids()
f = c.faces()
e = c.edges()

a = S.from_cq(c)
a3 = S.from_cq(s)
a2 = S.from_cq(f)
a1 = S.from_cq(e)

print(a3.dim)
print(a2.dim)
print(a1.dim)
show(a, a1, a2, a3)

# %%


a = Cylinder(1, 1) @ Plane.XZ
s = a.solids()
f = a.faces()
e = a.edges()

c = S.to_cq(a)
c3 = S.to_cq(s)
c2 = S.to_cq(f)
c1 = S.to_cq(e)

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
a -= CounterBore(a, 0.2, 0.3, 0.3) @ Plane(S.max_face(a))

new_edges = S.diff(l, a.edges())
new_faces = S.diff(f, a.faces())
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
key_cap += S.min_solid(ribs - key_cap, wrapped=True)

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

s = Empty()
for i, outer_loc in enumerate(GridLocations(3, 3, 2, 2)):
    c_plane = plane * outer_loc * locs[i]
    s += Circle(1) @ c_plane

    for loc in PolarLocations(0.8, (i + 3) * 2):
        s -= Rectangle(0.1, 0.3) @ (c_plane * loc * Rotation(0, 0, 45))

e = extrude(s, 0.3)
show(e, reset_camera=False)

# %%

show(Empty() + Box(1, 1, 1))
# %%

show(Box(1, 2, 3) + Empty())

# %%

show(Box(2, 3, 1) - Empty())

# %%

show(Box(3, 2, 1) & Empty())

# %%

show(Empty() + Rectangle(1, 1))
# %%

show(Rectangle(1, 2) + Empty())

# %%

show(Rectangle(2, 2) - Empty())

# %%

show(Rectangle(2, 1) & Empty())

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
