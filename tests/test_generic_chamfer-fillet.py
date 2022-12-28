from alg123d import *

set_defaults(axes=True, axes0=True, transparent=False)

# %%

a = Box(1, 1, 1)
b = a + Cylinder(0.1, 2) @ Pos(-0.3, -0.3)
c = chamfer(b, a.edges(), 0.1)
show(a, b @ Pos(0, 2), c @ Pos(y=4))

# %%

a = Box(1, 1, 1)
b = a - Cylinder(0.1, 2) @ Pos(0.3, 0.3)
c = fillet(b, a.edges(), 0.1)
show(a, b @ Pos(0, 2), c @ Pos(0, 4))

# %%

a = Rectangle(1, 2)
b = fillet(a, a.vertices(), 0.3)

show(a, b @ Pos(0, 3))

# %%

a = Rectangle(1, 2)
b = chamfer(a, a.vertices(), 0.3)

show(a, b @ Pos(0, 3))

# %%
