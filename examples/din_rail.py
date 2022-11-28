from alg123d import *


# 35x7.5mm DIN Rail Dimensions
overall_width, top_width, height, thickness, fillet_radius = 35, 27, 7.5, 1, 0.8
rail_length = 1000
slot_width, slot_length, slot_pitch = 6.2, 15, 25

din = Rectangle(overall_width, thickness, centered=(True, False))
din += Rectangle(top_width, height, centered=(True, False))
din -= Rectangle(
    top_width - 2 * thickness,
    height - thickness,
    centered=(True, False),
)

inside_vertices = (
    din.vertices()
    .filter_by_position(Axis.Y, 0.0, height, inclusive=(False, False))
    .filter_by_position(
        Axis.X,
        -overall_width / 2,
        overall_width / 2,
        inclusive=(False, False),
    )
)

din = fillet(din, inside_vertices, radius=fillet_radius)

outside_vertices = filter(
    lambda v: (v.Y == 0.0 or v.Y == height)
    and -overall_width / 2 < v.X < overall_width / 2,
    din.vertices(),
)
din = fillet(din, outside_vertices, radius=fillet_radius + thickness)

rail = extrude(din, rail_length)

plane = back_plane(rail)

slot_faces = Empty2()
for loc in GridLocations(0, slot_pitch, 1, rail_length // slot_pitch - 1):
    slot_faces += SlotOverall(slot_length, slot_width) @ (plane * loc)

slots = extrude(slot_faces, -height)

rail -= slots

if "show_object" in locals():
    show_object(rail, name="rail")
