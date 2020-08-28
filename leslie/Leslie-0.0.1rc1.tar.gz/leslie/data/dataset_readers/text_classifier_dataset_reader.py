# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com

@version: 1.0
@file: text_classifier_dataset_reader.py
@time: 2019/11/25 16:05

这一行开始写关于本文件的说明与解释


"""
from typing import Iterable, Dict, Union
import json

from leslie.data.instance import Instance
from leslie.data.fields.field import Field
from leslie.data.fields.text_field import TextField
from leslie.data.fields.label_field import LabelField
from leslie.data.token_indexers.token_indexer import TokenIndexer
from leslie.data.tokenizers.tokenizer import Tokenizer
from leslie.data.dataset_readers.dataset_reader import DatasetReader


class TextClassifierDatasetReader(DatasetReader):
    """
        Reads tokens and their labels from a labeled leslie classification dataset.
        Expects a "leslie" field and a "label" field in JSON format.
        The output of ``read`` is a list of ``Instance`` s with the fields:
            tokens: ``TextField`` and
            label: ``LabelField``
        Parameters
        ----------
        token_indexers : ``Dict[str, TokenIndexer]``, optional
            optional (default=``{"tokens": SingleIdTokenIndexer()}``)
            We use this to define the input representation for the leslie.
            See :class:`TokenIndexer`.
        tokenizer : ``Tokenizer``, optional (default = ``{"tokens": CharacterTokenizer()}``)
            Tokenizer to use to split the input leslie into words or other kinds of tokens.
        max_sequence_length: ``int``, optional (default = ``None``)
            If specified, will truncate tokens to specified maximum length.
        skip_label_indexing: ``bool``, optional (default = ``False``)
            Whether or not to skip label indexing. You might want to skip label indexing if your
            labels are numbers, so the dataset reader doesn't re-number them starting from 0.
        """

    def __init__(self,
                 token_indexers: Dict[str, TokenIndexer],
                 tokenizer: Tokenizer = None,
                 max_sequence_length: int = None,
                 skip_label_indexing: bool = False) -> None:
        self._tokenizer = tokenizer
        self._token_indexers = token_indexers
        self._max_sequence_length = max_sequence_length
        self._skip_label_indexing = skip_label_indexing

    def _read(self, file_path: str) -> Iterable:
        with open(file_path, "r") as data_file:
            for line in data_file:
                line_data = json.loads(line)
                text = line_data["query"]
                label = line_data["label"]
                instance = self.text_to_instance(text=text, label=label)
                if instance:
                    yield instance

    def text_to_instance(self, text: str, label: Union[str, int]) -> Instance:
        fields: Dict[str, Field] = {}
        tokens = self._tokenizer.tokenize(text)
        if self._max_sequence_length:
            tokens = self._truncated(tokens)
        fields["tokens"] = TextField(tokens, self._token_indexers)
        fields["label"] = LabelField(label, skip_indexing=self._skip_label_indexing)
        return Instance(fields)

    def _truncated(self, tokens):
        if len(tokens) > self._max_sequence_length:
            tokens = tokens[:self._max_sequence_length]
        return tokens
