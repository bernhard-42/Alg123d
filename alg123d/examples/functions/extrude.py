from alg123d import *
from cq_vscode import show, set_defaults

set_defaults(axes=True, axes0=True, transparent=False)

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

e = Extrusion(s, 0.3)

show(e)
# %%

show(e @ (0.5, 2, 1))

# %%
