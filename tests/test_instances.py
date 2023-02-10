from alg123d import *
import cadquery as cq

# %%

# CadQuery

b = cq.Workplane().sphere(0.5)
s = cq.Workplane().sphere(1)

a = cq.Assembly(name="boxes")
a.add(b, name="box1", loc=cq.Location((-2, 0, 0)))
a.add(b, name="box2")
a.add(b, name="box3", loc=cq.Location((2, 0, 0)))
a.add(s, name="sphere", loc=cq.Location((0, 2, 0)))

show(a, timeit=True)

# %%

show(s)

# %%

cq_screw = cq.importers.importStep(
    "/Users/bernhard.walter/Development/cad/build123d/docs/M6-1x12-countersunk-screw.step"
)
locs = HexLocations(6, 10, 10).locations

a = cq.Assembly(name="screws")

for i, loc in enumerate([cq.Location(loc.wrapped) for loc in locs]):
    a.add(cq_screw, loc=loc, name=f"screw{i}")
# %%
show(a, timeit=False)
# %%

show(cq_screw, timeit=True)

# %%
