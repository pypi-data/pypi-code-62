from typing import Optional

from aim.ql.tree.abstract_syntax_tree import AbstractSyntaxTree
from aim.ql.tree.binary_expression_tree import BinaryExpressionTree
from aim.ql.grammar.expression import Expression
from aim.ql.tokens.token import Token, TokenList


def parse(query: str):
    parser = Expression()
    expression = parser.parse(query)
    return expression


def match(strict: bool, expression: str,
          concat_default_expression: Optional[str] = None,
          fields: Optional[dict] = None, *add_fields):
    if isinstance(expression, str):
        expression = parse(expression)
    elif not isinstance(expression, (Token, TokenList)):
        raise TypeError('undefined expression type')

    ast = AbstractSyntaxTree()
    ast.build_from_expression(expression)

    bet = BinaryExpressionTree()
    bet.build_from_ast(ast)
    bet.strict = strict

    if concat_default_expression:
        if isinstance(concat_default_expression, str):
            concat_default_expression = parse(concat_default_expression)
        elif not isinstance(concat_default_expression, (Token, TokenList)):
            raise TypeError('undefined default expression type')

        ast_def = AbstractSyntaxTree()
        ast_def.build_from_expression(concat_default_expression)

        bet_def = BinaryExpressionTree()
        bet_def.build_from_ast(ast_def)
        bet.concat(bet_def)

    match_res = bet.match(fields, add_fields)
    return match_res
