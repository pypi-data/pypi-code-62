#!/usr/bin/env python3

"""IO

Any I/O functions will go here

Author(s)
---------
Daniel Gisolfi <Daniel.Gisolfi1@marist.edu>
"""

import sys
import json


def jsonToDict(path: str) -> dict:
    """loads JSON from a file and converts to a dict
    Parameters
    ----------
    path : str
        path to json file 
    Returns
    -------
    dict
        json object as a dict
    """
    try:
        json_file = open(path, "r")
        json_data = json_file.read()
        json_file.close()

        return json.loads(json_data)
    except ValueError as e:
        print(f"Error: cannot load JSON at path: {path}. Invalid json: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Cannot load json data from path: {path}")
        sys.exit(1)
