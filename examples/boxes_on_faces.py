from alg123d import *
import alg123d.shortcuts as S

b = Box(3, 3, 3)
for plane in S.planes(b.faces()):
    b += Box(1, 2, 0.1) @ (plane * Rotation(0, 0, 45))

if "show_object" in locals():
    show_object(b)
