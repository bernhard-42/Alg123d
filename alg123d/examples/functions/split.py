from alg123d import *
from cq_vscode import show, set_defaults

set_defaults(axes=True, axes0=True, transparent=True)

# %%

a = Box(1, 2, 3) + Cylinder(0.3, 4) + Cylinder(0.3, 4) @ Workplane.XZ

b = split(a)

show(a.edges(), b)
# %%

b = split(a, Plane.XY, keep=bd.Keep.BOTTOM)
show(a.edges(), b)

# %%

b = split(a, Plane.XY, keep=bd.Keep.BOTH)

show(a.edges(), *b.solids())

# %%

a = Rectangle(1, 2)
b = split(a)

show(a.edges(), b)

# %%

b = split(a.edges(), Plane.YZ)

show(a, b)

# %%
