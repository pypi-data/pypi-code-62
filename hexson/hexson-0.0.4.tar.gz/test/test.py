#!/usr/bin/env python3
# Json library support hex escape.
import hexson
import json


if __name__ == '__main__':
    data = '{"a": "\\\\x00"}'
    print(data)
    print(json.loads(data))
    print(hexson.loads(data, utf_8_string=False))
