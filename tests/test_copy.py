from alg123d import *
from ocp_tessellate.tessellator import cache

import copy

s = Sphere(1)
s2 = Pos(1, 2, 3) * s
s3 = copy.copy(s)
s3._align(Align.MIN)

cache.clear()
# %%

show(
    s,
    s,
    s,
    s2,
    s2,
    s2,
    s3,
    s3,
    s3,
    names=["sa", "sb", "sc", "sa2", "sb2", "sc2", "sa3", "sb3", "sc3"],
    timeit=False,
)

# %%

show(s, s, s, s2, s2, s2, s3, s3, s3, timeit=False)

# %%

cache.clear()
show(s, s, s, s2, s2, s2, s3, s3, s3, timeit=False)

# %%

show(
    Pos(2, 0, 0) * s,
    Pos(4, 0, 0) * s,
    Pos(0, 2, 0) * s,
    Pos(0, 4, 0) * s,
    s,
    Pos(0, 0, 2) * s3,
    Pos(0, 0, 4) * s3,
    Pos(0, 0, 6) * s3,
    names=["sa", "sb", "sc", "sd", "se", "sa3", "sb3", "sc3"],
    timeit=False,
)

# %%

show(
    Pos(2, 0, 0) * s,
    Pos(4, 0, 0) * s,
    Pos(0, 2, 0) * s,
    Pos(0, 4, 0) * s,
    s,
    Pos(0, 0, 2) * s3,
    Pos(0, 0, 4) * s3,
    Pos(0, 0, 6) * s3,
    names=["sa", "sb", "sc", "sd", "se", "sa3", "sb3", "sc3"],
    timeit=False,
)

# %%
