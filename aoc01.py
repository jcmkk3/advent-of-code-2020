from itertools import combinations
from math import prod
from typing import Iterable


def find_combination(numbers: Iterable[int], target: int, n_combos: int = 2):
    """
    Given a list of `numbers`, returns the first combination that equals
    the `target`.
    Combinations greater than 2 can be calculated by setting `n_combos`.
    """
    combos = combinations(numbers, n_combos)
    matches = (c for c in combos if sum(c) == target)
    # Return product of only first matching combo
    return next(matches)


with open("input/aoc01.txt") as f:
    expenses = [int(line) for line in f.readlines()]

assert prod(find_combination(expenses, 2020)) == 776_064  # Solution 1
assert prod(find_combination(expenses, 2020, n_combos=3)) == 6_964_490  # Solution 2
