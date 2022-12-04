# Alg123d

## Overview

### Classes

`class AlgCompound(Compound)` with one additional property `a.dim in [1,2,3]`

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

$A^n$ is the set of all AlgCompounds `a` with `a.dim = n` for $n = 1,2,3$

$e_n$ := `Empty` are AlgCompounds `a` with `a.dim = n` and `a.wrapped = None` for $n = 1,2,3$

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
