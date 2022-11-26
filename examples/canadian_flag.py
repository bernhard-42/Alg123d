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

flag += make_face(mirror(flag, about=Plane.YZ))

show(flag)
