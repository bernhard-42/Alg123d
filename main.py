from py123d import *
from cq_vscode import show

p = Part()
p.add(Cylinder(1, 1))

p.subtract(Box(0.2, 0.2, 3), at=grid_locations(2, 3, 0.5, 0.4))
show(p.obj)
