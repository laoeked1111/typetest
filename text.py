
import random

def generate_text(num_words: int) -> list[str]:
    """
    Generates num_words words randomly from the text file.

    Args:
        num_words (int) - number of words to generate
    Ret:
        a list of num_words strings (words)
    """

    file = open("5000-more-common.txt", 'r')
    text = [s.strip() for s in file.readlines()]

    return random.sample(text, num_words)

if __name__ == "__main__":
    print("10 randomly generated words:")
    print(generate_text(10))