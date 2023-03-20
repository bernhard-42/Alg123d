# Algebraic definition

## Objects and object arithmetic

$A^n$ is the set of all `AlgCompounds a` with `a._dim = n` for $n = 1,2,3$

$e_n$ := `Zero` , for $n = 1,2,3$ , are `AlgCompounds a` with `a._dim = n` and `a.wrapped = None`

**Sets of predefined basic shapes:**

$B^3 := \lbrace$`Zero`, `Box`, `Cylinder`, `Cone`, `Sphere`, `Torus`, `Wedge`, `Bore`, `CounterBore`, `CounterSink`$\rbrace$

$B^2 := \lbrace$`Zero`, `Rectangle`, `Circle`, `Ellipse`, `Rectangle`, `Polygon`, `RegularPolygon`, `Text`, `Trapezoid`, `SlotArc`, `SlotCenterPoint`, `SlotCenterToCenter`, `SlotOverall`$\rbrace$

$B^1 := \lbrace$`Zero`, `Bezier`, `PolarLine`, `Polyline`, `Spline`, `Helix`, `CenterArc`, `EllipticalCenterArc`, `RadiusArc`, `SagittaArc`, `TangentArc`, `ThreePointArc`, `JernArc`$\rbrace$

with $B^n \subset A^n$

**Operations:**

$+: A^n \times A^n \rightarrow A^n$ with $(a,b) \mapsto a + b$ , for $n=1,2,3$

$\\;\\;\\;\\;\\;\\; a + b :=$ `a.fuse(b)`

$-: A^n \rightarrow A^n$ with $a \mapsto -a$ , for $n=2,3$

$\\;\\;\\;\\;\\;\\; b + (-a)$ := `b.cut(a)` (implicit definition)

$\\& : A^n \times A^n \rightarrow A^n$ with $(a,b) \mapsto a \\; \\& \\; b$ , for $n=2,3$

$\\;\\;\\;\\;\\;\\; a \\; \\& \\; b :=$ `a.intersect(b)` (note: $a \\; \\& \\; b = (a + b) + -(a + (-b)) + -(b + (-a))$ )

**Abelian groups**

$( A^1, e_1, +)$ is an abelian semigroup

$( A^n, e_n, +, -)$ is an abelian group for $n=2,3$

Note: The implementation `a - b = a.cut(b)` needs to be read as $a + (-b)$ since the group does not have a binary $-$ operation. As such, $a - (b - c) = a + -(b + -c)) \ne a - b + c$

## Locations, planes and location arithmentic

$L  := \lbrace$ `Location` $((x,y,z), (a,b,c)): x,y,z \in R \land a,b,c \in R\rbrace$ with $a,b,c$ being angles in degrees

$P  := \lbrace$ `Plane` $(o,x,z): o,x,z ∈ R^3 \land \|x\| = \|z\| = 1\rbrace$

For $n = 1, 2, 3$:

$*: L \times L \rightarrow L$ (multiply two locations $l_1, l_2 \in L$, i.e. `l1 * l2`)

$*: P \times L \rightarrow P$ (locate plane $p \in P$ at location $l \in L$, i.e. `Plane(p.to_location() * l)`)

Neutral element: $l_0 \in L$: `Location()`

Inverse element: $l^{-1} \in L$: `l.inverse()`

## Placing objects on planes and at locations

For $n = 1, 2, 3$:

$*: L \times A^n  \rightarrow A^n$ (locate an object $a \in A^n$ at location $l \in L$, i.e. `a.moved(l)`)

$*: P \times A^n  \rightarrow A^n$ (locate an object $a \in A^n$ on a plane $p \in P$, i.e. `a.moved(p.to_location())`)
