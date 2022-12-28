# API

## 3-dim objects (parts)

```python
Box(
    length: float,
    width: float,
    height: float,
    centered: bool | Tuple[bool, bool, bool] = (True, True, True)
    )

Cylinder(
    radius: float,
    height: float,
    arc_size: float = 360,
    centered: bool | Tuple[bool, bool, bool] = (True, True, True)
)

Cone(
    bottom_radius: float,
    top_radius: float,
    height: float,
    arc_size: float = 360,
    centered: bool | Tuple[bool, bool, bool] = (True, True, True)
)

Sphere(
    radius: float,
    arc_size1: float = -90,
    arc_size2: float = 90,
    arc_size3: float = 360,
    centered: bool | Tuple[bool, bool, bool] = (True, True, True)
)

Torus(
    major_radius: float,
    minor_radius: float,
    minor_start_angle: float = 0,
    minor_end_angle: float = 360,
    major_angle: float = 360,
    centered: bool | Tuple[bool, bool, bool] = (True, True, True)
)

Wedge(
    dx: float,
    dy: float,
    dz: float,
    xmin: float,
    zmin: float,
    xmax: float,
    zmax: float
)

CounterBore(
    part: AlgCompound,
    radius: float,
    counter_bore_radius: float,
    counter_bore_depth: float,
    depth: float = None
)

CounterSink(
    part: AlgCompound,
    radius: float,
    counter_sink_radius: float,
    counter_sink_angle: float = 82,
    depth: float = None
)

Bore(
    part: AlgCompound,
    radius: float,
    depth: float = None
)
```

## 3-dim functions

```python
extrude(
    to_extrude: Compound,
    amount: float = None,
    both: bool = False,
    taper: float = 0.0
) -> AlgCompound

extrude_until(
    face: Face | AlgCompound,
    limit: AlgCompound
    taper: float = 0.0
) -> AlgCompound

loft(
    sections: List[AlgCompound | Face],
    ruled: bool = False
) -> AlgCompound

revolve(
    profiles: List[Compound | Face] | Compound | Face,
    axis: Axis,
    arc: float = 360.0
) -> AlgCompound

sweep(
    sections: List[Compound | Face],
    path: Edge | Wire = None,
    multisection: bool = False,
    is_frenet: bool = False,
    transition: Transition = Transition.TRANSFORMED,
    normal: Union[Vector, tuple[float, float], tuple[float, float, float]] = None,
    binormal: Edge | Wire = None
) -> AlgCompound

section(
    part: AlgCompound,
    by: List[Plane],
    height: float = 0.0
) -> AlgCompound

shell(
    objects: List[AlgCompound] | AlgCompound],
    amount: float,
    openings: Face | List[Face] = None,
    kind: Kind = Kind.ARC
)  -> AlgCompound
```

## 2-dim objects (sketches)

```python
Circle(
    radius: float,
    centered: bool | Tuple[bool, bool] = (True, True)
)

Ellipse(
    x_radius: float,
    y_radius: float,
    centered: bool | Tuple[bool, bool] = (True, True)
)

Rectangle(
    width: float,
    height: float,
    centered: bool | Tuple[bool, bool] = (True, True)
)

Polygon(
    pts: List[Vector | tuple[float, float] | tuple[float, float, float]]
    )

RegularPolygon(
    radius: float,
    side_count: int,
    centered: bool | Tuple[bool, bool] = (True, True)
)

Text(
    txt: str,
    fontsize: float,
    font: str = 'Arial',
    font_path: str = None,
    font_style: FontStyle = FontStyle.REGULAR,
    halign: Halign = Halign.LEFT,
    valign: Valign = Valign.CENTER,
    path: Edge | Wire = None,
    position_on_path: float = 0.0
)

Trapezoid(
    width: float,
    height: float,
    left_side_angle: float,
    right_side_angle: float = None,
    centered: bool | Tuple[bool, bool] = (True, True)
)

SlotArc(
    arc: Edge | Wire,
    height: float
)

SlotCenterPoint(
    center: Vector | tuple[float, float] | tuple[float, float, float],
    point: Vector | tuple[float, float] | tuple[float, float, float],
    height: float
)

SlotCenterToCenter(
    center_separation: float,
    height: float
)

SlotOverall(
    width: float,
    height: float
)
```

