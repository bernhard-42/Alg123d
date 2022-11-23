from py123d import *
import build123d as bd
from cq_vscode import show, set_defaults

set_defaults(
    axes=True, axes0=True, transparent=True, grid=(True, True, True), reset_camera=False
)

# %%

r = Rectangle(1, 2)

o = offset(r, 0.1)
show(o, r.edges(), Rectangle(1.5, 2.5).edges())

# %%

o = offset(r, -0.1)
show(o, r.edges(), Rectangle(1.5, 2.5).edges())

# %%

o = r - offset(r, -0.1)
show(o, r.edges(), Rectangle(1.5, 2.5).edges())

# %%

o = offset(r, 0.1) - r
show(o, r.edges(), Rectangle(1.5, 2.5).edges())

# %%

b = Box(1, 2, 3)

openings = b.faces().sort_by()[-1]

o = offset(b, 0.1, openings)

show(b.edges(), o, transparent=False)

# %%

openings = (b.faces().sort_by()[-1], b.faces().sort_by()[0])

o = offset(b, 0.1, openings)

show(b.edges(), o, transparent=False)

# %%

openings = b.faces().sort_by()[-1]

o = offset(b, -0.1, openings)

show(b.edges(), o, transparent=False)

# %%

o = offset(b, -0.1)

show(b.edges(), o)

# %%

o = offset(b, 0.1)

show(b.edges(), o)

# %%
