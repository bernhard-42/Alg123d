## Example 1

-   **Build23d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    with BuildPart() as ex1:
        Box(length, width, thickness)
    ```

-   **Alg123d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    ex1 = Box(length, width, thickness)
    ```

## Example 2

-   **Build23d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0
    center_hole_dia = 22.0

    with BuildPart() as ex2:
        Box(length, width, thickness)
        Cylinder(radius=center_hole_dia / 2, height=thickness, mode=Mode.SUBTRACT)
    ```

-   **Alg123d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0
    center_hole_dia = 22.0

    ex2 = Box(length, width, thickness)
    ex2 -= Cylinder(radius=center_hole_dia / 2, height=thickness)
    ```

## Example 3

-   **Build23d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    with BuildPart() as ex3:
        with BuildSketch() as ex3_sk:
            Circle(width)
            Rectangle(length / 2, width / 2, mode=Mode.SUBTRACT)
        Extrude(amount=2 * thickness)
    ```

-   **Alg123d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    sk3 = Circle(width) - Rectangle(length / 2, width / 2)
    ex3 = extrude(sk3, amount=2 * thickness)
    ```

## Example 4

-   **Build23d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    with BuildPart() as ex4:
        with BuildSketch() as ex4_sk:
            with BuildLine() as ex4_ln:
                l1 = Line((0, 0), (length, 0))
                l2 = Line((length, 0), (length, width))
                l3 = ThreePointArc((length, width), (width, width * 1.5), (0.0, width))
                l4 = Line((0.0, width), (0, 0))
            MakeFace()
        Extrude(amount=thickness)
    ```

-   **Alg123d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    lines = [
        Line((0, 0), (length, 0)),
        Line((length, 0), (length, width)),
        ThreePointArc((length, width), (width, width * 1.5), (0.0, width)),
        Line((0.0, width), (0, 0)),
    ]
    sk4 = make_face(lines)
    ex4 = extrude(sk4, thickness)
    ```

## Example 5

-   **Build23d**

    ```python
    a, b, c, d = 90, 45, 15, 7.5

    with BuildPart() as ex5:
        with BuildSketch() as ex5_sk:
            Circle(a)
            with Locations((b, 0.0)):
                Rectangle(c, c, mode=Mode.SUBTRACT)
            with Locations((0, b)):
                Circle(d, mode=Mode.SUBTRACT)
        Extrude(amount=c)
    ```

-   **Alg123d**

    ```python
    a, b, c, d = 90, 45, 15, 7.5

    sk5 = Circle(a) - Rectangle(c, c) @ Pos(b, 0.0) - Circle(d) @ Pos(0.0, b)
    ex5 = extrude(sk5, c)
    ```

## Example 6

-   **Build23d**

    ```python
    a, b, c = 80, 60, 10

    with BuildPart() as ex6:
        with BuildSketch() as ex6_sk:
            Circle(a)
            with Locations((b, 0), (0, b), (-b, 0), (0, -b)):
                Circle(c, mode=Mode.SUBTRACT)
        Extrude(amount=c)
    ```

-   **Alg123d**

    ```python
    a, b, c = 80, 60, 10

    sk6 = [Circle(c) @ loc for loc in Locations((b, 0), (0, b), (-b, 0), (0, -b))]
    ex6 = extrude(Circle(a) - sk6, c)
    ```

## Example 7

-   **Build23d**

    ```python
    a, b, c = 60, 80, 5

    with BuildPart() as ex7:
        with BuildSketch() as ex7_sk:
            Rectangle(a, b, c)
            with Locations((0, 3 * c), (0, -3 * c)):
                RegularPolygon(radius=2 * c, side_count=6, mode=Mode.SUBTRACT)
        Extrude(amount=c)
    ```

-   **Alg123d**

    ```python
    a, b, c = 60, 80, 5

    polygons = [
        RegularPolygon(radius=2 * c, side_count=6) @ loc
        for loc in Locations((0, 3 * c), (0, -3 * c))
    ]
    sk7 = Rectangle(a, b) @ Rot(z=5) - polygons
    ex7 = extrude(sk7, c)
    ```

## Example 8

