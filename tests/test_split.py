from alg123d import *

set_defaults(axes=True, axes0=True, transparent=True)

# %%

a = Box(1, 2, 3) + Cylinder(0.3, 4) + Plane.XZ * Cylinder(0.3, 4)

b = split(a)

show(a.edges(), b)
# %%

b = split(a, Plane.XY, Keep.BOTTOM)
show(a.edges(), b)

# %%

b = split(a, Plane.XY, Keep.BOTH)

show(a.edges(), *b.solids())

# %%

a = Rectangle(1, 2)
b = split(a)

show(a.edges(), b)

# %%

b = split(a, Plane.YZ)

show(a.edges(), b)

# %%
