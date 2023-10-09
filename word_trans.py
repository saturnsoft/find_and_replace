#!/usr/bin/python3

def apply_rule(w: str, r: tuple) -> str:
    if r[0] == "r":
        return w.replace(r[1], r[2])
    elif r[0] == "f":
        return w[::-1]
    elif r[0] == "rl":
        return w[1:] + w[0]
    elif r[0] == "rr":
        return w[-1] + w[:-1]

w1 = "abcd"

print(apply_rule(w1, ("rr",) ))