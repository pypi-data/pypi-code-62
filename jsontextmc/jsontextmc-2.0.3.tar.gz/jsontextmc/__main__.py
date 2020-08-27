#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Console argument parser for JSONTextMC."""
import argparse

from jsontextmc import translate
from jsontextmc import constants

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=constants.PROJECT, description=constants.LONG_DOC
    )
    parser.add_argument(
        "-t",
        "--text",
        required=True,
        metavar="legacy text",
        dest="text",
        help="Legacy text to translate",
    )
    parser.add_argument(
        "-s",
        "--separator",
        default="&",
        metavar="seperator",
        dest="sep",
        help="""Character before color/formatting codes, in \"§cRed!\", \"§\" is the
        character""",
    )
    parser.add_argument(
        "-hx",
        "--hexchar",
        default="#",
        metavar="character",
        dest="hexchar",
        type=str,
        help="""Character to use for 1.16 hexidecimal colors""",
    )
    parser.add_argument(
        "--strict",
        default=False,
        dest="strict",
        action="store_true",
        help="Explicitly set formatting options for each JSON entry",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{constants.PROJECT} v{constants.VERSION}",
    )
    args = parser.parse_args()
    print(translate(args.text, args.sep, args.hexchar, args.strict))
