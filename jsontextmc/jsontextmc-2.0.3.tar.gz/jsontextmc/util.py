#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tool to translate old Minecraft formatting codes to the modern JSON format."""


def leftmost_split(string: str, sep: str, trailing: bool = False) -> list:
    """
    Return list of a split string.

    The seperator is included on the left-most side of its' nearest look-behind character.

    :param string: String to split into
    :type string: str
    :param sep: Character to split
    :type sep: str
    :param trailing: Leave trailing seperator in or not
    :type trailing: bool
    :return: Split string
    :rtype: str
    """
    ret = [(sep + x) for x in string.split(sep)]
    if not trailing:
        ret[0] = ret[0].strip(sep)
    return ret


def rightmost_split(string: str, sep: str, trailing: bool = False) -> list:
    """
    Return list of a split string.

    The seperator is included on the right-most side of its' nearest look-ahead character.

    :param string: String to split into
    :type string: str
    :param sep: Character to split
    :type sep: str
    :param trailing: Leave trailing seperator in or not
    :type trailing: bool
    :return: Split string
    :rtype: str
    """
    ret = [x + sep for x in string.split(sep)]
    if not trailing:
        ret[-1] = ret[-1].strip(sep)
    return ret
