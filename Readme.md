# Alg123d

## Algebraic definitions

**Sets:**

$G^2 := \lbrace$`Empty`, `Rectangle`, `Circle`$\rbrace$

$G^3 := \lbrace$`Empty`, `Box`, `Cylinder`, `Extrusion`$\rbrace$

$L  := \lbrace$ `Location` $((x,y,z), (a,b,c)): x,y,z \in R \land a,b,c \in [-360.0,360.0]\rbrace$

$W  := \lbrace$ `Workplane` $(o,x,z): o,x,z ∈ R^3 \land \|x\| == \|z\| == 1\rbrace$

**Operations:**

For $n = 2, 3$:

- Location arithmentic
    - $*: W,L \rightarrow W$   (locate workplane $w \in W$ at location $l \in L$, i.e. `Workplane(w.to_location() * l)`)
    - $*: L,L \rightarrow L$   (multiply two locations $l_1, l_2 \in L$, i.e. `l1 * l2`)
    - $@: G^n,W \rightarrow G^n$  (locate an object $g \in G^n$ to the location of workplane $w \in W$, i.e. `g.located(w.to_location())`)
    - $@: G^n,L \rightarrow G^n$  (locate an object $g \in G^n$ to the location $l \in L$, i.e. `g.located(l)`)

- Fuse or cut objects
    - $+: G^n, G^n \rightarrow G^n$  with $a, b \rightarrow$ `a + b = a.fuse(b)` (fuse two objects)
    - $-: G^n \rightarrow G^n$ with $a \rightarrow -a$ (not implemented, use, use $b - a$, see below)
    - $-: G^n \rightarrow G^n$ with $a, b \rightarrow$ `a - b = a.cut(b)` (cut two objects)

- Intersect objects
    - &amp; $: G^n, G^n \rightarrow G^n$ with $a, b \rightarrow$ `a & b = a.intersect(b)`

- Neutral elements

    - $e_0 =$ `Empty` is the neutral element for $+$
    - $l_0 =$ `Location()` and $w_0 =$ `Workplane.XY` are the neutral elements for $*$ and $@$

- Inverse elements

    - For $l \in L: l^{-1} =$ `l.inverse()`
    - For $w \in W: w^{-1} =$ `Workplane(w.to_location().inverse())`
    - For $g \in G^n: g^{-1}$ is defined by $g + g^{-1} := g - g = e_0$