from __future__ import annotations
from dataclasses import dataclass
from typing import overload, Union, Tuple, Dict, List, overload
from webcolors import name_to_rgb
from enum import Enum, auto

from .direct_api import *


class Action(Enum):
    ROTATE = "t"
    ROTATE_X = "tx"
    ROTATE_Y = "ty"
    ROTATE_Z = "tz"
    TRANSLATE = "t"
    TRANSLATE_X = "tx"
    TRANSLATE_Y = "ty"
    TRANSLATE_Z = "tz"

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self.name}>"


class Color:
    @overload
    def __init__(self):
        ...

    @overload
    def __init__(self, color: str, a=1):
        ...

    @overload
    def __init__(self, r: int, g: int, b: int, a: float = 1):
        ...

    def __init__(self, *args):
        if len(args) == 0:
            self.r = 0
            self.g = 0
            self.b = 0
            self.a = 1.0

        elif len(args) >= 1 and isinstance(args[0], str):
            rgb = name_to_rgb(args[0])
            self.r = rgb.red
            self.g = rgb.green
            self.b = rgb.blue
            if len(args) == 2:
                self.a = args[1]
            else:
                self.a = 1.0

        elif (
            len(args) >= 3
            and isinstance(args[0], int)
            and isinstance(args[1], int)
            and isinstance(args[2], int)
        ):
            self.r = args[0]
            self.g = args[1]
            self.b = args[2]
            if len(args) == 4 and args[3] < 1.0:
                self.a = args[3]
            else:
                self.a = 1.0

        else:
            raise ValueError(f"Cannot define color from {args}")

    def to_tuple(self, percentage=False):
        if percentage:
            return (self.r / 255, self.g / 255, self.b / 255, self.a)
        else:
            return (self.r, self.g, self.b, self.a)

    def __repr__(self):
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"


@dataclass
class MateDef:
    mate: Mate
    assembly: str
    origin: bool

    @property
    def world_mate(self):
        mate = self.mate
        assembly = self.assembly

        while assembly is not None:
            mate = mate.moved(assembly.loc)
            assembly = assembly.parent

        return mate


