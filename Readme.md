# Alg123d

## Algebraic definitions

**Sets:**

$G^2 := \{$`Empty, Rectangle, Circle`$\}$

$G^3 := \{$`Empty, Box, Cylinder, Extrusion`$\}$

$L  := \{$`Location((x,y,z), (a,b,c))`$: x,y,z \in \R$ and $a,b,c \in [-360.0,360.0] \} $

$W  := \{$`Workplane(o,x,z)`$: o,x,z ∈ \R^3$ and $\|x\| == \|z\| == 1 \}$

**Operations:**

For $n = 2, 3$:

- Location arithmentic
    - $*: W,L \rightarrow W$   (locate workplane $w \in W$ at location $l \in L$, i.e. `Workplane(w.to_location() * l)`)
    - $*: L,L \rightarrow L$   (multiply two locations $l_1, l_2 \in L$, i.e. `l1 * l2`)
    - $*: G^n,P \rightarrow G^n$  (locate an object $g \in G^n$ to the location of workplane $w \in W$ of the plane, i.e. `g.located(w.to_location())`)
    - $*: G^n,L \rightarrow G^n$  (locate an object $g \in G^n$ to the location $l \in L$, i.e. `g.located(l)`)

- Fuse or cut objects
    - $+: G^n, G^n \rightarrow G^n$  with $a, b \rightarrow$ `a + b = a.fuse(b)` (fuse two objects)
    - $-: G^n \rightarrow G^n$ with $a \rightarrow -a$ (not implemented, use, use $b - a$, see below)
    - $-: G3, G3 \rightarrow G3$ with $a, b \rightarrow$ `a - b = a.cut(b)` (cut two objects)

- Intersect objects
    - $\&: G^n, G^n \rightarrow G^n$ with $a, b \rightarrow$ `a & b = a.intersect(b)`, with `a & b = (a + b) - (a - b) - (b - a)`

Some more theoretical topics (can be ignored for Alg123d)

- **Neutral elements**

    For $n = 2, 3$:

    - $e_0 = $ `Empty` is the neutral element for $+$
    - $l_0 =$ `Location()` and $p_0 =$ `Plane.XY` are the neutral elements for $*$

- **Inverse elements**

    For $n = 2, 3$:

    - For $l \in L: l^{-1} =$ `l.inverse()`
    - For $w \in W: w^{-1} = $ `Workplane(w.to_location().inverse())``
    - For $g \in G^n: g^{-1}$ is defined by $h - g$ for $h \in G^n$
