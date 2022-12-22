from alg123d import *
from alg123d.shortcuts import *

height, width, thickness, padding = 60, 80, 10, 12
screw_shaft_radius, screw_head_radius, screw_head_height = 1.5, 3, 3
bearing_axle_radius, bearing_radius, bearing_thickness = 4, 11, 7

# Build pillow block as an extruded sketch with counter bore holes
plan = Rectangle(width, height)
plan = fillet(plan, plan.vertices(), 5)
pillow_block = extrude(plan, thickness)

plane = Plane(pillow_block.faces().max())

pillow_block -= (
    CounterBore(pillow_block, bearing_axle_radius, bearing_radius, bearing_thickness)
    @ plane
)
for loc in GridLocations(width - 2 * padding, height - 2 * padding, 2, 2):
    pillow_block -= CounterBore(
        pillow_block, screw_shaft_radius, screw_head_radius, screw_head_height
    ) @ (plane * loc)

# Render the part
if "show_object" in locals():
    show_object(pillow_block)
