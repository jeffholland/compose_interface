from math import log

def p_to_f(p, f1, f2, f3):
    return pow(f1, ((p - 69) / f2)) * f3

def f_to_p(fq, f1, f2, f3):
    return (f2 * log((fq / f3), f1)) + 69