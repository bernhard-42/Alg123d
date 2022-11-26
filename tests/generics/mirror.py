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
