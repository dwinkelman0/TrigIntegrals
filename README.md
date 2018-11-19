# Trig Integral Evaluation

    print(Integral(3, 7, 1, 5).Eval())
    #              a  b  k  n

Evaluates the integral in the format `integral {k (sin(nx))^a (cos(nx))^b dx}`. Currently only supports `a` and `b` being 0 or positive, and `k` and `n` being fractions or integers. Outputs to a string.
