class Token(object):
    """
    Container for the token text and its annotations
    """

    def __init__(self, token: str, annotation=None, block_annotation=None):
        """

        :param token:
        :param annotation:
        :param block_annotation:
        """
        self._token = token
        self._annotation = annotation
        self._block = block_annotation

    @property
    def token(self):
        return self._token

    @property
    def annotation(self):
        return self._annotation

    @property
    def block(self):
        return self._block

    def __str__(self):
        return f"{self.token} - {self.annotation} - {self.block}"
