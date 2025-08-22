
import time
import curses

from text import generate_text
from metrics import print_metrics

def test(stdscr):
    """
    Decorator for tests.
    """
    intro_msg = "Type the following as quickly as possible: "
    start = None
    typed_chars = []
    position = 0

    # accuracy metric
    num_typed = 0
    num_incorrect = 0

    # consistency metric
    timestamps = []

    def setup(intro_msg:str, *target_args) -> None:
        """
        Setup for tests. 
        """
        # hide the cursor before test begins
        curses.curs_set(0)

        # disable mouse input to prevent copying and pasting
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        curses.mouseinterval(0)
        stdscr.clear()

        stdscr.addstr(0, 0, intro_msg)
        if len(target_args) == 1:
            stdscr.addstr(1, 0, target_args[0])
        else:
            for i, target in enumerate(target_args):
                stdscr.addstr(i + 1, 0, target)

        stdscr.addstr(len(target_args) + 2, 0, "Time: 0.00 s")
        stdscr.refresh()
        stdscr.nodelay(False) # block until first key pressed
    
    def update(*target_args):
        """
        Update screen.
        """
        nonlocal start, position, num_typed, num_incorrect

        target_text = target_args[0]

        if start is not None:
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
            timestamps.append(time.time() - start)
            if this_char != target_text[len(typed_chars) - 1]:
                num_incorrect += 1

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

        if len(target_args) > 1:
            for i, line in enumerate(target_args[1:]):
                stdscr.move(i + 2, 0)
                stdscr.addstr(line)

        stdscr.move(len(target_args) + 2, 0)
        stdscr.addstr(f"Time: {time.time() - start:.2f} s")

        stdscr.clrtoeol()
        stdscr.refresh()

    def finite_test(target: list[str]) -> None:
        """
        Conduct a test of a finite number of words. Prints WPM and accuracy at the end.

        WPM is calculated as the number of characters typed divided by 5, 
            divided by the number of minutes elapsed.

        Args:
            stdscr - the standard screen
            target - the list of words that must be typed
        """
        nonlocal start, typed_chars, position, num_typed, num_incorrect, timestamps

        target_text = " ".join(target)

        setup(intro_msg, target_text)

        while position < len(target_text):
            update(target_text)

        elapsed_time = time.time() - start
        print_metrics(num_typed, num_incorrect, elapsed_time, timestamps)

    def continuous_test(time_limit: int) -> None:
        """
        Conduct a test of an indefinite number of words and a given time limit. Prints WPM and accuracy at the end.

        WPM is calculated as the number of characters typed divided by 5, 
            divided by the number of minutes elapsed.

        Args:
            stdscr - the standard screen
            time_limit - the time limit for typing, in seconds
        """
        nonlocal start, typed_chars, position, num_typed, num_incorrect, timestamps

        target_text_1 = " ".join(generate_text(10)) + " "
        target_text_2 = " ".join(generate_text(10)) + " "
        
        setup(intro_msg, target_text_1, target_text_2)

        while start is None or time.time() - start < time_limit:
            if len(typed_chars) >= len(target_text_1):
                target_text_1 = target_text_2
                target_text_2 = " ".join(generate_text(10)) + " "
                typed_chars = []
            update(target_text_1, target_text_2)

        print_metrics(num_typed, num_incorrect, time_limit, timestamps)

    return finite_test, continuous_test

if __name__ == "__main__":
    pass