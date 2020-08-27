#! /usr/bin/env python

import argparse
import sys
import cssutils

from csscolorrule import *

__version__ = "0.1.0"

if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("cssfile", nargs=1)
    args_parser.add_argument("--version", action="store_true",\
        help="output version information and exit")
    args = args_parser.parse_args()

    if args.version:
        print("colorcheck %s" % __version__)
        sys.exit(0)

    parser = cssutils.CSSParser(raiseExceptions=True)
    sheet = parser.parseFile(sys.argv[1])

    for rule in sheet:
        if rule.type == rule.STYLE_RULE:
            csscolorrule = CSSColorRule(rule)
            result = csscolorrule.result()
            if result != None:
                print("%s : %.2f" % (rule.selectorText, result))
