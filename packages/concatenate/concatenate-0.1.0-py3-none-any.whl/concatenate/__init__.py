import math
import typing

import registrate

T = typing.TypeVar('T')

register = registrate.Register(lambda type: type)

@register(int)
def concatenate_int(a: int, b: int, /, *, base: int = 10) -> int:
    return a * base ** math.ceil(math.log(b, base)) + b

@register(set)
def concatenate_set(a: set, b: set) -> set:
    return a | b

@register(dict)
def concatenate_dict(a: dict, b: dict) -> dict:
    return {**a, **b}

@register(str)
def concatenate_str(a: str, b: str) -> str:
    return a + b

@register(list)
def concatenate_list(a: list, b: list) -> list:
    return [*a, *b]

@register(tuple)
def concatenate_tuple(a: tuple, b: tuple) -> tuple:
    return (*a, *b)

def concatenate(a: T, b: T, **kwargs) -> T:
    if type(a) != type(b):
        raise AttributeError('a and b must be of the same type')

    map = {value: key for key, value in register.items()}

    typ = type(a)

    if typ not in map:
        raise Exception('Type not supported') # NOTE: Default to a + b?

    return map[typ](a, b, **kwargs)
