from datetime import datetime

import pytz


def now():
    return pytz.timezone('Asia/Shanghai').localize(datetime.now())


def parse_time(time_str: str, format: str = "%Y-%m-%d %H:%M:%S"):
    parse_time = datetime.strptime(time_str, format)
    return pytz.timezone('Asia/Shanghai').localize(parse_time)


def parse_timestamp(timestamp: int):
    bit = len(str(timestamp))
    if bit == 13:
        timestamp /= 1000
    elif bit == 15:
        timestamp /= 1000
    return datetime.fromtimestamp(timestamp, pytz.timezone('Asia/Shanghai'))


