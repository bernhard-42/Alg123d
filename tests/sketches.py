from alg123d import *
from cq_vscode import show, set_defaults

set_defaults(axes=True, axes0=True, transparent=False)
centered = (False, False)

# %%

show(Circle(1))

# %%

show(Circle(1, centered=centered))

# %%

show(Ellipse(1, 2))

# %%

show(Ellipse(1, 2, centered=centered))

# %%

show(Ellipse(1, 2))

# %%

show(Rectangle(1, 2))

# %%

show(Rectangle(1, 2, centered=centered))

# %%

pts = [(0, 1), (1, 0), (1, 1), (0, 1)]
show(Polygon(pts))

# %%

show(Polygon(pts, centered=centered))

# %%

show(RegularPolygon(2, 7))

# %%

show(RegularPolygon(2, 7, centered=centered))

# %%

show(Trapezoid(1, 2, 80), Rectangle(1, 2).edges())

# %%


show(Trapezoid(1, 2, 80, centered=centered), Rectangle(1, 2, centered=centered).edges())

# %%

show(Text("Alg123d", 8, font_style=FontStyle.ITALIC))

# %%

from alg123d import *
from cq_vscode import show, set_defaults

set_defaults(axes=True, axes0=True, transparent=False)

# %%

c = Circle(1) - Rectangle(2, 2) @ (1, 0) - Rectangle(2, 2) @ (0, 0.75)
arc = c.edges()[0]

s = SlotArc(arc, 0.1)
show(s)

# %%

s = SlotCenterToCenter(6, 1)
show(s)

# %%

s = SlotCenterToCenter(6, 1) @ Location((0, 0), 30)
show(s)

# %%

s = SlotCenterPoint((1, 1), (2, 0), 2)
show(s)

# %%

s = SlotOverall(3, 1)

show(s)

# %%
