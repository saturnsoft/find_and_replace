import curses

def toggle_lock(c: str) -> str:
    return "X" if c == "." else "."

def add_char(w: str, i: int) -> str:
    ww = ""
    for c in w:
        ww += chr(((ord(c) - ord("a") + i) % 26) + ord("a"))
    return ww

theword = "bear"

word = theword
lock = "." * len(word)

window = curses.initscr()
curses.noecho()
window.keypad(True)
curses.curs_set(0)

while True:
    k = window.get_wch()

    if type(k) == str:
        if k == "q":
            break
        elif k.isnumeric():
            i = ord(k[0]) - ord("0")
            lock = lock[:i] + toggle_lock(lock[i]) + lock[i+1:]
        elif k == "a":
            word = word[1:] + word[0]
        elif k == "d":
            word = word[-1] + word[:-1]
        elif k == "w":
            w = ""
            for i, c in enumerate(word):
                if lock[i] != "X":
                    w += add_char(c, 1)
                else:
                    w += c
            word = w
        elif k == "s":
            w = ""
            for i, c in enumerate(word):
                if lock[i] != "X":
                    w += add_char(c, -1)
                else:
                    w += c
            word = w
        elif k == "r":
            word = theword

    window.addstr(1, 1, word)
    window.addstr(2, 1, lock)

