from alg123d import *
from ocp_vscode import (
    show,
    show_object,
    reset_show,
    set_port,
    set_defaults,
    get_defaults,
)

set_port(3939)

# %%

b = Box(3, 3, 3)
b2 = Rot(0, 0, 45) * extrude(Rectangle(1,2), 0.2)
for plane in Planes(b.faces()):
    b += plane * b2

show(b)

# %%
