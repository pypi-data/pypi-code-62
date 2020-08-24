import random

from cheerful_quotes import file_read


def get_randomic_quote(filename: str) -> dict:
    quotes = file_read.get_quotes_of_file(filename)
    random_number = random.randrange(0, len(quotes))

    object_quote = quotes[random_number]

    return object_quote


def get_a_phrase(filename: str) -> str:
    object_quote = get_randomic_quote(filename)

    message = f'Once {object_quote["author"]} says: "{object_quote["quote"]}"'

    return message
