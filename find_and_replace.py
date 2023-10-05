import itertools

#alphabet = [ "a", "b", "c", "d" ]

w1 = "abcd"
w2 = "deed"

alphabet = list()
for c in w1:
    if c not in alphabet:
        alphabet.append(c)
for c in w2:
    if c not in alphabet:
        alphabet.append(c)
alphabet.sort()

rules = list()

for rule_len_left in range (1, 2):
    for rule_len_right in range (1, 2):
        for rule_left_tuple in itertools.combinations_with_replacement(alphabet, rule_len_left):
            for rule_right_tuple in itertools.combinations_with_replacement(alphabet, rule_len_right):
                if rule_left_tuple != rule_right_tuple:
                    rules.append( ( "".join([c for c in rule_left_tuple]) , "".join([c for c in rule_right_tuple])) )

for n in range(1, len(w1) + 1):
    print("Checking {} step solutions".format(n))
    
    for rules_n in itertools.combinations(rules, n):
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
                if winner_permutation_count > 5:
                    break
        
        if winner_permutation_count > 0 and winner_permutation_count <= 5:
            print("Permutations: {} for {}".format(winner_permutation_count, rules_n))

#print(rules)
#print(len(rules))
#print(len(list(itertools.combinations(rules, 5))))