from alg123d import *
from alg123d.shortcuts import *

set_defaults(axes=True, axes0=True, transparent=True, grid=(True, True, True))

# %%

# Offset line

p = Polyline([(-2, 5), (-12, 5), (-12, 10), (10, 10)])
o = offset(p, 1)
show(o, p @ Pos(0, -15, 0))


# %%

# Offset face

f = Rectangle(10, 20)
o = offset(f, 1)
show(f, o @ Pos(15, 0, 0))

# %%

# Offset solid

b = Box(10, 20, 15)
o = offset(b, 1)
show(b, o @ Pos(15, 0, 0), transparent=True)

# %%
b = Box(10, 20, 15)
o = offset(b, 1) - b
show(b, o @ Pos(15, 0, 0), transparent=True)

# %%
# Offset solid

b = Box(10, 20, 15)
o = offset(b, -1)
show(b, o @ Pos(15, 0, 0), transparent=True)

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

o = shell(b, 0.1, openings)

show(b.edges(), o, transparent=False)

# %%

openings = (b.faces().sort_by()[-1], b.faces().sort_by()[0])

o = shell(b, 0.1, openings)

show(b.edges(), o, transparent=False)

# %%

openings = S.max_face(b)

o = shell(b, -0.1, openings)

show(b.edges(), o, transparent=False)

# %%