-   **Build23d**

    ```python
    (L, H, W, t) = (100.0, 20.0, 20.0, 1.0)
    pts = [
        (0, H / 2.0),
        (W / 2.0, H / 2.0),
        (W / 2.0, (H / 2.0 - t)),
        (t / 2.0, (H / 2.0 - t)),
        (t / 2.0, (t - H / 2.0)),
        (W / 2.0, (t - H / 2.0)),
        (W / 2.0, H / -2.0),
        (0, H / -2.0),
    ]

    with BuildPart() as ex8:
        with BuildSketch() as ex8_sk:
            with BuildLine() as ex8_ln:
                Polyline(*pts)
                Mirror(ex8_ln.line, about=Plane.YZ)
            MakeFace()
        Extrude(amount=L / 2)
    ```

-   **Alg123d**

    ```python
    (L, H, W, t) = (100.0, 20.0, 20.0, 1.0)
    pts = [
        (0, H / 2.0),
        (W / 2.0, H / 2.0),
        (W / 2.0, (H / 2.0 - t)),
        (t / 2.0, (H / 2.0 - t)),
        (t / 2.0, (t - H / 2.0)),
        (W / 2.0, (t - H / 2.0)),
        (W / 2.0, H / -2.0),
        (0, H / -2.0),
    ]

    ln = Polyline(pts)
    ln += mirror(ln, about=Plane.YZ)

    sk8 = make_face(ln)
    ex8 = extrude(sk8, L / 2)
    ```

## Example 9

-   **Build23d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    with BuildPart() as ex9:
        Box(length, width, thickness)
        Chamfer(*ex9.edges().group_by(Axis.Z)[-1], length=4)
        Fillet(*ex9.edges().filter_by(Axis.Z), radius=5)
    ```

-   **Alg123d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    ex9 = Box(length, width, thickness)
    ex9 = chamfer(ex9, ex9.edges().max_group(), length=4)
    ex9 = fillet(ex9, ex9.edges(Axis.Z), radius=5)
    ```

## Example 10

-   **Build23d**

    ```python
    with BuildPart() as ex10:
        Box(length, width, thickness)
        Chamfer(*ex10.edges().group_by(Axis.Z)[-1], length=4)
        Fillet(*ex10.edges().filter_by(Axis.Z), radius=5)
        Hole(radius=width / 4)
        Fillet(ex10.edges(Select.LAST).sort_by(Axis.Z)[-1], radius=2)
    ```

-   **Alg123d**

    ```python
    ex10 = Box(length, width, thickness)
    ex10 = chamfer(ex10, ex10.edges().max_group(), length=4)
    ex10 = fillet(ex10, ex10.edges(Axis.Z), radius=5)

    last = ex10.edges()
    ex10 -= Bore(ex10, radius=width / 4)
    ex10 = fillet(ex10, (ex10.edges() - last).max(), radius=2)
    ```

## Example 11

