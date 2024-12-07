import functools
import itertools
import re
import typing


def iter_pattern_one(width: int) -> typing.Iterator[str]:
    for delimeter in (
        # HORIZONTAL
        "",
        # RIGHT
        f".{{{2 * width:d}}}",
        # EVEN
        f".{{{2 * width - 1:d}}}",
        # LEFT
        f".{{{2 * width - 2:d}}}",
    ):
        yield delimeter.join("XMAS")
        yield delimeter.join("SAMX")


def iter_re_overlapping(
    pattern: str,
    string: str,
) -> typing.Iterator[str]:
    pat = re.compile(pattern=pattern)
    idx = 0
    while True:
        if (match := pat.search(string=string[idx:])) is None:
            return
        else:
            idx += match.start() + 1
            yield match.group()


def count(it: typing.Iterable) -> int:
    count = 0
    for _ in it:
        count += 1
    return count


def part_one(path_to_input: str, width: int) -> int:
    with open(file=path_to_input) as f:
        payload = f.read()

    finditer = functools.partial(
        iter_re_overlapping,
        string=(" " * width).join(payload.splitlines()),
    )
    return count(itertools.chain(*map(finditer, iter_pattern_one(width=width))))


def iter_pattern_two(width: int) -> typing.Iterator[str]:
    middle = f"{{{2 * width - 2:d}}}A.{{{2 * width - 3:d}}}"
    for a, b, c, d in (
        # RIGHT
        ("M", "S", "M", "S"),
        # DOWN
        ("M", "M", "S", "S"),
        # LEFT
        ("S", "M", "S", "M"),
        # UP
        ("S", "S", "M", "M"),
    ):
        yield ".".join((a, b, middle, c, d))


def part_two(path_to_input: str, width: int) -> int:
    with open(file=path_to_input) as f:
        payload = f.read()
    finditer = functools.partial(
        iter_re_overlapping,
        string=(" " * width).join(payload.splitlines()),
    )
    return count(itertools.chain(*map(finditer, iter_pattern_two(width=width))))


def main() -> int:
    print(part_one(path_to_input="04.input", width=140))
    print(part_two(path_to_input="04.input", width=140))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
