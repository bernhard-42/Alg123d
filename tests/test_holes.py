from alg123d import *

set_defaults(axes=True, axes0=True, transparent=True)

# %%
a = Box(1, 2, 3)
for loc in Locations((0.3, 0.3), (-0.3, -0.3)):
    b = Bore(a, 0.1)
    a -= loc * b

show(a)
# %%

a = Box(1, 2, 3)
wp = Plane(a.faces().max())
for loc in Locations((0.2, 0.2), (-0.2, -0.2)):
    b = CounterBore(a, 0.1, 0.2, 0.1)
    a -= wp * loc * b

show(a, reset_camera=False)

# %%

a = Box(1, 2, 3) + Pos(x=3) * Box(1, 1, 3)
for wp in Planes(a.faces().max_group()):
    for loc in Locations((0.2, 0.2), (-0.2, -0.2)):
        b = CounterSink(a, 0.1, 0.2)
        a -= wp * loc * b

show(a, reset_camera=False, transparent=True)

# %%

a = Box(1, 2, 3) + Pos(x=3) * Box(1, 1, 3)
for wp in Planes(a.faces().max_group(-Axis.Y)):
    for loc in Locations((0.2, 0.2), (-0.2, -0.2)):
        b = CounterSink(a, 0.1, 0.2)
        a -= wp * loc * b

show(a, reset_camera=False, transparent=True)

# %%

a = Box(1, 2, 3) + Pos(x=3) * Box(1, 1, 3)
for wp in Planes(a.faces().min_group()):
    for loc in Locations((0.2, 0.2), (-0.2, -0.2)):
        b = CounterBore(a, 0.1, 0.2, 0.1)
        a -= wp * loc * b

show(a, reset_camera=False, transparent=True)

# %%
