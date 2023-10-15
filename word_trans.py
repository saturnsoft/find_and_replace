#!/usr/bin/python3

#import queue
from collections import deque
import itertools
import enum
from datetime import datetime

class Operation(enum.Enum):
    REP = 1
    FLP = 2
    ROL = 3
    ROR = 4
    SHL = 5
    SHR = 6
    ADL = 7
    ADR = 8
    INC = 9
    DEC = 10

def add_char(w: str, i: int) -> str:
    ww = ""
    for c in w:
        ww += chr(((ord(c) - ord("a") + i) % 26) + ord("a"))
    return ww

def apply_rule(w: str, r: tuple) -> str:
    if r[0] == Operation.REP:
        return w.replace(r[1], r[2])
    elif r[0] == Operation.FLP:
        return w[::-1]
    elif r[0] == Operation.ROL:
        return w[1:] + w[0]
    elif r[0] == Operation.ROR:
        return w[-1] + w[:-1]
    elif r[0] == Operation.SHL:
        return w[1:]
    elif r[0] == Operation.SHR:
        return w[:-1]
    elif r[0] == Operation.ADL:
        return r[1] + w
    elif r[0] == Operation.ADR:
        return w + r[1]
    elif r[0] == Operation.INC:
        return add_char(w, 1)
    elif r[0] == Operation.DEC:
        return add_char(w, -1)
    else:
        return w

def format_rule(r: tuple) -> str:
    return r[0].name + ("" if len(r) == 1 else " ") + " ".join(r[1:])

def format_rules(rules: list[tuple]) -> str:
    return ", ".join( [ format_rule(r) for r in rules ] )

def generate_one_param_rules(op: Operation, alphabet: str, rule_lens: list[int]) -> list[tuple]:
    rules = []
    for rule_len in rule_lens:
        for rule in itertools.combinations_with_replacement(alphabet, rule_len):
            rules.append( (op, "".join([c for c in rule])) )
    return rules

def generate_two_param_rules(op: Operation, alphabet: str, rule_lens: list[tuple[int, int]]) -> list[tuple]:
    rules = []
    for (rule_len_left, rule_len_right) in rule_lens:
        for rule_left_tuple in itertools.combinations_with_replacement(alphabet, rule_len_left):
            for rule_right_tuple in itertools.combinations_with_replacement(alphabet, rule_len_right):
                if rule_left_tuple != rule_right_tuple:
                    rules.append( ( op, "".join([c for c in rule_left_tuple]) , "".join([c for c in rule_right_tuple])) )
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

def check_unique_solution(w1: str, w2: str, rules: list[tuple]) -> bool:
    solution_num = 0
    for rules_perm in itertools.permutations(rules):
        w = w1
        for rule in rules_perm:
            w = apply_rule(w, rule)
        if w == w2:
            solution_num += 1
        if solution_num >= 2:
            break
    return solution_num == 1

def solve_any_word(w1: str, words: list[str], rules: list[tuple], rules_repeatable: bool):
    words_found = set()
    words_found.add(w1)

    states = deque()
    states.append( (w1, []) )

    state_processed = 0
    last_print_time = datetime.now()

    while len(states) > 0:
        t = datetime.now()
        if (t - last_print_time).seconds > 5:
            print("States processed: {}, states in queue: {}".format(state_processed, len(states)))
            last_print_time = t
        
        state = states.pop()
        #print("Checking state: {}".format(state))
        for r in rules:
            if rules_repeatable or (r not in state[1]):
                w = apply_rule(state[0], r)
                if w not in words_found:
                    words_found.add(w)
                    applied_rules = state[1] + [r]

                    if w in words:
                        unique_solution = check_unique_solution(w1, w, applied_rules)
                        if unique_solution:
                            print("Found {}unique solution of {}: {}->{} - {}".format("" if unique_solution else "NOT ", len(applied_rules), w1, w, format_rules(applied_rules)))

                    states.append( (w, applied_rules) )
        state_processed += 1
    print("States processed: {}".format(state_processed))

#w1 = "apple"
#w2 = "saddle"
#alphabet = "".join(sorted(list(set(w1+w2))))
#rules = [ (Operation.INC,), (Operation.DEC,), (Operation.ROR,), (Operation.ROL,) ]
#rules += generate_two_param_rules(Operation.REP, alphabet, [ (1, 1), (1, 2) ])
#solve(w1, w2, rules, False)

w1 = "apple"
alphabet = "iosth"
#alphabet = "aeioubplfskth"
words = read_words("words2.txt", True, True, alphabet)
rules1 = [ (Operation.INC,), (Operation.DEC,), (Operation.ROR,), (Operation.ROL,), (Operation.SHR,), (Operation.SHL,) ]
#rules += generate_two_param_rules(Operation.REP,alphabet, [ (1, 2), (2, 1) ])

rules2 = generate_one_param_rules(Operation.ADL, alphabet, [1])
rules2 += generate_one_param_rules(Operation.ADR, alphabet, [1])
solve_any_word(w1, words, rules1 + rules2, False)

