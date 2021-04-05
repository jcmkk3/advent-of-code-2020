import re
from typing import NamedTuple


class PasswordRecord(NamedTuple):
    "A record representing the password and policy parameters for a user"

    lo: int
    hi: int
    letter: str
    password: str

    @classmethod
    def from_line(cls, line: str):
        """
        Given a `line` that represents an entry in the password database
        will return a `PasswordRecord`.

        ```
        assert parse_line("1-3 a: abcde") == PasswordRecord(
            lo=1, hi=3, letter='a', password='abcde'
        )
        ```
        """
        m = re.match(r"^(\d+)-(\d+) (\w): (\w+)$", line)
        lo, hi, letter, password = m.groups()
        return cls(int(lo), int(hi), letter, password)

    @property
    def is_valid1(self) -> bool:
        """
        The password policy indicates the lowest and highest number of
        times a given letter must appear for the password to be valid.
        """
        lo, hi, letter, password = self
        return lo <= password.count(letter) <= hi

    @property
    def is_valid2(self) -> bool:
        """
        The password policy describes two positions in the password, where
        1 means the first character, 2 means the second character. *Exactly*
        one of these positions must contain the given letter.
        """
        lo, hi, letter, password = self
        lo, hi = lo - 1, hi - 1  # Account for zero index
        return (password[lo] == letter) ^ (password[hi] == letter)


with open("input/aoc02.txt") as f:
    passwords = [PasswordRecord.from_line(l) for l in f.readlines()]

assert sum(p.is_valid1 for p in passwords) == 416  # Solution 1
assert sum(p.is_valid2 for p in passwords) == 688  # Solution 2
