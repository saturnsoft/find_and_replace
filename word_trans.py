#!/usr/bin/python3

#import queue
from collections import deque

def shift(w, i):
    ww = ""
    for c in w:
        ww += chr(((ord(c) - ord("a") + i) % 26) + ord("a"))
    return ww

def apply_rule(w: str, r: tuple) -> str:
    if r[0] == "r":
        return w.replace(r[1], r[2])
    elif r[0] == "f":
        return w[::-1]
    elif r[0] == "rl":
        return w[1:] + w[0]
    elif r[0] == "rr":
        return w[-1] + w[:-1]
    elif r[0] == "i":
        return shift(w, 1)
    elif r[0] == "d":
        return shift(w, -1)

w1 = "abcdz"
w2 = "bcde"

rules = [ ("i",), ("rr",), ("r","za","a") ]

states = deque()

states.append( (w1, []) )

while len(states) > 0:
    state = states.popleft()
    print("Checking state: {}".format(state))
    for r in rules:
        if r not in state[1]:
            w = apply_rule(state[0], r)
            applied_states = state[1] + [r]

            if w == w2:
                print("Found solution: {}".format(applied_states))

            states.append( (w, applied_states) )

#print(apply_rule(w1, ("d",) ))