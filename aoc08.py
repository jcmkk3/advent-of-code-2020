from typing import Iterable, NamedTuple


class Instruction(NamedTuple):
    """
    A single program instruction. Includes an operation to perform
    and an argument specifying the magnitude of that operation.
    """
    op: str
    arg: int

    @classmethod
    def from_line(cls, text: str):
        op, arg = text.split()
        return cls(op, int(arg))


Program = Iterable[Instruction]


class Exit(NamedTuple):
    """
    The result upon exiting after running a program. Provides the
    final `accumulator` value, along with a status to describe the run.
    """
    status: str
    accumulator: int


class GameConsole:
    """
    A game console! Given a program, provides the means to `run`
    said program.
    """

    def __init__(self, program: Program):
        self._program = list(program)

    def __getitem__(self, key: int):
        # Make indexing start at 1 instead of 0
        return self._program[key - 1]

    def __len__(self):
        return len(self._program)

    def run(self) -> Exit:
        """
        Using the `GameConsole` program, will run each instruction, then
        return the result (`Exit`) of the completed program.
        """
        line_number = 1
        accumulator = 0
        visited = set()
        while 1 <= line_number <= len(self):
            if line_number in visited:
                return Exit("Infinite Loop", accumulator)

            visited.add(line_number)
            op, arg = self[line_number]

            if op == "acc":
                accumulator += arg
                line_number += 1
            elif op == "jmp":
                line_number += arg
            elif op == "nop":
                line_number += 1
            else:
                return Exit("Invalid Operation", accumulator)

        return Exit("Success", accumulator)


def mutate_instructions(program: Program) -> Program:
    """
    Given a `program`, returns a generator that will eventually
    yield each variation of the program by swaping the `operation`
    of a single line in each result.
    """
    swap = {"jmp": "nop", "nop": "jmp"}
    for idx, line in enumerate(program):
        op, arg = line
        if op not in swap:
            continue
        mutated = program.copy()
        mutated[idx] = Instruction(swap[op], arg)
        yield mutated


def fix_program(program: Program) -> Program:
    """
    Given a program, runs every mutation of the program until
    it finds a version that finishes successfully. Returns the
    successful program.
    """
    mutations = mutate_instructions(program)
    for mutated_program in mutations:
        exit = GameConsole(mutated_program).run()
        if exit.status == "Success":
            return mutated_program


with open("input/aoc08.txt") as f:
    program = [Instruction.from_line(l) for l in f.readlines()]

assert GameConsole(program).run().accumulator == 1949  # Solution 1

fixed_program = fix_program(program)
assert GameConsole(fixed_program).run().accumulator == 2092  # Solution 2
