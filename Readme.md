# Alg123d

## Classes

`class AlgCompound(Compound)` with one additional property `a.dim in [1,2,3]`

## Algebraic definition

### Objects and object arithmetic

$A^n$ is the set of all AlgCompounds `a` with `a.dim = n` for $n = 1,2,3$

$e_1$ := `Empty1`, $e_2$ := `Empty2`, $e_3$ := `Empty3` are AlgCompounds `a` with `a.dim = n` and `a.wrapped = None` for $n = 1,2,3$

**Sets of predefined basic shapes:**

$B^3 := \lbrace$`Empty3`, `Box`, `Cylinder`, `Cone`, `Sphere`, `Torus`, `Wedge`, `Bore`, `CounterBore`, `CounterSink`$\rbrace$ 

$B^2 := \lbrace$`Empty2`, `Rectangle`, `Circle`, `Ellipse`, `Rectangle`, `Polygon`, `RegularPolygon`, `Text`, `Trapezoid`, `SlotArc`, `SlotCenterPoint`, `SlotCenterToCenter`, `SlotOverall`$\rbrace$

$B^1 := \lbrace$`Empty1`, `Bezier`, `PolarLine`, `Polyline`, `Spline`, `Helix`, `CenterArc`, `EllipticalCenterArc`, `RadiusArc`, `SagittaArc`, `TangentArc`, `ThreePointArc`, `JernArc`$\rbrace$

with $B^n \subset A^n$


**Operations:**

$+: A^n, A^n \rightarrow A^n$  with $a, b \rightarrow a + b$ , for $n=1,2,3$
    
$a + b :=$ `a.fuse(b)`

$-: A^n \rightarrow A^n$ with $a \rightarrow -a$ , for $n=1, 2,3$ 

$b := -a$  if `a.cut(b).wrapped == None and b.cut(a).wrapped == None`

Note: The actual implementation does not implement the inverse of an AlgCompound, but defines `a + (-b) = a - b == a.cut(b)`
    
**Abelian groups**

$( A^n, e_n, +, -)$ is an abelian group for $n=1,2,3$ 


**Intersect objects**

$| : A^n, A^n \rightarrow A^n$ with $a, b \rightarrow a | b$ 

$b | a :=$ `a.intersect(b)` for $n=2,3$

Note: $a | b = (a + b) - (a - b) - (b - a)$

### Locations and location arithmentic

$L  := \lbrace$ `Location` $((x,y,z), (a,b,c)): x,y,z \in R \land a,b,c \in R\rbrace$ with $a,b,c$ being angles in degrees



For $n = 1, 2, 3$:

$*: L,L \rightarrow L$   (multiply two locations $l_1, l_2 \in L$, i.e. `l1 * l2`)

$*: A^n,L \rightarrow A^n$  (locate an object $a \in A^n$ at location $l \in L$, i.e. `a.located(l)`)

**Neutral element**: $l_0 \in L$: `Location()`

**Inverse element**: $l^{-1} \in L$: `l.inverse()`


### Planes and placing on planes:

$P  := \lbrace$ `Plane` $(o,x,z): o,x,z ∈ R^3 \land \|x\| = \|z\| = 1\rbrace$

For $n = 1, 2, 3$:

$@: A^n,P \rightarrow A^n$  (locate an object $a \in A^n$ at location of plane $p \in P$, i.e. `a.located(p.to_location())`)

$*: P,L \rightarrow P$   (locate plane $p \in P$ at location $l \in L$, i.e. `Plane(p.to_location() * l)`)

