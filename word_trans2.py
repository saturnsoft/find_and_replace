#!/usr/bin/python3

#import queue
from collections import deque
import itertools
import enum
from datetime import datetime
from math import factorial
from tqdm import tqdm

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

def apply_rule(w: str, r: tuple) -> tuple[str, tuple]:
    ww = w
    rr = None

    if r[0] == Operation.REP:
        ww = w.replace(r[1], r[2])
        rr = Operation.REP, r[2], r[1]
    elif r[0] == Operation.FLP:
        ww = w[::-1]
        rr = Operation.FLP,
    elif r[0] == Operation.ROL:
        ww = w[1:] + w[0]
        rr = Operation.ROR,
    elif r[0] == Operation.ROR:
        ww = w[-1] + w[:-1]
        rr = Operation.ROL,
    elif r[0] == Operation.SHL:
        ww = w[1:]
        rr  = Operation.ADL, w[0]
    elif r[0] == Operation.SHR:
        ww = w[:-1]
        rr = Operation.ADR, w[-1]
    elif r[0] == Operation.ADL:
        ww = r[1] + w
        rr = Operation.SHL,
    elif r[0] == Operation.ADR:
        ww = w + r[1]
        rr = Operation.SHR,
    elif r[0] == Operation.INC:
        ww = add_char(w, 1)
        rr = Operation.DEC,
    elif r[0] == Operation.DEC:
        ww = add_char(w, -1)
        rr = Operation.INC,
    return ww, rr

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

def check_solution_num(w1: str, w2: str, rules: list[tuple], max_solution_num: int) -> bool:
    words = set()
    
    solution_num = 0
    for rules_perm in itertools.permutations(rules):
        w = w1
        for rule in rules_perm:
            words.add(w)
            w, _ = apply_rule(w, rule)
        if w == w2:
            solution_num += 1
        if w in words:
            solution_num = 0
            break
        if solution_num > max_solution_num:
            break
    return solution_num > 0 and solution_num <= max_solution_num

# number of combinations (without replacement), that is, n! / r! / (n-r)!
def num_combinations(n, r):
    if r < n // 2:
        r = n - r
    num = 1
    for i in range(r + 1, n + 1):
        num *= i
    
    num //= factorial(n - r)
    return num

# fun starts here...................................

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
                        unique_solution = check_solution_num(w1, w, applied_rules)
                        if unique_solution:
                            print("Found {}unique solution of {}: {}->{} - {}".format("" if unique_solution else "NOT ", len(applied_rules), w1, w, format_rules(applied_rules)))

                    states.append( (w, applied_rules) )
        state_processed += 1
    print("States processed: {}".format(state_processed))



def find_puzzle(w1: str, rule_num: int, rules: list[tuple]):
    for rules_sel in tqdm(itertools.combinations(rules, rule_num), total=num_combinations(len(rules), rule_num)):
        for rules_sel_perm in itertools.permutations(rules_sel):

            w2 = w1
            rules_rev = []
            for rule in rules_sel_perm:
                w2, rule_rev = apply_rule(w2, rule)
                rules_rev.append(rule_rev)
            rules_rev.reverse()

            if check_solution_num(w2, w1, rules_rev, 8192):
                print("Found unique solution of {}: {}->{} - {}".format(len(rules_rev), w2, w1, format_rules(rules_rev)))


w1 = "apple"
#alphabet = "iosth"
#alphabet = "aeioubplfskth"
#rules1 = [ (Operation.INC,), (Operation.DEC,), (Operation.ROR,), (Operation.ROL,), (Operation.SHR,), (Operation.SHL,) ]
rules1 = [ (Operation.INC,), (Operation.DEC,), (Operation.ROR,), (Operation.ROL,), (Operation.SHL,) ]
#rules += generate_two_param_rules(Operation.REP,alphabet, [ (1, 2), (2, 1) ])

rules2 = generate_one_param_rules(Operation.ADL, w1, [1])
#rules2 += generate_one_param_rules(Operation.ADR, w1, [1])

find_puzzle(w1, 6, rules1 + rules2)
