from math import sin, pi
from alg123d import *
from cq_vscode import show, set_defaults

set_defaults(axes=True, axes0=True, transparent=False)
centered = (False, False, False)

# %%

import cadquery as cq

arch = cq.Workplane(origin=(20, 0, 0)).circle(2).revolve(180, (-20, 0, 0), (-20, -1, 0))
result = arch.center(-20, 0).workplane().rect(20, 4)
face = arch.faces().val()
result = result.extrude(face)
show(result)

# %%

show(Box(1, 2, 3))

# %%

show(Box(1, 2, 3, centered=centered))

# %%

show(Cylinder(1, 2))

# %%

show(Cylinder(1, 2, centered=centered))

# %%

show(Cylinder(1, 2).edges(), Cylinder(1, 2, 75))

# %%

show(Cylinder(1, 2, centered=centered).edges(), Cylinder(1, 2, 75, centered=centered))

# %%

show(Cone(1, 0.1, 1))

# %%

show(Cone(1, 0.1, 1, 75))

# %%

show(Cone(1, 0, 2))

# %%

show(Cone(1, 0, 2, centered=centered))

# %%

show(Sphere(1))

# %%

show(Sphere(1, arc_size2=45, arc_size3=75))

# %%

show(
    Sphere(1, centered=centered).faces(),
    Sphere(1, arc_size2=45, arc_size3=75, centered=centered),
    transparent=True,
)

# %%

show(Torus(1, 0.2))

# %%

show(Torus(1, 0.2, centered=centered))

# %%

show(
    Torus(1, 0.2, minor_start_angle=15, minor_end_angle=135, major_angle=90)
)  # OCC broken

# %%

show(Wedge(1, 1, 1, 0.1, 0.1, 0.5, 0.5), Box(1, 1, 1, centered=centered).edges())

# %%

s = Circle(1) + Circle(0.5) @ (0.9, 0) + Circle(0.5) @ (-0.7, 0) - Circle(0.5)

show(extrude(s, 0.1))
# loft

# %%

s1 = Rectangle(1, 1)
s2 = Rectangle(0.5, 2) @ (1, 0, 1)

l = loft([s1, s2])
show(s1.edges(), s2.edges(), l)

# %%

slice_count = 10
sections = [
    Circle(5 + 10 * sin(i * pi / slice_count)) @ (0, 0, 3 * i)
    for i in range(slice_count + 1)
]

l = loft(sections)

show(*[s.edges() for s in sections], l)

# revolve

# %%
s1 = Circle(0.1) @ (0, 0.5, 0)
r = revolve(s1, Axis.X, 90)
show(r)

# %%

s1 = Circle(0.1) @ (0, 0.5, 0)
r = revolve(s1, Axis.X, -130)
show(r)

# %%

s = Sphere(1) @ (0.9, 0.2, 0)
sections = section(s, [Plane.XZ, Plane.ZY, as_plane(Location((0, 1, 2), (60, 0, 0)))])
show(s, sections, transparent=True)


# %%

import build123d as bd

with bd.BuildPart() as bp:
    with bd.Locations(bd.Rotation(0, 180, 0)):
        with bd.BuildSketch() as sk:
            with bd.Locations((20, 0, 0)):
                bd.Circle(2)
        bd.Revolve(axis=bd.Axis.Y, revolution_arc=180)
        with bd.BuildSketch():
            bd.Rectangle(20, 4)
        bd.Extrude(amount=22)
        # bd.Extrude(until=bd.Until.NEXT)
show(bp)
# %%

c = Circle(2) @ (20, 0, 0)
a = revolve(c, Axis.Y, 180) @ Rotation(0, 180, 0)
r = Rectangle(20, 4)
a += extrude(r, 22)
show(r, a)
# %%
# %%
