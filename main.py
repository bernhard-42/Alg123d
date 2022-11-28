from alg123d import *
from cq_vscode import show, set_defaults

set_defaults(axes=True, axes0=True, transparent=False)


# %%
pts = [(0, 1), (1, 0), (1, 1), (0, 1)]
show(Polygon(pts))

# %%
plane = Workplane.ZX

cyl = Cylinder(1, 0.5)
box = Box(0.3, 0.3, 0.5)

# %%

p = cyl @ plane

for loc in PolarLocations(0.7, 10):
    p -= box @ (plane * loc)

show(p)
# %%

show(p, p.faces().group_by(Axis.Y)[0], transparent=True)

# %%

locs = [Location((0, 0, 0), (0, a, 0)) for a in (0, 45, 90, 135)]

s = Empty3()
for i, outer_loc in enumerate(GridLocations(3, 3, 2, 2)):
    c_plane = plane * outer_loc * locs[i]
    s += Circle(1) @ c_plane

    for loc in PolarLocations(0.8, (i + 3) * 2):
        s -= Rectangle(0.1, 0.3) @ (c_plane * loc * Rotation(0, 0, 45))

e = extrude(s, 0.3)
show(e, reset_camera=False)
