from itertools import product

from alg123d import *

pcb = Rectangle(70, 30)

for loc in GridLocations(60, 20, 2, 2):
    pcb -= Circle(2) @ loc

for i, y in product(range(65 // 5), (-15, -10, 10, 15)):
    x = i * 5 - 30
    pcb -= Circle(1) @ (x, y)

for x, i in product((30, 35), range(30 // 5 - 1)):
    y = i * 5 - 10
    pcb -= Circle(1) @ (x, y)

pcb = extrude(pcb, 3)

if "show_object" in locals():
    show(pcb)
