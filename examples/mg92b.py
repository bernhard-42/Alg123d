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
        self.cable_depth = 2
        self.f = 0.3

    def bottom(self):
        b = Box(
            self.body_length,
            self.body_width,
            self.bottom_height,
            centered=(True, True, False),
        )
        loc = b.faces().min(Axis.X).center_location

        b = fillet(b, b.edges(Axis.Z), self.f)
        b = fillet(b, b.edges().min(), self.f)

        loc.position -= Vector(0, 0, (self.bottom_height - self.cable_diameter) / 2)
        r = Rectangle(self.cable_diameter, 5 * self.cable_diameter) @ loc
        b -= extrude(r, -self.cable_depth)
        return b

    def cable(self):
        return extrude(Circle(0.5), 5) @ (
            Location(
                (
                    -self.body_length / 2 + self.cable_depth,
                    0,
                    (self.cable_diameter) / 2,
                ),
                (0, -90, 0),
            )
        )

    def body(self):
        b = Box(
            self.body_length,
            self.body_width,
            self.body_height,
            centered=(True, True, False),
        ) @ Pos(z=self.bottom_height)
        return fillet(b, b.edges(Axis.Z), self.f)

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
        t = fillet(t, t.edges(Axis.Z), self.f)
        t = t @ Pos(z=self.bottom_height + self.body_height)

        last = t.edges()
        for loc in Locations((-self.hole_distance / 2, 0), (self.hole_distance / 2, 0)):
            t -= Bore(t, self.hole_diameter / 2) @ loc
        self.holes = (t.edges(GeomType.CIRCLE) - last).min_group()

        offset = t.faces().max().center_location.position.Z
        loc = Pos((self.body_length - self.body_width) / 2, 0, offset)
        motor = extrude(Circle(self.motor_diameter / 2), self.motor_height) @ loc
        motor = fillet(motor, motor.edges().max(), self.f)
        plane = Plane(motor.faces().max())
        motor += extrude(Circle(3.65), 0.5) @ plane
        t += motor

        loc.position -= Vector(self.motor_diameter / 2, 0)
        gear = extrude(Circle(self.gear_diameter / 2), self.motor_height) @ loc
        gear = fillet(gear, gear.edges().max(), self.f)
        t += gear

        spline = extrude(Circle(self.spline_radius1), self.spline_height1) @ Plane(
            t.faces().max()
        )
        spline += extrude(Circle(self.spline_radius2), self.spline_height2) @ Plane(
            spline.faces().max()
        )
        self.spline_hole = spline.edges(GeomType.CIRCLE).max()
        spline -= Bore(spline, 1, self.spline_height2) @ Plane(spline.faces().max())
        spline = chamfer(spline, spline.edges().max(), 0.3)
        t += spline
        return t


servo = MG92B("mg92b")
bottom = servo.bottom()
loc = Location(
    (
        -servo.body_length / 2 + servo.cable_depth,
        0,
        -(servo.bottom_height - servo.cable_diameter) / 2,
    ),
    (0, -90, 0),
)
cable2 = servo.cable()
cable1 = cable2.moved(Pos(y=-1))
cable3 = cable2.moved(Pos(y=1))
body = servo.body()
top = servo.top()
mg92b = bottom + cable1 + cable2 + cable3 + body + top

show(mg92b, *servo.holes, servo.spline_hole, transparent=False)
