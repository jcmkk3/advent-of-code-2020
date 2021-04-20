from collections import deque
from itertools import accumulate, combinations, islice
from typing import Iterator, List, Tuple, TypeVar

T = TypeVar


def split(iterator: Iterator[T], index: int) -> Tuple[Iterator[T], Iterator[T]]:
    return islice(iterator, 0, index), islice(iterator, index, None)


def sliding(iterator: Iterator[T], window_size: int = 2) -> Iterator[Iterator[T]]:
    first_window, rest = split(iterator, window_size)
    window = deque(first_window, maxlen=window_size)
    yield iter(window)
    for item in rest:
        window.append(item)
        yield iter(window)


def growing(iterator: Iterator[T]) -> Iterator[List[T]]:
    iterator = list(iterator)
    for i, _ in enumerate(iterator):
        yield iterator[:i]


class DataPort:
    def __init__(self, numbers: Iterator[int], preamble_length: int = 25):
        self._numbers = list(numbers)
        self.preamble_length = preamble_length

    def __iter__(self) -> List[int]:
        return iter(self._numbers)

    def __getitem__(self, key):
        return self._numbers[key]

    @staticmethod
    def is_valid(number: int, numbers: Iterator[int]) -> bool:
        return any(number == sum(combo) for combo in combinations(numbers, 2))

    def first_invalid(self) -> int:
        numbers = self[self.preamble_length :]
        windows = sliding(self, window_size=self.preamble_length)
        return next(n for n, w in zip(numbers, windows) if not self.is_valid(n, w))

    def encryption_weakness(self) -> int:
        target = self.first_invalid()
        for i, _ in enumerate(self):
            window = growing(self[i:])
            largest = max(n for n in window if sum(n) <= target)
            if sum(largest) == target:
                return min(largest) + max(largest)


with open("input/aoc09.txt") as f:
    data = DataPort(int(l) for l in f.readlines())

assert data.first_invalid() == 104054607  # Solution 1
assert data.encryption_weakness() == 13935797  # Solution 2
