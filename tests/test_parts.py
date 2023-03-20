from math import sin, pi

from alg123d import *

set_defaults(axes=True, axes0=True, transparent=True)

# %%

show(Box(1, 2, 3))

# %%

show(Box(1, 2, 3, align=Align.MIN))

# %%

show(Box(1, 2, 3, align=Align.MAX))

# %%

show(Cylinder(1, 2))

# %%

show(Cylinder(1, 2, align=Align.MIN), Box(2, 2, 2, align=Align.MIN).edges())

# %%

show(Cylinder(1, 2, align=Align.MAX), Box(2, 2, 2, align=Align.MAX).edges())

# %%

show(Cylinder(1, 2, 75))

# %%

show(Cylinder(1, 2, 75, align=Align.MIN))

# %%

show(Cylinder(1, 2, 75, align=Align.MAX))

# %%

show(Cone(1, 0.1, 1))

# %%

show(Cone(1, 0.1, 1, 75))

# %%

show(Cone(1, 0, 2))

# %%

show(Cone(1, 0, 2, align=Align.MIN), Box(2, 2, 2, align=Align.MIN).edges())

# %%

show(Cone(1, 0, 2, align=Align.MAX), Box(2, 2, 2, align=Align.MAX).edges())

# %%

show(Sphere(1))

# %%

show(Sphere(1, arc_size2=45, arc_size3=75))

# %%

show(
    Sphere(1, arc_size2=45, arc_size3=75, align=Align.MIN),
    transparent=True,
)

# %%

show(
    Sphere(1, arc_size2=45, arc_size3=75, align=Align.MAX),
    transparent=True,
)

# %%

show(Torus(1, 0.2))

# %%

show(Torus(1, 0.2, align=Align.MIN), Box(2.4, 2.4, 0.4, align=Align.MIN).edges())

# %%

show(Torus(1, 0.2, align=Align.MAX), Box(2.4, 2.4, 0.4, align=Align.MAX).edges())

# %%

show(
    Torus(1, 0.2, minor_start_angle=15, minor_end_angle=135, major_angle=90)
)  # OCC broken

# %%

show(Wedge(1, 1, 1, 0.1, 0.1, 0.5, 0.5))

# %%

s = Circle(1) + Circle(0.5) @ Pos(0.9, 0) + Circle(0.5) @ Pos(-0.7, 0) - Circle(0.5)

show(extrude(s, 0.1))
# loft

# %%

s1 = Rectangle(1, 1)
s2 = Pos(1, 0, 1) * Rectangle(0.5, 2)

l = loft([s1, s2])
show(s1.edges(), s2.edges(), l)

# %%

slice_count = 10
sections = [
    Pos(z=3 * i) * Circle(5 + 10 * sin(i * pi / slice_count))
    for i in range(slice_count + 1)
]

l = loft(sections)

show(*[s.edges() for s in sections], l)

# revolve

# %%
s1 = Pos(0, 0.5, 0) * Circle(0.1)
r = revolve(s1, Axis.X, 90)
show(r)

# %%

s1 = Pos(0, 0.5, 0) * Circle(0.1)
r = revolve(s1, Axis.X, -130)
show(r)

# %%

s = Pos(0.9, 0.2, 0) * Sphere(1)
sections = section(s, [Plane.XZ, Plane.ZY, Plane(Location((0, 1, 2), (60, 0, 0)))])
show(s, sections, transparent=True)

# %%

c = Pos(20, 0, 0) * Circle(2)
a = revolve(c, -Axis.Y, 180)
r = extrude(Rectangle(20, 4), 17.5)
a += (r - a).solids().min()

show(a)
# %%

c = Pos(20, 0, 0) * Circle(2)
a = revolve(c, -Axis.Y, 180)
f = Rectangle(20, 4)
e = extrude_until(f, a)

show(e, a, alphas=(1, 0.5))

# %%

e = extrude_until(f, a, until=Until.LAST)

show(e, a, alphas=(1, 0.5))

# %%
e = extrude_until(Rectangle(20, 3.9).faces()[0], a, (0, 0, 1), until=Until.NEXT)

show(e)

# %%
f = Rectangle(20, 3.8).faces()[0]
e = extrude_until(f, a, (0, 0, 1), until=Until.LAST)

show(f, a, e)

# %%

c = ThreePointArc((0, 0, -5), (0, -5, 0), (0, 5, 1.5))
f = Plane.XZ * Pos(y=-5) * Circle(0.5)
t = sweep(f.face(), path=c.wire())

f2 = Plane.XZ * Pos(z=-7) * Rectangle(0.9999, 8)
a = Solid.extrude_until(f2.faces()[0], t, (0, -1, 0))
show(a, t)

# %%

f2 = Plane.XZ * Pos(z=-7) * Rectangle(0.999, 8)
a = Solid.extrude_until(f2.faces()[0], t, (0, -1, 0), Until.LAST)
show(a)

# %%

a = extrude_until(f2, t)
show(a)

# %%

pts = [(-2, 5), (-12, 5), (-12, 10), (10, 10)]
l = offset(Polyline(pts), 1)
f = Plane.XZ * make_face(l)
flange = Rot(10, 20, -30) * extrude(f, 10, both=True)

rect = Rot(0, 10, 0) * Rectangle(8, 8)
flange += extrude_until(rect.face(), flange)

show(rect, flange)

# %%
