from typing import Any, Tuple, List


def to_tuple(arg: Any) -> Tuple:
    if isinstance(arg, (tuple, list)):
        return tuple(arg)
    else:
        return (arg,)


def to_list(arg: Any) -> List:
    if isinstance(arg, (tuple, list)):
        return list(arg)
    else:
        return [arg]
