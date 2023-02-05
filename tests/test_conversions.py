from alg123d import *
import build123d as bd
import cadquery as cq

set_defaults(axes=True, axes0=True)

# CQ <-> Alg123d

# %%
c = cq.Workplane("XZ").circle(1).extrude(1)
s = c.solids()
f = c.faces()
e = c.edges()

a = from_cq(c)
a3 = from_cq(s)
a2 = from_cq(f)
a1 = from_cq(e)

show(
    c,
    a @ Pos(2, 0, 0),
    a1 @ Pos(4, 0, 0),
    a2 @ Pos(6, 0, 0),
    a3 @ Pos(8, 0, 0),
)

# %%

a = Cylinder(1, 1, align=Align.MIN) @ Plane.XZ
s = a.solids()
f = a.faces()
e = a.edges()

c = to_cq(a)
c3 = to_cq(s)
c2 = to_cq(f)
c1 = to_cq(e)

show(
    a,
    c.translate((2, 0, 0)),
    c1.translate((4, 0, 0)),
    c2.translate((6, 0, 0)),
    c3.translate((8, 0, 0)),
    show_parent=False,
)

# %%

# Build123d <-> Alg123d

with bd.BuildPart() as b:
    with bd.Workplanes(Plane.XZ):
        bd.Cylinder(1, 1)


a = from_bd(b)
a3 = from_bd(b.solids())
a2 = from_bd(b.faces())
a1 = from_bd(b.edges())

show(
    b,
    a @ Pos(2, 0, 0),
    a1 @ Pos(4, 0, 0),
    a2 @ Pos(6, 0, 0),
    a3 @ Pos(8, 0, 0),
)

# %%

with bd.BuildSketch() as s:
    bd.Circle(1)
    bd.Rectangle(0.1, 3, mode=bd.Mode.SUBTRACT)

a = from_bd(s)
a2 = from_bd(s.faces())
a1 = from_bd(s.edges())
show(a, a2 @ Pos(2, 0, 0), a1 @ Pos(4, 0, 0))

# %%
