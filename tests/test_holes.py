from alg123d import *
import alg123d.shortcuts as S
from cq_vscode import show, set_defaults

set_defaults(axes=True, axes0=True, transparent=True)

# %%
a = Box(1, 2, 3)
for loc in Locations((0.3, 0.3), (-0.3, -0.3)):
    b = Bore(a, 0.1)
    a -= b @ loc

show(a)
# %%

a = Box(1, 2, 3)
wp = Plane(S.max_face(a))
for loc in Locations((0.2, 0.2), (-0.2, -0.2)):
    b = CounterBore(a, 0.1, 0.2, 0.1)
    a -= b @ (wp * loc)

show(a, reset_camera=False)

# %%

a = Box(1, 2, 3) + Box(1, 1, 3) @ (3, 0)
for wp in S.planes(S.max_faces(a)):
    for loc in Locations((0.2, 0.2), (-0.2, -0.2)):
        b = CounterSink(a, 0.1, 0.2)
        a -= b @ (wp * loc)

show(a, reset_camera=False, transparent=True)

# %%

a = Box(1, 2, 3) + Box(1, 1, 3) @ (3, 0)
for wp in S.planes(S.max_faces(a, -Axis.Y)):
    for loc in Locations((0.2, 0.2), (-0.2, -0.2)):
        b = CounterSink(a, 0.1, 0.2)
        a -= b @ (wp * loc)

show(a, reset_camera=False, transparent=True)

# %%

a = Box(1, 2, 3) + Box(1, 1, 3) @ (3, 0)
for wp in S.planes(S.min_faces(a)):
    for loc in Locations((0.2, 0.2), (-0.2, -0.2)):
        b = CounterBore(a, 0.1, 0.2, 0.1)
        a -= b @ (wp * loc)

show(a, reset_camera=False, transparent=True)

# %%
