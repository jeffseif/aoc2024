import os
import typing

DO_SLOW_TASKS_ENVVAR = "DO_SLOW_TASKS"


def skip_slow(f):
    if os.environ.get(DO_SLOW_TASKS_ENVVAR) == "1":
        return f
    else:

        def inner(*args, **kwargs) -> str:
            return "<SKIPPED>"

        return inner


def count(it: typing.Iterable) -> int:
    count = 0
    for _ in it:
        count += 1
    return count
