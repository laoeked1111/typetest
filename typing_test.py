
import time
import curses
from colorama import Fore, Style

from text import generate_text

def finite_test(stdscr, target: list[str]) -> None:
    """
    Conduct a test of a finite number of words. Prints WPM and accuracy at the end.

    WPM is calculated as the number of characters typed divided by 5, 
        divided by the number of minutes elapsed.

    Args:
        stdscr - the standard screen
        target - the list of words that must be typed
    Ret:
        None
    """

    # hide the cursor before test begins
    curses.curs_set(0)

    stdscr.clear()
    intro_msg = "Type the following as quickly as possible: "
    target_text = " ".join(target)
    stdscr.addstr(0, 0, intro_msg)
    stdscr.addstr(1, 0, target_text)
    stdscr.addstr(3, 0, "Time: 0.00 s")
    stdscr.refresh()

    stdscr.nodelay(False)

    start = None
    typed_chars = []
    position = 0

    # accuracy metric
    num_incorrect = 0
    num_typed = 0

    while position < len(target_text):
        if start is None:
            stdscr.nodelay(False) # block if haven't started
        else:
            stdscr.nodelay(True)

        key = stdscr.getch()

        if start is None:
            start = time.time()

        if key in (8, 127): # backspace or delete
            if position > 0:
                position -= 1
                typed_chars.pop()
        elif (65 <= key <= 90) or (97 <= key <= 122) or (key == 32): # only accepting letters and space
            this_char = chr(key)
            typed_chars.append(this_char)
            position += 1
            num_typed += 1 # not including backspaces
            if this_char != target_text[len(typed_chars) - 1]:
                num_incorrect += 1

        # TODO: prevent copy paste capability

        stdscr.clear()
        stdscr.move(0, 0)
        stdscr.addstr(intro_msg)

        stdscr.move(1, 0)
        for i, char in enumerate(target_text):
            if i < len(typed_chars):
                if typed_chars[i] == char:
                    stdscr.addstr(char, curses.color_pair(1)) # correct
                else:
                    stdscr.addstr(typed_chars[i], curses.color_pair(2)) # incorrect
            else:
                stdscr.addstr(char) # default
        
        stdscr.move(3, 0)
        stdscr.addstr(f"Time: {time.time() - start:.2f} s")

        stdscr.clrtoeol()
        stdscr.refresh()

    elapsed_time = time.time() - start
    accuracy = round(100 - 100 * num_incorrect / num_typed)
    raw_wpm = round(num_typed / 5 / (elapsed_time / 60))
    actual_wpm = round(((num_typed - num_incorrect) / 5) / (elapsed_time / 60))

    print("You took " + Fore.GREEN + f"{elapsed_time:.2f} s " + Style.RESET_ALL + f"to type {len(target)} words.")
    print("Your raw WPM was " + Fore.GREEN + f"{raw_wpm}" + Style.RESET_ALL + ".")
    print("Your actual WPM was " + Fore.GREEN + f"{actual_wpm}" + Style.RESET_ALL + ".")
    print("Your accuracy was " + Fore.GREEN + f"{accuracy}%" + Style.RESET_ALL + ".")


def continuous_test(stdscr, time_limit):
    """
    """

    # hide cursor before test begins
    curses.curs_set(0)

    stdscr.clear()
    intro_msg = "Type the following as quickly as possible:"
    target_text_1 = " ".join(generate_text(10)) + " "
    target_text_2 = " ".join(generate_text(10)) + " "

    stdscr.addstr(0, 0, intro_msg)
    stdscr.addstr(1, 0, target_text_1)
    stdscr.addstr(2, 0, target_text_2)
    stdscr.addstr(4, 0, "Time: 0.00 s")
    stdscr.refresh()

    stdscr.nodelay(False)

    start = None
    typed_chars = []
    position = 0

    # accuracy metric
    num_incorrect = 0
    num_typed = 0

    while start is None or time.time() - start < time_limit:
        if start is None:
            stdscr.nodelay(False) # block if haven't started
        else:
            stdscr.nodelay(True)

        key = stdscr.getch()

        if start is None:
            start = time.time()

        if key in (8, 127): # backspace or delete
            if position > 0:
                position -= 1
                typed_chars.pop()
        elif (65 <= key <= 90) or (97 <= key <= 122) or (key == 32): # only accepting letters and space
            this_char = chr(key)
            typed_chars.append(this_char)
            position += 1
            num_typed += 1 # not including backspaces
            if this_char != target_text_1[len(typed_chars) - 1]:
                num_incorrect += 1

        # TODO: prevent copy paste capability

        if len(typed_chars) == len(target_text_1):
            target_text_1 = target_text_2
            target_text_2 = " ".join(generate_text(10)) + " "
            typed_chars = []
            position = 0
        
        stdscr.clear()
        stdscr.move(0, 0)
        stdscr.addstr(intro_msg)

        stdscr.move(1, 0)
        for i, char in enumerate(target_text_1):
            if i < len(typed_chars):
                if typed_chars[i] == char:
                    stdscr.addstr(char, curses.color_pair(1)) # correct
                else:
                    stdscr.addstr(typed_chars[i], curses.color_pair(2)) # incorrect
            else:
                stdscr.addstr(char) # default

        stdscr.move(2, 0)
        stdscr.addstr(target_text_2)

        stdscr.move(4, 0)
        stdscr.addstr(f"Time: {time.time() - start:.2f} s")

        stdscr.clrtoeol()
        stdscr.refresh()

    accuracy = round(100 - 100 * num_incorrect / num_typed)
    raw_wpm = round(num_typed / 5 / (time_limit / 60))
    actual_wpm = round(((num_typed - num_incorrect) / 5) / (time_limit / 60))

    print("Your raw WPM was " + Fore.GREEN + f"{raw_wpm}" + Style.RESET_ALL + ".")
    print("Your actual WPM was " + Fore.GREEN + f"{actual_wpm}" + Style.RESET_ALL + ".")
    print("Your accuracy was " + Fore.GREEN + f"{accuracy}%" + Style.RESET_ALL + ".")

