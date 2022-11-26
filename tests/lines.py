from alg123d import *
from cq_vscode import show, set_defaults

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

l = PolarLine((1, 1, 1), 2, direction=(-1, 1, 1))
show(l)

# %%

l = PolarLine((1, 1, 1), 2, angle=25)
show(l)

# %%
# Spline


# %%
# Line

l = Line((0, 0, 0), (0, 1, 1))
show(l)

# %%
# Helix

l = Helix(75, 150, 15, center=(75, 40, 15), direction=(1, 0, 0))
show(l)
# %%
# EllipticalCenterArc

l = EllipticalCenterArc((0, 0, 0), 1, 2, 15, 260, AngularDirection.COUNTER_CLOCKWISE)
show(l)
# %%
# RadiusArc

# %%
# SagittaArc

# %%
# TangentArc

# %%
# ThreePointArc

# %%
# JernArc

# %%
