from alg123d import *
import copy

s = Sphere(1)
s2 = s * Pos(1, 2, 3)
s3 = copy.copy(s)
s3._align(Align.MIN)

# %%
show(s, s, s, s, s, s2, s2, s2, timeit=True)  # show 1 dots progress
# %%
show(s, s, s, s, s, s2, s2, s2, timeit=True)  # show 0 dots progress
# %%
show(s, s, s, s, s, s3, s3, s3, timeit=True)  # show 0 dot progress
# %%
