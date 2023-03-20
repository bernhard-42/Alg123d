from alg123d import *


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

        self.top_cable_side_height = 1
        self.top_height = 2.2
        self.wing_height = 2.1
        self.top_height_under_wing = 3.9

        self.gap = 0.25

        self.motor_height1 = 4.6
        self.motor_height2 = 0.5
        self.motor_diameter = 11.5
        self.gear_diameter = 6

        self.cable_diameter = 1
        self.cable_depth = 2
        self.f = 0.3

        self._bottom = None
        self._body = None
        self._top = None
        self._spline = None

    def bottom(self):
        if self._bottom is not None:
            return self._bottom

        # create a box that is not centered in z direction
        b = Box(
            self.body_length,
            self.body_width,
            self.bottom_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        # before filleting, caclulate the location for the cable inset
        cable_loc = b.faces().min(Axis.X).center_location
        cable_loc *= Pos(x=-(self.bottom_height - self.cable_diameter) / 2)

        b = fillet(b, b.edges(Axis.Z), self.f)
        b = fillet(b, b.edges().min(), self.f)

        #  extrude the rectangle in minus direction and subtract it from the object
        r = cable_loc * Rectangle(self.cable_diameter, 5 * self.cable_diameter)
        b -= extrude(r, -self.cable_depth)

        self._bottom = b
        return self._bottom

    def cable(self):
        # select the face of the inset in x direction
        loc = self.bottom().faces(Axis.X)[-2].center_location
        # create one cable of length 5 there
        cable = extrude(Circle(0.5), 5)

        # return 3 cables at location loc with "* Pos" means locate relative to the object location
        return (
            loc * Pos(y=-self.cable_diameter) * cable
            + loc * cable
            + loc * Pos(y=self.cable_diameter) * cable
        )

    def body(self):
        if self._body is not None:
            return self._body

        # get the top plane of the bottom
        plane = Plane(self.bottom().faces().max())

        # create a box, not centered in z direction on this plane
        b = plane * Box(
            self.body_length,
            self.body_width,
            self.body_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
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
            (self.body_length / 2, self.top_height_under_wing),
            (self.overall_length / 2, self.top_height_under_wing),
            (
                self.overall_length / 2,
                self.top_height_under_wing + self.wing_height,
            ),
            (
                self.body_length / 2,
                self.top_height_under_wing + self.wing_height,
            ),
            (
                self.body_length / 2,
                self.top_height_under_wing + self.wing_height + self.top_height,
            ),
            (
                self.body_length / 2 - self.top_length,
                self.top_height_under_wing + self.wing_height + self.top_height,
            ),
            (
                -self.body_length / 2,
                self.top_height_under_wing
                + self.wing_height
                + self.top_cable_side_height,
            ),
            (
                -self.body_length / 2,
                self.top_height_under_wing + self.wing_height,
            ),
            (
                -self.overall_length / 2,
                self.top_height_under_wing + self.wing_height,
            ),
            (-self.overall_length / 2, self.top_height_under_wing),
            (-self.body_length / 2, self.top_height_under_wing),
            (-self.body_length / 2, 0.0),
        )
        self.poly = polygon
        # create the polygon, extrude it and rotate it upwards to the XZ plane
        t = Plane.XZ * extrude(Polygon(polygon), self.body_width / 2, both=True)

        t = fillet(t, t.edges(Axis.Z), self.f)

        # finally lift it up to top body plane
        t = plane * t

        # create the holes in the wings.
        # First, remember all edges before the action
        last = t.edges()

        # Since we don't restrict the depth of the Bore, we can define the locations on the XY plane
        for loc in Locations((-self.hole_distance / 2, 0), (self.hole_distance / 2, 0)):
            t -= loc * Bore(t, self.hole_diameter / 2)

        # Finally get the circles of all new edges and select the two lowest
        self.fix_holes = (t.edges(GeomType.CIRCLE) - last).min_group()

        # Get the height of the overall servo by now
        offset = t.faces().max().center_location.position.Z
        # and set x to be the right center for the motor
        loc = Pos((self.body_length - self.body_width) / 2, 0, offset)

        # create the motor housing
        motor = loc * extrude(Circle(self.motor_diameter / 2), self.motor_height1)
        motor = fillet(motor, motor.edges().max(), self.f)

        # get the max face of the motor in z direction
        plane = Plane(motor.faces().max())
        # and add the second cylinder on top of the motor
        motor += plane * extrude(Circle(3.65), self.motor_height2)

        # add the motor to the top
        t += motor

        # shift the location in x for the center of the gear box
        loc.position -= Vector(self.motor_diameter / 2, 0, 0)

        # create the gear at this location
        gear = loc * extrude(Circle(self.gear_diameter / 2), self.motor_height1)
        gear = fillet(gear, gear.edges().max(), self.f)

        # add the geat to the top
        t += gear
        self._top = t

        return self._top

    def spline(self):
        # get the top plane of the body
        plane = Plane(self.top().faces().max())

        # create the spline axis as cylinder on top of the result
        spline = plane * extrude(Circle(self.spline_radius1), self.spline_height1)

        # create the spline gear as cylinder on top of the new result
        plane = Plane(spline.faces().max())
        spline += plane * extrude(Circle(self.spline_radius2), self.spline_height2)

        # select the spline gear top face
        self.spline_hole = spline.edges(GeomType.CIRCLE).max()

        # and drill a hole into it
        spline -= Plane(spline.faces().max()) * Bore(spline, 1, self.spline_height2)

        self._spline = chamfer(spline, spline.edges().max(), 0.3)

        return self._spline

    def create(self):
        # assemble the servo
        servo = self.bottom() + self.body() + self.top() + self.cable() + self.spline()

        # and add joints using the center_location of edges (absolute locations)
        RevoluteJoint(
            "spline",
            servo,
            self.spline_hole.center_location.z_axis,
            angular_range=(270, 90),
        )
        RigidJoint("cable_side_hole", servo, self.fix_holes.min(Axis.X).center_location)
        RigidJoint(
            "spline_side_hole",
            servo,
            self.fix_holes.max(Axis.X).center_location * Rot(z=180),
        )

        height_under_wing = self.fix_holes.min(Axis.X).center_location.position.Z
        height = self.top().faces().max().center_location.position.Z

        servo.metadata = {
            "hole_distance": self.hole_distance,
            "hole_radius": self.hole_diameter / 2,
            "spline_radius": self.spline_radius2,
            "spline_height": self.spline_height1 + self.spline_height2,
            "body_height_under_wings": height_under_wing,
            "body_height": height,
            "body_width": self.body_width,
        }
        servo.poly = self.poly
        return servo


servo = MG92B("mg92b").create()

show(
    servo,
    *[obj.symbol for obj in servo.joints.values()],
    transparent=True,
    reset_camera=True,
    grid=True,
    axes=True,
    axes0=True,
    # ticks=50,
)
