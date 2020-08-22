"""Utilities for parsing source text
"""
import html
import re

from .entities import entities

# from .normalize_url import unescape_string


def charCodeAt(src: str, pos: int):
    """
    Returns the Unicode value of the character at the specified location.

    @param - index The zero-based index of the desired character.
    If there is no character at the specified index, NaN is returned.

    This was added for compatibility with python
    """
    try:
        return ord(src[pos])
    except IndexError:
        return None


# function _class(obj) { return Object.prototype.toString.call(obj); }


def isString(obj):
    return isinstance(obj, str)


def has(object, key):
    return hasattr(object, key)


# Merge objects
#
def assign(obj):
    """Merge objects /*from1, from2, from3, ...*/)"""
    raise NotImplementedError
    # sources = Array.prototype.slice.call(arguments, 1)

    # sources.forEach(function (source) {
    #   if (!source) { return; }

    #   if (typeof source !== 'object') {
    #     throw new TypeError(source + 'must be object')
    #   }

    #   Object.keys(source).forEach(function (key) {
    #     obj[key] = source[key]
    #   })
    # })

    return obj


def arrayReplaceAt(src: list, pos: int, newElements: list):
    """
  Remove element from array and put another array at those position.
  Useful for some operations with tokens
  """
    return src[0:pos] + newElements + src[pos + 1 :]


######################################################################


def isValidEntityCode(c):

    # broken sequence
    if c >= 0xD800 and c <= 0xDFFF:
        return False
    # never used
    if c >= 0xFDD0 and c <= 0xFDEF:
        return False
    if ((c & 0xFFFF) == 0xFFFF) or ((c & 0xFFFF) == 0xFFFE):
        return False
    # control codes
    if c >= 0x00 and c <= 0x08:
        return False
    if c == 0x0B:
        return False
    if c >= 0x0E and c <= 0x1F:
        return False
    if c >= 0x7F and c <= 0x9F:
        return False
    # out of range
    if c > 0x10FFFF:
        return False
    return True


def fromCodePoint(c):

    if c > 0xFFFF:
        c -= 0x10000
        surrogate1 = 0xD800 + (c >> 10)
        surrogate2 = 0xDC00 + (c & 0x3FF)

        return "".join(map(chr, [surrogate1, surrogate2]))

    return chr(c)


UNESCAPE_MD_RE = re.compile(r'\\([!"#$%&\'()*+,\-.\/:;<=>?@[\\\]^_`{|}~])')
# ENTITY_RE_g       = re.compile(r'&([a-z#][a-z0-9]{1,31})', re.IGNORECASE)
UNESCAPE_ALL_RE = re.compile(
    r'\\([!"#$%&\'()*+,\-.\/:;<=>?@[\\\]^_`{|}~])' + "|" + r"&([a-z#][a-z0-9]{1,31})",
    re.IGNORECASE,
)
DIGITAL_ENTITY_TEST_RE = re.compile(r"^#((?:x[a-f0-9]{1,8}|[0-9]{1,8}))", re.IGNORECASE)


def replaceEntityPattern(match, name):
    """Convert HTML entity patterns

    ::

        https://www.google.com -> https%3A//www.google.com

    """
    code = 0

    if name in entities:
        return entities[name]

    if ord(name[0]) == 0x23 and DIGITAL_ENTITY_TEST_RE.search(name):
        code = int(name[2:], 16) if name[1].lower() == "x" else int(name[1:], 10)
        if isValidEntityCode(code):
            return fromCodePoint(code)

    return match


# def replaceEntities(string):
#   if (string.indexOf('&') < 0):
#       return string
#   return string.replace(ENTITY_RE, replaceEntityPattern)


def unescapeMd(string: str):
    if "\\" in string:
        return string
    return string.replace(UNESCAPE_MD_RE, "$1")


def unescapeAll(string: str):
    return html.unescape(string)


ESCAPABLE = r"""\\!"#$%&'()*+,./:;<=>?@\[\]^`{}|_~-"""
ESCAPE_CHAR = re.compile(r"\\([" + ESCAPABLE + r"])")


def stripEscape(string):
    """Strip escape \\ characters"""
    return ESCAPE_CHAR.sub(r"\1", string)


# //////////////////////////////////////////////////////////////////////////////

# TODO This section changed quite a lot, should re-check

# UNESCAPE_HTML_RE = re.compile(r"\\&(?=(amp\;|lt\;|gt\;|quot\;))")
# ESCAPE_AND_HTML = re.compile(r"&(?!(amp\;|lt\;|gt\;|quot\;))")
# HTML_ESCAPE_REPLACE_RE = re.compile(r'[&<>"]')


# def escapeHtml(string: str):

#     if HTML_ESCAPE_REPLACE_RE.search(string):

