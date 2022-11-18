import build123d as bd


class Location(bd.Location):
    def __init__(self, *args, **kwargs):
        if (
            len(args) == 2
            and isinstance(args[0], (tuple, bd.Vector))
            and isinstance(args[1], (tuple, bd.Rotation))
        ):
            rot = (
                bd.Rotation(*args[1]) if isinstance(args[1], (tuple, list)) else args[1]
            )
            pos = bd.Location(args[0])
            self.wrapped = (pos * rot).wrapped

        elif len(args) == 1 and isinstance(args[0], bd.Location):
            super().__init__(args[0].wrapped)

        elif len(args) == 1 and kwargs.get("angle") is not None:
            axis = kwargs.get("axis", (0, 0, 1))
            super().__init__(args[0], axis, kwargs["angle"])

        else:
            super().__init__(*args)
