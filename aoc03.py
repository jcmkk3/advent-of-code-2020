from typing import List, Iterable, Tuple
from math import prod


class Terrain:
    """
    A textual representation of terrain. Each row wraps, mimicing an
    endless horizontal scroll (like a classic video game).

    An individual character in the terrain can be accessed by row,
    then column (`terrain[row, col]`)

    ```
    terrain = Terrain([
        "abcd",
        "efgh",
        "ijkl"
    ])
    assert terrain[0, 2] == "c"
    assert terrain[1, 6] == "g"
    ```
    """

    def __init__(self, data=Iterable[str]):
        self._data = list(data)
        self._width = len(self._data[0])

    def __getitem__(self, coordinates: Tuple[int, int]) -> str:
        row, col = coordinates
        col = col % self._width  # Will endlessly wrap around row
        return self._data[row][col]

    def __len__(self) -> int:
        return len(self._data)


class Toboggan:
    """
    A transportation device that travels using a pre-determined
    trajectory (`angle`).

    The angle is a tuple with a slope of `(right, down)`.

    ```
    toboggan = Toboggan((3, 1)) # Right: 3, Down: 1
    ```
    """

    def __init__(self, angle: Tuple[int, int]):
        self.angle = angle

    def sled(self, terrain: Terrain) -> List[str]:
        """
        Given a `Terrain` object, will traverse the object from the top-left
        coordinate `(0, 0)` using the toboggan's angle until it reaches the
        bottom of the terrain.

        Outputs a list of the characters found at each point in the toboggan's
        journey.

        ```
        terrain = Terrain([
           "abcd",
           "efgh",
           "ijkl"
        ])
        toboggan = Toboggan((3, 1))
        assert toboggan.sled(terrain) == ["h", "k"])
        ```
        """
        right, down = self.angle
        distance = len(terrain)
        rows = range(down, distance, down)
        return [terrain[row, right * step] for step, row in enumerate(rows, 1)]


with open("input/aoc03.txt") as f:
    terrain = Terrain(l.strip() for l in f.readlines())

slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

solution1 = Toboggan((3, 1)).sled(terrain).count("#")
solution2 = prod(Toboggan().sled(terrain).count("#") for slope in slopes)

assert solution1 == 234  # Solution 1
assert solution2 == 5_813_773_056  # Solution 2
