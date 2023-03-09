from alg123d import *

set_defaults(axes=True, axes0=True, transparent=True)

# %%

a = Box(1, 2, 3)

b = scale(a, (2, 1, 2 / 3))

show(a, b)
# %%

b = scale(a, 1.1)

show(a, b)

# %%

a = Rectangle(1, 2)
b = scale(a, 2)

show(a, b)

# %%
# TODO
a = Rectangle(1, 2)
b = scale(a, (2, 1))

# show(a, b)
