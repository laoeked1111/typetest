
import curses

from text import generate_text
from typing_test import test

def main():
    """
    Entry point.
    """
    prompt = "Welcome to the type trainer! Select your test type:\n[1] Finite\n[2] Continuous Timed\n"
    test_type = input(prompt)

    while test_type not in ("1", "2"):
        test_type = input(prompt)

    if test_type == "1":
        num_words = 0
        while num_words <= 0:
            prompt = "Enter the number of words to use, or hit enter for default (10): "
            response = input(prompt)

            if not response:
                num_words = 10
                break

            try:
                num_words = int(response)
            except:
                pass
        target = generate_text(num_words)
        curses.wrapper(init, 1, target)
    
    elif test_type == "2":
        time_limit = 0
        while time_limit <= 0:
            prompt = "Enter the time limit in seconds, or hit enter for default (30): "
            response = input(prompt)

            if not response:
                time_limit = 30
                break
            
            try:
                time_limit = int(response)
            except:
                pass
        curses.wrapper(init, 2, time_limit)

def init(stdscr, *args) -> None:
    """
    Create the testing window and begin the test.

    Args:
        stdscr - the standard screen
        args - tuple
            args[0] gives the type of test (1 or 2)
            args[1:] gives additional information for the test
    Ret:
        None 
    """
    curses.start_color()
    curses.noecho()
    stdscr.keypad(True)

     # green for correct, red for incorrect, white for not done 
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    finite, continuous = test(stdscr)

    # finite test
    if args[0] == 1:
        finite(args[1])

    # continuous test
    elif args[0] == 2:
        continuous(args[1])

if __name__ == "__main__":
    main()