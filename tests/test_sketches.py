from alg123d import *

set_defaults(axes=True, axes0=True, transparent=False)

# %%

show(Circle(1))

# %%

show(Circle(1, align=Align.MIN))

# %%

show(Circle(1, align=Align.MAX))

# %%

show(Ellipse(1, 2))

# %%

show(Ellipse(1, 2, align=Align.MIN))

# %%

show(Ellipse(1, 2, align=Align.MAX))

# %%

show(Rectangle(1, 2))

# %%

show(Rectangle(1, 2, align=Align.MIN))

# %%

show(Rectangle(1, 2, align=Align.MAX))

# %%

show(RectangleRounded(1, 2, 0.1))

# %%

show(RectangleRounded(1, 2, 0.1, align=Align.MIN))

# %%

show(RectangleRounded(1, 2, 0.1, align=Align.MAX))
# %%

pts = [(0, 1), (1, 0), (1, 1), (0, 1)]
show(Polygon(pts))

# %%

show(Polygon(pts, align=Align.MIN))

# %%

show(Polygon(pts, align=Align.MAX))

# %%

show(RegularPolygon(2, 7))

# %%

show(RegularPolygon(2, 7, align=Align.MIN))

# %%

show(RegularPolygon(2, 7, align=Align.MAX))

# %%

show(Trapezoid(1, 2, 80), Rectangle(1, 2).edges())

# %%

show(Trapezoid(1, 2, 80, align=Align.MIN), Rectangle(1, 2, align=Align.MIN).edges())

# %%

show(Trapezoid(1, 2, 80, align=Align.MAX), Rectangle(1, 2, align=Align.MAX).edges())

# %%

show(Text("Alg123d", 8, font_style=FontStyle.ITALIC))

# %%

c = Circle(1) - Rectangle(2, 2) @ Pos(0.75, 0) - Rectangle(2, 2) @ Pos(y=0.75)
arc = c.edges()[0]

s = SlotArc(arc, 0.1)
show(Rectangle(2, 2).edges(), s)

# %%

s = SlotCenterToCenter(6, 1)
show(Rectangle(8, 2).edges(), s)

# %%

s = Location((0, 0), 30) * SlotCenterToCenter(6, 1)
show(Rectangle(8, 2).edges(), s)

# %%

s = SlotCenterPoint((1, 1), (2, 0), 2)
show((Pos(1, 1)*Rectangle(4, 4)).edges(), s)


# %%

s = SlotOverall(3, 1)

show(Rectangle(3, 1).edges(), s)

# %%
