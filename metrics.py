
import statistics
from colorama import Fore, Style

def get_wpm(typed:int, elapsed_time:float) -> int:
    """
    Calculates the wpm given the number of characters typed and the time.
        Can be used for raw or actual wpm.

    Args:
        typed (int) - number of characters typed
        elapsed_time (float) - number of seconds that have passed
    Ret:
        wpm (int) - words per minute
    """
    return round(typed / 5 / (elapsed_time / 60))

def get_accuracy(typed, incorrect):
    """
    Calculates the accuracy of typing.

    Args:
        typed (int) - total number of chars typed
        incorrect (int) - number of incorrect chars
    Ret:
        accuracy (int) - percentage accuracy 
    """
    return round(100 - 100 * incorrect / typed)

def get_consistency(timestamps: list[float], tolerance=0.7) -> float:
    """
    Calculate consistency given a list of times of strokes and tolerance.

    Args:
        timestamps (list) - a list of floats representing times of keystrokes
        tolerance (float) - a number that allows mapping b/w CV and consistency
    Ret:
        consistency (float) - a decimal representing the consistency
    """ 

    # too short
    if len(timestamps) < 2:
        return 1

    # get time between strokes, eliminating extremely short or long strokes
    times_bw_strokes = [
        t2 - t1
        for t1, t2 in zip(timestamps, timestamps[1:])
        if 0.001 <= t2 - t1 <= 2
    ]

    if not times_bw_strokes[2:]:
        return 0

    # ignore the first few keystrokes
    std = statistics.pstdev(times_bw_strokes[2:])
    mean = statistics.mean(times_bw_strokes[2:])
    cv = std/mean

    score = max(0, 1 - cv / tolerance)
    return score

def print_metrics(num_typed:int, num_incorrect:int, elapsed_time:float, timestamps:list) -> None:
    """
    Calculate and display metrics.

    Args:
        num_typed (int) - total number of chars typed
        incorrect (int) - number of incorrect chars
        elapsed_time (float) - amount of time in seconds
        timestamps (list) - times of keystrokes
    """
    raw_wpm = get_wpm(num_typed, elapsed_time)
    actual_wpm = get_wpm(num_typed - num_incorrect, elapsed_time)
    accuracy = get_accuracy(num_typed, num_incorrect)
    consistency = get_consistency(timestamps)

    print("Your raw WPM was " + Fore.GREEN + f"{raw_wpm}" + Style.RESET_ALL + ".")
    print("Your actual WPM was " + Fore.GREEN + f"{actual_wpm}" + Style.RESET_ALL + ".")
    print("Your accuracy was " + Fore.GREEN + f"{accuracy}%" + Style.RESET_ALL + ".")
    print("Your consistency was " + Fore.GREEN + f"{100 * consistency:.2f}%" + Style.RESET_ALL + ".")

if __name__ == "__main__":
    pass