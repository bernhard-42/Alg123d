from alg123d import *
from alg123d.shortcuts import *

blocks = Box(1, 2, 1, centered=(True, False, False)) @ Pos(-1, -1, 0)
blocks += Box(1, 1, 2, centered=(True, False, False))
blocks += Box(1, 2, 1, centered=(True, False, False)) @ Pos(1, -1, 0)

bottom_edges = blocks.edges().filter_by_position(Axis.Z, 0, 1, inclusive=(True, False))
blocks2 = chamfer(blocks, bottom_edges, length=0.1)

top_edges = blocks2.edges().filter_by_position(Axis.Z, 1, 2, inclusive=(False, True))
blocks2 = chamfer(blocks2, top_edges, length=0.1)


if "show_object" in locals():
    show_object(blocks2)
