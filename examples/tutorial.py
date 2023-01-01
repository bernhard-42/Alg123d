from alg123d import *

# %%

# 1. Simple Rectangular Plate

length, width, thickness = 80.0, 60.0, 10.0

ex1 = Box(length, width, thickness)

show(ex1)
# %%

# 2. Plate with Hole

length, width, thickness = 80.0, 60.0, 10.0
center_hole_dia = 22.0

ex2 = Box(length, width, thickness)
ex2 -= Cylinder(radius=center_hole_dia / 2, height=thickness)

show(ex2)
# %%

# 3. An extruded prismatic solid

length, width, thickness = 80.0, 60.0, 10.0

sk3 = Circle(width) - Rectangle(length / 2, width / 2)
ex3 = extrude(sk3, amount=2 * thickness)

show(ex3)

# %%

# 4. Building Profiles using lines and arcs

length, width, thickness = 80.0, 60.0, 10.0

lines = [
    Line((0, 0), (length, 0)),
    Line((length, 0), (length, width)),
    ThreePointArc((length, width), (width, width * 1.5), (0.0, width)),
    Line((0.0, width), (0, 0)),
]
sk4 = make_face(lines)
ex4 = extrude(sk4, amount=thickness)

show(ex4)

# %%

# 5. Moving the current working point

a, b, c, d = 90, 45, 15, 7.5

sk5 = Circle(a) - Rectangle(c, c) @ Pos(b, 0.0) - Circle(d) @ Pos(0.0, b)
ex5 = extrude(sk5, amount=c)

show(ex5)

# %%

# 6. Using Point Lists

a, b, c = 80, 60, 10

sk6 = [Circle(c) @ loc for loc in Locations((b, 0), (0, b), (-b, 0), (0, -b))]
ex6 = extrude(Circle(a) - sk6, amount=c)

show(ex6)

# %%

# 7. Polygons

a, b, c = 60, 80, 5

polygons = [
    RegularPolygon(radius=2 * c, side_count=6) @ loc
    for loc in Locations((0, 3 * c), (0, -3 * c))
]
sk7 = Rectangle(a, b) @ Rot(z=5) - polygons
ex7 = extrude(sk7, amount=c)

show(ex7)


# %%

# 8. Polylines

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
ex8 = extrude(sk8, amount=L / 2)

show(ex8)

# %%

# 9. Selectors, Fillets, and Chamfers

length, width, thickness = 80.0, 60.0, 10.0

ex9 = Box(length, width, thickness)
ex9 = chamfer(ex9, ex9.edges().max_group(), length=4)
ex9 = fillet(ex9, ex9.edges(Axis.Z), radius=5)

show(ex9)

# %%

# 10. Select Last and Hole


ex10 = Box(length, width, thickness)
ex10 = chamfer(ex10, ex10.edges().max_group(), length=4)
ex10 = fillet(ex10, ex10.edges(Axis.Z), radius=5)

last = ex10.edges()
ex10 -= Bore(ex10, radius=width / 4)
ex10 = fillet(ex10, (ex10.edges() - last).max(), radius=2)

show(ex10)

# %%

# 11. Use a face as a plane for BuildSketch and introduce GridLocations

length, width, thickness = 80.0, 60.0, 10.0

ex11 = Box(length, width, thickness)
ex11 = chamfer(ex11, ex11.edges().max_group(), length=4)
ex11 = fillet(ex11, ex11.edges(Axis.Z), radius=5)
last = ex11.edges()
ex11 -= Bore(ex11, radius=width / 4)
ex11 = fillet(ex11, (ex11.edges() - last).max(), radius=2)

plane = Plane(ex11.faces().max())
polygons = [
    RegularPolygon(radius=5, side_count=5) @ (plane * loc)
    for loc in GridLocations(length / 2, width / 2, 2, 2)
]
ex11 -= extrude(polygons, amount=thickness)

show(ex11)

# %%

# 12. Defining an Edge with a Spline

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

show(ex12)

# %%

# 13. CounterBoreHoles, CounterSinkHoles and PolarLocations

a, b = 40, 4

ex13 = Cylinder(radius=50, height=10)
plane = Plane(ex13.faces().max())

ex13 -= [
    CounterSink(ex13, radius=b, counter_sink_radius=2 * b) @ (plane * loc)
    for loc in PolarLocations(radius=a, count=4)
]
ex13 -= [
    CounterBore(ex13, radius=b, counter_bore_radius=2 * b, counter_bore_depth=b)
    @ (plane * loc)
    for loc in PolarLocations(radius=a, count=4, start_angle=45, stop_angle=360 + 45)
]

show(ex13)

# %%

# 14. Position on a line with ‘@’, ‘%’ and introduce Sweep