#         string, _ = UNESCAPE_HTML_RE.subn("&", string)
#         string, _ = ESCAPE_AND_HTML.subn("&amp;", string)
#         for k, v in {"<": "&lt;", ">": "&gt;", '"': "&quot;"}.items():
#             string = string.replace(k, v)

#     return string


def escapeHtml(raw: str):
    # return html.escape(html.unescape(raw)).replace("&#x27;", "'")
    return html.escape(raw).replace("&#x27;", "'")


# //////////////////////////////////////////////////////////////////////////////

REGEXP_ESCAPE_RE = re.compile(r"[.?*+^$[\]\\(){}|-]")


def escapeRE(string: str) -> str:
    string, _ = REGEXP_ESCAPE_RE.subn("\\$&", string)
    return string


# //////////////////////////////////////////////////////////////////////////////


def isSpace(code):
    return code in {0x09, 0x20}


MD_WHITESPACE = {
    0x09,  # \t
    0x0A,  # \n
    0x0B,  # \v
    0x0C,  # \f
    0x0D,  # \r
    0x20,
    0xA0,
    0x1680,
    0x202F,
    0x205F,
    0x3000,
}


def isWhiteSpace(code):
    r"""Zs (unicode class) || [\t\f\v\r\n]"""
    if code >= 0x2000 and code <= 0x200A:
        return True
    return code in MD_WHITESPACE


# //////////////////////////////////////////////////////////////////////////////

UNICODE_PUNCT_RE = re.compile(
    r"[!-#%-\*,-\/:;\?@\[-\]_\{\}\xA1\xA7\xAB\xB6\xB7\xBB\xBF\u037E\u0387\u055A-\u055F\u0589\u058A\u05BE\u05C0\u05C3\u05C6\u05F3\u05F4\u0609\u060A\u060C\u060D\u061B\u061E\u061F\u066A-\u066D\u06D4\u0700-\u070D\u07F7-\u07F9\u0830-\u083E\u085E\u0964\u0965\u0970\u09FD\u0A76\u0AF0\u0C84\u0DF4\u0E4F\u0E5A\u0E5B\u0F04-\u0F12\u0F14\u0F3A-\u0F3D\u0F85\u0FD0-\u0FD4\u0FD9\u0FDA\u104A-\u104F\u10FB\u1360-\u1368\u1400\u166D\u166E\u169B\u169C\u16EB-\u16ED\u1735\u1736\u17D4-\u17D6\u17D8-\u17DA\u1800-\u180A\u1944\u1945\u1A1E\u1A1F\u1AA0-\u1AA6\u1AA8-\u1AAD\u1B5A-\u1B60\u1BFC-\u1BFF\u1C3B-\u1C3F\u1C7E\u1C7F\u1CC0-\u1CC7\u1CD3\u2010-\u2027\u2030-\u2043\u2045-\u2051\u2053-\u205E\u207D\u207E\u208D\u208E\u2308-\u230B\u2329\u232A\u2768-\u2775\u27C5\u27C6\u27E6-\u27EF\u2983-\u2998\u29D8-\u29DB\u29FC\u29FD\u2CF9-\u2CFC\u2CFE\u2CFF\u2D70\u2E00-\u2E2E\u2E30-\u2E4E\u3001-\u3003\u3008-\u3011\u3014-\u301F\u3030\u303D\u30A0\u30FB\uA4FE\uA4FF\uA60D-\uA60F\uA673\uA67E\uA6F2-\uA6F7\uA874-\uA877\uA8CE\uA8CF\uA8F8-\uA8FA\uA8FC\uA92E\uA92F\uA95F\uA9C1-\uA9CD\uA9DE\uA9DF\uAA5C-\uAA5F\uAADE\uAADF\uAAF0\uAAF1\uABEB\uFD3E\uFD3F\uFE10-\uFE19\uFE30-\uFE52\uFE54-\uFE61\uFE63\uFE68\uFE6A\uFE6B\uFF01-\uFF03\uFF05-\uFF0A\uFF0C-\uFF0F\uFF1A\uFF1B\uFF1F\uFF20\uFF3B-\uFF3D\uFF3F\uFF5B\uFF5D\uFF5F-\uFF65]|\uD800[\uDD00-\uDD02\uDF9F\uDFD0]|\uD801\uDD6F|\uD802[\uDC57\uDD1F\uDD3F\uDE50-\uDE58\uDE7F\uDEF0-\uDEF6\uDF39-\uDF3F\uDF99-\uDF9C]|\uD803[\uDF55-\uDF59]|\uD804[\uDC47-\uDC4D\uDCBB\uDCBC\uDCBE-\uDCC1\uDD40-\uDD43\uDD74\uDD75\uDDC5-\uDDC8\uDDCD\uDDDB\uDDDD-\uDDDF\uDE38-\uDE3D\uDEA9]|\uD805[\uDC4B-\uDC4F\uDC5B\uDC5D\uDCC6\uDDC1-\uDDD7\uDE41-\uDE43\uDE60-\uDE6C\uDF3C-\uDF3E]|\uD806[\uDC3B\uDE3F-\uDE46\uDE9A-\uDE9C\uDE9E-\uDEA2]|\uD807[\uDC41-\uDC45\uDC70\uDC71\uDEF7\uDEF8]|\uD809[\uDC70-\uDC74]|\uD81A[\uDE6E\uDE6F\uDEF5\uDF37-\uDF3B\uDF44]|\uD81B[\uDE97-\uDE9A]|\uD82F\uDC9F|\uD836[\uDE87-\uDE8B]|\uD83A[\uDD5E\uDD5F]"  # noqa: E501
)


