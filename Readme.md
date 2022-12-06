# Alg123d

## Overview

### Classes

`class AlgCompound(build123d.Compound)`

#### Additional properties:

- `dim`: Dimensionality of the `AlgCompound a` with `a.dim in [0,1,2,3]`:
    - `0`: Empty element
    - `1`: Lines
    - `2`: Sketches
    - `3`: Parts

#### Additional user facing operators:

- `+`: `(AlgCompound, AlgCompound) -> AlgCompound`: Fuse two objects
- `-`: `(AlgCompound, AlgCompound) -> AlgCompound`: Cut first object with second object
- `&`: `(AlgCompound, AlgCompound) -> AlgCompound`: Intersect two objects
- `@`: `(AlgCompound, Plane|Location) -> AlgCompound`: Change location of an AlgCompound

Proxying build123d operators `position_at` and `tangent_at` to a line object (`dim==1` only)

- `@`: `(AlgCompound, float) -> Vector`: `position_at` for AlgCompound with `dim==1` 
- `%`: `(AlgCompound, float) -> Vector`: `tangent_at` for AlgCompound with `dim==1`

Another important operator is used from build123d:

- `*`: `(Location, Location) -> Location`: Multiple (concatenate) two locations
- `*`: `(Plane, Location) -> Plane`: Change location of a plane

### 3-dim objects (parts)

- `Box(length: float, width: float, height: float, centered: bool | Tuple[bool, bool, bool] = (True, True, True))`
- `Cylinder(radius: float, height: float, arc_size: float = 360, centered: [bool | Tuple[bool, bool, bool] = (True, True, True))`
- `Cone(bottom_radius: float, top_radius: float, height: float, arc_size: float = 360, centered: bool | Tuple[bool, bool, bool] = (True, True, True))`
- `Sphere(radius: float, arc_size1: float = -90, arc_size2: float = 90, arc_size3: float = 360, centered: bool | Tuple[bool, bool, bool] = (True, True, True))`
- `Torus(major_radius: float, minor_radius: float, minor_start_angle: float = 0, minor_end_angle: float = 360, major_angle: float = 360, centered: bool | Tuple[bool, bool, bool] = (True, True, True))`
- `Wedge(dx: float, dy: float, dz: float, xmin: float, zmin: float, xmax: float, zmax: float)`
- `CounterBore(part: AlgCompound, radius: float, counter_bore_radius: float, counter_bore_depth: float, depth: float = None)`
- `CounterSink(part: AlgCompound, radius: float, counter_sink_radius: float, counter_sink_angle: float = 82, depth: float = None)`
- `Bore(part: AlgCompound, radius: float, depth: float = None)`
### 3-dim functions

- `extrude(to_extrude: Compound, amount: float = None, both: bool = False, taper: float = 0.0)`
- `extrude_until(face: Face|AlgCompound, limit: AlgCompound) -> AlgCompound`
- `loft(sections: List[AlgCompound | Face], ruled: bool = False)`
- `revolve(profiles: List[Compound | Face] | Compound | Face, axis: Axis, arc: float = 360.0)`
- `sweep(sections: List[Compound | Face], path: Edge | Wire = None, multisection: bool = False, is_frenet: bool = False, transition: Transition = Transition.TRANSFORMED, normal: Union[Vector, tuple[float, float], tuple[float, float, float]] = None, binormal: Edge | Wire = None)`
- `section(part: AlgCompound, by: List[Plane], height: float = 0.0)`
- `shell(objects: List[AlgCompound] | AlgCompound], amount: float, openings: Face | List[Face] = None, kind: Kind = Kind.ARC)`

