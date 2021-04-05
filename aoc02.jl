using Test


function parse_line(text)
    m = match(r"^(\d+)-(\d+) (\w): (\w+)$", text)
    lo, hi, char, password = m.captures
    (lo = parse(Int, lo), hi = parse(Int, hi), char = first(char), password)
end


is_valid_password1(p) = p.lo <= count(==(p.char), p.password) <= p.hi
is_valid_password2(p) = xor(p.password[p.lo] == p.char, p.password[p.hi] == p.char)


problem_input = readlines("input/aoc02.txt") .|> parse_line

@test sum(is_valid_password1.(problem_input)) == 416 # Solution 1
@test sum(is_valid_password2.(problem_input)) == 688 # Solution 2
