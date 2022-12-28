# Shortcuts and extensions

## Planes

| Shortcut         | Long form / description                                           |
| ---------------- | ----------------------------------------------------------------- |
| `Planes(list)`   | Transform a mixed list of faces and locations to a list of planes |
| `plane.location` | `plane.to_location()`                                             |

with

-   `plane` being a `Plane`

## Locations

| Shortcut                          | Long form / description                                                                                                                                                   |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Create a position only `Location` |                                                                                                                                                                           |
| `Pos(x, y, z)`                    | `Location((x, y, z), (0, 0, 0))`                                                                                                                                          |
| `Pos(x=a)`                        | `Location((a, 0, 0), (0, 0, 0))`                                                                                                                                          |
| `Pos(y=a)`                        | `Location((0, a, 0), (0, 0, 0))`                                                                                                                                          |
| `Pos(z=a)`                        | `Location((0, 0, a), (0, 0, 0))`                                                                                                                                          |
| Create a rotation only `Location` |                                                                                                                                                                           |
| `Rot(x, y, z)`                    | `Location((0, 0, 0), (x, y, z))`                                                                                                                                          |
| `Rot(x=a)`                        | `Location((0, 0, 0), (a, 0, 0))`                                                                                                                                          |
| `Rot(y=a)`                        | `Location((0, 0, 0), (0, a, 0))`                                                                                                                                          |
| `Rot(z=a)`                        | `Location((0, 0, 0), (0, 0, a))`                                                                                                                                          |
| Properties                        |                                                                                                                                                                           |
| `loc.plane`                       | `Plane(loc)`                                                                                                                                                              |
| `loc.x_axis`                      | `Axis(p.origin, p.x_dir)` for `p=Plane(loc)`                                                                                                                              |
| `loc.y_axis`                      | `Axis(p.origin, p.y_dir)` for `p=Plane(loc)`                                                                                                                              |
| `loc.z_axis`                      | `Axis(p.origin, p.z_dir)` for `p=Plane(loc)`                                                                                                                              |
| `edge.origin_location`            | Location at the start point of an edge</br>if `edge` is a "LINE": `edge.to_axis().to_location()`</br> else `Location(orgin=edge @ 0, x_dir=edge % 0, z_dir=edge.normal()` |
| `edge.center_location`            | Location at the center of a closed `Edge` with `x_dir` going from `origin` to `vertex` of the edge                                                                        |
| `face.center_location`            | Location at the center of a `Face`                                                                                                                                        |

with

-   `loc` being a `Location`
-   `edge` being an `Edge`
-   `face` being an `Face`

## ShapeLists

| Shortcut                                      | Long form / description                                   |
| --------------------------------------------- | --------------------------------------------------------- |
| Simple filters                                |                                                           |
| `ac.vertices(filter_by, reverse, tolerance)`  | `ac.vertices().filter_by(filter_by, reverse, tolerance)`  |
| `ac.edges(filter_by, reverse, tolerance)`     | `ac.edges().filter_by(filter_by, reverse, tolerance)`     |
| `ac.compounds(filter_by, reverse, tolerance)` | `ac.compounds().filter_by(filter_by, reverse, tolerance)` |
| `ac.wires(filter_by, reverse, tolerance)`     | `ac.wires().filter_by(filter_by, reverse, tolerance)`     |
| `ac.faces(filter_by, reverse, tolerance)`     | `ac.faces().filter_by(filter_by, reverse, tolerance)`     |
| `ac.shells(filter_by, reverse, tolerance)`    | `ac.shells().filter_by(filter_by, reverse, tolerance)`    |
| `ac.solids(filter_by, reverse, tolerance)`    | `ac.solids().filter_by(filter_by, reverse, tolerance)`    |
| Better readability                            |                                                           |
| `ls.max(axis, wrapped)`                       | `ls.sort_by(axis)[-1]`                                    |
| `ls.min(axis, wrapped)`                       | `ls.sort_by(axis)[0]`                                     |
| `ls.min_group(axis)`                          | `ls.group_by(axis)[-1]`                                   |
| `ls.max_group(axis)`                          | `ls.group_by(axis)[0]`                                    |
| Difference                                    |                                                           |
| `sl.__sub__(other)`                           | Difference of two `ShapeList`s: `sl - other`              |

with

-   `ac` being an `AlgCompound`
-   `ls` being a list of `Shape`s
-   `sl` being a `ShapeList`

## Symbols

| Shortcut               | Long form / description                                                                             |
| ---------------------- | --------------------------------------------------------------------------------------------------- |
| `loc.symbol(size=1)`   | returns `SVG.axis` at `loc` with `size`                                                             |
| `plane.symbol(size=1)` | returns a `Compound`of an `SVG.axis` at `plane.location` with `size` and a circle around the origin |
| `axis.symbol(size=1)`  | returns a `Compound` of an arrow of length `size`                                                   |

with

-   `loc` being a `Location`
-   `plane` being a `Plane`
-   `axis` being an `Axis`
