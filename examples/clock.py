from alg123d import *

clock_radius = 10

l1 = CenterArc((0, 0), clock_radius * 0.975, 0.75, 4.5)
l2 = CenterArc((0, 0), clock_radius * 0.925, 0.75, 4.5)
l3 = Line(l1 @ 0, l2 @ 0)
l4 = Line(l1 @ 1, l2 @ 1)
minute_indicator = make_face([l1, l3, l2, l4])
minute_indicator = fillet(
    minute_indicator, minute_indicator.vertices(), radius=clock_radius * 0.01
)

clock_face = Circle(clock_radius)
for loc in PolarLocations(0, 60):
    clock_face -= minute_indicator @ loc

for loc in PolarLocations(clock_radius * 0.875, 12):
    clock_face -= SlotOverall(clock_radius * 0.05, clock_radius * 0.025) @ loc

for hour, loc in enumerate(
    PolarLocations(clock_radius * 0.75, 12, 420, 60, rotate=False)
):
    clock_face -= (
        Text(
            str(hour + 1),
            fontsize=clock_radius * 0.175,
            font_style=FontStyle.BOLD,
            halign=Halign.CENTER,
        )
        @ loc
    )

if "show_object" in locals():
    show_object(clock_face)
