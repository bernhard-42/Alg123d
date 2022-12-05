from math import sin, pi
from alg123d import *
import alg123d.shortcuts as S
from cq_vscode import show, set_defaults

set_defaults(axes=True, axes0=True, transparent=False)

# %%

show(Box(1, 2, 3))

# %%

show(Box(1, 2, 3, centered=False))

# %%

show(Cylinder(1, 2))

# %%

show(Cylinder(1, 2, centered=False))

# %%

show(Cylinder(1, 2).edges(), Cylinder(1, 2, 75))

# %%

show(Cylinder(1, 2, centered=False).edges(), Cylinder(1, 2, 75, centered=False))

# %%

show(Cone(1, 0.1, 1))

# %%

show(Cone(1, 0.1, 1, 75))

# %%

show(Cone(1, 0, 2))

# %%

show(Cone(1, 0, 2, centered=False))

# %%

show(Sphere(1))

# %%

show(Sphere(1, arc_size2=45, arc_size3=75))

# %%

show(
    Sphere(1, centered=False).faces(),
    Sphere(1, arc_size2=45, arc_size3=75, centered=False),
    transparent=True,
)

# %%

show(Torus(1, 0.2))

# %%

show(Torus(1, 0.2, centered=False))

# %%

show(
    Torus(1, 0.2, minor_start_angle=15, minor_end_angle=135, major_angle=90)
)  # OCC broken

# %%

show(Wedge(1, 1, 1, 0.1, 0.1, 0.5, 0.5), Box(1, 1, 1, centered=False).edges())

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
sections = section(s, [Plane.XZ, Plane.ZY, Plane(Location((0, 1, 2), (60, 0, 0)))])
show(s, sections, transparent=True)

# %%

c = Circle(2) @ (20, 0, 0)
a = revolve(c, -Axis.Y, 180)
r = extrude(Rectangle(20, 4), 17.5)
a += S.min_solid(r - a, wrapped=True)

show(a)
# %%

c = Circle(2) @ (20, 0, 0)
a = revolve(c, -Axis.Y, 180)
a = extrude_until(Rectangle(20, 4), a)

show(a)
# %%

pts = [(-2, 5), (-12, 5), (-12, 10), (10, 10)]
l = offset(Polyline(pts), 1)
f = make_face(l) @ Plane.XZ
flange = extrude(f, 10, both=True) @ Rotation(10, 20, -30)

rect = Rectangle(8, 8) @ Rotation(0, 10, 0)
flange = extrude_until(rect.faces()[0], flange)

show(rect, flange)

# %%