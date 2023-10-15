#!/usr/bin/python3
from math import factorial
import itertools
from tqdm import tqdm

#alphabet = [ "a", "b", "c", "d" ]

#w1 = "abcd"
#w2 = "deed"

w1 = "abc"
w2 = "beepy"

(('d', 'e'), ('ab', 'bd'), ('ce', 'ep'))

# number of combinations (without replacement), that is, n! / r! / (n-r)!
def num_combinations(n, r):
    if r < n // 2:
        r = n - r
    num = 1
    for i in range(r + 1, n + 1):
        num *= i
    
    num //= factorial(n - r)
    return num

alphabet = list()
for c in w1:
    if c not in alphabet:
        alphabet.append(c)
for c in w2:
    if c not in alphabet:
        alphabet.append(c)
alphabet.sort()

alphabet_only_in_w2 = list()
for c in w2:
    if (c not in w1) and (c not in alphabet_only_in_w2):
        alphabet_only_in_w2.append(c)

rules = list()

for rule_len_left in range (1, 3):
    for rule_len_right in range (1, 3):
        for rule_left_tuple in itertools.combinations_with_replacement(alphabet, rule_len_left):
            for rule_right_tuple in itertools.combinations_with_replacement(alphabet, rule_len_right):
                if rule_left_tuple != rule_right_tuple:
                    rules.append( ( "".join([c for c in rule_left_tuple]) , "".join([c for c in rule_right_tuple])) )

for n in range(3, len(w1) + 1):
    print("Checking {} step solutions".format(n))
    
    dropped_combinations_first = 0
    dropped_combinations_last = 0
    for rules_n in tqdm(itertools.combinations(rules, n), total = num_combinations(len(rules), n)):
        
        #if "{}".format(rules_n) == "(('a', 'd'), ('b', 'c'), ('c', 'e'))":
        #    q = 1

        # if there is no rule that can be applied on w1, skip testing the combination
        found_possible_first_rule = False
        for rule in rules_n:
            if w1.find(rule[0]) >= 0:
                found_possible_first_rule = True
                break
        if not found_possible_first_rule:
            dropped_combinations_first += 1
            #print("dropped_combinations_first={}, dropped_combinations_last={}".format(dropped_combinations_first, dropped_combinations_last))
            continue
        
        # if there is no rule that replaces to one of the w2 unique characters, skip testing the combination
        found_possible_last_rule = True
        for c in alphabet_only_in_w2:
            found = False
            for rule in rules_n:
                if rule[1].find(c) >= 0:
                    found = True
                    break
            if not found:
                found_possible_last_rule = False
                break
        if not found_possible_last_rule:
            dropped_combinations_last += 1
            #print("dropped_combinations_first={}, dropped_combinations_last={}".format(dropped_combinations_first, dropped_combinations_last))
            continue
        
        
        winner_permutation_count = 0
        #print("Trying rule set: {}".format(rules_n))

        #if rules_n == (('a', 'c'), ('b', 'a'), ('c', 'd')):
        #    q = 1

        for rules_n_perm in itertools.permutations(rules_n):
            #print("Trying rule sequence: {}".format(rules_n_perm))
            w = w1

            is_win = False

            for rule in rules_n_perm:
                if w.find(rule[0]) == -1:
                    break
                w = w.replace(rule[0], rule[1])
                if w == w2:
                    is_win = True
                    break

            if is_win:
                winner_permutation_count += 1
                #print("Win" if is_win else "No win")
                #input()
                #if winner_permutation_count >= 1:
                #    break
        
        if winner_permutation_count > 0 and winner_permutation_count <= 1:
            print("Permutations: {} for {}".format(winner_permutation_count, rules_n))

#print(rules)
#print(len(rules))
#print(len(list(itertools.combinations(rules, 5))))