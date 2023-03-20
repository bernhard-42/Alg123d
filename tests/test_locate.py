from alg123d import *

set_defaults(grid=(True, True, True), axes=True, axes0=True)

# %%

# Place circle on XY plane

s = Circle(1)

show(s)

# %%

# Place circle on XZ plane

s = Plane.XZ * Circle(1)

show(s)

# %%

# Place circle on XZ plane and then move relative to XY plane

s = Plane.XZ * Pos(1, 1, 1) * Circle(1)

show(s)

# %%

s = Pos(1, 1, 1) * Circle(1)

show(s)

# %%

s = Plane.ZY * Circle(1)

show(s)

# %%

s = Plane.XY * Pos(1, 1, 1) * Circle(1)

show(s)

# %%