### 2-dim objects (sketches)
- `Circle(radius: float, centered: bool | Tuple[bool, bool] = (True, True))`
- `Ellipse(x_radius: float, y_radius: float, centered: bool | Tuple[bool, bool] = (True, True))`
- `Rectangle(width: float, height: float, centered: bool | Tuple[bool, bool] = (True, True))`
- `Polygon(pts: List[Vector | tuple[float, float] | tuple[float, float, float]])`
- `RegularPolygon(radius: float, side_count: int, centered: bool | Tuple[bool, bool] = (True, True))`
- `Text(txt: str, fontsize: float, font: str = 'Arial', font_path: str = None, font_style: FontStyle = FontStyle.REGULAR, halign: Halign = Halign.LEFT, valign: Valign = Valign.CENTER, path: Edge | Wire = None, position_on_path: float = 0.0)`
- `Trapezoid(width: float, height: float, left_side_angle: float, right_side_angle: float = None, centered: bool | Tuple[bool, bool] = (True, True))`
- `SlotArc(arc: Edge | Wire, height: float)`
- `SlotCenterPoint(center: Vector | tuple[float, float] | tuple[float, float, float], point: Vector | tuple[float, float] | tuple[float, float, float], height: float)`
- `SlotCenterToCenter(center_separation: float, height: float)`
- `SlotOverall(width: float, height: float)`

### 2-dim functions
- `make_face(objs: AlgCompound, | List[Edge])`

### 1-dim objects (lines)

- `Line(start: Vector | tuple[float, float] | tuple[float, float, float], end: Vector | tuple[float, float] | tuple[float, float, float])`
- `Bezier(cntl_pts: Iterable[Vector | tuple[float, float] | tuple[float, float, float]], weights: List[float] = None)`
- `PolarLine(start: Vector | tuple[float, float] | tuple[float, float, float], length: float, angle: float = None, direction: Vector | tuple[float, float] | tuple[float, float, float] = None)`
- `Polyline(pts: List[Vector | tuple[float, float] | tuple[float, float, float]], close: bool = False)`
- `Spline(pts: Iterable[Vector | tuple[float, float] | tuple[float, float, float]], tangents: Iterable[Vector | tuple[float, float] | tuple[float, float, float]] = None, tangent_scalars: Iterable[float] = None, periodic: bool = False)`
- `Helix(pitch: float, height: float, radius: float, direction: Vector | tuple[float, float] | tuple[float, float, float] = (0, 0, 1), cone_angle: float = 0, lefthand: bool = False)`
- `CenterArc(center: Vector | tuple[float, float] | tuple[float, float, float], radius: float, start_angle: float, arc_size: float)`
- `EllipticalCenterArc(center: Vector | tuple[float, float] | tuple[float, float, float], x_radius: float, y_radius: float, start_angle: float = 0.0, end_angle: float = 90.0, angular_direction: build123d.build_enums.AngularDirection = <AngularDirection.COUNTER_CLOCKWISE>, plane: Plane = Plane(o=(0.00, 0.00, 0.00), x=(1.00, 0.00, 0.00), z=(0.00, 0.00, 1.00)))`
- `RadiusArc(start_point: Vector | tuple[float, float] | tuple[float, float, float], end_point: Vector | tuple[float, float] | tuple[float, float, float], radius: float)`
- `SagittaArc(start_point: Vector | tuple[float, float] | tuple[float, float, float], end_point: Vector | tuple[float, float] | tuple[float, float, float], sagitta: float)`
- `TangentArc(start_point: Vector | tuple[float, float] | tuple[float, float, float], end_point: Vector | tuple[float, float] | tuple[float, float, float], tangent: Union[Vector, tuple[float, float], tuple[float, float, float]], tangent_from_first: bool = True)`
- `ThreePointArc(p1: Vector | tuple[float, float] | tuple[float, float, float], p2: Vector | tuple[float, float] | tuple[float, float, float], p3: Vector | tuple[float, float] | tuple[float, float, float])`
- `JernArc(start: Vector | tuple[float, float] | tuple[float, float, float], tangent: Vector | tuple[float, float] | tuple[float, float, float], radius: float, arc_size: float, plane: Plane = Plane(o=(0.00, 0.00, 0.00), x=(1.00, 0.00, 0.00), z=(0.00, 0.00, 1.00)))`



### Location handling

Box at `origin = (0,0,0)` without rotation:

```python
b = Box(1,2,3)
```

Box at `origin = (0,1,0)` without rotation:

```python
b = Box(1,2,3) @ Location((0,1,0))
b = Box(1,2,3) @ (0,1,0)             # shortcut
```

