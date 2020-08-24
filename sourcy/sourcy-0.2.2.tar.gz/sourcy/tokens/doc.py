from typing import Generator, List

from sourcy.tokens.token import Token


class Document(object):
    """
    Wrapper for a sequence of :class: 'tokens.token.Token' containing the annotations for the source code
    """

    def __init__(self, code: str, tokens: List[Token], *args, **kwargs):
        """

        :param code:
        :param tokens:
        :param args:
        :param kwargs:
        """
        self._code = code
        self._tokens = tokens

    @property
    def tokens(self) -> List[Token]:
        return self._tokens

    @property
    def code(self) -> str:
        return self._code

    @tokens.setter
    def tokens(self, value: List[Token]):
        self._tokens = value

    @code.setter
    def code(self, value: str):
        self._code = value

    def __getitem__(self, item) -> Generator[Token, None, None]:
        yield self.tokens[item]

    def __iter__(self) -> Generator[Token, None, None]:
        for token in self.tokens:
            yield token

    def __len__(self) -> int:
        return len(self.tokens)

    @property
    def identifiers(self) -> Generator[Token, None, None]:
        for token in self.tokens:
            if "identifier" in token.annotation:
                yield token

    @property
    def classes(self) -> Generator[Token, None, None]:
        for token in self.tokens:
            if token.annotation == "identifier" and token.block == "class_declaration":
                yield token

    @property
    def comments(self) -> Generator[Token, None, None]:
        for token in self.tokens:
            if token.annotation == "comment":
                yield token
