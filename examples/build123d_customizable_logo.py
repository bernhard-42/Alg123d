from alg123d import *

logo_text = Text("123d", font_size=10, align=(Align.MIN, Align.MIN))
font_height = logo_text.vertices().sort_by(Axis.Y)[-1].Y

build_text = Text("build", font_size=5, align=(Align.CENTER, Align.CENTER))
build_bb = build_text.bounding_box()
build_width = build_bb.max.X - build_bb.min.X

cust_text = Text(
    "customizable",
    font_size=2.9,
    align=(Align.CENTER, Align.CENTER),
    font_style=FontStyle.BOLD,
)
cust_bb = cust_text.bounding_box()
cust_width = cust_bb.max.X - cust_bb.min.X

l1 = Line((font_height * 0.3, 0), (font_height * 0.3, font_height))
one = l1 + TangentArc(l1 @ 1, (0, font_height * 0.7), tangent=(l1 % 1) * -1)

two = Pos(font_height * 0.35, 0) * Text("2", font_size=10, align=(Align.MIN, Align.MIN))

three_d = Text("3d", font_size=10, align=(Align.MIN, Align.MIN))
three_d = Pos(font_height * 1.1, 0) * extrude(three_d, amount=font_height * 0.3)
logo_width = three_d.vertices().sort_by(Axis.X)[-1].X

t1 = TangentArc((0, 0), (1, 0.75), tangent=(1, 0))
arrow_left = t1 + mirror(t1, about=Plane.XZ)

ext_line_length = font_height * 0.5
dim_line_length = (logo_width - build_width - 2 * font_height * 0.05) / 2

l1 = Line((0, -font_height * 0.1), (0, -ext_line_length - font_height * 0.1))
l2 = Line(
    (logo_width, -font_height * 0.1),
    (logo_width, -ext_line_length - font_height * 0.1),
)
extension_lines = Pos(*(l1 @ 0.5)) * arrow_left
extension_lines += (Pos(*(l2 @ 0.5)) * Rot(z=180)) * arrow_left
extension_lines += Line(l1 @ 0.5, l1 @ 0.5 + Vector(dim_line_length, 0))
extension_lines += Line(l2 @ 0.5, l2 @ 0.5 - Vector(dim_line_length, 0))

# Precisely center the build Faces
p1 = Pos((l1 @ 0.5 + l2 @ 0.5) / 2 - Vector((build_bb.max.X + build_bb.min.X) / 2, 0))
build = p1 * build_text

# add the customizable text to the build text sketch
p2 = Pos((l1 @ 1 + l2 @ 1) / 2 - Vector(cust_bb.max.X + cust_bb.min.X, 1.4))
build += p2 * cust_text

cmpd = Compound.make_compound([three_d, two, one, build, extension_lines])

if "show_object" in locals():
    show_object(cmpd, name="compound")
    # show_object(one.line.wrapped, name="one")
    # show_object(two.sketch.wrapped, name="two")
    # show_object(three_d.part.wrapped, name="three_d")
    # show_object(extension_lines.line.wrapped, name="extension_lines")
    # show_object(build.sketch.wrapped, name="build")