Box at `origin = (0,0,0)` and `rotation = (0, 100, 45)`:

```python
b = Box(1,2,3) @ Rotation((0, 100, 45))
```

Box at `origin = (0,1,0)` and `rotation = (0, 100, 45)`:

```python
b = Box(1,2,3) @ Location((0,1,0), (0,100,45))
```

Box on plane `Plane.YZ`:

```python
b = Box(1,2,3) @ Plane.XZ
```

Box on plane `Plane.YZ` rotated around `X` by 45°:

```python
b = Box(1,2,3) @ (Plane.XZ * Rotation(45, 0, 0))
```

## Algebraic definition

### Objects and object arithmetic

$A^n$ is the set of all `AlgCompounds a` with `a.dim = n` for $n = 1,2,3$

$e_n$ := `Empty` , for $n = 1,2,3$ , are `AlgCompounds a` with `a.dim = n` and `a.wrapped = None`

**Sets of predefined basic shapes:**

$B^3 := \lbrace$`Empty`, `Box`, `Cylinder`, `Cone`, `Sphere`, `Torus`, `Wedge`, `Bore`, `CounterBore`, `CounterSink`$\rbrace$

$B^2 := \lbrace$`Empty`, `Rectangle`, `Circle`, `Ellipse`, `Rectangle`, `Polygon`, `RegularPolygon`, `Text`, `Trapezoid`, `SlotArc`, `SlotCenterPoint`, `SlotCenterToCenter`, `SlotOverall`$\rbrace$

$B^1 := \lbrace$`Empty`, `Bezier`, `PolarLine`, `Polyline`, `Spline`, `Helix`, `CenterArc`, `EllipticalCenterArc`, `RadiusArc`, `SagittaArc`, `TangentArc`, `ThreePointArc`, `JernArc`$\rbrace$

with $B^n \subset A^n$

**Operations:**

$+: A^n \times A^n \rightarrow A^n$ with $(a,b) \mapsto a + b$ , for $n=1,2,3$

$\\;\\;\\;\\;\\;\\; a + b :=$ `a.fuse(b)`

$-: A^n \rightarrow A^n$ with $a \mapsto -a$ , for $n=1, 2,3$

$\\;\\;\\;\\;\\;\\; b + (-a) = (-a) + b = b - a$ := `b.cut(a)` (implicit definition)

$\\& : A^n \times A^n \rightarrow A^n$ with $(a,b) \mapsto a \\; \\& \\; b$ , for $n=2,3$

$\\;\\;\\;\\;\\;\\; a \\; \\& \\; b :=$ `a.intersect(b)` (note: $a \\; \\& \\; b = (a + b) - (a - b) - (b - a)$ )

**Abelian groups**

$( A^n, e_n, +, -)$ is an abelian group for $n=2,3$

$( A^1, e_1, +)$ is an abelian semigroup

### Locations, planes and location arithmentic

$L  := \lbrace$ `Location` $((x,y,z), (a,b,c)): x,y,z \in R \land a,b,c \in R\rbrace$ with $a,b,c$ being angles in degrees

$P  := \lbrace$ `Plane` $(o,x,z): o,x,z ∈ R^3 \land \|x\| = \|z\| = 1\rbrace$

For $n = 1, 2, 3$:

$*: L \times L \rightarrow L$ (multiply two locations $l_1, l_2 \in L$, i.e. `l1 * l2`)

$*: P \times L \rightarrow P$ (locate plane $p \in P$ at location $l \in L$, i.e. `Plane(p.to_location() * l)`)

Neutral element: $l_0 \in L$: `Location()`

Inverse element: $l^{-1} \in L$: `l.inverse()`

### Placing objects on planes and at locations:

For $n = 1, 2, 3$:

$@: A^n \times L \rightarrow A^n$ (locate an object $a \in A^n$ at location $l \in L$, i.e. `a.located(l)`)

$@: A^n \times P \rightarrow A^n$ (locate an object $a \in A^n$ on a plane $p \in P$, i.e. `a.located(p.to_location())`)
