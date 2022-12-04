from alg123d import *
import alg123d.shortcuts as S

pipes = Box(10, 10, 10) @ Rotation(10, 20, 30)

for plane in S.planes(pipes.faces()):
    pipe = Circle(4) @ plane
    pipes -= extrude(pipe, amount=-5)
    pipe = Circle(4.5) @ plane
    pipe -= Circle(4) @ plane

    last = pipes.edges()
    pipes += extrude(pipe, amount=10)
    pipes = fillet(pipes, S.diff(pipes.edges(), last), radius=0.2)

if "show_object" in locals():
    show_object(pipes, name="intersecting pipes")
