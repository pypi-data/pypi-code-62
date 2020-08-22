import unittest
from modules import grammar as gm
from fixtures import cases


class ParserTestCase(unittest.TestCase):
    def test_parse_grammar(self):
        for x, y in zip(cases.parser_test_cases, cases.parser_test_cases_targets):
            self.assertEqual(gm.parse(x), y)


if __name__ == "__main__":
    unittest.main()
