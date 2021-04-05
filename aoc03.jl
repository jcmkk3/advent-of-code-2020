function sled(line, slope)
    i, line = line
    x, y = slope
    if y % i != 0
        return Nothing
    end
    line[(i * x) % length(line)]
end

solution1(input) = map(x -> sled(x, (3, 1)), enumerate(input))

problem_input = readlines("input/aoc03.txt")

solution1(problem_input[begin:5])
