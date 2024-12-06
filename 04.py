"""
--- Day 4: Ceres Search ---
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:


..X...
.SAMX.
.A..A.
XMAS.S
.X....
The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
Take a look at the little Elf's word search. How many times does XMAS appear?

Your puzzle answer was 2557.

--- Part Two ---
The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?

Your puzzle answer was 1854.
"""

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
