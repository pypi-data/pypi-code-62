from random import randint


def krand(digits: int):
    return randint(10 ** digits - 1, (10 ** digits) - 1)
