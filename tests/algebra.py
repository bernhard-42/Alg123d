from alg123d import *
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

show(p, p.faces().group_by(Axis.Y)[0], transparent=True)

# %%

plane = Workplane.ZX

rotations = [Location((0, 0, 0), (0, a, 0)) for a in (0, 45, 90, 135)]

s = Empty3()
for i, outer_loc in enumerate(GridLocations(3, 3, 2, 2)):
    # on plane, located to grid position, and finally rotated
    c_plane = plane * outer_loc * rotations[i]
    s += Circle(1) @ c_plane
    for loc in PolarLocations(0.8, (i + 3) * 2):
        # Use polar locations on c_plane
        s -= Rectangle(0.1, 0.3) @ (c_plane * loc)

e = extrude(s, 0.3)

show(e)

# %%

plane = Workplane((20, 0, 0))
c = Circle(2) @ plane
a = revolve(c, Axis.Y, 180) @ Rotation(0, 180, 0)
r = Rectangle(20, 4)
e = extrude(r, until_part=a, until=Until.NEXT)
show(e)

# %%
