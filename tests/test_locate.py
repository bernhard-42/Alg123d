from alg123d import *
set_defaults(grid=(True,True,True), axes=True, axes0=True)

# %%

# Place circle on XY plane

s = Circle(1)

show(s)

# %%

# Place circle on XZ plane

s = Circle(1) @ Plane.XZ

show(s)

# %%

# Place circle on XZ plane and then move relative to XY plane

s = (Circle(1) @ Plane.XZ) * Pos(1,1,1)

show(s)

# %%

# Place circle on a plane that is XZ plane moved relative to XZ plane
# "Local" movement on plane

s = Circle(1) @ (Plane.XZ * Pos(1,1,1))

show(s)
# %%

s = Circle(1) * Pos(1,1,1)

show(s)

# %%

s = Circle(1) @ Pos(1,1,1)

show(s)

# %%

s = Circle(1) @ Plane.XY

show(s)

# %%

s = (Circle(1) @ Plane.XY) * Pos(1,1,1)

show(s)

# %%

s = Circle(1) @ (Plane.XY * Pos(1,1,1))

show(s)

# %%