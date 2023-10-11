#!/usr/bin/python3

#import queue
from collections import deque
import itertools

def shift(w: str, i: int) -> str:
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
    elif r[0] == "tl":
        return w[1:]
    elif r[0] == "tr":
        return w[:-1]
    elif r[0] == "al":
        return r[1] + w
    elif r[0] == "ar":
        return w + r[1]
    elif r[0] == "i":
        return shift(w, 1)
    elif r[0] == "d":
        return shift(w, -1)

def generate_replace_rules(alphabet: str, rule_lens: list[tuple[int, int]]) -> list[tuple]:
    rules = []
    for (rule_len_left, rule_len_right) in rule_lens:
        for rule_left_tuple in itertools.combinations_with_replacement(alphabet, rule_len_left):
            for rule_right_tuple in itertools.combinations_with_replacement(alphabet, rule_len_right):
                if rule_left_tuple != rule_right_tuple:
                    rules.append( ( "r", "".join([c for c in rule_left_tuple]) , "".join([c for c in rule_right_tuple])) )
    return rules

def generate_add_left_rules(alphabet: str, rule_lens: list[int]) -> list[tuple]:
    rules = []
    for rule_len in rule_lens:
        for rule in itertools.combinations_with_replacement(alphabet, rule_len):
            rules.append( ("al", "".join([c for c in rule])) )
    return rules

def generate_add_right_rules(alphabet: str, rule_lens: list[int]) -> list[tuple]:
    rules = []
    for rule_len in rule_lens:
        for rule in itertools.combinations_with_replacement(alphabet, rule_len):
            rules.append( ("ar", "".join([c for c in rule])) )
    return rules

def solve(w1: str, w2: str, rules: list[tuple], rules_repeatable: bool):
    states = deque()
    states.append( (w1, []) )

    while len(states) > 0:
        state = states.popleft()
        #print("Checking state: {}".format(state))
        for r in rules:
            if rules_repeatable or (r not in state[1]):
                w = apply_rule(state[0], r)
                if w != state[0]:
                    applied_states = state[1] + [r]

                    if w == w2:
                        print("Found solution: {}".format(applied_states))

                    states.append( (w, applied_states) )

def read_words(fn: str, do_strip: bool = False, do_lower: bool = False, alphabet: str = "") -> list[str]:
    words = []
    with open(fn, "r") as f:
        for word in f.readlines():
            word = word[:-1]
            if do_strip:
                word = word.strip()
            if do_lower:
                word = word.lower()
            if alphabet == "":
                words.append(word)
            else:
                found = True
                for c in word:
                    if c not in alphabet:
                        found = False
                        break
                if found:
                    words.append(word)
    return words

def solve_any_word(w1: str, words: list[str], rules: list[tuple], rules_repeatable: bool):
    words_found = set()
    words_found.add(w1)

    states = deque()
    states.append( (w1, []) )

    while len(states) > 0:
        state = states.popleft()
        #print("Checking state: {}".format(state))
        for r in rules:
            if rules_repeatable or (r not in state[1]):
                w = apply_rule(state[0], r)
                if w not in words_found:
                    words_found.add(w)
                    applied_states = state[1] + [r]

                    if w in words:
                        print("Found solution: {}->{} - {}".format(w1, w, applied_states))

                    states.append( (w, applied_states) )

#w1 = "apple"
#w2 = "saddle"
#alphabet = "".join(sorted(list(set(w1+w2))))
#rules = [ ("i",), ("d",), ("rr",), ("rl",) ]
#rules += generate_replace_rules(alphabet, [ (1, 1), (1, 2) ])
#solve(w1, w2, rules, False)

w1 = "apple"
alphabet = "aebplfskth"
words = read_words("words2.txt", True, True, alphabet)
rules = [ ("i",), ("d",), ("rr",), ("rl",) ]
#rules += generate_replace_rules(alphabet, [ (1, 2), (2, 1) ])
rules += generate_add_left_rules(alphabet, [1])
rules += generate_add_right_rules(alphabet, [1])
solve_any_word(w1, words, rules, False)

