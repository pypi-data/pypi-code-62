"""
data validation helper functions
================================

This module is pure Python and has no dependencies.

The two slightly bigger helper functions provided by
this namespace portion are :func:`correct_email`
and :func:`correct_phone`, which are useful for to
check if a string contains a valid email address
or phone number.

They also allow you to automatically correct an
email address or a phone number to a valid format.
More sophisticated helpers for the validation
of email addresses, phone numbers and post
addresses are available in the :mod:`ae.validation`
namespace portion.
"""
from string import ascii_letters, digits
from typing import List, Optional, Tuple


__version__ = '0.1.1'


def correct_email(email: str, changed: bool = False, removed: Optional[List[str]] = None) -> Tuple[str, bool]:
    """ check and correct email address from a user input (removing all comments)

    Special conversions that are not returned as changed/corrected are: the domain part of an email will be corrected
    to lowercase characters, additionally emails with all letters in uppercase will be converted into lowercase.

    Regular expressions are not working for all edge cases (see the answer to this SO question:
    https://stackoverflow.com/questions/201323/using-a-regular-expression-to-validate-an-email-address) because RFC822
    is very complex (even the reg expression recommended by RFC 5322 is not complete; there is also a
    more readable form given in the informational RFC 3696). Additionally a regular expression
    does not allow corrections. Therefore this function is using a procedural approach (using recommendations from
    RFC 822 and https://en.wikipedia.org/wiki/Email_address).

    :param email:       email address
    :param changed:     (optional) flag if email address got changed (before calling this function) - will be returned
                        unchanged if email did not get corrected.
    :param removed:     (optional) list declared by caller for to pass back all the removed characters including
                        the index in the format "<index>:<removed_character(s)>".
    :return:            tuple of (possibly corrected email address, flag if email got changed/corrected)
    """
    if not email:       # email could be None, also shortcut if email == ""
        return "", False

    if removed is None:
        removed = list()

    letters_or_digits = ascii_letters + digits
    in_local_part = True
    in_quoted_part = False
    in_comment = False
    all_upper_case = True
    local_part = ""
    domain_part = ""
    domain_beg_idx = -1
    domain_end_idx = len(email) - 1
    comment = ''
    last_ch = ''
    ch_before_comment = ''
    for idx, char in enumerate(email):
        if char.islower():
            all_upper_case = False
        next_ch = email[idx + 1] if idx + 1 < domain_end_idx else ''
        if in_comment:
            comment += char
            if char == ')':
                in_comment = False
                removed.append(comment)
                last_ch = ch_before_comment
            continue
        if char == '(' and not in_quoted_part \
                and (idx == 0 or email[idx:].find(')@') >= 0 if in_local_part
                     else idx == domain_beg_idx or email[idx:].find(')') == domain_end_idx - idx):
            comment = str(idx) + ':('
            ch_before_comment = last_ch
            in_comment = True
            changed = True
            continue
        if char == '"' \
                and (not in_local_part
                     or last_ch != '.' and idx and not in_quoted_part
                     or next_ch not in ('.', '@') and last_ch != '\\' and in_quoted_part):
            removed.append(str(idx) + ':' + char)
            changed = True
            continue

        if char == '@' and in_local_part and not in_quoted_part:
            in_local_part = False
            domain_beg_idx = idx + 1
        elif char in letters_or_digits:  # ch.isalnum():
            pass  # uppercase and lowercase Latin letters A to Z and a to z (isalnum() includes also umlauts)
        elif ord(char) > 127 and in_local_part:
            pass    # international characters above U+007F
        elif char == '.' and in_local_part and not in_quoted_part and last_ch != '.' and idx and next_ch != '@':
            pass    # if not the first or last unless quoted, and does not appear consecutively unless quoted
        elif char in ('-', '.') and not in_local_part and (last_ch != '.' or char == '-') \
                and idx not in (domain_beg_idx, domain_end_idx):
            pass    # if not duplicated dot and not the first or last character in domain part
        elif (char in ' (),:;<>@[]' or char in '\\"' and last_ch == '\\' or char == '\\' and next_ch == '\\') \
                and in_quoted_part:
            pass    # in quoted part and in addition, a backslash or double-quote must be preceded by a backslash
        elif char == '"' and in_local_part:
            in_quoted_part = not in_quoted_part
        elif (char in "!#$%&'*+-/=?^_`{|}~"
              or char == '.' and (last_ch and last_ch != '.' and next_ch != '@' or in_quoted_part)) \
                and in_local_part:
            pass    # special characters (in local part only and not at beg/end and no dup dot outside of quoted part)
        else:
            removed.append(str(idx) + ':' + char)
            changed = True
            continue

        if in_local_part:
            local_part += char
        else:
            domain_part += char.lower()
        last_ch = char

    if all_upper_case:
        local_part = local_part.lower()

    return local_part + domain_part, changed


def correct_phone(phone: str, changed: bool = False, removed: Optional[List[str]] = None, keep_1st_hyphen: bool = False
                  ) -> Tuple[str, bool]:
    """ check and correct phone number from a user input (removing all invalid characters including spaces)

    :param phone:           phone number
    :param changed:         (optional) flag if phone got changed (before calling this function) - will be returned
                            unchanged if phone did not get corrected.
    :param removed:         (optional) list declared by caller for to pass back all the removed characters including
                            the index in the format "<index>:<removed_character(s)>".
    :param keep_1st_hyphen: (optional, def=False) pass True for to keep at least the first occurring hyphen character.
    :return:                tuple of (possibly corrected phone number, flag if phone got changed/corrected).
    """
    if removed is None:
        removed = list()

    corr_phone = ''
    got_hyphen = False
    for idx, char in enumerate(phone or ""):      # allow phone Is None
        if char.isdigit():
            corr_phone += char
        elif keep_1st_hyphen and char == '-' and not got_hyphen:
            got_hyphen = True
            corr_phone += char
        else:
            if char == '+' and not corr_phone and not phone[idx + 1:].startswith('00'):
                corr_phone = '00'
            removed.append(str(idx) + ':' + char)
            changed = True

    return corr_phone, changed
