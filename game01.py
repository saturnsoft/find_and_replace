#import keyboard
from getkey import getkey

def toggle_lock(c: str) -> str:
    return "X" if c == "." else "."

word = "applepie"
lock = "." * len(word)

print(word)
print(lock)

while True:
    #c = keyboard.read_key()

    
    if c == "q":
        break
    elif c.isnumeric():
        i = ord(c[0]) - ord("0")

        l1 = lock[:i]
        l2 = toggle_lock(lock[i])
        l3 = lock[i+1:]
        
        lock = lock[:i] + toggle_lock(lock[i]) + lock[i+1:]
    
    print(word)
    print(lock)

