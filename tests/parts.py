from math import sin, pi
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

show(
    Torus(1, 0.2, minor_start_angle=15, minor_end_angle=135, major_angle=90)
)  # OCC broken

# %%

show(Wedge(1, 1, 1, 0.1, 0.1, 0.5, 0.5), Box(1, 1, 1, centered=centered).edges())

# loft

# %%

s1 = Rectangle(1, 1)
s2 = Rectangle(0.5, 2) @ (1, 0, 1)

l = loft([s1, s2])
show(s1.edges(), s2.edges(), l)

# %%

slice_count = 10
sections = [
    Circle(5 + 10 * sin(i * pi / slice_count)) @ (0, 0, 3 * i)
    for i in range(slice_count + 1)
]

l = loft(sections)

show(*[s.edges() for s in sections], l)

# revolve

# %%
s1 = Circle(0.1) @ (0, 0.5, 0)
r = revolve(s1, Axis.X, 90)
show(r)

# %%

s1 = Circle(0.1) @ (0, 0.5, 0)
r = revolve(s1, Axis.X, -130)
show(r)

# %%
from alg123d import *
from cq_vscode import show, set_defaults

set_defaults(axes=True, axes0=True, transparent=False)

# %%

s = Sphere(1) @ (0.9, 0, 0)
sections = section(s, [Plane.XZ, Plane.ZY])
show(s, sections, transparent=True)

# %%
