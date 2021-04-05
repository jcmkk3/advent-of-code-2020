from functools import reduce
from typing import Iterator, Set


class CustomsForm:
    """
    A form containing `answers` for all members of a traveling group.
    Each item in `answers` contains the textual representation of the
    questions in which the member answered "yes".
    """

    def __init__(self, answers: Iterator[str]):
        self.answers = list(answers)

    @classmethod
    def from_str(cls, text: str):
        """
        Given a block of text that represents the answers of a group,
        creates a `CustomsForm` using those answers.

        ```
        text = '''ab
        abc
        bcd'''
        assert CustomsForm.from_str(text) == CustomsForm(['ab', 'abc', 'bcd'])
        ```
        """
        return cls(s.strip() for s in text.splitlines())

    @property
    def any_answered(self) -> Set[str]:
        """
        Returns a set of each question that any member of the group
        answered at least one time.

        ```
        form = CustomsForm(['ab', 'abc', 'abcd'])
        assert form.any_answerd == {'a', 'b', 'c', 'd'}
        ```
        """
        return reduce(set.union, self.answers, set())

    @property
    def all_answered(self) -> Set[str]:
        """
        Returns a set of each question that all members of the group
        answered.

        ```
        form = CustomsForm(['ab', 'abc', 'abcd'])
        assert form.all_answerd == {'a', 'b'}
        ```
        """
        return reduce(set.intersection, self.answers, self.any_answered)


with open("input/aoc06.txt") as f:
    forms = [CustomsForm.from_str(l) for l in f.read().split("\n\n")]

assert sum(len(f.any_answered) for f in forms) == 6506  # Solution 1
assert sum(len(f.all_answered) for f in forms) == 3243  # Solution 2
