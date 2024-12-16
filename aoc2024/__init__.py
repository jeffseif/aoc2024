import functools
import os
import typing


def expects(expected: int):
    def decorator(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            if (ret := f(*args, **kwargs)) != expected:
                raise ValueError(f"{expected=:d} but got {ret=:d} instead")
            else:
                return ret

        inner.__expected = expected
        return inner

    return decorator


DO_SLOW_TASKS_ENVVAR = "DO_SLOW_TASKS"


def skip_slow(f):
    if os.environ.get(DO_SLOW_TASKS_ENVVAR) == "1":
        return f
    else:

        def inner(*args, **kwargs) -> str:
            return f.__expected

        return inner


def count(it: typing.Iterable) -> int:
    count = 0
    for _ in it:
        count += 1
    return count
