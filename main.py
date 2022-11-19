from py123d import *
from cq_vscode import show


# %%

cyl = Cylinder(1, 0.5)
box = Box(0.3, 0.3, 0.5)

p = Part()
p.add(cyl)

for loc in PolarLocations(0.7, 8):
    p.subtract(box, at=loc)

show(p.obj)

# %%

p = Part()
p += cyl

for loc in PolarLocations(0.7, 8):
    p -= box @ loc

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
    s += Circle(1) @ outer_loc

    for loc in PolarLocations(0.8, 12):
        s -= Rectangle(0.1, 0.3) @ (outer_loc * loc)

show(s.obj)
# %%

e = Part()
e += Extrusion(s, 0.3)

show(e.obj, e.obj.faces().group_by()[-1])
# %%
