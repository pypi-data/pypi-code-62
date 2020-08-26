from __future__ import unicode_literals

import unittest
import sys

import fast_diff_match

if sys.version_info[0] == 3:
    diff = fast_diff_match.diff
    diff_bytes = fast_diff_match.diff_bytes
    match_main = fast_diff_match.match_main
    match_main_bytes = fast_diff_match.match_main_bytes
else:
    diff = fast_diff_match.diff_unicode
    diff_bytes = fast_diff_match.diff_str
    match_main = fast_diff_match.match_main_unicode
    match_main_bytes = fast_diff_match.match_main_str


class MatchTests(unittest.TestCase):
    def test_unicode(self):
        self.assertEqual(0, match_main('abcdef', 'abcdef', 1000))

        self.assertEqual(-1, match_main('', 'abcdef', 1))

        self.assertEqual(3, match_main('abcdef', '', 3))

        self.assertEqual(3, match_main('abcdef', 'de', 3))

        self.assertEqual(3, match_main('abcdef', 'defy', 4))

        self.assertEqual(0, match_main('abcdef', 'abcdefy', 0))

        self.assertEqual(2, match_main('abc\u2192def', 'c\u2192defy', 0))

    def test_bytes(self):
        self.assertEqual(0, match_main_bytes(b'abcdef', b'abcdef', 1000))

        self.assertEqual(-1, match_main_bytes(b'', b'abcdef', 1))

        self.assertEqual(3, match_main_bytes(b'abcdef', b'', 3))

        self.assertEqual(3, match_main_bytes(b'abcdef', b'de', 3))

        self.assertEqual(3, match_main_bytes(b'abcdef', b'defy', 4))

        self.assertEqual(0, match_main_bytes(b'abcdef', b'abcdefy', 0))

        self.assertEqual(2, match_main_bytes(b'abc\xe2\x86\x92def', b'c\xe2\x86\x92defy', 0))
