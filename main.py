from py123d import *
from cq_vscode import show, set_defaults

set_defaults(axes=True, axes0=True, transparent=False)


# %%
plane = Workplane.ZX

cyl = Cylinder(1, 0.5)
box = Box(0.3, 0.3, 0.5)

p = cyl @ plane

for loc in PolarLocations(0.7, 10):
    p -= box @ (plane * loc)

show(p)

# %%

s = Empty()
for outer_loc in GridLocations(3, 3, 2, 2):
    s += Circle(1) @ (plane * outer_loc)

    for loc in PolarLocations(0.8, 12):
        s -= Rectangle(0.1, 0.3) @ (plane * outer_loc * loc)

e = Extrusion(s, 0.3)
show(e)

# %%

show(e, e.faces().group_by(Axis.Y)[0])

# %%
