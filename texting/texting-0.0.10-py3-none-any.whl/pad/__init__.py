from texting import SP


def lpad(text: str, width: int, fill: str = SP):
    return f'{text:{fill[0]}>{width}}'


def rpad(text: str, width: int, fill: str = SP):
    return f'{text:{fill[0]}<{width}}'


def cpad(text: str, width: int, fill: str = SP):
    return f'{text:{fill[0]}^{width}}'
