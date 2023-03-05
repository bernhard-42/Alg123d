import math
from alg123d import *

set_defaults(axes=True, axes0=True, transparent=False)

# %%
# Bezier
pts = (0, 0, 0), (0, 1, 1), (2, 2, 1), (3, 0, 2)

l = Bezier(pts)
show(l, *[Vertex(*p) for p in pts])

# %%
# CenterArc

l = CenterArc((0, 0), 2, 15, 30)
show(l)
# %%
# PolarLine

l = PolarLine((1, 1, 1), -math.sqrt(2), 45)
show(Box(1, 1, 1, align=Align.MIN), l, transparent=True)

# %%

l = PolarLine((1, 1, 1), math.sqrt(2), angle=180)
show(Box(1, 1, 1, align=Align.MIN), l, transparent=True)

# %%
# Spline

l = Spline(
    ((0, 0, 0), (50, 0, 50), (100, 0, 0)),
    tangents=((1, 0, 0), (1, 0, 0)),
    tangent_scalars=(0.5, 2),
)

show(l)

# %%
# Line

l = Line((0, 0, 0), (0, 1, 1))
show(l)

# %%
# Helix

l = Helix(75, 150, 15, lefthand=True)
show(l)

# %%
# EllipticalCenterArc

l = EllipticalCenterArc((0, 0, 0), 1, 2, 15, 260, AngularDirection.COUNTER_CLOCKWISE)
show(l)

# %%

p1, p2, p3 = (1, 2, 3), (1, 1, 1), (2, 0, 0)
v1, v2, v3 = Vertex(*p1), Vertex(*p2), Vertex(*p3)

# RadiusArc

l = RadiusArc(p1, p2, 1.2)
show(v1, v2, l)

# %%
# SagittaArc

l = SagittaArc(p1, p2, 1.5)
show(l, v1, v2)

# %%
# TangentArc

t = (0, -1, 1)
l = TangentArc(p1, p2, tangent=t)

p4 = [x + y for x, y in zip(p1, t)]
show(l, v1, v2, Vertex(1, 1, 4), Line(p1, p4))

# %%
# ThreePointArc

l = ThreePointArc(p1, p2, p3)
show(l, v1, v2, v3)

# %%
# JernArc

# %%
