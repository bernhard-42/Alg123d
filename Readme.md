# Alg123d

## Credits

Alg123d is a thin facade on top of [build123d](https://github.com/gumyr/build123d), so most of the credit goes to Roger Maitland.

## Design philosophy

1. Explicit is better than implicit
2. Minimum boilerplate
3. Interoperability with build123d and CadQuery

So Alg123d

-   removes all implicit computations (e.g. Build contexts, Location contexts, pending_xxx and last selection) to get compliant with 1 and improve on 2
-   adds shortcuts and direct API changes to improve on 2
-   adds conversion functions to act on 3

## Overview

Alg123d consists of basically one class: `class AlgCompound(build123d.Compound)`

**Additional properties:**

-   `dim`: Dimensionality of the `AlgCompound a` with `a.dim in [0,1,2,3]`: 0=empty, 1=line, 2=sketch, 3=part
-   `metadata`: Expose metadata of an AlgCompound (e.g. sizes or distances) for later use with the compound, default = `{}`
-   `joints`: Support build123d's joint connectors directly on `AlgCompound`'s, default = `{}`
-   `mates`: Support manual assemblies with `MAssembly`, default =`{}`

`dim` is used to check compatibility of algebra operationes, see below.

`metadata` is a free form dict that is not used by any CAD algorithm.

`joints` and `mates` can be safely ignored if one doesn't use `build123d.Joint` or `alg123d.MAsembly`.

**Additional user facing operators:**

-   `+`: `(AlgCompound, AlgCompound) -> AlgCompound`: Fuse two objects
-   `-`: `(AlgCompound, AlgCompound) -> AlgCompound`: Cut first object with second object
-   `&`: `(AlgCompound, AlgCompound) -> AlgCompound`: Intersect two objects
-   `@`: `(AlgCompound, Plane|Location) -> AlgCompound`: Change absolute location of an AlgCompound

Another important operator is used from build123d:

-   `*`: `(Location, Location) -> Location`: Multiply (concatenate) two locations
-   `*`: `(Plane, Location) -> Plane`: Change location of a plane

Proxying build123d operators `position_at` and `tangent_at` to a line object (`dim==1` only)

-   `@`: `(AlgCompound, float) -> Vector`: `position_at` for AlgCompound with `dim==1`
-   `%`: `(AlgCompound, float) -> Vector`: `tangent_at` for AlgCompound with `dim==1`

**Objects:**

-   3-dim: {`Box`, `Cylinder`, `Cone`, `Sphere`, `Torus`, `Wedge`, `Bore`, `CounterBore`, `CounterSink`}
-   2-dim: {`Rectangle`, `Circle`, `Ellipse`, `Rectangle`, `Polygon`, `RegularPolygon`, `Text`, `Trapezoid`, `SlotArc`, `SlotCenterPoint`, `SlotCenterToCenter`, `SlotOverall`}
-   1-dim: {`Bezier`, `PolarLine`, `Polyline`, `Spline`, `Helix`, `CenterArc`, `EllipticalCenterArc`, `RadiusArc`, `SagittaArc`, `TangentArc`, `ThreePointArc`, `JernArc`}

**Functions:**

-   3-dim: {`extrude`, `extrude_until`, `loft`, `revolve`, `sweep`, `section`, `shell`}
-   2-dim: {`make_face`}

## Shortcuts

| Shortcut       | Long form                        | Description   |
| -------------- | -------------------------------- | ------------- |
| `Rot(x, y, z)` | `Location((0, 0, 0), (x, y, z))` | Create a      |
| `Rot(x=a)`     | `Location((0, 0, 0), (a, 0, 0))` | rotation only |
| `Rot(y=a)`     | `Location((0, 0, 0), (0, a, 0))` | Location      |
| `Rot(z=a)`     | `Location((0, 0, 0), (0, 0, a))` |               |
| ---            | ---                              | ---           |
| `Pos(x, y, z)` | `Location((x, y, z), (0, 0, 0))` | Create a      |
| `Pos(x=a)`     | `Location((a, 0, 0), (0, 0, 0))` | position only |
| `Pos(y=a)`     | `Location((0, a, 0), (0, 0, 0))` | Location      |
| `Pos(z=a)`     | `Location((0, 0, a), (0, 0, 0))` |               |
| ---            | ---                              | ---           |

_Location classes_:

-   `Rot`: Create a rotation only Location
-   `Pos`: Create a position only Location

_Plane class_:

-   `Location.x_axis`
-   `Location.y_axis`
-   `Location.z_axis`
-   `Location.plane`
-   `Planes`: Transform a mixed list of faces and locations to a list of planes

_Face class_

-   `Face.center_location`

_Edge class_

-   `Edge.origin_location`
-   `Edge.center_location`

_Conversions_:

-   `from_cq`: Load a CadQuery object into Alg123d
-   `to_cq`: Convert Alg123d object to CadQuery
-   `from_bd`: Load a Build123d object into Alg123d
-   `to_bd`: Convert Alg123d object to Build123d

## Usage

### Object creation

```python
b = Box(1,2,3)
```

is an `AlgCompound` placed on the `XY` plane. It can be immediately shown. `AlgCompund`s do not have any location or rotation paramater. They will be relocated with the `@` operator (see below) which will then be reflected in the `location` property of the underlying `build123d.Compound`.

### Object arithmetic

-   Fusing a box and a cylinder:

    ```python
    f = Box(1,2,3) + Cylinder(0.2, 5)
    ```

-   Cutting a cylinder from a box

    ```python
    f = Box(1,2,3) - Cylinder(0.2, 5)
    ```

-   Intersecting a box and a cylinder

    ```python
    f = Box(1,2,3) & Cylinder(0.2, 5)
    ```

### Location handling

-   Box at `origin = (0,0,0)` without rotation:

    ```python
    b = Box(1,2,3)
    ```

-   Box at `origin = (0,1,0)` without rotation:

    ```python
    b = Box(1,2,3) @ Pos((0,1,0))
    b = Box(1,2,3) @ Pos((y=1)
    ```

-   Box at `origin = (0,0,0)` with `rotation = (0, 100, 45)`:

    ```python
    b = Box(1,2,3) @ Rot((0, 100, 45))
    ```

-   Box at `origin = (0,1,0)` with `rotation = (0, 100, 45)`:

    ```python
    b = Box(1,2,3) @ Location((0,1,0), (0,100,45))
    ```

-   Box on plane `Plane.YZ`:

    ```python
    b = Box(1,2,3) @ Plane.XZ
    ```

-   Box on plane `Plane.YZ` rotated around `X` by 45°:

    ```python
    b = Box(1,2,3) @ (Plane.XZ * Rot(x=45))
    ```

### Direct API extension

**Location**

Return x-, y- or z-axis of a location:

```python
Location.x_axis(self) -> Axis
Location.y_axis(self) -> Axis
Location.z_axis(self) -> Axis
```

**Shape**

Add filters to shape accessors:

With the following types

```Python
filter_by: Union[Axis, GeomType]
reverse: bool
tolerance: float
```

the following extensions are the same as e.g. `faces().filter_by(filter_by, reverse, tolerance)`

```python
Shape.vertices(self, filter_by=None, reverse=False, tolerance=1e-5)
Shape.edges(self, filter_by=None, reverse=False, tolerance=1e-5)
Shape.compounds(self, filter_by=None, reverse=False, tolerance=1e-5)
Shape.wires(self, filter_by=None, reverse=False, tolerance=1e-5)
Shape.faces(self, filter_by=None, reverse=False, tolerance=1e-5)
Shape.shells(self, filter_by=None, reverse=False, tolerance=1e-5)
Shape.solids(self, filter_by=None, reverse=False, tolerance=1e-5)
```

**ShapeList**

Allow two `ShapeList`s to be subtracted:

```python
ShapeList.__sub__(self, other: List[Shape]) -> ShapeList
```

Use case:

```python
last = obj.faces()
obj = my_transformation(obj)
new_faces = obj.faces() - last
```

Get min or max element/group of a ShapeList. Simply for readability:

`obj.faces().min(axis)` is easier to read then `obj.faces().sort_by(axis)[0]`
`obj.faces().max_group(axis)` is easier to read then `obj.faces().group_by(axis)[-1]`

```python
ShapeList.max(self, axis: Axis = Axis.Z, wrapped=False) -> Union[AlgCompound, Solid, Face, Wire, Edge, Vertex]
ShapeList.min(self, axis: Axis = Axis.Z, wrapped=False) -> Union[AlgCompound, Solid, Face, Wire, Edge, Vertex]
ShapeList.min_group(self, axis: Axis = Axis.Z) -> ShapeList
ShapeList.max_group(self, axis: Axis = Axis.Z) -> ShapeList
```

`min` and `max` can also return an `AlgCompound` if `wrapped=True`

### Examples

**Dice**

```python
from alg123d import *
from alg123d.shortcuts import *
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