class Mate:
    @overload
    def __init__(
        self,
        name,
        origin: VectorLike = Vector(0, 0, 0),
        x_dir: VectorLike = Vector(1, 0, 0),
        z_dir: VectorLike = Vector(0, 0, 1),
        center_of: CenterOf = CenterOf.BOUNDING_BOX,
    ):
        ...

    @overload
    def __init__(
        self,
        shape: Union[Face, Wire, Edge, ShapeList],
        name: str = "",
        center_of: CenterOf = CenterOf.BOUNDING_BOX,
    ):
        ...

    @overload
    def __init__(
        self,
        plane: Plane,
        name: str = "",
        center_of: CenterOf = CenterOf.BOUNDING_BOX,
    ):
        ...

    def __init__(
        self,
        *args,
        name: str = "",
        center_of: CenterOf = CenterOf.BOUNDING_BOX,
    ):

        self.name = name

        if len(args) == 1 and isinstance(args[0], Mate):
            val = args[0]

            self.name = val.name
            self.origin = val.origin
            self.x_dir = val.x_dir
            self.y_dir = val.y_dir
            self.z_dir = val.z_dir

        elif len(args) == 1 and isinstance(args[0], Plane):
            val = args[0]

            self.origin = Vector(val.origin.to_tuple())
            self.x_dir = Vector(val.x_dir.to_tuple())
            self.z_dir = Vector(val.z_dir.to_tuple())

        elif len(args) == 1 and isinstance(args[0], Edge):
            val = args[0]

            self.z_dir = val.normal()

            vertices = val.vertices()
            if len(vertices) == 1:  # e.g. a single closed spline
                self.origin = val.center(center_of)
                # Use the vector defined by the vertex and the origin as x direction
                self.x_dir = Vector((vertices[0] - self.origin).to_tuple()).normalized()
            else:
                self.origin = Vector(vertices[0].to_tuple())
                # Use the vector defined by the first two vertices as x direction
                self.x_dir = Vector((vertices[0] - vertices[1]).to_tuple()).normalized()

            self.y_dir = self.z_dir.cross(self.x_dir)

        elif len(args) == 1 and isinstance(args[0], (Face, Wire, ShapeList)):
            val = args[0]

            if isinstance(val, Wire):
                if val.is_closed():
                    val = Face.make_from_wires(val)
                else:
                    raise ValueError("Only closed wires supported")

            elif isinstance(val, ShapeList):
                if all([isinstance(o, Edge) for o in val]):
                    val = Face.make_from_wires(Wire.make_wire(val, sequenced=True))
                else:
                    raise ValueError("Only ShapeLists of Edges supported")

            self.origin = val.center(center_of)

            # x_dir, y_dir will be derived from the local coord system of the underlying plane
            p = val._geom_adaptor().Position()
            xd = p.Ax2().XDirection()
            yd = p.Ax2().YDirection()
            self.x_dir = Vector(xd.X(), xd.Y(), xd.Z())
            self.y_dir = Vector(yd.X(), yd.Y(), yd.Z())
            self.z_dir = self.x_dir.cross(self.y_dir)

        elif len(args) <= 3 and all([isinstance(a, (Vector, tuple)) for a in args]):
            self.origin = Vector(args[0])
            self.x_dir = Vector(args[1]).normalized()
            self.z_dir = Vector(args[2]).normalized()
            self.y_dir = self.z_dir.cross(self.x_dir)

        else:
            raise ValueError(
                f"Needs a 1-3 Vectors or a single Mate, Plane, Face, Edge or Wire, not {args}"
            )

        if self.name == "":
            print(self)
            raise ValueError("name cannot be empty")

    def __repr__(self) -> str:
        c = lambda v: f"({v.X:.2f}, {v.Y:.2f}, {v.Z:.2f})"
        return f"Mate(name='{self.name}', origin={c(self.origin)}, x_dir={c(self.x_dir)}, z_dir={c(self.z_dir)})"

    def __deepcopy__(self, memo):
        return Mate(self)

    @property
    def loc(self) -> Location:
        return Location(self.to_plane())

    @classmethod
    def from_plane(cls, plane: Plane) -> "Mate":
        return cls(plane.origin, plane.x_dir, plane.z_dir)

    def to_plane(self) -> Plane:
        return Plane(self.origin, self.x_dir, self.z_dir)

    def __matmul__(self, loc: Location):
        """
        Change location to a given loc
        :param loc: Location
        """
        plane = self.to_plane() * loc
        return Mate(
            plane.origin,
            plane.x_dir,
            plane.z_dir,
            name=self.name,
        )

    def move(self, loc: Location):
        """
        Move by the given Location
        :param loc: The Location object to move the mate
        """

        def move(origin: Vector, vec: Vector, loc: Location) -> Tuple[Vector, Vector]:
            reloc = Edge.make_line(origin, origin + vec).moved(loc)
            v1, v2 = reloc.start_point(), reloc.end_point()
            return v1, v2 - v1

        origin, x_dir = move(self.origin, self.x_dir, loc)
        _, z_dir = move(self.origin, self.z_dir, loc)

        self.origin = origin
        self.x_dir = x_dir
        self.z_dir = z_dir
        self.y_dir = z_dir.cross(x_dir)

    def moved(self, loc: Location) -> "Mate":
        """
        Return a new mate moved by the given Location
        :param loc: The Location object to move the mate
        :return: Mate
        """
        mate = Mate(self)  # copy mate
        mate.move(loc)
        return mate


