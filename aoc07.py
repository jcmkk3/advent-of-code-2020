import re
from typing import Tuple, Dict, Set
from collections import deque, Counter

#  ('light red', {'bright white': 1, 'muted yellow': 2})
Bag = Tuple[str, Dict[str, int]]

#  {'light red': {'bright white': 1, 'muted yellow': 2}, 'shiny silver': {'light red': 3}}
Bags = Dict[str, Dict[str, int]]


def parse_bag(text: str) -> Bag:
    """
    Given a line of text representing a bag and it's contents, will
    return a `tuple` containing the bag's names, along with a `dictionary`
    of it's contents.

    ```
    text = "light red bags contain 1 bright white bag, 2 muted yellow bags."
    assert parse_bag(text) == ('light red', {'bright white': 1, 'muted yellow': 2})
    ```
    """
    text = "1 " + text  # Add 1 to parent bag to make pattern consistent
    m = re.findall(r"(\d+) (\w+ \w+) bags?", text)
    _, color = m.pop(0)  # First match is the parent bag
    contents = {color: int(quantity) for quantity, color in m}
    return (color, contents)


def find_parents(color: str, bags: Bags) -> Set[str]:
    """
    Given a starting `color` and a dictionary of `bags`, returns a
    set of each direct or indirect parent of the starting `color`.
    """
    parents = set()
    queue = deque([color])
    while queue:
        bag = queue.pop()
        if bag in parents:
            continue
        parents.add(bag)
        queue.extend(b for b, c in bags.items() if bag in c.keys())
    return parents - {color}  # Return without original color


def find_children(color: str, bags: Bags) -> Counter:
    """
    Given a starting `color` and a dictionary of `bags`, returns a
    `Counter` of each direct child or indirect child of that bag,
    along with the total quantity of that child.
    """
    children = Counter({color: -1})  # Do not count original bag
    queue = deque([(color, 1)])
    while queue:
        color, quantity = queue.pop()
        children[color] += quantity
        contents = bags[color]
        queue.extend(
            (c, q * quantity)  # Scale bags by number of parent bags
            for c, q in contents.items()
        )
    return children


with open("input/aoc07.txt") as f:
    bags: Bags = dict(parse_bag(l) for l in f.readlines())

assert len(find_parents("shiny gold", bags)) == 335  # Solution 1
assert sum(find_children("shiny gold", bags).values()) == 2431  # Solution 2
