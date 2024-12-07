import argparse
import pathlib
import importlib
import os
import types
import typing

import aoc2024


def iter_day_module() -> typing.Iterator[tuple[int, types.ModuleType]]:
    for path in pathlib.Path(__file__).parent.glob("day*.py"):
        name = path.with_suffix("").name
        _, _, day = name.partition("day")
        yield int(day), importlib.import_module(name=f"aoc2024.{name:s}")


def run_module(day: int, module: types.ModuleType) -> None:
    print(f"> Day {day:d}")
    path_to_input = str(pathlib.Path(__file__).parent / f"input{day:02d}.txt")
    for task in (module.part_one, module.part_two):
        print(task(path_to_input=path_to_input))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--do-slow-tasks", action="store_true")
    parser.add_argument("--day", action="append", default=[], type=int)
    args = parser.parse_args()

    if args.do_slow_tasks:
        os.environ[aoc2024.DO_SLOW_TASKS_ENVVAR] = "1"
    day_to_module = dict(iter_day_module())
    for day in sorted(args.day or day_to_module):
        run_module(
            day=day,
            module=day_to_module[day],
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
