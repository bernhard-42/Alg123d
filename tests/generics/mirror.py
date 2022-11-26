from alg123d import *
from cq_vscode import show, set_defaults

set_defaults(axes=True, axes0=True, transparent=False)

# %%

a = Box(1, 2, 3) @ (4, 2, 0)
a = fillet(a, a.edges(), 0.1)
b = a + mirror(a, Plane.XZ)
show(a.edges(), b)


# %%

a = Box(1, 2, 3) @ (4, 2, 0)
a = fillet(a, a.edges(), 0.1)
b = mirror(a, Plane.XZ)
show(a.edges(), b)

# %%

a = Circle(1) @ (4, 2, 0)
b = a + mirror(a, Plane.XZ)
show(a.edges(), b)

# %%

# %%

a = Circle(1) @ (4, 2, 0)
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