-   **Build23d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    with BuildPart() as ex11:
        Box(length, width, thickness)
        Chamfer(*ex11.edges().group_by(Axis.Z)[-1], length=4)
        Fillet(*ex11.edges().filter_by(Axis.Z), radius=5)
        Hole(radius=width / 4)
        Fillet(ex11.edges(Select.LAST).sort_by(Axis.Z)[-1], radius=2)
        with BuildSketch(ex11.faces().sort_by(Axis.Z)[-1]) as ex11_sk:
            with GridLocations(length / 2, width / 2, 2, 2):
                RegularPolygon(radius=5, side_count=5)
        Extrude(amount=-thickness, mode=Mode.SUBTRACT)
    ```

-   **Alg123d**

    ```pthon
    length, width, thickness = 80.0, 60.0, 10.0

    ex11 = Box(length, width, thickness)
    ex11 = chamfer(ex11, ex11.edges().max_group(), 4)
    ex11 = fillet(ex11, ex11.edges(Axis.Z), 5)

    last = ex11.edges()
    ex11 -= Bore(ex11, radius=width / 4)
    ex11 = fillet(ex11, (ex11.edges() - last).max(), 2)

    plane = Plane(ex11.faces().max())
    sk11 = [
        RegularPolygon(radius=5, side_count=5) @ (plane * loc)
        for loc in GridLocations(length / 2, width / 2, 2, 2)
    ]
    ex11 -= extrude(sk11, thickness)
    ```

## Example 12

-   **Build23d**

    ```python
    sPnts = [
        (55, 30),
        (50, 35),
        (40, 30),
        (30, 20),
        (20, 25),
        (10, 20),
        (0, 20),
    ]

    with BuildPart() as ex12:
        with BuildSketch() as ex12_sk:
            with BuildLine() as ex12_ln:
                l1 = Spline(*sPnts)
                l2 = Line(l1 @ 0, (60, 0))
                l3 = Line(l2 @ 1, (0, 0))
                l4 = Line(l3 @ 1, l1 @ 1)
            MakeFace()
        Extrude(amount=10)
    ```

-   **Alg123d**

    ```python
    sPnts = [
        (55, 30),
        (50, 35),
        (40, 30),
        (30, 20),
        (20, 25),
        (10, 20),
        (0, 20),
    ]

    l1 = Spline(sPnts)
    l2 = Line(l1 @ 0, (60, 0))
    l3 = Line(l2 @ 1, (0, 0))
    l4 = Line(l3 @ 1, l1 @ 1)

    sk12 = make_face([l1, l2, l3, l4])
    ex12 = extrude(sk12, amount=10)
    ```

## Example 13

-   **Build23d**

    ```python
    a, b = 40, 4

    with BuildPart() as ex13:
        Cylinder(radius=50, height=10)
        with Workplanes(ex13.faces().sort_by(Axis.Z)[-1]):
            with PolarLocations(radius=a, count=4):
                CounterSinkHole(radius=b, counter_sink_radius=2 * b)
            with PolarLocations(radius=a, count=4, start_angle=45, stop_angle=360 + 45):
                CounterBoreHole(radius=b, counter_bore_radius=2 * b, counter_bore_depth=b)
    ```

-   **Alg123d**

    ```python
    a, b = 40, 4

    ex13 = Cylinder(radius=50, height=10)
    plane = Plane(ex13.faces().max())

    ex13 -= [
        CounterSink(ex13, radius=b, counter_sink_radius=2 * b) @ (plane * loc)
        for loc in PolarLocations(radius=a, count=4)
    ]
    ex13 -= [
        CounterBore(ex13, radius=b, counter_bore_radius=2 * b, counter_bore_depth=b) @ (plane * loc)
        for loc in PolarLocations(radius=a, count=4, start_angle=45, stop_angle=360 + 45)
    ]
    ```

## Example 14

-   **Build23d**

    ```python
    a, b = 40, 20

    with BuildPart() as ex14:
        with BuildLine() as ex14_ln:
            l1 = JernArc(start=(0, 0), tangent=(0, 1), radius=a, arc_size=180)
            l2 = JernArc(start=l1 @ 1, tangent=l1 % 1, radius=a, arc_size=-90)
            l3 = Line(l2 @ 1, l2 @ 1 + Vector(-a, a))
        with BuildSketch(Plane.XZ) as ex14_sk:
            Rectangle(b, b)
        Sweep(path=ex14_ln.wires()[0])
    ```

-   **Alg123d**

    ```python
    a, b = 40, 20

    l1 = JernArc(start=(0, 0), tangent=(0, 1), radius=a, arc_size=180)
    l2 = JernArc(start=l1 @ 1, tangent=l1 % 1, radius=a, arc_size=-90)
    l3 = Line(l2 @ 1, l2 @ 1 + Vector(-a, a))

    sk14 = Rectangle(b, b) @ Plane.XZ
    ex14 = sweep(sk14.faces(), path=(l1 + l2 + l3).wire())
    ```

## Example 15

-   **Build23d**

    ```python
    a, b, c = 80, 40, 20

    with BuildPart() as ex15:
        with BuildSketch() as ex15_sk:
            with BuildLine() as ex15_ln:
                l1 = Line((0, 0), (a, 0))
                l2 = Line(l1 @ 1, l1 @ 1 + Vector(0, b))
                l3 = Line(l2 @ 1, l2 @ 1 + Vector(-c, 0))
                l4 = Line(l3 @ 1, l3 @ 1 + Vector(0, -c))
                l5 = Line(l4 @ 1, Vector(0, (l4 @ 1).Y))
                Mirror(ex15_ln.line, about=Plane.YZ)
            MakeFace()
        Extrude(amount=c)
    ```

-   **Alg123d**

    ```python
    a, b, c = 80, 40, 20

    l1 = Line((0, 0), (a, 0))
    l2 = Line(l1 @ 1, l1 @ 1 + Vector(0, b))
    l3 = Line(l2 @ 1, l2 @ 1 + Vector(-c, 0))
    l4 = Line(l3 @ 1, l3 @ 1 + Vector(0, -c))
    l5 = Line(l4 @ 1, Vector(0, (l4 @ 1).Y))
    ln = l1 + l2 + l3 + l4 + l5
    ln += mirror(ln, about=Plane.YZ)

    sk15 = make_face(ln)
    ex15 = extrude(sk15, c)
    ```

## Example 16

-   **Build23d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    with BuildPart() as ex16_single:
        with BuildSketch(Plane.XZ) as ex16_sk:
            Rectangle(length, width)
            Fillet(*ex16_sk.vertices(), radius=length / 10)
            with GridLocations(x_spacing=length / 4, y_spacing=0, x_count=3, y_count=1):
                Circle(length / 12, mode=Mode.SUBTRACT)
            Rectangle(length, width, centered=(False, False), mode=Mode.SUBTRACT)
        Extrude(amount=length)

    with BuildPart() as ex16:
        Add(ex16_single.part)
        Mirror(ex16_single.part, about=Plane.XY.offset(width))
        Mirror(ex16_single.part, about=Plane.YX.offset(width))
        Mirror(ex16_single.part, about=Plane.YZ.offset(width))
        Mirror(ex16_single.part, about=Plane.YZ.offset(-width))
    ```

