#!/usr/bin/python3

# ▒▒▒▒▒▒▒▒▒
# ▒5▒2▒1▒5▒
# ▒6233236▒
# ▒7▒4▒3▒7▒
# ▒▒▒▒▒▒▒▒▒

from collections import deque
import curses
from random import randint

symbols = "01234567"
sn = len(symbols)
theword = deque([0, 0, 0, 0, 0, 0, 0, 0])
word = theword
wn = len(word)
lock = [False] * len(word)

window = curses.initscr()
curses.noecho()
window.keypad(True)
curses.curs_set(False)

def refresh_screen():
    for i in range(0, wn):
        if lock[i]:
            window.addstr(1, 1 + i, "▒")
            window.addstr(3, 1 + i, "▒")
        else:
            window.addstr(1, 1 + i, symbols[(word[i] - 1) % sn])
            window.addstr(3, 1 + i, symbols[(word[i] + 1) % sn])
    
    for i in range(0, wn):
        window.addstr(2, 1 + i, symbols[word[i]])

def init_screen():
    window.addstr(0, 0, "▒" * (len(word) + 2))
    window.addstr(4, 0, "▒" * (len(word) + 2))

    for i in range(0, 3):
        window.addstr(1 + i, 0, "▒")
        window.addstr(1 + i, len(word) + 1, "▒")
   
    refresh_screen()

def process_cursor_key(k: str):
    global word
    if k == "a":
        word.rotate(-1)
    elif k == "d":
        word.rotate(1)
    elif k == "w":
        w = deque()
        for i in range(0, wn):
            if not lock[i]:
                w.append((word[i] + 1) % sn)
            else:
                w.append(word[i])
        word = w
    elif k == "s":
        w = deque()
        for i in range(0, wn):
            if not lock[i]:
                w.append((word[i] - 1) % sn)
            else:
                w.append(word[i])
        word = w


cursor_keys = "adws"
init_screen()

while True:
    k = window.get_wch()

    if type(k) == str:
        if k == "q":
            break
        elif k.isnumeric():
            i = min(ord(k[0]) - ord("0"), wn - 1)
            lock = lock[:i] + [ not lock[i] ] + lock[i+1:]
        elif k == "r":
            word = theword
        elif k == "x":
            for _ in range(0, 4):
                x = randint(0, 3)
                process_cursor_key(cursor_keys[x])
        else:
            process_cursor_key(k)

    
    refresh_screen()
