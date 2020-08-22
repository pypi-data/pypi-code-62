import unittest
from modules import grammar as gm
from fixtures import cases


class CompilerToolKitTestCase(unittest.TestCase):
    def test_parse_grammar(self):
        for x, y in zip(cases.parser_test_cases, cases.parser_test_cases_targets):
            self.assertEqual(gm.parse(x), y)

    def test_elim_left_recursion(self):
        for x, y in zip(cases.elim_lr_test_cases, cases.elim_lr_test_cases_targets):
            x, f = x
            pgrammar = gm.parse(x, f)
            pgrammar_y = gm.parse(y)
            ng = elim_left_recursion.elim_lr(pgrammar)
            self.assertEqual(ng, pgrammar_y)


if __name__ == "__main__":
    unittest.main()
