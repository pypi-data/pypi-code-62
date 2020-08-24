"""Tests for `sourcy` package."""
import os
import unittest

import sourcy


class TestJava(unittest.TestCase):
    maxDiff = None
    rel_path = os.path.dirname(os.path.abspath(__file__))

    def setUp(self) -> None:
        with open(os.path.join(self.rel_path, "resources", "SignerOutputStream.java"), "rt", encoding="utf8") as inf:
            self.code = inf.read()

        self.scp = sourcy.load("java")

        self.parsed = self.scp(self.code)

    def test_parser(self):
        with open(os.path.join(self.rel_path, "resources", "SignerOutputStream.tokens.gold"), "rt",
                  encoding="utf8") as inf:
            self.gold = [x.strip() for x in inf.read().split("|")]

        self.assertListEqual([item.token.strip() for item in self.parsed], self.gold)

    def test_classes(self):
        self.assertListEqual([item.token.strip() for item in self.parsed.classes], ["SignerOutputStream"])

    def test_comments(self):
        self.assertEqual(len(list(self.parsed.comments)), 4)

    def test_identifiers(self):
        with open(os.path.join(self.rel_path, "resources", "SignerOutputStream.identifiers.gold"), "rt",
                  encoding="utf8") as inf:
            self.gold = [x.strip() for x in inf.read().split("|")]

        self.assertListEqual([item.token.strip() for item in self.parsed.identifiers], self.gold)


if __name__ == '__main__':
    unittest.main()
