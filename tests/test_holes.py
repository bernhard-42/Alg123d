from alg123d import *
from alg123d.shortcuts import *

set_defaults(axes=True, axes0=True, transparent=True)

# %%
a = Box(1, 2, 3)
for loc in Locations((0.3, 0.3), (-0.3, -0.3)):
    b = Bore(a, 0.1)
    a -= b @ loc

show(a)
# %%

a = Box(1, 2, 3)
wp = Plane(max_face(a))
for loc in Locations((0.2, 0.2), (-0.2, -0.2)):
    b = CounterBore(a, 0.1, 0.2, 0.1)
    a -= b @ (wp * loc)

show(a, reset_camera=False)

# %%

a = Box(1, 2, 3) + Box(1, 1, 3) @ Pos(x=3)
for wp in Planes(max_faces(a)):
    for loc in Locations((0.2, 0.2), (-0.2, -0.2)):
        b = CounterSink(a, 0.1, 0.2)
        a -= b @ (wp * loc)

show(a, reset_camera=False, transparent=True)

# %%

a = Box(1, 2, 3) + Box(1, 1, 3) @ Pos(x=3)
for wp in Planes(max_faces(a, -Axis.Y)):
    for loc in Locations((0.2, 0.2), (-0.2, -0.2)):
        b = CounterSink(a, 0.1, 0.2)
        a -= b @ (wp * loc)

show(a, reset_camera=False, transparent=True)

# %%

a = Box(1, 2, 3) + Box(1, 1, 3) @ Pos(x=3)
for wp in Planes(min_faces(a)):
    for loc in Locations((0.2, 0.2), (-0.2, -0.2)):
        b = CounterBore(a, 0.1, 0.2, 0.1)
        a -= b @ (wp * loc)

show(a, reset_camera=False, transparent=True)

# %%
