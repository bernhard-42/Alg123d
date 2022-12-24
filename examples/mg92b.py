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

        self._bottom = None
        self._body = None
        self._top = None

    def bottom(self):
        if self._bottom is not None:
            return self._bottom

        # create a box that is not centered in z direction
        b = Box(
            self.body_length,
            self.body_width,
            self.bottom_height,
            centered=(True, True, False),
        )
        # before filleting, caclulate the location for the cable inset
        cable_loc = b.faces().min(Axis.X).origin_location
        cable_loc *= Pos(x=-(self.bottom_height - self.cable_diameter) / 2)

        b = fillet(b, b.edges(Axis.Z), self.f)
        b = fillet(b, b.edges().min(), self.f)

        #  extrude the rectangle in minus direction and subtract it from the object
        r = Rectangle(self.cable_diameter, 5 * self.cable_diameter) @ cable_loc
        b -= extrude(r, -self.cable_depth)

        self._bottom = b
        return self._bottom

    def cable(self):
        # select the face of the inset in x direction
        loc = self.bottom().faces(Axis.X)[-2].origin_location
        # create one cable of length 5 there
        cable = extrude(Circle(0.5), 5) * loc

        # return 3 cables, "* Pos" means locate relative to the object location
        return (
            cable * Pos(y=-self.cable_diameter)
            + cable
            + cable * Pos(y=self.cable_diameter)
        )

    def body(self):
        if self._body is not None:
            return self._body

        # get the top plane of the bottom
        plane = Plane(self.bottom().faces().max())

        # create a box, not centered in z direction on this plane
        b = (
            Box(
                self.body_length,
                self.body_width,
                self.body_height,
                centered=(True, True, False),
            )
            @ plane
        )

        self._body = fillet(b, b.edges(Axis.Z), self.f)

        return self._body

    def top(self):
        if self._top is not None:
            return self._top

        # get the top plane of the body
        plane = Plane(self.body().faces().max())

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

        # create the polygon, extrude it and rotate it upwards to the XZ plane
        t = extrude(Polygon(polygon), self.body_width / 2, both=True) @ Plane.XZ

        t = fillet(t, t.edges(Axis.Z), self.f)

        # finally lift it up to top body plane
        t = t @ plane

        # create the holes in the wings.
        # First, remember all edges before the action
        last = t.edges()

        # Since we don't restrict the depth of the Bore, we can define the locations on the XY plane
        for loc in Locations((-self.hole_distance / 2, 0), (self.hole_distance / 2, 0)):
            t -= Bore(t, self.hole_diameter / 2) @ loc

        # Finally get the circles of all new edges and select the two lowest
        self.fix_holes = (t.edges(GeomType.CIRCLE) - last).min_group()

        # Get the height of the overall servo by now
        offset = t.faces().max().origin_location.position.Z
        # and set x to be the right center for the motor
        loc = Pos((self.body_length - self.body_width) / 2, 0, offset)

        # create the motor housing
        motor = extrude(Circle(self.motor_diameter / 2), self.motor_height) @ loc
        motor = fillet(motor, motor.edges().max(), self.f)

        # get the max face of the motor in z direction
        plane = Plane(motor.faces().max())
        # and add the second cylinder on top of the motor
        motor += extrude(Circle(3.65), 0.5) @ plane

        # add the motor to the top
        t += motor

        # shift the location in x for the center of the gear box
        loc.position -= Vector(self.motor_diameter / 2, 0, 0)

        # create the gear at this location
        gear = extrude(Circle(self.gear_diameter / 2), self.motor_height) @ loc
        gear = fillet(gear, gear.edges().max(), self.f)

        # add the geat to the top
        t += gear

        # create the spline axis as cylinder on top of the result
        spline = extrude(Circle(self.spline_radius1), self.spline_height1) @ Plane(
            t.faces().max()
        )

        # create the spline gear as cylinder on top of the new result
        spline += extrude(Circle(self.spline_radius2), self.spline_height2) @ Plane(
            spline.faces().max()
        )
        # select the spline gear top face
        self.spline_hole = spline.edges(GeomType.CIRCLE).max()

        # and drill a hole into it
        spline -= Bore(spline, 1, self.spline_height2) @ Plane(spline.faces().max())
        spline = chamfer(spline, spline.edges().max(), 0.3)

        self._top = t + spline

        return self._top

    def create(self):
        # assemble the servo
        servo = self.bottom() + self.body() + self.top() + self.cable()

        # and add joints using the origin_location of edges (absolute locations)
        RevoluteJoint("spline", servo, self.spline_hole.origin_location.z_axis)
        RigidJoint("cable_side_hole", servo, self.fix_holes.min(Axis.X).origin_location)
        RigidJoint(
            "spline_side_hole",
            servo,
            self.fix_holes.max(Axis.X).origin_location * Rot(z=180),
        )

        return servo


servo = MG92B("mg92b").create()

show(
    servo,
    *[obj.symbol for obj in servo.joints.values()],
    transparent=True,
    reset_camera=True
)
