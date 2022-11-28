from alg123d import *

b = Box(3, 3, 3)
for plane in b.workplanes():
    b += Box(1, 2, 0.1) @ (plane * Rotation(0, 0, 45))

if "show_object" in locals():
    show_object(b)

# %%
