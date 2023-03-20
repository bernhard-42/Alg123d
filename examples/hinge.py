from alg123d import *


class Hinge(AlgCompound):
    """Hinge

    Half a simple hinge with several joints. The joints are:
    - "leaf": RigidJoint where hinge attaches to object
    - "hinge_axis": RigidJoint (inner) or RevoluteJoint (outer)
    - "hole0", "hole1", "hole2": CylindricalJoints for attachment screws

    Args:
        width (float): width of one leaf
        length (float): hinge length
        barrel_diameter (float): size of hinge pin barrel
        thickness (float): hinge leaf thickness
        pin_diameter (float): hinge pin diameter
        inner (bool, optional): inner or outer half of hinge . Defaults to True.
    """

    def __init__(
        self,
        width: float,
        length: float,
        barrel_diameter: float,
        thickness: float,
        pin_diameter: float,
        inner: bool = True,
    ):
        # The profile of the hinge used to create the tabs

        hinge_profile = AlgCompound()
        for i, loc in enumerate(GridLocations(0, length / 5, 1, 5, align=Align.MIN)):
            if i % 2 == inner:
                hinge_profile += loc * Rectangle(width, length / 5, align=Align.MIN)
        hinge_profile += Rectangle(width - barrel_diameter, length, align=Align.MIN)
        hinge_profile = extrude(hinge_profile, -barrel_diameter)

        # The hinge pin
        pin = Cylinder(
            radius=pin_diameter / 2,
            height=length,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )

        pin_head = Cylinder(
            radius=barrel_diameter / 2,
            height=pin_diameter,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        pin_head = fillet(
            pin_head, pin_head.edges(GeomType.CIRCLE).max(), radius=pin_diameter / 3
        )
        pin += Plane(pin.faces().max()) * pin_head

        # The leaf
        l1 = Line((0, 0), (width - barrel_diameter / 2, 0))
        l2 = RadiusArc(
            l1 @ 1,
            l1 @ 1 + Vector(0, barrel_diameter),
            -barrel_diameter / 2,
        )
        l3 = RadiusArc(
            l2 @ 1,
            (width - barrel_diameter, barrel_diameter / 2),
            -barrel_diameter / 2,
        )
        l4 = Line(l3 @ 1, (width - barrel_diameter, thickness))
        l5 = Line(l4 @ 1, (0, thickness))
        l6 = Line(l5 @ 1, l1 @ 0)
        face = make_face([l1, l2, l3, l4, l5, l6])
        pin_center = Pos(width - barrel_diameter / 2, barrel_diameter / 2)
        pin_hole = pin_center * Circle(pin_diameter / 2 + 0.1 * MM)
        face -= pin_hole
        leaf = extrude(face, length)
        leaf &= Rot(x=90) * hinge_profile

        # Create holes for fasteners
        plane = Plane(leaf.faces(Axis.Y).max())

        holes = [
            plane * loc * CounterSink(leaf, 3 * MM, 5 * MM)
            for loc in GridLocations(0, length / 3, 1, 3)
        ]
        leaf -= holes

        # Add the hinge pin to the external leaf
        if not inner:
            leaf = Compound.make_compound([leaf, pin_center * pin])

        # super().__init__(leaf)
        self.wrapped = leaf.wrapped
        self._dim = 3

        # Leaf attachment
        RigidJoint(
            label="leaf",
            to_part=leaf,
            joint_location=Location(
                (width - barrel_diameter, 0, length / 2), (90, 0, 0)
            ),
        )

        # Leaf attachment
        RigidJoint(
            label="leaf",
            to_part=leaf,
            joint_location=Location(
                (width - barrel_diameter, 0, length / 2), (90, 0, 0)
            ),
        )
        # Hinge axis (fixed with inner)
        if inner:
            RigidJoint(
                "hinge_axis",
                leaf,
                Location((width - barrel_diameter / 2, barrel_diameter / 2, 0)),
            )
        else:
            RevoluteJoint(
                "hinge_axis",
                leaf,
                axis=Axis(
                    (width - barrel_diameter / 2, barrel_diameter / 2, 0), (0, 0, 1)
                ),
                angular_range=(90, 270),
            )

        # Leaf attachment
        RigidJoint(
            label="leaf",
            to_part=leaf,
            joint_location=Location(
                (width - barrel_diameter, 0, length / 2), (90, 0, 0)
            ),
        )
        # Hinge axis (fixed with inner)
        if inner:
            RigidJoint(
                "hinge_axis",
                leaf,
                Location((width - barrel_diameter / 2, barrel_diameter / 2, 0)),
            )
        else:
            RevoluteJoint(
                "hinge_axis",
                leaf,
                axis=Axis(
                    (width - barrel_diameter / 2, barrel_diameter / 2, 0), (0, 0, 1)
                ),
                angular_range=(90, 270),
            )
        # Fastener holes
        hole_locations = [hole.location for hole in holes]
        for hole, hole_location in enumerate(hole_locations):
            CylindricalJoint(
                label="hole" + str(hole),
                to_part=leaf,
                axis=hole_location.to_axis(),
                linear_range=(0, 2 * CM),
                angular_range=(0, 360),
            )

        self.joints = leaf.joints


# Create the hinges

hinge_inner = Hinge(
    width=5 * CM,
    length=12 * CM,
    barrel_diameter=1 * CM,
    thickness=2 * MM,
    pin_diameter=4 * MM,
)
# %%
hinge_outer = Hinge(
    width=5 * CM,
    length=12 * CM,
    barrel_diameter=1 * CM,
    thickness=2 * MM,
    pin_diameter=4 * MM,
    inner=False,
)

# %%
# show(
#     hinge_inner,
#     *[h.symbol for h in hinge_inner.joints.values()],
#     Pos(6 * CM, 0) * hinge_outer,
#     *[h.symbol.moved(Pos(6 * CM, 0)) for h in hinge_outer.joints.values()],
# )
# %%

# Create the box

box = Box(30 * CM, 30 * CM, 10 * CM)
box = shell(box, -1 * CM, openings=box.faces().max())
# Create a notch for the hinge
box -= Pos(-15 * CM, 0, 5 * CM) * Box(2 * CM, 12 * CM, 4 * MM)
plane = Plane(box.faces().min(Axis.X)) * Pos(2 * CM, 0, 0)
for loc in GridLocations(0, 40 * MM, 1, 3):
    box -= plane * loc * Bore(box, 3 * MM, 1 * CM)

RigidJoint(
    "hinge_attachment",
    box,
    Location((-15 * CM, 0, 4 * CM), (180, 90, 0)),
)

# show(box, box.joints["hinge_attachment"].symbol)
# %%

# Create the lid

lid = Box(30 * CM, 30 * CM, 1 * CM)

plane = Plane(lid.faces().min()) * Pos(13 * CM, 0)
for loc in GridLocations(0, 40 * MM, 1, 3):
    lid -= plane * loc * Bore(lid, 3 * MM, 1 * CM)

RigidJoint(
    "hinge_attachment",
    lid,
    Location((15 * CM, 0, 5 * MM), (180, 0, 0)),
)

# show(lid, lid.joints["hinge_attachment"].symbol, plane.symbol(5))
# %%

box.joints["hinge_attachment"].connect_to(hinge_outer.joints["leaf"])
hinge_outer.joints["hinge_axis"].connect_to(hinge_inner.joints["hinge_axis"], angle=150)
hinge_inner.joints["leaf"].connect_to(lid.joints["hinge_attachment"])

show(box, lid, hinge_inner, hinge_outer)

# %%
