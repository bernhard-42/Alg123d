from alg123d import *
from cq_vscode import show, set_defaults

set_defaults(axes=True, axes0=True, transparent=False)
centered = (False, False, False)

# %%

show(Box(1, 2, 3))

# %%

show(Box(1, 2, 3, centered=centered))

# %%

show(Cylinder(1, 2))

# %%

show(Cylinder(1, 2, centered=centered))

# %%

show(Cylinder(1, 2).edges(), Cylinder(1, 2, 75))

# %%

show(Cylinder(1, 2, centered=centered).edges(), Cylinder(1, 2, 75, centered=centered))

# %%

show(Cone(1, 0.1, 1))

# %%

show(Cone(1, 0.1, 1, 75))

# %%

show(Cone(1, 0, 2))

# %%

show(Cone(1, 0, 2, centered=centered))

# %%

show(Sphere(1))

# %%

show(Sphere(1, arc_size2=45, arc_size3=75))

# %%

show(
    Sphere(1, centered=centered).faces(),
    Sphere(1, arc_size2=45, arc_size3=75, centered=centered),
    transparent=True,
)

# %%

show(Torus(1, 0.2))

# %%

show(Torus(1, 0.2, centered=centered))

# %%

show(Torus(1, 0.2, minor_start_angle=0, minor_end_angle=90, major_angle=90))  # broken

# %%

show(Wedge(1, 1, 1, 0.1, 0.1, 0.5, 0.5), Box(1, 1, 1, centered=centered).edges())

# %%

# %%
