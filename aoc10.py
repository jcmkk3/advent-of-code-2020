from collections import Counter, OrderedDict
from itertools import tee
from typing import Iterable


#  Vendored from python itertools documentation. Will be included in 3.10 standard library.
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class Adapters:
    def __init__(self, joltages: Iterable[int]):
        joltages = list(joltages)
        self.device_joltage = max(joltages) + 3
        # outlet + adapters + device
        self._joltages = sorted([0] + joltages + [self.device_joltage])

    def __iter__(self):
        return iter(self._joltages)

    def differences(self) -> Counter:
        return Counter(curr - prev for prev, curr in pairwise(self))

    def n_combinations(self) -> int:
        joltages = Counter(self)
        for jolt in range(1, self.device_joltage + 1):
            prev_combos = sum(
                joltages[jolt - step] for step in [1, 2, 3] if jolt - step >= 0
            )
            joltages[jolt] = prev_combos * joltages[jolt]
        return joltages[self.device_joltage]


with open("input/aoc10.txt") as f:
    adapters = Adapters(int(l) for l in f.readlines())

differences = adapters.differences()
assert differences[1] * differences[3] == 2346  # Solution 1
assert adapters.n_combinations() == 6_044_831_973_376  # Solution 2
