from typing import List, Set


def translate_seat_number(seat_code: str) -> int:
    """
    Given a seat code, returns the translated plane seat number.

    ```
    assert translate_seat_number("FBFBBFFRLR") == 357
    ```
    """
    t = str.maketrans("FBLR", "0101")
    binary = seat_code.translate(t)
    return int(binary, base=2)


def find_missing_seats(seats: List[int]) -> Set[int]:
    """
    Given a list of seat *numbers*, will return a set of any
    unaccounted for seats in the range.
    """
    all_seats = range(min(seats), max(seats))
    return set(all_seats).difference(seats)


with open("input/aoc05.txt") as f:
    seats = [translate_seat_number(l) for l in f.readlines()]

assert max(seats) == 915  # Solution 1
assert find_missing_seats(seats) == {699}  # Solution 2
