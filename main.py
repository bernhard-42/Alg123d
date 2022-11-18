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
p + cyl

for loc in PolarLocations(0.7, 8):
    p - box @ loc

show(p.obj)

# %%

s = Sketch()
s = s.add(Circle(1))

for loc in PolarLocations(0.8, 12):
    s.subtract(Rectangle(0.1, 0.3), at=loc)

show(s.obj)

# %%
