import json


def get_quotes_of_file(filename: str) -> dict:
    with open(filename, 'r') as f:
        data = json.loads(f.read())

        return data['quotes']
