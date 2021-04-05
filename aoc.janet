(defn slurp-lines [path]
  (with [f (file/open path)]
    (seq [line :iterate (file/read f :line)]
      (string/trimr line "\n"))))
