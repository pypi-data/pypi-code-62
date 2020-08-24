import os
from collections import deque
from typing import List

import tree_sitter
from tree_sitter.binding import Tree, Node

from sourcy.tokens.doc import Document
from sourcy.tokens.token import Token


class Parser(object):
    """

    """

    def __init__(self, lang: str, *args, **kwargs):
        """

        :param lang: The name of the language to parse
        :param args:
        :param kwargs:
        """
        self.lang = lang
        self.language = tree_sitter.Language(os.path.join(os.path.dirname(__file__), "grammars", "languages.so"),
                                             f"{lang}")
        self.parser = tree_sitter.Parser()
        self.parser.set_language(self.language)

    def _create_tree(self, code: bytes) -> Tree:
        """
        Parses the code and returns a (S-expression)[https://en.wikipedia.org/wiki/S-expression] formatted Concrete
        Syntax Tree.

        :param code:
        :return:
        """
        tree = self.parser.parse(code)
        return tree

    def __call__(self, code: str, *args, **kwargs) -> Document:
        code_b = bytes(code, "utf8")
        tree = self._create_tree(code_b)
        tokens = self._traverse(code_b, tree)

        return Document(code, tokens)

    def _traverse(self, code: bytes, tree: Tree) -> List[Token]:
        """
        Post-order tree traversal that returns a list of tokens with their annotations

        :param code: A byte string representation of the code
        :param tree: The tree representation of the code
        :return:
        """
        root = tree.root_node
        stack = deque()
        stack.append((root, None))

        tokens = []
        while len(stack):
            current, parent = stack.pop()

            if current.type != tree.root_node.type and len(current.children) == 0:
                token, annotation = self._extract_token_annotation(code, current)
                _, block_annotation = self._extract_token_annotation(code, parent)
                tokens.append(Token(token.decode("utf8"), annotation, block_annotation))
            for child in current.children:
                stack.append((child, current))

        return tokens[::-1]

    @staticmethod
    def _extract_token_annotation(code: bytes, node: Node) -> (bytes, str):
        """
        Extract the token string from the code

        :param code: The code textual representation
        :param node: A node containing the start and end positions of the token
        :return:
        """
        token = code[node.start_byte:node.end_byte]
        annotations = node.type
        return token, annotations
