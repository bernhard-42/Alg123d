from alg123d import *
from cq_vscode import show, show_object, set_defaults


def vx(v):
    return Vertex(*v.to_tuple())


# %%

l1 = Polyline(((0.0000, 0.0771), (0.0187, 0.0771), (0.0094, 0.2569)))
l2 = Polyline(((0.0325, 0.2773), (0.2115, 0.2458), (0.1873, 0.3125)))
l3 = Polyline(((0.1915, 0.3277), (0.3875, 0.4865), (0.3433, 0.5071)))
l4 = Polyline(((0.3362, 0.5235), (0.375, 0.6427), (0.2621, 0.6188)))
l5 = Polyline(((0.2469, 0.6267), (0.225, 0.6781), (0.1369, 0.5835)))
l6 = Polyline(((0.1138, 0.5954), (0.1562, 0.8146), (0.0881, 0.7752)))
l7 = Line((0.0692, 0.7808), (0.0000, 0.9167))

r1 = RadiusArc(l1(1), l2(0), 0.0271)
r2 = TangentArc(l2(1), l3(0), tangent=l2 % 1)
r3 = SagittaArc(l3(1), l4(0), 0.003)
r4 = ThreePointArc((l4(1), (l4(1) + l5(0)) * 0.5 + Vector(-0.002, -0.002), l5(0)))
r5 = TangentArc(l6(1), l7(0), tangent=l6 % 1)
s = Spline((l5(1), l6(0)), tangents=(l5 % 1, l6 % 0), tangent_scalars=(2, 2))

flag = l1 + l2 + l3 + l4 + l5 + l6 + l7 + r1 + r2 + r3 + r4 + r5 + s
# flag = mirror(flag, about=Plane.YZ)

show(flag)

# %%

import build123d as bd

with bd.BuildSketch() as leaf:
    with bd.BuildLine() as outline:
        b_l1 = bd.Polyline((0.0000, 0.0771), (0.0187, 0.0771), (0.0094, 0.2569))
        b_l2 = bd.Polyline((0.0325, 0.2773), (0.2115, 0.2458), (0.1873, 0.3125))
        b_r1 = bd.RadiusArc(b_l1 @ 1, b_l2 @ 0, 0.0271)
        b_l3 = bd.Polyline((0.1915, 0.3277), (0.3875, 0.4865), (0.3433, 0.5071))
        b_r2 = bd.TangentArc(b_l2 @ 1, b_l3 @ 0, tangent=b_l2 % 1)
        b_l4 = bd.Polyline((0.3362, 0.5235), (0.375, 0.6427), (0.2621, 0.6188))
        b_r3 = bd.SagittaArc(b_l3 @ 1, b_l4 @ 0, 0.003)
        b_l5 = bd.Polyline((0.2469, 0.6267), (0.225, 0.6781), (0.1369, 0.5835))
        b_r4 = bd.ThreePointArc(
            b_l4 @ 1, (b_l4 @ 1 + b_l5 @ 0) * 0.5 + bd.Vector(-0.002, -0.002), b_l5 @ 0
        )
        b_l6 = bd.Polyline((0.1138, 0.5954), (0.1562, 0.8146), (0.0881, 0.7752))
        b_s = bd.Spline(
            b_l5 @ 1, b_l6 @ 0, tangents=(b_l5 % 1, b_l6 % 0), tangent_scalars=(2, 2)
        )
        b_l7 = bd.Line((0.0692, 0.7808), (0.0000, 0.9167))
        b_r5 = bd.TangentArc(b_l6 @ 1, b_l7 @ 0, tangent=b_l6 % 1)
        bd.Mirror(*outline.edges(), about=bd.Plane.YZ)
    bd.MakeFace(*leaf.pending_edges)

with bd.BuildSketch() as west_field:
    with bd.Locations((-1, 0)):
        bd.Rectangle(0.5, 1, centered=(False, False))

with bd.BuildSketch() as east_field:
    bd.Mirror(west_field.sketch, about=bd.Plane.YZ)

with bd.BuildSketch() as centre_field:
    bd.Rectangle(1, 1, centered=(True, False))
    bd.Add(leaf.sketch, mode=bd.Mode.SUBTRACT)

show(leaf)
# %%

# if "show_object" in locals():
#     show_object(
#         [west_field.sketch.wrapped, east_field.sketch.wrapped, leaf.sketch.wrapped],
#         name="flag_red_parts",
#         options={"color": (255, 0, 0)},
#     )
#     show_object(
#         centre_field.sketch.wrapped,
#         name="flag_white_part",
#         options={"color": (255, 255, 255)},
#     )
# %%
