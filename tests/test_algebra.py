from alg123d import *

set_defaults(axes=True, axes0=True, transparent=False)

# %%
plane = Plane.ZX

cyl = Cylinder(1, 0.5)
box = Box(0.3, 0.3, 0.5)

p = cyl @ plane

for loc in PolarLocations(0.7, 10):
    p -= box @ (plane * loc)

show(p)
# %%

show(p, p.faces().group_by(Axis.Y)[0], transparent=True)

# %%

plane = Plane.ZX

rotations = [Rot(y=a) for a in (0, 45, 90, 135)]

s = AlgCompound()
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


c = Circle(2) @ Pos(x=20)
a = revolve(c, -Axis.Y, 180)
r = extrude(Rectangle(20, 4), 17.5)
a += (r - a).solids().min(wrapped=True)

show(a)

# %%

show(AlgCompound() + Box(1, 1, 1))
# %%

show(Box(1, 2, 3) + AlgCompound())

# %%

show(Box(2, 3, 1) - AlgCompound())

# %%

show(Box(3, 2, 1) & AlgCompound())

# %%

show(AlgCompound() + Rectangle(1, 1))
# %%

show(Rectangle(1, 2) + AlgCompound())

# %%

show(Rectangle(2, 2) - AlgCompound())

# %%

show(Rectangle(2, 1) & AlgCompound())

# %%

show(AlgCompound() + RegularPolygon(2, 3))

# %%

show(RegularPolygon(2, 4) + AlgCompound())

# %%
