from build123d import *
from cq_vscode import show, set_port

# set_port(3940)

f = Face.import_stl("/tmp/base.stl")
show(f, colors=["#999"], default_edgecolor="#bbc")

# %%


with BuildPart() as box:
    Box(1, 2, 3)

show(box, default_edgecolor=(255, 0, 0))
# %%
pts = ((0, 0), (0, 1), (1, 1), (0, 0))

with BuildPart() as bp:
    with BuildSketch() as bs:
        with BuildLine() as bl:
            Polyline(*pts)
        MakeFace()
    Extrude(amount=1)

show(bp)

# %%


from alg123d import *
from time import time
import build123d as bd

set_defaults(grid=(True, True, True), axes=True, axes0=True)

MAX_HASH_KEY = 2147483647


# %%

import cadquery as cq
from cq_vscode.show import _tessellate, _convert
from ocp_tessellate.utils import numpy_to_json, Timer, numpy_to_buffer_json

b = cq.Workplane().box(1, 2, 3)
s = cq.Workplane().box(1, 1, 1)

a = cq.Assembly(name="boxes")
a.add(b, name="box1", loc=cq.Location((-2, 0, 0)))
a.add(b, name="box2")
a.add(b, name="box3", loc=cq.Location((2, 0, 0)))
a.add(s, name="sphere", loc=cq.Location((0, 2, 0)))

show(a)

# %%

screw = Compound.import_step("../build123d/docs/M6-1x12-countersunk-screw.step")
cq_screw = cq.importers.importStep("../build123d/docs/M6-1x12-countersunk-screw.step")
locs = HexLocations(6, 10, 10).locations

# %%
import cadquery as cq

a = cq.Assembly(name="screws")
for i, loc in enumerate([cq.Location(loc.wrapped) for loc in locs]):
    a.add(cq_screw, loc=loc, name=f"screw{i}")

data = _convert(a)
show(a, timeit=True)

# %%


with Timer(True, "json", "bin json"):
    data = numpy_to_binary_json(dict(shapes=shapes, states=states))

# %%

screw_references = [copy.copy(screw).locate(loc) for loc in locs]
reference_assembly = AlgCompound(children=screw_references)

# show(reference_assembly)

# %%
xy_loc = Location()
# %%
s3 = screw_references[3]
s4 = screw_references[4]


def splitcopy(obj):
    loc = obj.location
    shape = Box(0.1, 0.1, 0.1)
    shape.wrapped.TShape(obj.wrapped.TShape())
    # shape = copy.copy(obj)
    # shape.locate(Location())
    return shape, loc


t4, l4 = splitcopy(s4)
t3, l3 = splitcopy(s3)


show(s3, s4, t3, t4)

# %%
screw_copies = [copy.deepcopy(screw).locate(loc) for loc in locs]
copy_assembly = Compound(children=screw_copies)

show(copy_assembly, timeit=True)
# %%

from copy import copy, deepcopy


def pp_loc(l):
    r = l.Transformation().GetRotation()
    t = l.Transformation().TranslationPart()
    print(r.X(), r.Y(), r.Z())
    print(r.W(), r.X(), r.Y(), r.Z())


# %%

b = Box(1, 2, 3)
s = Sphere(1)
ss = copy(s)
ss2 = s * Pos(2, 0, 0)
sd = deepcopy(s)
h = Box(0.5, 6, 0.5)
# %%
print("s  ", s.wrapped.TShape())
print("ss ", ss.wrapped.TShape())
print("ss2", ss2.wrapped.TShape())
print("sd", sd.wrapped.TShape())

# %%

print("s  ", str(s.wrapped.TShape()))
print("ss ", str(ss.wrapped.TShape()))
print("ss2", str(ss2.wrapped.TShape()))
print("sd", str(sd.wrapped.TShape()))
# %%
show(s, ss)

# %%

print("s", s.hash_code())
print("ss", ss.hash_code())
print("ss2", ss2.hash_code())
print("sd", sd.hash_code())

# %%

c = s * Pos(-2, 0, 0) + b * Pos(2, 0, 0)

print("c", c.hash_code())
print("s", s.hash_code())
print("b", b.hash_code())
print("s", s.location)
print("b", b.location)

show(s, ss * Pos(2, 0, 0))
# %%

s = s - h
show(s, ss * Pos(2, 0, 0))


# %%
show(s * Pos(-4, 0, 0), b, c * Pos(2, 0, 0))
# %%


# %%

n = 10
sphere = Sphere(1)
boxes = []
for loc in GridLocations(2.5, 2.5, n, n):
    # boxes.append(Sphere(random.random() / 3 + 1) @ loc)
    boxes.append(sphere @ loc)

# %%
s = time()
objects = Compound.make_compound(boxes)

s2 = time()
print(s2 - s)

show(objects)

print(time() - s2)

# %%

s = time()

b = boxes[0]
c = b.fuse(*boxes[1:])

s2 = time()
print(s2 - s)

show(c)
print(time() - s2)
# %%


# %%

c = AlgCompound()
c.label = "spheres"
s1 = sphere
s1.position = (2, 0, 0)
s1.name = "s1"
s2 = sphere
s2.position = (0, 2, 0)
s2.name = "s2"
s3 = sphere
s3.position = (0, 0, 2)
s3.name = "s3"
c.children = [s1, s2, s3]

# %%
