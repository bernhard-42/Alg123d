from alg123d import *
from alg123d.shortcuts import *


class MG92B:
    def __init__(self, name):
        self.name = name

        self.body_height = 14
        self.body_length = 22.8
        self.body_width = 12.00

        self.overall_length = 31.3
        self.top_length = 15.6
        self.hole_distance = 27.8
        self.hole_diameter = 2

        self.spline_radius1 = 2.1
        self.spline_radius2 = 2.4
        self.spline_height1 = 1.2
        self.spline_height2 = 2.8

        self.bottom_height = 2.8

        self.side_height = 1
        self.top_cable_side_height = 2.2
        self.wing_thickness = 2.1
        self.top_wing_distance = 3.9
        self.offset = 1.0

        self.gap = 0.25

        self.motor_height = 4.6
        self.motor_diameter = 11.5
        self.gear_diameter = 6

        self.cable_diameter = 1
        self.f = 0.3

    def bottom(self):
        b = Box(self.body_length, self.body_width, self.bottom_height)
        loc = min_face(b, Axis.X).center_location

        b = fillet(b, b.edges().filter_by(Axis.Z), self.f)
        b = fillet(b, min_edges(b), self.f)

        loc.position -= Vector(0, 0, (self.bottom_height - self.cable_diameter) / 2)
        r = Rectangle(self.cable_diameter, 5 * self.cable_diameter) @ (loc)
        b -= extrude(r, -2)
        return b

    def cable(self):
        return extrude(Circle(0.5), 5) @ Plane.YZ

    def body(self):
        b = Box(self.body_length, self.body_width, self.body_height)
        return fillet(b, b.edges().filter_by(Axis.Z), self.f)

    def top(self):
        polygon = (
            (-self.body_length / 2, 0.0),
            (self.body_length / 2, 0.0),
            (self.body_length / 2, self.top_wing_distance),
            (self.overall_length / 2, self.top_wing_distance),
            (
                self.overall_length / 2,
                self.top_wing_distance + self.wing_thickness,
            ),
            (
                self.body_length / 2,
                self.top_wing_distance + self.wing_thickness,
            ),
            (
                self.body_length / 2,
                self.top_wing_distance
                + self.wing_thickness
                + self.top_cable_side_height,
            ),
            (
                self.body_length / 2 - self.top_length,
                self.top_wing_distance
                + self.wing_thickness
                + self.top_cable_side_height,
            ),
            (
                -self.body_length / 2,
                self.top_wing_distance + self.wing_thickness + self.side_height,
            ),
            (
                -self.body_length / 2,
                self.top_wing_distance + self.wing_thickness,
            ),
            (
                -self.overall_length / 2,
                self.top_wing_distance + self.wing_thickness,
            ),
            (-self.overall_length / 2, self.top_wing_distance),
            (-self.body_length / 2, self.top_wing_distance),
            (-self.body_length / 2, 0.0),
        )
        self.poly = polygon
        t = extrude(Polygon(polygon), self.body_width / 2, both=True) @ Plane.XZ
        t = fillet(t, t.edges().filter_by(Axis.Z), self.f)

        for plane in Planes(t.faces().filter_by(Axis.Z).group_by()[-2]):
            print(plane)
            d = 0  # (self.hole_distance - self.body_length) / 8
            print(d)
            for loc in Locations(Pos(-d, 0), Pos(d, 0)):
                print(loc)
                t -= Bore(t, self.hole_diameter / 2) @ (plane * loc)
        return t


servo = MG92B("mg92b")
bottom = servo.bottom()
cable = servo.cable()
body = servo.body()
top = servo.top()
show(top)
# show(bottom, cable, body, top, transparent=True)
