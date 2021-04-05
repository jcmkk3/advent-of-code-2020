using Test


function solution1(input; target=2020)
    seen = Set()
    for i in input
        need = target - i
        need in seen && return i * need
        push!(seen, i)
    end
end


function solution2(input; target=2020)
    for i in input
        need = target - i
        need = solution1(input; target=need)
        !isnothing(need) && return i * need
    end
end


problem_input = readlines("input/aoc01.txt") .|> x -> parse(Int, x)

@test solution1(problem_input) == 776_064   # Solution 1
@test solution2(problem_input) == 6_964_490 # Solution 2