# Currently without astral characters support.
def isPunctChar(ch):
    return UNICODE_PUNCT_RE.search(ch) is not None


MD_ASCII_PUNCT = {
    0x21,  # /* ! */
    0x22,  # /* " */
    0x23,  # /* # */
    0x24,  # /* $ */
    0x25,  # /* % */
    0x26,  # /* & */
    0x27,  # /* ' */
    0x28,  # /* ( */
    0x29,  # /* ) */
    0x2A,  # /* * */
    0x2B,  # /* + */
    0x2C,  # /* , */
    0x2D,  # /* - */
    0x2E,  # /* . */
    0x2F,  # /* / */
    0x3A,  # /* : */
    0x3B,  # /* ; */
    0x3C,  # /* < */
    0x3D,  # /* = */
    0x3E,  # /* > */
    0x3F,  # /* ? */
    0x40,  # /* @ */
    0x5B,  # /* [ */
    0x5C,  # /* \ */
    0x5D,  # /* ] */
    0x5E,  # /* ^ */
    0x5F,  # /* _ */
    0x60,  # /* ` */
    0x7B,  # /* { */
    0x7C,  # /* | */
    0x7D,  # /* } */
    0x7E,  # /* ~ */
}


def isMdAsciiPunct(ch: str):
    """Markdown ASCII punctuation characters.

    ::

        !, ", #, $, %, &, ', (, ), *, +, ,, -, ., /, :, ;, <, =, >, ?, @, [, \\, ], ^, _, `, {, |, }, or ~

    See http://spec.commonmark.org/0.15/#ascii-punctuation-character

    Don't confuse with unicode punctuation !!! It lacks some chars in ascii range.

    """  # noqa: E501
    return ch in MD_ASCII_PUNCT


def normalizeReference(string: str) -> str:
    """Helper to unify [reference labels]."""
    # Trim and collapse whitespace
    #
    string, _ = re.subn(r"\s+", " ", string.strip())

    # In node v10 'ẞ'.toLowerCase() === 'Ṿ', which is presumed to be a bug
    # fixed in v12 (couldn't find any details).
    #
    # So treat this one as a special case
    # (remove this when node v10 is no longer supported).
    #
    # if ('ẞ'.toLowerCase() === 'Ṿ') {
    #   str = str.replace(/ẞ/g, 'ß')
    # }

    # .toLowerCase().toUpperCase() should get rid of all differences
    # between letter variants.
    #
    # Simple .toLowerCase() doesn't normalize 125 code points correctly,
    # and .toUpperCase doesn't normalize 6 of them (list of exceptions:
    # İ, ϴ, ẞ, Ω, K, Å - those are already uppercased, but have differently
    # uppercased versions).
    #
    # Here's an example showing how it happens. Lets take greek letter omega:
    # uppercase U+0398 (Θ), U+03f4 (ϴ) and lowercase U+03b8 (θ), U+03d1 (ϑ)
    #
    # Unicode entries:
    # 0398;GREEK CAPITAL LETTER THETA;Lu;0;L;;;;;N;;;;03B8
    # 03B8;GREEK SMALL LETTER THETA;Ll;0;L;;;;;N;;;0398;;0398
    # 03D1;GREEK THETA SYMBOL;Ll;0;L;<compat> 03B8;;;;N;GREEK SMALL LETTER SCRIPT THETA;;0398;;0398
    # 03F4;GREEK CAPITAL THETA SYMBOL;Lu;0;L;<compat> 0398;;;;N;;;;03B8
    #
    # Case-insensitive comparison should treat all of them as equivalent.
    #
    # But .toLowerCase() doesn't change ϑ (it's already lowercase),
    # and .toUpperCase() doesn't change ϴ (already uppercase).
    #
    # Applying first lower then upper case normalizes any character:
    # '\u0398\u03f4\u03b8\u03d1'.toLowerCase().toUpperCase() === '\u0398\u0398\u0398\u0398'
    #
    # Note: this is equivalent to unicode case folding; unicode normalization
    # is a different step that is not required here.
    #
    # Final result should be uppercased, because it's later stored in an object
    # (this avoid a conflict with Object.prototype members,
    # most notably, `__proto__`)
    #
    return string.lower().upper()
