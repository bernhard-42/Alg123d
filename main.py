from py123d import *
from cq_vscode import show, set_defaults
set_defaults(axes=True, axes0=True, transparent=False)


# %%

plane = Workplane.ZY

cyl = Cylinder(1, 0.5)
box = Box(0.3, 0.3, 0.5)

p = Part()
p.add(cyl, on=plane)

for loc in PolarLocations(0.7, 8):
    p.subtract(box, on=plane, at=loc)

show(p.obj)

# %%

p = Part()
p += cyl @ plane

for loc in PolarLocations(0.7, 10):
    p -= box @ (plane * loc)

show(p.obj)

# %%

s = Sketch()
s.add(Circle(1))

for loc in PolarLocations(0.8, 12):
    s.subtract(Rectangle(0.1, 0.3), at=loc)

show(s.obj)

# %%

s = Sketch()
for outer_loc in GridLocations(3, 3, 2, 2):
    s += Circle(1) @ (plane * outer_loc)

    for loc in PolarLocations(0.8, 12):
        s -= Rectangle(0.1, 0.3) @ (plane * outer_loc * loc)

show(s.obj)
# %%

e = Part()
e += Extrusion(s, 0.3)

show(e.obj, e.obj.faces().group_by()[-1])
# %%
