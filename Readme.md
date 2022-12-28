# Alg123d

## Credits

Alg123d is a thin facade on top of [build123d](https://github.com/gumyr/build123d), so most of the credit goes to Roger Maitland.

## Design philosophy

1. Explicit is better than implicit
2. Minimum boilerplate
3. Interoperability with build123d and CadQuery

## Introduction

Alg123d removes all implicit computations (e.g. `Builder` contexts, `Location` contexts, `pending_*` and `last_*`) from build123d. It adds a few direct API extensions to make some statements shorter or better readable and provides a set of conversion functions.

Alg123d defines a `class AlgCompound(build123d.Compound)` and uses two concepts, "_Object arithmetic_" and "_Placement at Locations_"

### Object arithmetic

-   Creating a box and a cylinder placed on the `XY` plane centered at `(0, 0, 0)`

    ```python
    b = Box(1, 2, 3)
    c = Cylinder(0.2, 5)
    ```

-   Fusing a box and a cylinder

    ```python
    f = Box(1, 2, 3) + Cylinder(0.2, 5)
    ```

-   Cutting a cylinder from a box

    ```python
    f = Box(1, 2, 3) - Cylinder(0.2, 5)
    ```

-   Intersecting a box and a cylinder

    ```python
    f = Box(1, 2, 3) & Cylinder(0.2, 5)
    ```

Notes:

-   `b`, `c` and `f` are instances of `AlgCompound` and can be viewed with every viewer that can show `build123d.Compound`s
-   Some advanced concepts for performance reasons can be found in [Performance](./docs/performance.md)
-   Some shortcuts can be found in [Shortcuts](./docs/shortcuts.md)

### Placement at locations

An `AlgCompound` does not have any location or rotation paramater. The rationale is that a box defines its topology (shape, sizes and its center), but does not know where in space it will be located. Instead, it will be relocated with the `@` operator. The object location can be retrieved as usual in build123d via the `location` property of the underlying `build123d.Compound`.

The generic form of object placement is

```python
alg_compound @ (plane * location)
```

and describes an `alg_compound`being placed on the`plane`and then moved relative to the`plane` by `location`.

Details can be found in [Locations](./docs/locations.md).

Examples:

-   Box on the `XY` plane, centered at `(0, 0, 0)`

    ```python
    Box(1, 2, 3) @ Plane.XY
    Box(1, 2, 3)
    ```

    Note: On the `XY` plane no placement is needed (mathematically `@ Plane.XY` will not change the location of an object).

-   Box on the `XY` plane centered at `(0, 1, 0)`:

    ```python
    Box(1, 2, 3) @ (Plane.XY * Pos(0, 1, 0))
    Box(1, 2, 3) @ Pos(0, 1, 0)
    Box(1, 2, 3) @ Pos(y=1)
    ```

    Note: Again, `Plane.XY` can be omitted and `@ location` is actually an absolute placement in space.

-   Box on plane `Plane.XZ`:

    ```python
    Box(1, 2, 3) @ Plane.XZ
    ```

-   Box on plane `Plane.XZ` with a location `(x=1, y=2, z=3)` relative to the `XZ` plane, i.e., using the x-, y- and z-axis of the `XZ` plane:

    ```python
    Box(1, 2, 3) @ (Plane.XZ * Pos(1, 2, 3))
    ```

-   Box on plane `Plane.XZ` moved to `(x=1, y=2, z=3)` relative to this plane and rotated there by the angles `(x=0, y=100, z=45)` around `Plane.XZ` axes:

    ```python
    Box(1, 2, 3) @ (Plane.XZ * Pos(1, 2, 3) * Rot(0, 100, 45))
    Box(1, 2, 3) @ Location((1, 2, 3), (0, 100, 45))
    ```

    Note: `Pos * Rot` is the same as using `Location` directly

-   Box on plane `Plane.XZ` rotated on this plane by the angles `(x=0, y=100, z=45)` (using the x-, y- and z-axis of the `XZ` plane) and then moved to `(x=1, y=2, z=3)` relative to the `XZ` plane:

    ```python
    Box(1, 2, 3) @ (Plane.XZ * Rot(0, 100, 45) * Pos(0,1,2))
    ```

### Combing both concepts

_Object arithmetic_ and _Placement at locations_ can be combined:

```
b = Box(1, 2, 3) @ (Plane.XZ * Rot(x=30)) + Cylinder(0.2, 5) @ (Plane.YZ * Pos(x=-1))
```

Note: In Python `@` binds stronger then `+`, `-`, `&`, hence brackets are not needed.

## Definition

Alg123d consists of one class: `class AlgCompound(build123d.Compound)`

**Additional properties:**

-   `dim`: Dimensionality of the `AlgCompound a` with `a.dim in [0,1,2,3]`: 0=empty, 1=line, 2=sketch, 3=part (used to check compatibility of algebra operationes)
-   `joints`: Support build123d's `Joint` connectors directly on `AlgCompound`'s, default = `{}`
-   `mates`: Support manual assemblies with `alg123d.MAssembly`, default =`{}`
-   `metadata`: Expose metadata of an AlgCompound (e.g. sizes or distances) for later use with the compound, default = `{}` (free form dict that is not used by any CAD algorithm)

**Additional operators:**

-   `+`: `(AlgCompound, AlgCompound) -> AlgCompound`: Fuse two objects
-   `-`: `(AlgCompound, AlgCompound) -> AlgCompound`: Cut first object with second object
-   `&`: `(AlgCompound, AlgCompound) -> AlgCompound`: Intersect two objects
-   `@`: `(AlgCompound, Plane|Location) -> AlgCompound`: Change absolute location of an AlgCompound

**Use of existing build123d operators**

-   `*`: `(Location, Location) -> Location`: Multiply (concatenate) two locations
-   `*`: `(Plane, Location) -> Plane`: Change location of a plane

Proxying the build123d operators `position_at` and `tangent_at` of line objects (`dim==1` only)

-   `@`: `(AlgCompound, float) -> Vector`: `position_at` for AlgCompound with `dim==1`
-   `%`: `(AlgCompound, float) -> Vector`: `tangent_at` for AlgCompound with `dim==1`

**Objects:**

-   3-dim: `Box`, `Cylinder`, `Cone`, `Sphere`, `Torus`, `Wedge`, `Bore`, `CounterBore`, `CounterSink`
-   2-dim: `Rectangle`, `Circle`, `Ellipse`, `Rectangle`, `Polygon`, `RegularPolygon`, `Text`, `Trapezoid`, `SlotArc`, `SlotCenterPoint`, `SlotCenterToCenter`, `SlotOverall`
-   1-dim: `Bezier`, `PolarLine`, `Polyline`, `Spline`, `Helix`, `CenterArc`, `EllipticalCenterArc`, `RadiusArc`, `SagittaArc`, `TangentArc`, `ThreePointArc`, `JernArc`

**Functions:**

-   3-dim: `extrude`, `extrude_until`, `loft`, `revolve`, `sweep`, `section`, `shell`
-   2-dim: `make_face`

Notes:

-   An algebraic definition can be found in [Algebra](./docs/algebra.md)
-   The API description can be found in [Algebra](./docs/api.md)

## Examples

**Dice**

```python
from alg123d import *
width = 1.6
fillet_radius = 0.08
dist = 0.9
eye_radius = 0.23
eye_offset = 0.15

eye_locs = list(GridLocations(dist, dist / 2, 2, 3)) + [Pos((0, 0, 0))]

def eyes(face, ind):
    """build a compound of spheres representing the eyes of a side"""
    p = Plane(face) * Pos(z=eye_offset)  # eye offset above plane
    rv = AlgCompound()
    for loc in [eye_locs[i] for i in ind]:
        rv += Sphere(eye_radius) @ (p * loc)
    return rv

# create the actual body
dice = Box(width, width, width)
dice = fillet(dice, dice.edges(), fillet_radius)

# define sides and their eyes
sides = [
    (min_face(dice, Axis.Z), [6]),  # 1
    (max_face(dice, Axis.Z), [0, 1, 2, 3, 4, 5]),  # 6
    (min_face(dice, Axis.Y), [0, 5]),  # 2
    (max_face(dice, Axis.Y), [0, 2, 3, 5, 6]),  # 5
    (min_face(dice, Axis.X), [2, 3, 6]),  # 3
    (max_face(dice, Axis.X), [0, 2, 3, 5]),  # 4
]

# and cut out the eyes
for side in sides:
    dice -= eyes(*side)
```

![dice](./images/dice.png)

**Location handling**

```python
plane = Plane.ZX

# Four rotations around Y
rotations = [Rotation(0, a, 0) for a in (0, 45, 90, 135)]

# initialize result with empty AlgCompound
s = AlgCompound()

# get four locations on a grid
for i, outer_loc in enumerate(GridLocations(3, 3, 2, 2)):

    # move the ZX plane to one of the four grid locations and rotate it aropund Y
    c_plane = plane * outer_loc * rotations[i]

    # Create a circle and place it the c_plane.
    # Fuse the result with s (hence we need to initiailize s with empty AlgCompound for the first loop)
    s += Circle(1) @ c_plane

    # Get a different amount of polar locations per loop
    for loc in PolarLocations(0.8, (i + 3) * 2):

        # place the polar location onto the c_plane
        # and create a rectangle at this location
        # cut the rectangle from s
        s -= Rectangle(0.1, 0.3) @ (c_plane * loc)

# Finally extrude each rotated circle with cuts in the circle normal direction
e = extrude(s, 0.3)
```

![Example](./images/example.png)
