from alg123d import *
import alg123d.shortcuts as S
import build123d as bd
import cadquery as cq

# CQ <-> Alg123d

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

show(
    a,
    a1 @ (2, 0, 0),
    a2 @ (4, 0, 0),
    a3 @ (6, 0, 0),
)

# %%

a = Cylinder(1, 1) @ Plane.XZ
s = a.solids()
f = a.faces()
e = a.edges()

c = S.to_cq(a)
c3 = S.to_cq(s)
c2 = S.to_cq(f)
c1 = S.to_cq(e)

show(
    c,
    c1.translate((2, 0, 0)),
    c2.translate((4, 0, 0)),
    c3.translate((6, 0, 0)),
    show_parent=False,
)

# %%

# Build123d <-> Alg123d


def from_bd(obj):
    if hasattr(obj, "_obj_name"):
        return AlgCompound(getattr(obj, obj._obj_name))
    else:
        return AlgCompound.make_compound([Shape.cast(o.wrapped) for o in obj])


with bd.BuildPart() as b:
    with bd.Workplanes(Plane.XZ):
        bd.Cylinder(1, 1)

show(b)
a = from_bd(b)
a3 = from_bd(b.solids())
a2 = from_bd(b.faces())
a1 = from_bd(b.edges())

show(
    a,
    a1 @ (2, 0, 0),
    a2 @ (4, 0, 0),
    a3 @ (6, 0, 0),
)

# %%

with bd.BuildSketch() as s:
    bd.Circle(1)
    bd.Rectangle(0.1, 3, mode=bd.Mode.SUBTRACT)

a = from_bd(s)
a2 = from_bd(s.faces())
a1 = from_bd(s.edges())
show(
    a, 
    a2 @ (2, 0, 0),
    a1 @ (4, 0, 0)
)

# %%
