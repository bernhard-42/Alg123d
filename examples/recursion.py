from cq_vscode import show
from alg123d import *

c0 = Text(
    "|―|―|―|―|",
    font="Times New Roman",
    font_size=15,
    font_style=FontStyle.BOLD,
    align=(Align.MIN, Align.CENTER),
)

c = [offset(c0, 1.2 * i) for i in range(0, 14)]


def func(idx):
    return c[idx] if idx == 0 else c[idx] - func(idx - 1)


mainp = extrude(func(13), 1) @ Pos(0, 2.25)

show(mainp, axes=True, axes0=True)
