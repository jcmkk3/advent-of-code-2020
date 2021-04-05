(use aoc)


(defn solution1 [input]
  (-> (seq [i :in input
            j :in input
            :when (= 2020 (+ i j))]
         (* i j))
       first))


(defn solution2 [input]
  (-> (seq [i :in input
            j :in input
            k :in input
            :when (= 2020 (+ i j k))]
         (* i j k))
       first))


(def problem-input (->> (slurp-lines "input/aoc01.txt")
                        (map scan-number)))

(assert (= 776_064   (solution1 problem-input))) # Solution 1
(assert (= 6_964_490 (solution2 problem-input))) # Solution 2
