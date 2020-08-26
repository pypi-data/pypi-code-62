import numpy as np


def print_random():
    ra = np.random.rand(1)
    print(f"Printing a random number {float(ra)}")
    return ra


if __name__ == "__main__":
    print_random()

