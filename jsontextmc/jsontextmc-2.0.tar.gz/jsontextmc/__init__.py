#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSONTextMC converts legacy color codes to the modern JSON format.

Legacy Minecraft text could use ``&`` as a character for defining colored text.
With the advent of JSON text components, legacy color text replaced what was too long to type in
JSON manually.

This module can quickly transform that legacy text into a JSON-compatible format.
"""
import re

from jsontextmc import util
from jsontextmc import constants

DEFAULT_COLOR_CHAR = "\u00A7"
ALL_CODES = "0123456789AaBbCcDdEeFfKkLlMmNnOoRrXx"

BLACK = ("000000", "black", "0")

DARK_BLUE = ("0000aa", "dark_blue", "1")

DARK_GREEN = ("008000", "dark_green", "2")

DARK_AQUA = ("00aaaa", "dark_aqua", "3")

DARK_RED = ("aa0000", "dark_red", "4")

DARK_PURPLE = ("aa00aa", "dark_purple", "5")

GOLD = ("ffaa00", "gold", "6")

GRAY = ("aaaaaa", "gray", "7")

DARK_GRAY = ("555555", "dark_gray", "8")

BLUE = ("5555ff", "blue", "9")

GREEN = ("3ce63c", "green", "a")

AQUA = ("3ce6e6", "aqua", "blue")

RED = ("ff5555", "red", "c")

LIGHT_PURPLE = ("ff55ff", "light_purple", "d")

YELLOW = ("ffff55", "yellow", "e")

WHITE = ("ffffff", "white", "f")

MAGIC = ("obfuscated", "k")
OBFUSCATED = MAGIC

BOLD = ("bold", "l")

STRIKETHROUGH = ("strikethrough", "m")

UNDERLINE = ("underline", "n")

ITALIC = ("italic", "o")

RESET = ("reset", "r")


def data_color_codes() -> dict:
    """
    Wool color codes.

    :return: Dictionary of wool color codes
    :rtype: dict
    """
    return {
        0: [WHITE, "#e9ecec"],
        1: [GOLD, "#f07613"],
        2: [DARK_PURPLE, "#bd44b3"],
        3: [BLUE, "#3aafd9"],
        4: [YELLOW, "#f8c627"],
        5: [GREEN, "#70b919"],
        6: [LIGHT_PURPLE, "#ed8dac"],
        7: [GRAY, "#3e4447"],
        8: [DARK_GRAY, "#8e8e86"],
        9: [AQUA, "#158991"],
        10: [LIGHT_PURPLE, "#729aac"],
        11: [DARK_BLUE, "#35399d"],
        12: [YELLOW, "#724728"],
        13: [GREEN, "#546d1b"],
        14: [RED, "#a12722"],
        15: [BLACK, "#141519"],
    }


CODES = [
    {
        "0": BLACK,
        "1": DARK_BLUE,
        "2": DARK_GREEN,
        "3": DARK_AQUA,
        "4": DARK_RED,
        "5": DARK_PURPLE,
        "6": GOLD,
        "7": GRAY,
        "8": DARK_GRAY,
        "9": BLUE,
        "a": GREEN,
        "b": AQUA,
        "c": RED,
        "d": LIGHT_PURPLE,
        "e": YELLOW,
        "f": WHITE,
    },
    {"k": OBFUSCATED, "l": BOLD, "m": STRIKETHROUGH, "n": UNDERLINE, "o": ITALIC},
    {"r": RESET},
]

ALL_CODES_SHORT = list(tempkeys for tempdict in CODES for tempkeys in tempdict)
URL_REGEX = re.compile(
    r"(?:http(?:s)?://.)?(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{2,256}\.[a-z]{2,"
    r"6}\b(?:[-a-zA-Z0-9@:%_+.~#?&//=]*)"
)


def translate(
    text: str, sep: str = "&", hexchar: str = "#", strict: bool = True
) -> list:
    """
    Translate format-text to list, using ``sep`` as the format code separator.

    To use 1.16 hex colors, use ``&#RRGGBB``, where R, G, B are red, green, blue, respectively.

    If strict mode is on:
      * codes inherited from previous entries in the string will not carry over
      * formatting will not work after a color char
      * color will not work after a formatting char
    If you have issues with not being able to combine character codes, turn ``strict`` off.


    :param text: Text to process
    :type text: str
    :param sep: Character before color/formatting codes
    :type sep: str
    :param hexchar: Character to use for 1.16 hexidecimal colors
    :type hexchar: str
    :param strict: Explicitly set formatting options for each JSON entry
    :type strict: bool
    :return: JSON-compatible list
    :rtype: list
    """
    jsontext = [""]
    det_sepcode = False
    bold = False
    italic = False
    strikethru = False
    underlined = False
    obfuscated = False
    color = False
    url = False
    marked = False
    for entry in util.leftmost_split(text, sep):
        if strict:
            det_sepcode = False
            bold = False
            italic = False
            strikethru = False
            underlined = False
            obfuscated = False
            color = False
            url = False
            marked = False
        if entry.startswith(sep):
            det_sepcode = True
        if det_sepcode:
            try:
                char = entry[1]
            except IndexError:
                continue
            if char == hexchar:
                marked = True
                color = entry[1:8].upper()
                entry = entry[8:]
            else:
                try:
                    char = entry[1].lower()
                except IndexError:
                    continue
                if char in ALL_CODES_SHORT:
                    marked = True
                    if char in CODES[0].keys():
                        color = CODES[0][char][1].lower()
                    elif char == OBFUSCATED[1]:
                        obfuscated = True
                    elif char == BOLD[1]:
                        bold = True
                    elif char == STRIKETHROUGH[1]:
                        strikethru = True
                    elif char == UNDERLINE[1]:
                        underlined = True
                    elif char == ITALIC[1]:
                        italic = True
                    elif char == RESET[1]:
                        color = False
                        bold = False
                        italic = False
                        strikethru = False
                        underlined = False
                        obfuscated = False
                if marked:
                    entry = entry[2:]
        elif URL_REGEX.match(entry):
            url = URL_REGEX.match(entry).group(0)
        tempjson = {"text": entry}
        if color:
            tempjson["color"] = color
        if bold:
            tempjson["bold"] = True
        if italic:
            tempjson["italic"] = True
        if underlined:
            tempjson["underlined"] = True
        if strikethru:
            tempjson["strikethrough"] = True
        if obfuscated:
            tempjson["obfuscated"] = True
        if url:
            tempjson["clickEvent"] = {"action": "open_url", "value": url}
        jsontext.append(tempjson)
    return jsontext
