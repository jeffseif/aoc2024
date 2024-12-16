import functools
import os
import typing


def expected(value: int):
    def decorator(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            if (ret := f(*args, **kwargs)) != value:
                raise ValueError(f"Expected {value=:d} but got {ret=:d}")
            else:
                return ret

        inner.__expected = value
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
