import os

os.environ["JCQ_CACHE_SIZE_MB"] = "1024"

import cadquery as cq
from alg123d import *
from alg123d.stepreader import StepReader
import time

# %%
from ocp_tessellate.tessellator import make_key

b = Box(1, 2, 3)
b = fillet(b, b.edges(), 0.1)

# %%

make_key(b.wrapped, 0.1, 0.2, True, True)
show(b, b, names=["b1", "b2"])

# %%

box = cq.Workplane().box(1, 1, 1).fillet(0.1)

show(box, box, names=["box1", "box2"])

# %%

reader = StepReader()
reader.load("/tmp/RC_Buggy_2_front_suspension.stp")
rc = reader.to_cadquery()

# %%

t = time.time()
show(rc, up="Y", parallel=True, timeit=False)
print("\n", time.time() - t)

# %%

t = time.time()
show(rc, up="Y", parallel=True, timeit=False)
print("\n", time.time() - t)


# %%

a = cq.Assembly(name="boxes")
a.add(b, name="b1", loc=cq.Location((0, 3, 0)))
a.add(b, name="b2", loc=cq.Location((0, -3, 0)))

t = time.time()
show(a, parallel=True)
print("\n", time.time() - t)
# %%
