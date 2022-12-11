from alg123d import *
from alg123d.shortcuts import *

obj = Box(5, 5, 1)
for plane in planes(obj.faces().filter_by(Axis.Z)):
    obj -= Sphere(1.8) @ plane

if "show_object" in locals():
    show_object(obj)
