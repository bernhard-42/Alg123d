from alg123d import *

l1 = Polyline(((0.0000, 0.0771), (0.0187, 0.0771), (0.0094, 0.2569)))
l2 = Polyline(((0.0325, 0.2773), (0.2115, 0.2458), (0.1873, 0.3125)))
l3 = Polyline(((0.1915, 0.3277), (0.3875, 0.4865), (0.3433, 0.5071)))
l4 = Polyline(((0.3362, 0.5235), (0.375, 0.6427), (0.2621, 0.6188)))
l5 = Polyline(((0.2469, 0.6267), (0.225, 0.6781), (0.1369, 0.5835)))
l6 = Polyline(((0.1138, 0.5954), (0.1562, 0.8146), (0.0881, 0.7752)))
l7 = Line((0.0692, 0.7808), (0.0000, 0.9167))

r1 = RadiusArc(l1 @ 1, l2 @ 0, 0.0271)
r2 = TangentArc(l2 @ 1, l3 @ 0, tangent=l2 % 1)
r3 = SagittaArc(l3 @ 1, l4 @ 0, 0.003)
r4 = ThreePointArc(l4 @ 1, (l4 @ 1 + l5 @ 0) * 0.5 + Vector(-0.002, -0.002), l5 @ 0)
r5 = TangentArc(l6 @ 1, l7 @ 0, tangent=l6 % 1)
s = Spline((l5 @ 1, l6 @ 0), tangents=(l5 % 1, l6 % 0), tangent_scalars=(2, 2))

# leaf = l1 + l2 + l3 + l4 + l5 + l6 + l7 + r1 + r2 + r3 + r4 + r5 + s
# The vectorized version is faster:
leaf = l1 + [l2, l3, l4, l5, l6, l7, r1, r2, r3, r4, r5, s]

leaf += mirror(leaf, about=Plane.YZ)
leaf = make_face(leaf)

field = Rectangle(0.5, 1, align=(Align.MIN, Align.MIN))
west_field = Pos(-1, 0) * field
east_field = Pos(0.5, 0) * field
centre_field = Rectangle(1, 1, align=(Align.CENTER, Align.MIN)) - leaf
# %%

if "show_object" in locals():
    show_object(
        centre_field,
        name="flag_white_part",
        options={"color": (255, 255, 255)},
    )

    show_object(west_field, name="west_field", options={"color": (255, 0, 0)})
    show_object(east_field, name="east_field", options={"color": (255, 0, 0)})
    show_object(leaf, name="leaf", options={"color": (255, 0, 0)})
