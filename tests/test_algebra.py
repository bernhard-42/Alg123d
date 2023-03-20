from alg123d import *

set_defaults(axes=True, axes0=True, transparent=False)

# %%
plane = Plane.ZX

cyl = Cylinder(1, 0.5)
box = Box(0.3, 0.3, 0.5)

p = plane * cyl 

for loc in PolarLocations(0.7, 10):
    p -= plane * loc * box

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
    s += c_plane * Circle(1)

    for loc in PolarLocations(0.8, (i + 3) * 2):
        # Use polar locations on c_plane
        s -= c_plane * loc * Rectangle(0.1, 0.3)

e = extrude(s, 0.3)

show(e)

# %%
a, b, c = 80.0, 5.0, 3.0

# shapes = [
#     ploc * RegularPolygon(b, 4)
#     + [ploc * gloc * RegularPolygon(b, 3) for gloc in GridLocations(3 * b, 3 * b, 2, 2)]
#     for ploc in PolarLocations(a / 2, 6)
# ]
shapes = PolarLocations(a / 2, 6) * (
    RegularPolygon(b, 4) + GridLocations(3 * b, 3 * b, 2, 2) * RegularPolygon(b, 3)
)
ex31 = extrude(Rot(z=30) * RegularPolygon(3 * b, 6) + shapes, 3) # vertorized + !

show(ex31)

# %%

c = Pos(x=20) * Circle(2)
a = revolve(c, -Axis.Y, 180)
r = extrude(Rectangle(20, 4), 17.5)
a += (r - a).solids().min()

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
