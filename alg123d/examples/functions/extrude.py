from alg123d import *
from cq_vscode import show, set_defaults

set_defaults(axes=True, axes0=True, transparent=False)

# %%
plane = Workplane.ZX

locs = [Location((0, 0, 0), (0, a, 0)) for a in (0, 45, 90, 135)]

s = Empty3d()
for i, outer_loc in enumerate(GridLocations(3, 3, 2, 2)):
    c_plane = (
        plane * outer_loc * locs[i]
    )  # on plane, located to grid positions, and finally rotated
    s += Circle(1) @ c_plane

    for loc in PolarLocations(0.8, (i + 3) * 2):
        s -= Rectangle(0.1, 0.3) @ (c_plane * loc)  # Use polar locations on c_plane

e = extrude(s, 0.3)
show(e)

# %%