-   **Alg123d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    sk16 = Rectangle(length, width)
    sk16 = fillet(sk16, sk16.vertices(), radius=length / 10)

    circles = [Circle(length / 12) @ loc for loc in GridLocations(length / 4, 0, 3, 1)]
    sk16 = sk16 - circles - Rectangle(length, width, centered=(False, False))

    ex16_single = extrude(sk16 @ Plane.XZ, length)

    planes = [
        Plane.XY.offset(width),
        Plane.YX.offset(width),
        Plane.YZ.offset(width),
        Plane.YZ.offset(-width),
    ]
    objs = [mirror(ex16_single, plane) for plane in planes]
    ex16 = ex16_single + objs
    ```

## Example 17

-   **Build23d**

    ```python
    a, b = 30, 20

    with BuildPart() as ex17:
        with BuildSketch() as ex17_sk:
            RegularPolygon(radius=a, side_count=5)
        Extrude(amount=b)
        Mirror(ex17.part, about=Plane((ex17.faces() << Axis.Y)[0].to_pln()))
    ```

-   **Alg123d**

    ```python
    a, b = 30, 20

    sk17 = RegularPolygon(radius=a, side_count=5)
    ex17 = extrude(sk17, b)
    ex17 += mirror(ex17, about=Plane(ex17.faces().min(Axis.Y)))
    ```

## Example 18

-   **Build23d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0
    a, b = 4, 5

    with BuildPart() as ex18:
        Box(length, width, thickness)
        Chamfer(*ex18.edges().group_by(Axis.Z)[-1], length=a)
        Fillet(*ex18.edges().filter_by(Axis.Z), radius=b)
        with BuildSketch(ex18.faces().sort_by(Axis.Z)[-1]):
            Rectangle(2 * b, 2 * b)
        Extrude(amount=-thickness, mode=Mode.SUBTRACT)
    ```

-   **Alg123d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0
    a, b = 4, 5

    ex18 = Box(length, width, thickness)
    ex18 = chamfer(ex18, ex18.edges().max_group(), a)
    ex18 = fillet(ex18, ex18.edges(Axis.Z), b)

    sk18 = Rectangle(2 * b, 2 * b) @ Plane(ex18.faces().min())
    ex18 -= extrude(sk18, -thickness)
    ```

## Example 19

-   **Build23d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    with BuildPart() as ex19:
        Box(length, width, thickness)
        with Locations(ex19.faces().sort_by(Axis.Z)[-1].vertices()[-1]):
            Hole(radius=width / 4)
    ```

