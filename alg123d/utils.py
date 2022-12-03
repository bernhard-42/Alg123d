def tupleize(arg):
    if isinstance(arg, (tuple, list)):
        return tuple(arg)
    else:
        return (arg,)