a, b = 40, 20

l1 = JernArc(start=(0, 0), tangent=(0, 1), radius=a, arc_size=180)
l2 = JernArc(start=l1 @ 1, tangent=l1 % 1, radius=a, arc_size=-90)
l3 = Line(l2 @ 1, l2 @ 1 + Vector(-a, a))

sk14 = Rectangle(b, b) @ Plane.XZ
ex14 = sweep(sk14.faces(), path=(l1 + l2 + l3).wire())

show(ex14)


# %%

# 15. Mirroring Symmetric Geometry

a, b, c = 80, 40, 20

l1 = Line((0, 0), (a, 0))
l2 = Line(l1 @ 1, l1 @ 1 + Vector(0, b))
l3 = Line(l2 @ 1, l2 @ 1 + Vector(-c, 0))
l4 = Line(l3 @ 1, l3 @ 1 + Vector(0, -c))
l5 = Line(l4 @ 1, Vector(0, (l4 @ 1).Y))
ln = l1 + l2 + l3 + l4 + l5
ln += mirror(ln, about=Plane.YZ)

sk15 = make_face(ln)
ex15 = extrude(sk15, amount=c)

show(ex15)

# %%

# 16. Mirroring 3D Objects

length, width, thickness = 80.0, 60.0, 10.0

sk16 = Rectangle(length, width)
sk16 = fillet(sk16, sk16.vertices(), radius=length / 10)
circles = [Circle(length / 12) @ loc for loc in GridLocations(length / 4, 0, 3, 1)]
sk16 = sk16 - circles - Rectangle(length, width, centered=(False, False))
ex16_single = extrude(sk16 @ Plane.XZ, amount=length)

planes = [
    Plane.XY.offset(width),
    Plane.YX.offset(width),
    Plane.YZ.offset(width),
    Plane.YZ.offset(-width),
]
objs = [mirror(ex16_single, plane) for plane in planes]
ex16 = ex16_single + objs

show(ex16)

# %%

# 17. Mirroring From Faces

a, b = 30, 20

sk17 = RegularPolygon(radius=a, side_count=5)
ex17 = extrude(sk17, amount=b)
ex17 += mirror(ex17, about=Plane(ex17.faces().min(Axis.Y)))

show(ex17)

# %%

# 18. Creating Workplanes on Faces

length, width, thickness = 80.0, 60.0, 10.0
a, b = 4, 5

ex18 = Box(length, width, thickness)
ex18 = chamfer(ex18, ex18.edges().max_group(), length=a)
ex18 = fillet(ex18, ex18.edges(Axis.Z), radius=b)

sk18 = Rectangle(2 * b, 2 * b) @ Plane(ex18.faces().min())
ex18 -= extrude(sk18, amount=-thickness)

show(ex18)

# %%

# 19. Locating a Workplane on a vertex

length, width, thickness = 80.0, 60.0, 10.0

ex19 = Box(length, width, thickness)
vertex = ex19.faces().min().vertices()[-1]
ex19 -= Bore(ex19, radius=width / 4) @ Pos(vertex)

show(ex19)

# %%

# 20. Offset Sketch Workplane


length, width, thickness = 80.0, 60.0, 10.0

ex20 = Box(length, width, thickness)
plane = Plane(ex20.faces().min(Axis.X)).offset(thickness)
# plane = Plane(ex20.faces().min(Axis.X)) * Pos(z=thickness)

sk20 = Circle(width / 2) @ plane
ex20 += extrude(sk20, amount=thickness)

show(ex20)


# %%

# 21. Create a Workplanes in the center of another shape


width, length = 10.0, 60.0

ex21 = extrude(Circle(width / 2), amount=length)
plane = Plane(origin=ex21.center(), z_dir=(-1, 0, 0))
ex21 += extrude(Circle(width / 2), amount=length) @ plane

show(ex21)

# %%

# 22. Rotated Workplanes


length, width, thickness = 80.0, 60.0, 10.0

ex22 = Box(length, width, thickness)
plane = Plane(ex22.faces().max()) * Rot(0, 50, 0)

holes = [
    Circle(thickness / 4) @ (plane * loc)
    for loc in GridLocations(length / 4, width / 4, 2, 2)
]
ex22 -= extrude(holes, amount=-100, both=True)

show(ex22)

# %%

# 23. Revolve


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

show(ex23, transparent=True)

# %%

# 24. Loft


length, width, thickness = 80.0, 60.0, 10.0

ex24 = Box(length, length, thickness)
plane = Plane(ex24.faces().max())

faces = [
    Circle(length / 3) @ plane,
    Rectangle(length / 6, width / 6) @ plane.offset(length / 2),
]

ex24 += loft(faces)

show(ex24)

# %%