-   **Alg123d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    ex19 = Box(length, width, thickness)
    vertex = ex19.faces().min().vertices()[-1]
    ex19 -= Bore(ex19, radius=width / 4) @ Pos(vertex)
    ```

## Example 20

-   **Build23d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    with BuildPart() as ex20:
        Box(length, width, thickness)
        pln = Plane((ex20.faces() << Axis.X)[0].to_pln())
        pln.origin = (ex20.faces() << Axis.X)[0].center()
        with BuildSketch(pln.offset(thickness)):
            Circle(width / 2)
        Extrude(amount=thickness)
    ```

-   **Alg123d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    ex20 = Box(length, width, thickness)
    plane = Plane(ex20.faces().min(Axis.X)).offset(thickness)
    # plane = Plane(ex20.faces().min(Axis.X)) * Pos(z=thickness)

    sk20 = Circle(width / 2) @ plane
    ex20 += extrude(sk20, thickness)
    ```

## Example 21

-   **Build23d**

    ```python
    width, length = 10.0, 60.0

    with BuildPart() as ex21:
        with BuildSketch() as ex21_sk:
            Circle(width / 2)
        Extrude(amount=length)
        with BuildSketch(Plane(origin=ex21.part.center(), z_dir=(-1, 0, 0))):
            Circle(width / 2)
        Extrude(amount=length)
    ```

-   **Alg123d**

    ```python
    width, length = 10.0, 60.0

    ex21 = extrude(Circle(width / 2), length)
    plane = Plane(origin=ex21.center(), z_dir=(-1, 0, 0))
    ex21 += extrude(Circle(width / 2), length) @ plane
    ```

## Example 22

-   **Build23d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    with BuildPart() as ex22:
        Box(length, width, thickness)
        pln = Plane((ex22.faces() >> Axis.Z)[0].to_pln()).rotated((0, 50, 0))
        pln.origin = (ex20.faces() >> Axis.Z)[0].center()
        with BuildSketch(pln) as ex22_sk:
            with GridLocations(length / 4, width / 4, 2, 2):
                Circle(thickness / 4)
        Extrude(amount=-100, both=True, mode=Mode.SUBTRACT)
    ```

-   **Alg123d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    ex22 = Box(length, width, thickness)
    plane = Plane(ex22.faces().max()) * Rot(0, 50, 0)

    holes = [
        Circle(thickness / 4) @ (plane * loc)
        for loc in GridLocations(length / 4, width / 4, 2, 2)
    ]
    ex22 -= extrude(holes, -100, both=True)
    ```

## Example 23

-   **Build23d**

    ```python
    pts = [
        (-25, 35),
        (-25, 0),
        (-20, 0),
        (-20, 5),
        (-15, 10),
        (-15, 35),
    ]

    with BuildPart() as ex23:
        with BuildSketch(Plane.XZ) as ex23_sk:
            with BuildLine() as ex23_ln:
                l1 = Polyline(*pts)
                l2 = Line(l1 @ 1, l1 @ 0)
            MakeFace()
            with Locations((0, 35)):
                Circle(25)
            Split(bisect_by=Plane.ZY)
        Revolve(axis=Axis.Z)
    ```

-   **Alg123d**

    ```python
    pts = [
        (-25, 35),
        (-25, 0),
        (-20, 0),
        (-20, 5),
        (-15, 10),
        (-15, 35),
    ]

    l1 = Polyline(pts)
    l2 = Line(l1 @ 1, l1 @ 0)
    sk23 = make_face([l1, l2])

    sk23 += Circle(25) @ Pos(0, 35)
    sk23 = split(sk23, by=Plane.ZY) @ Plane.XZ

    ex23 = revolve(sk23, axis=Axis.Z)
    ```

## Example 24

-   **Build23d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    with BuildPart() as ex24:
        Box(length, length, thickness)
        with BuildSketch((ex24.faces() >> Axis.Z)[0]) as ex24_sk:
            Circle(length / 3)
        with BuildSketch(ex24_sk.faces()[0].offset(length / 2)) as ex24_sk2:
            Rectangle(length / 6, width / 6)
        Loft()
    ```

-   **Alg123d**

    ```python
    length, width, thickness = 80.0, 60.0, 10.0

    ex24 = Box(length, length, thickness)
    plane = Plane(ex24.faces().max())

    faces = [
        Circle(length / 3) @ plane,
        Rectangle(length / 6, width / 6) @ plane.offset(length / 2),
    ]

    ex24 += loft(faces)
    ```
