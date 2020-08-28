import math
import string
from datetime import datetime
import random

from m2m_token.errors import ConfigError


def generate(seed: str, ttl: int, sequence: str = string.ascii_letters + string.digits, token_len: int = 6) -> str:
    """
    Generate a token based on current datetime and a given seed
    :param seed: Seed to initialize the random module with
    :param ttl: Time To Live for a token
    :param sequence: List of characters to use when generating a token
    :param token_len: Token length
    :return: Generated token as a string
    """
    if not seed:
        raise ConfigError('seed', 'Seed can not be empty')
    if type(ttl) is not int or ttl <= 0:
        raise ConfigError('ttl', 'The TTL value needs to be an int greater than 0')
    if type(sequence) is not str or len(sequence) == 0:
        raise ConfigError('sequence', 'The character sequence can not be empty')
    if type(token_len) is not int or token_len <= 0:
        raise ConfigError('token_len', 'The token length value needs to be an int greater than 0')
    current_time = datetime.utcnow()
    token_seconds = math.modf(current_time.second / ttl)[1]  # Retrieves the integer part of the result
    seconds_diff = current_time.second - (token_seconds * ttl)
    timestamp_seconds = round(datetime.timestamp(current_time)) - seconds_diff
    random.seed(f'{seed}{timestamp_seconds}')

    return ''.join(random.choices(sequence, k=token_len))
