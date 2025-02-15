#curses is used to work on terminal
import curses
from curses import wrapper 
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the speed Typing test", curses.color_pair(3))
    stdscr.addstr("\nPress any key to begin\n")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(5,0,f"WPM: {wpm}", curses.color_pair(3))
    for i,char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
             color = curses.color_pair(2)     

        row = i // curses.COLS # COLS give the number of column(text) present on screen. This gives the number of complete rows
        col = i % curses.COLS # this ensures that when line ends it starts with 0 again.
        stdscr.addstr(row, col, char, color) 

def load_text(key,stdscr):
    if ord(key) == 49: 
        with open('easy-text.txt','r') as f:
             lines = f.readlines()
             return random.choice(lines).strip()
    elif ord(key) == 50:
          with open('medium-text.txt','r') as f:
             lines = f.readlines()
             return random.choice(lines).strip()
    elif ord(key) == 51:
          with open('hard-text.txt','r') as f:
             lines = f.readlines()
             return random.choice(lines).strip()
    elif ord(key) == 52 :
          with open('advance-text.txt','r') as f:
             lines = f.readlines()
             return random.choice(lines).strip()
    else:
         return stdscr.addstr('enter a valid choice\n')

     
def difficulty_level(stdscr):
     stdscr.addstr('Choose your difficulty level\n')
     stdscr.addstr('1. Easy\n2. Medium\n3. Hard\n4. Advance\n')
     stdscr.addstr('Enter Your Choice option: ')
     stdscr.refresh()
     key = stdscr.getkey()
     return key
    


def wpm_test(stdscr):
    target_text = load_text(difficulty_level(stdscr),stdscr)
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)
    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round( (len(current_text) / (time_elapsed / 60)) / 5)
        stdscr.clear()
        display_text(stdscr, target_text, current_text,wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
             stdscr.nodelay(False)
             break
        

        try:
            key = stdscr.getkey()
        except:
             continue
        
        #Word is the ordinal value of that key which is the ASCII code to represent that key
        # 27 represent the escape key
        if ord(key) == 27:
            break
        
        #making backspace to work and the given value below is different representation of backspace
        if key in ("KEY_BACKSPACE", '\b', '\x7f'):
                if len(current_text) > 0:
                     current_text.pop()
        elif len(current_text)< len(target_text):
             current_text.append(key)
                     


# stdscr -> standard screens
def main(stdscr):
    #styling terminal
    #init_pair makes pair of foreground and background where an integer represents its ID
    #curses.init_pair(ID, Foreground, Background)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    #----------------------SCREEN PART-----------------------
    start_screen(stdscr)
    
    while True:
        wpm_test(stdscr)
        stdscr.addstr(3,0, "You completed the text! Press any key to continue...")
        stdscr.addstr(4,0, "Press Escape to exit program...")
        key = stdscr.getkey()
        if ord(key)== 27:
             break
    return
wrapper(main)
