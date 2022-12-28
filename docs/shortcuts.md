# Shortcuts and extensions

## Location shortcuts

| Shortcut                          | Long form / description                                                                                                                                                        |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Create a position only `Location` |                                                                                                                                                                                |
| `Pos(x, y, z)`                    | `Location((x, y, z), (0, 0, 0))`                                                                                                                                               |
| `Pos(x=a)`                        | `Location((a, 0, 0), (0, 0, 0))`                                                                                                                                               |
| `Pos(y=a)`                        | `Location((0, a, 0), (0, 0, 0))`                                                                                                                                               |
| `Pos(z=a)`                        | `Location((0, 0, a), (0, 0, 0))`                                                                                                                                               |
| Create a rotation only `Location` |                                                                                                                                                                                |
| `Rot(x, y, z)`                    | `Location((0, 0, 0), (x, y, z))`                                                                                                                                               |
| `Rot(x=a)`                        | `Location((0, 0, 0), (a, 0, 0))`                                                                                                                                               |
| `Rot(y=a)`                        | `Location((0, 0, 0), (0, a, 0))`                                                                                                                                               |
| `Rot(z=a)`                        | `Location((0, 0, 0), (0, 0, a))`                                                                                                                                               |
| Properties                        |                                                                                                                                                                                |
| `loc.plane`                       | `Plane(loc)`                                                                                                                                                                   |
| `loc.x_axis`                      | `Axis(p.origin, p.x_dir)` for `p=Plane(loc)`                                                                                                                                   |
| `loc.y_axis`                      | `Axis(p.origin, p.y_dir)` for `p=Plane(loc)`                                                                                                                                   |
| `loc.z_axis`                      | `Axis(p.origin, p.z_dir)` for `p=Plane(loc)`                                                                                                                                   |
| `Edge.origin_location`            | Location at the start point of an edge</br>if `edge` is a "LINE": `edge.to_axis</br>().to_location()`</br> else `Location(orgin=edge @ 0, x_dir=edge % 0, z_dir=edge.normal()` |
| `Edge.center_location`            | Location at the center of a closed `Edge`                                                                                                                                      |
| `Face.center_location`            | Location at the center of a `Face`                                                                                                                                             |

## Plane shortcuts

| Shortcut         | Long form / description                                           |
| ---------------- | ----------------------------------------------------------------- |
| `Planes(list)`   | Transform a mixed list of faces and locations to a list of planes |
| `Plane.location` | `plane.to_location()`                                             |

## Shape shortcuts

| Shortcut                                   | Long form / description                                |
| ------------------------------------------ | ------------------------------------------------------ |
| `vertices(filter_by, reverse, tolerance)`  | `vertices().filter_by(filter_by, reverse, tolerance)`  |
| `edges(filter_by, reverse, tolerance)`     | `edges().filter_by(filter_by, reverse, tolerance)`     |
| `compounds(filter_by, reverse, tolerance)` | `compounds().filter_by(filter_by, reverse, tolerance)` |
| `wires(filter_by, reverse, tolerance)`     | `wires().filter_by(filter_by, reverse, tolerance)`     |
| `faces(filter_by, reverse, tolerance)`     | `faces().filter_by(filter_by, reverse, tolerance)`     |
| `shells(filter_by, reverse, tolerance)`    | `shells().filter_by(filter_by, reverse, tolerance)`    |
| `solids(filter_by, reverse, tolerance)`    | `solids().filter_by(filter_by, reverse, tolerance)`    |

## ShapeList shortcuts

| Shortcut             | Long form / description             |
| -------------------- | ----------------------------------- |
| `__sub__(other)`     | Difference between 2 `ShapeList`s   |
| `max(axis, wrapped)` | `list_of_shapes.sort_by(axis)[-1]`  |
| `min(axis, wrapped)` | `list_of_shapes.sort_by(axis)[0]`   |
| `min_group(axis)`    | `list_of_shapes.group_by(axis)[-1]` |
| `max_group(axis)`    | `list_of_shapes.group_by(axis)[-1]` |

## Symbols

| Shortcut               | Long form / description                                         |
| ---------------------- | --------------------------------------------------------------- |
| `loc.symbol(size=1)`   | returns `SVG.axis` at `loc` with `size`                         |
| `plane.symbol(size=1)` | returns `SVG.axis` at `plane.location` with `size` and a circle |
| `axis.symbol(size=1)`  | returns an arrow of length `size`                               |
