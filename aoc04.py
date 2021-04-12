import re
from collections import UserDict


def _is_valid_height(value: str) -> bool:
    """
    A number followed by either cm or in:
    - If cm, the number must be at least 150 and at most 193.
    - If in, the number must be at least 59 and at most 76
    """
    m = re.match(r"^(\d+)(cm|in)$", value)
    height, unit = m.groups()
    lo, hi = {"cm": (150, 193), "in": (59, 76)}[unit]
    return lo <= int(height) <= hi


class Passport(UserDict):
    """
    A dictionary that represents a user's passport. Contains special methods
    that can verify the validity of the passport.
    """

    validators = {
        "byr": lambda x: 1920 <= int(x) <= 2002,
        "iyr": lambda x: 2010 <= int(x) <= 2020,
        "eyr": lambda x: 2020 <= int(x) <= 2030,
        "hgt": _is_valid_height,
        "hcl": lambda x: re.fullmatch(r"#[0-9a-f]{6}", x),  # #123abc
        "ecl": lambda x: x in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
        "pid": lambda x: re.fullmatch(r"\d{9}", x),  # 000000001
    }

    @classmethod
    def from_str(cls, text: str):
        """
        Given a block of text (can be multiple lines) that represents the fields
        and values of a user's passport, returns a `Passport` dictionary.

        ```
        text = "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd"
        assert Passport.from_str(text) == {
            'ecl': 'gry', 'pid': '860033327', 'eyr': '2020', 'hcl': '#fffffd'
        }
        ```
        """
        entries = text.split()  # Splits on spaces AND new lines
        return cls(e.split(":") for e in entries)

    @property
    def has_required_fields(self) -> bool:
        "Contains all fields which are found in `validators`"
        return set(self.validators.keys()).issubset(self.keys())

    def is_valid(self, key) -> bool:
        """
        Given a `key`, returns `True` or `False` based on the truthiness
        of applying the corresponding validator function to the key's value.

        In case of any errors, returns `False`.
        """
        try:
            value = self[key]
            is_valid = self.validators[key]
            return bool(is_valid(value))
        except Exception:
            return False

    @property
    def all_valid(self) -> bool:
        "The value in each field passes the applicable rule in `validators`"
        return all(self.is_valid(key) for key in self.validators.keys())


BLANK_LINE = "\n\n"

with open("input/aoc04.txt") as f:
    passports = [Passport.from_str(s) for s in f.read().split(BLANK_LINE)]

assert sum(p.has_required_fields for p in passports) == 196  # Solution 1
assert sum(p.all_valid for p in passports) == 114  # Solution 2
