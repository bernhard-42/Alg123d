from alg123d import *

set_defaults(axes=True, axes0=True, transparent=False)

# %%

a = Pos(4, 2, 0) * Box(1, 2, 3)
a = fillet(a, a.edges(), 0.1)
b = a + mirror(a, Plane.XZ)
show(a.edges(), b)


# %%

a = Pos(4, 2, 0) * Box(1, 2, 3)
a = fillet(a, a.edges(), 0.1)
b = mirror(a, Plane.XZ)
show(a.edges(), b)

# %%

a = Pos(4, 2, 0) * Circle(1)
b = a + mirror(a, Plane.XZ)
show(a.edges(), b)

# %%

a = Pos(4, 2, 0) * Circle(1)
b = mirror(a, Plane.XZ)
show(a.edges(), b)

# %%

l = Spline(
    ((0, 0, 0), (50, 0, 50), (100, 0, 0)),
    tangents=((1, 0, 0), (1, 0, 0)),
    tangent_scalars=(0.5, 2),
)
show(l, mirror(l, Plane.XY))

# %%

show(l, mirror(l, Plane.YZ))

# %%
