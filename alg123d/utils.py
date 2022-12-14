def to_tuple(arg):
    if isinstance(arg, (tuple, list)):
        return tuple(arg)
    else:
        return (arg,)


def to_list(arg):
    if isinstance(arg, (tuple, list)):
        return list(arg)
    else:
        return [arg]