## 2-dim functions

```python
make_face(
    objs: AlgCompound, | List[Edge]
)  -> AlgCompound
```

## 1-dim objects (lines)

```python
Line(
    start: Vector | tuple[float, float] | tuple[float, float, float],
    end: Vector | tuple[float, float] | tuple[float, float, float]
)

Bezier(
    cntl_pts: Iterable[Vector | tuple[float, float] | tuple[float, float, float]],
    weights: List[float] = None
)

PolarLine(
    start: Vector | tuple[float, float] | tuple[float, float, float],
    length: float,
    angle: float = None,
    direction: Vector | tuple[float, float] | tuple[float, float, float] = None
)

Polyline(
    pts: List[Vector | tuple[float, float] | tuple[float, float, float]],
    close: bool = False
)

Spline(
    pts: Iterable[Vector | tuple[float, float] | tuple[float, float, float]],
    tangents: Iterable[Vector | tuple[float, float] | tuple[float, float, float]] = None,
    tangent_scalars: Iterable[float] = None,
    periodic: bool = False
)

Helix(
    pitch: float,
    height: float,
    radius: float,
    direction: Vector | tuple[float, float] | tuple[float, float, float] = (0, 0, 1),
    cone_angle: float = 0,
    lefthand: bool = False
)

CenterArc(
    center: Vector | tuple[float, float] | tuple[float, float, float],
    radius: float,
    start_angle: float,
    arc_size: float
)

EllipticalCenterArc(
    center: Vector | tuple[float, float] | tuple[float, float, float],
    x_radius: float,
    y_radius: float,
    start_angle: float = 0.0,
    end_angle: float = 90.0,
    angular_direction: AngularDirection = AngularDirection.COUNTER_CLOCKWISE,
    plane: Plane = Plane(o=(0.00, 0.00, 0.00), x=(1.00, 0.00, 0.00), z=(0.00, 0.00, 1.00))
)

RadiusArc(
    start_point: Vector | tuple[float, float] | tuple[float, float, float],
    end_point: Vector | tuple[float, float] | tuple[float, float, float],
    radius: float
)

SagittaArc(
    start_point: Vector | tuple[float, float] | tuple[float, float, float],
    end_point: Vector | tuple[float, float] | tuple[float, float, float],
    sagitta: float
)

TangentArc(
    start_point: Vector | tuple[float, float] | tuple[float, float, float],
    end_point: Vector | tuple[float, float] | tuple[float, float, float],
    tangent: Union[Vector, tuple[float, float], tuple[float, float, float]],
    tangent_from_first: bool = True
)

ThreePointArc(
    p1: Vector | tuple[float, float] | tuple[float, float, float],
    p2: Vector | tuple[float, float] | tuple[float, float, float],
    p3: Vector | tuple[float, float] | tuple[float, float, float]
)

JernArc(
    start: Vector | tuple[float, float] | tuple[float, float, float],
    tangent: Vector | tuple[float, float] | tuple[float, float, float],
    radius: float,
    arc_size: float,
    plane: Plane = Plane(o=(0.00, 0.00, 0.00), x=(1.00, 0.00, 0.00), z=(0.00, 0.00, 1.00))
)
```

## Direct API extension

**Locations**

```python
Pos(x: float = 0, y: float = 0, z: float = 0) -> Location
Rot(x: float = 0, y: float = 0, z: float = 0) -> Location
```

```python
Location.x_axis(self) -> Axis
Location.y_axis(self) -> Axis
Location.z_axis(self) -> Axis
```

**Planes**

```python
Planes(objs: List[Union[Plane, Location, Face]]) -> List[Plane]
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

### Conversions

```python
from_cq(obj) -> AlgCompound
to_cq(obj) -> cq.Compound
from_bd(obj) -> AlgCompound
to_bd(obj) -> build123d.Compound
```