class MAssembly:
    def __init__(
        self,
        obj: Union["MAssembly", Compound] = None,
        name: str = None,
        color: Color = None,
        loc: Location = None,
    ):
        self.obj: Union["MAssembly", Compound] = obj
        self.name: str = name
        self.color: Color = color
        self.loc: Location = loc
        self.children = []
        self.parent = None
        self.mates = {}

    def _dump(self):
        def to_string(assy, matelist, ind="") -> str:
            result = f"\n{ind}{assy}\n"
            for name in matelist.get(assy.fq_name, []):
                result += f"{ind}  - {name:15s}: mate={self.mates[name].mate} origin={self.mates[name].origin}\n"
            for c in assy.children:
                result += to_string(c, matelist, ind + "    ")
            return result

        matelist: Dict[str, List[str]] = {}
        for k, v in ((k, v.assembly) for k, v in self.mates.items()):
            if matelist.get(v) is None:
                matelist[v] = [k]
            else:
                matelist[v].append(k)

        print(to_string(self, matelist, ""))

    def add(
        self,
        obj: Union["MAssembly", Compound],
        name: str = None,
        color: Color = None,
        loc: Location = Location(),
    ):
        if isinstance(obj, Compound):
            assembly = MAssembly(obj, name, color, loc)
            assembly.parent = self
            self.add(assembly)
        elif isinstance(obj, MAssembly):
            obj.parent = self
            self.children.append(obj)
        else:
            raise ValueError(f"Type {obj} not supported")

    def traverse(self):
        for ch in self.children:
            for el in ch.traverse():
                yield el
        yield (self.name, self)

    # for compatibility reasons apply the strange keys of cadquery
    @property
    def cq_name(self):
        return self.name if self.parent is None else self.fq_name[1:].partition("/")[2]

    # proper key path across the assembly
    @property
    def fq_name(self):
        return (
            f"/{self.name}"
            if self.parent is None
            else f"{self.parent.fq_name}/{self.name}"
        )

    @property
    def top(self):
        t = self
        while t.parent is not None:
            t = t.parent
        return t

    @property
    def objects(self):
        return {assy.fq_name: assy for _, assy in self.traverse()}

    def __getitem__(self, key):
        return self.objects[key]

    def mate(self, mate_name: str, mate: Mate, origin: bool = False) -> "MAssembly":
        self.top.mates[mate_name] = MateDef(mate, self.fq_name, origin)

    def relocate(self):
        def _relocate(assembly, origins):
            origin_mate = origins.get(assembly.fq_name)
            if origin_mate is not None:
                assembly.obj = (
                    None
                    if assembly.obj is None
                    else assembly.obj.moved(origin_mate.loc.inverse())
                )
                assembly.loc = Location()
            for c in assembly.children:
                _relocate(c, origins)

        origins = {
            mate_def.assembly: mate_def.mate
            for mate_def in self.mates.values()
            if mate_def.origin
        }

        # relocate all objects
        _relocate(self, origins)

        # relocate all mates
        for mate_def in self.mates.values():
            origin_mate = origins.get(mate_def.assembly)
            if origin_mate is not None:
                mate_def.mate = mate_def.mate.moved(origin_mate.loc.inverse())

    def assemble(
        self,
        object_name: str,
        target: Union[str, Location],
    ) -> Optional["MAssembly"]:
        """
        Translate and rotate a mate onto a target mate
        :param mate: name of the mate to be assembled
        :param target: name of the target mate or a Location object to assemble the mate to
        :return: self
        """

        o_mate, o_assy = (
            self.mates[object_name].mate,
            self.objects[self.mates[object_name].assembly],
        )
        if isinstance(target, str):
            t_mate, t_assy = (
                self.mates[target].mate,
                self.objects[self.mates[target].assembly],
            )
            if o_assy.parent == t_assy.parent or o_assy.parent is None:
                o_assy.loc = t_assy.loc
            else:
                o_assy.loc = t_assy.loc * o_assy.parent.loc.inverse()
            o_assy.loc = o_assy.loc * t_mate.loc * o_mate.loc.inverse()
        else:
            o_assy.loc = target

    def __repr__(self):
        parent = None if self.parent is None else self.parent.name
        return f"MAssembly(name={self.name}, parent={parent}, color={self.color}, loc={self.loc.__repr__()}"
