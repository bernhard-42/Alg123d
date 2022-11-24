import build123d as bd

from .common import AlgCompound, Step

CTX = [None, bd.BuildLine, bd.BuildSketch, bd.BuildPart]

__all__ = ["_function_wrap"]


def _function_wrap(cls, objects, ctx_add=None, mode=bd.Mode.PRIVATE, **kwargs):
    objs = objects if isinstance(objects, (list, tuple)) else [objects]

    if ctx_add is None:
        dim = max([o.dim for o in objs])
    else:
        dim = ctx_add.dim

    if mode is not None:
        kwargs["mode"] = mode

    with CTX[dim]() as ctx:
        if ctx_add is not None:
            ctx._add_to_context(bd.Compound(ctx_add.wrapped))
        compound = cls(*objs, **kwargs)

    steps = [Step(compound, compound.location, None)]  # TODO

    return AlgCompound(compound, steps, dim)
