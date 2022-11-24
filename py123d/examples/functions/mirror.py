from py123d import *
from cq_vscode import show, set_defaults

set_defaults(axes=True, axes0=True, transparent=False)

# %%

a = Box(1, 2, 3) @ (4, 2, 0)
b = a + mirror(a, Plane.XZ)
show(b)

# %%

a = Circle(1) @ (4, 2, 0)
b = a + mirror(a, Plane.XZ)
show(b)

# %%
