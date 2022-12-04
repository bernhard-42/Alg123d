from alg123d import *
import alg123d.shortcuts as S

obj = Box(5, 5, 1)
for plane in S.planes(obj.faces().filter_by(Axis.Z)):
    obj -= Sphere(1.8) @ plane

if "show_object" in locals():
    show_object(obj)
