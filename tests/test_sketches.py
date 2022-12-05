from alg123d import *
from cq_vscode import show, set_defaults

set_defaults(axes=True, axes0=True, transparent=False)

# %%

show(Circle(1))

# %%

show(Circle(1, centered=False))

# %%

show(Ellipse(1, 2))

# %%

show(Ellipse(1, 2, centered=False))

# %%

show(Ellipse(1, 2))

# %%

show(Rectangle(1, 2))

# %%

show(Rectangle(1, 2, centered=False))

# %%

pts = [(0, 1), (1, 0), (1, 1), (0, 1)]
show(Polygon(pts))

# %%

show(Polygon(pts, centered=False))

# %%

show(RegularPolygon(2, 7))

# %%

show(RegularPolygon(2, 7, centered=centered))

# %%

show(Trapezoid(1, 2, 80), Rectangle(1, 2).edges())

# %%


show(Trapezoid(1, 2, 80, centered=False), Rectangle(1, 2, centered=False).edges())

# %%

show(Text("Alg123d", 8, font_style=FontStyle.ITALIC))

# %%

from alg123d import *
from cq_vscode import show, set_defaults

set_defaults(axes=True, axes0=True, transparent=False)

# %%

c = Circle(1) - Rectangle(2, 2) @ (0.75, 0) - Rectangle(2, 2) @ (0, 0.75)
arc = c.edges()[0]

s = SlotArc(arc, 0.1)
show(Rectangle(2, 2).edges(), s)

# %%

s = SlotCenterToCenter(6, 1)
show(Rectangle(8, 2).edges(), s)

# %%

s = SlotCenterToCenter(6, 1) @ Location((0, 0), 30)
show(Rectangle(8, 2).edges(), s)

# %%

s = SlotCenterPoint((1, 1), (2, 0), 2)
show((Rectangle(4, 4) @ (1, 1)).edges(), s)


# %%

s = SlotOverall(3, 1)

show(Rectangle(3, 1).edges(), s)

# %%
