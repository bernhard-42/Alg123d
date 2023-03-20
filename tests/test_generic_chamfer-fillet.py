from alg123d import *

set_defaults(axes=True, axes0=True, transparent=False)

# %%

a = Box(1, 1, 1)
b = a + Pos(-0.3, -0.3) * Cylinder(0.1, 2)
c = chamfer(b, a.edges(), 0.1)
show(a, Pos(0, 2) * b, Pos(y=4) * c)

# %%

a = Box(1, 1, 1)
b = a - Pos(0.3, 0.3) * Cylinder(0.1, 2)
c = fillet(b, a.edges(), 0.1)
show(a, Pos(0, 2) * b, Pos(0, 4) * c)

# %%

a = Rectangle(1, 2)
b = fillet(a, a.vertices(), 0.3)

show(a, Pos(0, 3)*b)

# %%

a = Rectangle(1, 2)
b = chamfer(a, a.vertices(), 0.3)

show(a,  Pos(0, 3)*b)

# %%

b = Box(1, 1, 1) - Box(2, 2, 0.3)
b = fillet(b, b.edges(), 0.1)
show(b)

# %%

b = Rectangle(1, 2) - Rectangle(0.5, 3)
b = fillet(b, b.vertices(), 0.1)

show(b)

#
