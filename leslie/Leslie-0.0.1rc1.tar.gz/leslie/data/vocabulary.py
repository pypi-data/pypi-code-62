# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com

@version: 1.0
@file: vocabulary.py
@time: 2019/12/19 9:48

这一行开始写关于本文件的说明与解释

A Vocabulary maps strings to integers, allowing for strings to be mapped to an
out-of-vocabulary token.
"""
import codecs
import copy
import logging
import os
from collections import defaultdict
from typing import Callable, Dict, Iterable, List, Optional, Set, Union
from leslie.common.params import Params
from tqdm import tqdm

from leslie.common.registrable import Registrable
from leslie.common.checks import ConfigurationError
from leslie.common.util import namespace_match

DEFAULT_NON_PADDED_NAMESPACES = ("*tags", "*labels")
DEFAULT_PADDING_TOKEN = "@@PADDING@@"
DEFAULT_OOV_TOKEN = "@@UNKNOWN@@"
NAMESPACE_PADDING_FILE = 'non_padded_namespaces.txt'

logger = logging.getLogger(__name__)


class _NamespaceDependentDefaultDict(defaultdict):
    def __init__(self,
                 non_padded_namespaces: Iterable[str],
                 padded_function: Callable[[], any],
                 non_padded_function: Callable[[], any]) -> None:
        self._non_padded_namespaces = set(non_padded_namespaces)
        self._padded_function = padded_function
        self._non_padded_function = non_padded_function
        super(_NamespaceDependentDefaultDict, self).__init__()

    def __missing__(self, key: str):
        if any(namespace_match(pattern, key) for pattern in self._non_padded_namespaces):
            value = self._non_padded_function()
        else:
            value = self._padded_function()
        dict.__setitem__(self, key, value)
        return value

    def add_non_padded_namespaces(self, non_padded_namespaces: Set[str]):
        # add non_padded_namespaces which weren't already present
        self._non_padded_namespaces.update(non_padded_namespaces)


class _TokenToIndexDefaultDict(_NamespaceDependentDefaultDict):
    def __init__(self, non_padded_namespaces: Set[str], padding_token: str, oov_token: str) -> None:
        super(_TokenToIndexDefaultDict, self).__init__(
            non_padded_namespaces, lambda: {padding_token: 0, oov_token: 1}, lambda: {}
        )


class _IndexToTokenDefaultDict(_NamespaceDependentDefaultDict):
    def __init__(self, non_padded_namespaces: Set[str], padding_token: str, oov_token: str) -> None:
        super(_IndexToTokenDefaultDict, self).__init__(
            non_padded_namespaces, lambda: {0: padding_token, 1: oov_token}, lambda: {}
        )


def _read_pretrained_tokens(embeddings_file_uri: str) -> List[str]:
    # todo
    return []


def pop_max_vocab_size(params: Params) -> Union[int, Dict[str, int]]:
    """
    max_vocab_size limits the size of the vocabulary, not including the @@UNKNOWN@@ token.
    max_vocab_size is allowed to be either an int or a Dict[str, int] (or nothing).
    But it could also be a string representing an int (in the case of environment variable
    substitution). So we need some complex logic to handle it.
    """
    size = params.pop("max_vocab_size", None, keep_as_dict=True)

    if isinstance(size, dict):
        # This is the Dict[str, int] case.
        return size
    elif size is not None:
        # This is the int / str case.
        return int(size)
    else:
        return None


class Vocabulary(Registrable):
    def __init__(self,
                 counter: Dict[str, Dict[str, int]] = None,
                 min_count: Dict[str, int] = None,
                 max_vocab_size: Union[int, Dict[str, int]] = None,
                 non_padded_namespaces: Iterable[str] = DEFAULT_NON_PADDED_NAMESPACES,
                 pretrained_files: Optional[Dict[str, str]] = None,
                 only_include_pretrained_words: bool = False,
                 tokens_to_add: Dict[str, List[str]] = None,
                 min_pretrained_embeddings: Dict[str, int] = None,
                 padding_token: Optional[str] = DEFAULT_PADDING_TOKEN,
                 oov_token: Optional[str] = DEFAULT_OOV_TOKEN,
                 ) -> None:
        self._padding_token = padding_token if padding_token is not None else DEFAULT_PADDING_TOKEN
        self._oov_token = oov_token if oov_token is not None else DEFAULT_OOV_TOKEN

        self._non_padded_namespaces = set(non_padded_namespaces)

        self._token_to_index = _TokenToIndexDefaultDict(
            self._non_padded_namespaces, self._padding_token, self._oov_token
        )
        self._index_to_token = _IndexToTokenDefaultDict(
            self._non_padded_namespaces, self._padding_token, self._oov_token
        )

        self._retained_counter: Optional[Dict[str, Dict[str, int]]] = None
        # Made an empty vocabulary, now extend it.
        self._extend(
            counter,
            min_count,
            max_vocab_size,
            non_padded_namespaces,
            pretrained_files,
            only_include_pretrained_words,
            tokens_to_add,
            min_pretrained_embeddings,
        )

    def __getstate__(self):
        """
        Need to sanitize default_dict and default_like objects
        by converting them to vanilla dicts when we pickle the vocabulary.
        """
        state = copy.copy(self.__dict__)
        state["_token_to_idx"] = dict(state["_token_to_idx"])

    def __setstate__(self, state):
        """
        Conversely, when we unpickle, we need to reload the plain dicts
        into our special DefaultDict subclasses.
        """

        self.__dict__ = copy.copy(state)
        self._token_to_index = _TokenToIndexDefaultDict(
            self._non_padded_namespaces, self._padding_token, self._oov_token
        )
        self._token_to_index.update(state["_token_to_index"])
        self._index_to_token = _IndexToTokenDefaultDict(
            self._non_padded_namespaces, self._padding_token, self._oov_token
        )
        self._index_to_token.update(state["_index_to_token"])

    def _extend(
            self,
            counter: Dict[str, Dict[str, int]] = None,
            min_count: Dict[str, int] = None,
            max_vocab_size: Union[int, Dict[str, int]] = None,
            non_padded_namespaces: Iterable[str] = DEFAULT_NON_PADDED_NAMESPACES,
            pretrained_files: Optional[Dict[str, str]] = None,
            only_include_pretrained_words: bool = False,
            tokens_to_add: Dict[str, List[str]] = None,
            min_pretrained_embeddings: Dict[str, int] = None,
    ) -> None:
        if not isinstance(max_vocab_size, dict):
            int_max_vocab_size = max_vocab_size
            max_vocab_size = defaultdict(lambda: int_max_vocab_size)  # type: ignore
        min_count = min_count or {}
        pretrained_files = pretrained_files or {}
        min_pretrained_embeddings = min_pretrained_embeddings or {}
        non_padded_namespaces = set(non_padded_namespaces)
        counter = counter or {}
        tokens_to_add = tokens_to_add or {}

        self._retained_counter = counter
        # Make sure vocabulary extension is safe.
        current_namespaces = {*self._token_to_index}
        extension_namespaces = {*counter, *tokens_to_add}

        for namespace in current_namespaces & extension_namespaces:
            # if new namespace was already present
            # Either both should be padded or none should be.
            original_padded = not any(
                namespace_match(pattern, namespace) for pattern in self._non_padded_namespaces
            )
            extension_padded = not any(
                namespace_match(pattern, namespace) for pattern in non_padded_namespaces
            )
            if original_padded != extension_padded:
                raise ConfigurationError(
                    "Common namespace {} has conflicting ".format(namespace)
                    + "setting of padded = True/False. "
                    + "Hence extension cannot be done."
                )

        # Add new non-padded namespaces for extension
        self._token_to_index.add_non_padded_namespaces(non_padded_namespaces)
        self._index_to_token.add_non_padded_namespaces(non_padded_namespaces)
        self._non_padded_namespaces.update(non_padded_namespaces)

        for namespace in counter:
            if namespace in pretrained_files:
                pretrained_list = _read_pretrained_tokens(pretrained_files[namespace])
                min_embeddings = min_pretrained_embeddings.get(namespace, 0)
                if min_embeddings > 0:
                    tokens_old = tokens_to_add.get(namespace, [])
                    tokens_new = pretrained_list[:min_embeddings]
                    tokens_to_add[namespace] = tokens_old + tokens_new
                pretrained_set = set(pretrained_list)
            else:
                pretrained_set = None
            token_counts = list(counter[namespace].items())
            token_counts.sort(key=lambda x: x[1], reverse=True)
            try:
                max_vocab = max_vocab_size[namespace]
            except KeyError:
                max_vocab = None
            if max_vocab:
                token_counts = token_counts[:max_vocab]
            for token, count in token_counts:
                if pretrained_set is not None:
                    if only_include_pretrained_words:
                        if token in pretrained_set and count >= min_count.get(namespace, 1):
                            self.add_token_to_namespace(token, namespace)
                    elif token in pretrained_set or count >= min_count.get(namespace, 1):
                        self.add_token_to_namespace(token, namespace)
                elif count >= min_count.get(namespace, 1):
                    self.add_token_to_namespace(token, namespace)

        for namespace, tokens in tokens_to_add.items():
            for token in tokens:
                self.add_token_to_namespace(token, namespace)

    def add_token_to_namespace(self, token: str, namespace: str = "tokens") -> int:
        """
        Adds ``token`` to the index, if it is not already present.  Either way, we return the index of
        the token.
        """
        if not isinstance(token, str):
            raise ValueError(
                "Vocabulary tokens must be strings, or saving and loading will break."
                "  Got %s (with type %s)" % (repr(token), type(token))
            )
        if token not in self._token_to_index[namespace]:
            index = len(self._token_to_index[namespace])
            self._token_to_index[namespace][token] = index
            self._index_to_token[namespace][index] = token
            return index
        else:
            return self._token_to_index[namespace][token]

    def get_token_index(self, token: str, namespace: str = "tokens") -> int:
        if token in self._token_to_index[namespace]:
            return self._token_to_index[namespace][token]
        else:
            try:
                return self._token_to_index[namespace][self._oov_token]
            except KeyError:
                raise

    def get_token_from_index(self, index: int, namespace: str = "tokens") -> str:
        return self._index_to_token[namespace][index]

    @classmethod
    def from_instances(
            cls,
            instances: Iterable["adi.Instance"],
            min_count: Dict[str, int] = None,
            max_vocab_size: Union[int, Dict[str, int]] = None,
            non_padded_namespaces: Iterable[str] = DEFAULT_NON_PADDED_NAMESPACES,
            pretrained_files: Optional[Dict[str, str]] = None,
            only_include_pretrained_words: bool = False,
            tokens_to_add: Dict[str, List[str]] = None,
            min_pretrained_embeddings: Dict[str, int] = None,
            padding_token: Optional[str] = DEFAULT_PADDING_TOKEN,
            oov_token: Optional[str] = DEFAULT_OOV_TOKEN,
    ) -> "Vocabulary":
        """
        Constructs a vocabulary given a collection of `Instances` and some parameters.
        We count all of the vocabulary items in the instances, then pass those counts
        and the other parameters, to :func:`__init__`.  See that method for a description
        of what the other parameters do.
        """
        padding_token = padding_token if padding_token is not None else DEFAULT_PADDING_TOKEN
        oov_token = oov_token if oov_token is not None else DEFAULT_OOV_TOKEN
        namespace_token_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for instance in tqdm(instances):
            instance.count_vocab_items(namespace_token_counts)

        return cls(
            counter=namespace_token_counts,
            min_count=min_count,
            max_vocab_size=max_vocab_size,
            non_padded_namespaces=non_padded_namespaces,
            pretrained_files=pretrained_files,
            only_include_pretrained_words=only_include_pretrained_words,
            tokens_to_add=tokens_to_add,
            min_pretrained_embeddings=min_pretrained_embeddings,
            padding_token=padding_token,
            oov_token=oov_token,
        )

    def get_vocab_size(self, namespace: str = "tokens") -> int:
        return len(self._token_to_index[namespace])

    @classmethod
    def from_files(
            cls,
            directory: str,
            padding_token: Optional[str] = DEFAULT_PADDING_TOKEN,
            oov_token: Optional[str] = DEFAULT_OOV_TOKEN,
    ) -> "Vocabulary":
        """
        Loads a ``Vocabulary`` that was serialized using ``save_to_files``.
        Parameters
        ----------
        directory : ``str``
            The directory containing the serialized vocabulary.
            :param directory:
            :param padding_token:
            :param oov_token:
        """
        logger.info("Loading token dictionary from %s.", directory)
        padding_token = padding_token if padding_token is not None else DEFAULT_PADDING_TOKEN
        oov_token = oov_token if oov_token is not None else DEFAULT_OOV_TOKEN
        vocab = cls(
            padding_token=padding_token,
            oov_token=oov_token,
        )

        # Check every file in the directory.
        for namespace_filename in os.listdir(directory):
            if namespace_filename.startswith("."):
                continue
            namespace = namespace_filename.replace(".txt", "")
            if any(namespace_match(pattern, namespace) for pattern in DEFAULT_NON_PADDED_NAMESPACES):
                is_padded = False
            else:
                is_padded = True
            filename = os.path.join(directory, namespace_filename)
            vocab.set_from_file(filename, is_padded, namespace=namespace, oov_token=oov_token)

        return vocab

    def set_from_file(
            self,
            filename: str,
            is_padded: bool = True,
            oov_token: str = DEFAULT_OOV_TOKEN,
            namespace: str = "tokens",
    ):
        """
        If you already have a vocabulary file for a trained model somewhere, and you really want to
        use that vocabulary file instead of just setting the vocabulary from a dataset, for
        whatever reason, you can do that with this method.  You must specify the namespace to use,
        and we assume that you want to use padding and OOV tokens for this.
        Parameters
        ----------
        filename : ``str``
            The file containing the vocabulary to load.  It should be formatted as one token per
            line, with nothing else in the line.  The index we assign to the token is the line
            number in the file (1-indexed if ``is_padded``, 0-indexed otherwise).  Note that this
            file should contain the OOV token string!
        is_padded : ``bool``, optional (default=True)
            Is this vocabulary padded?  For token / word / character vocabularies, this should be
            ``True``; while for tag or label vocabularies, this should typically be ``False``.  If
            ``True``, we add a padding token with index 0, and we enforce that the ``oov_token`` is
            present in the file.
        oov_token : ``str``, optional (default=DEFAULT_OOV_TOKEN)
            What token does this vocabulary use to represent out-of-vocabulary characters?  This
            must show up as a line in the vocabulary file.  When we find it, we replace
            ``oov_token`` with ``self._oov_token``, because we only use one OOV token across
            namespaces.
        namespace : ``str``, optional (default="tokens")
            What namespace should we overwrite with this vocab file?
        """
        # if is_padded:
        #     self._token_to_index[namespace] = {self._padding_token: 0}
        #     self._index_to_token[namespace] = {0: self._padding_token}
        # else:
        #     self._token_to_index[namespace] = {}
        #     self._index_to_token[namespace] = {}
        #  取消is_pad判断
        self._token_to_index[namespace] = {}
        self._index_to_token[namespace] = {}

        with codecs.open(filename, "r", "utf-8") as input_file:
            lines = input_file.read().split("\n")
            # Be flexible about having final newline or not
            if lines and lines[-1] == "":
                lines = lines[:-1]
            for i, line in enumerate(lines):
                index = i + 1 if is_padded else i
                token = line.replace("@@NEWLINE@@", "\n")
                if token == oov_token:
                    token = self._oov_token
                self._token_to_index[namespace][token] = index
                self._index_to_token[namespace][index] = token
        # if is_padded:
        assert self._oov_token in self._token_to_index[namespace], "OOV token not found!"

    @classmethod
    def from_params(cls, params: Params, instances: Iterable["adi.Instance"] = None):
        """
        There are two possible ways to build a vocabulary; from a
        collection of instances, using :func:`Vocabulary.from_instances`, or
        from a pre-saved vocabulary, using :func:`Vocabulary.from_files`.
        You can also extend pre-saved vocabulary with collection of instances
        using this method. This method wraps these options, allowing their
        specification from a ``Params`` object, generated from a JSON
        configuration file.
        Parameters
        ----------
        params: Params, required.
        instances: Iterable['adi.Instance'], optional
            If ``params`` doesn't contain a ``directory_path`` key,
            the ``Vocabulary`` can be built directly from a collection of
            instances (i.e. a dataset). If ``extend`` key is set False,
            dataset instances will be ignored and final vocabulary will be
            one loaded from ``directory_path``. If ``extend`` key is set True,
            dataset instances will be used to extend the vocabulary loaded
            from ``directory_path`` and that will be final vocabulary used.
        Returns
        -------
        A ``Vocabulary``.
        """

        # Vocabulary is ``Registrable`` so that you can configure a custom subclass,
        # but (unlike most of our registrables) almost everyone will want to use the
        # base implementation. So instead of having an abstract ``VocabularyBase`` or
        # such, we just add the logic for instantiating a registered subclass here,
        # so that most users can continue doing what they were doing.
        vocab_type = params.pop("type", None)
        if vocab_type is not None:
            return cls.by_name(vocab_type).from_params(params=params, instances=instances)

        extend = params.pop("extend", False)
        vocabulary_directory = params.pop("directory_path", None)
        if not vocabulary_directory and not instances:
            raise ConfigurationError(
                "You must provide either a Params object containing a "
                "vocab_directory key or a Dataset to build a vocabulary from."
            )
        if extend and not instances:
            raise ConfigurationError(
                "'extend' is true but there are not instances passed to extend."
            )
        if extend and not vocabulary_directory:
            raise ConfigurationError(
                "'extend' is true but there is not 'directory_path' to extend from."
            )

        if vocabulary_directory and instances:
            if extend:
                logger.info("Loading Vocab from files and extending it with dataset.")
            else:
                logger.info("Loading Vocab from files instead of dataset.")

        padding_token = params.pop("padding_token", DEFAULT_PADDING_TOKEN)
        oov_token = params.pop("oov_token", DEFAULT_OOV_TOKEN)

        if vocabulary_directory:
            vocab = cls.from_files(vocabulary_directory, padding_token, oov_token)
            if not extend:
                params.assert_empty("Vocabulary - from files")
                return vocab
        if extend:
            vocab.extend_from_instances(params, instances=instances)
            return vocab
        min_count = params.pop("min_count", None, keep_as_dict=True)
        max_vocab_size = pop_max_vocab_size(params)
        non_padded_namespaces = params.pop("non_padded_namespaces", DEFAULT_NON_PADDED_NAMESPACES)
        pretrained_files = params.pop("pretrained_files", {}, keep_as_dict=True)
        min_pretrained_embeddings = params.pop("min_pretrained_embeddings", None)
        only_include_pretrained_words = params.pop_bool("only_include_pretrained_words", False)
        tokens_to_add = params.pop("tokens_to_add", None)
        params.assert_empty("Vocabulary - from dataset")
        return cls.from_instances(
            instances=instances,
            min_count=min_count,
            max_vocab_size=max_vocab_size,
            non_padded_namespaces=non_padded_namespaces,
            pretrained_files=pretrained_files,
            only_include_pretrained_words=only_include_pretrained_words,
            tokens_to_add=tokens_to_add,
            min_pretrained_embeddings=min_pretrained_embeddings,
            padding_token=padding_token,
            oov_token=oov_token,
        )

    def save_to_files(self, directory: str) -> None:
        """
        Persist this Vocabulary to files so it can be reloaded later.
        Each namespace corresponds to one file.
        Parameters
        ----------
        directory : ``str``
            The directory where we save the serialized vocabulary.
        """
        os.makedirs(directory, exist_ok=True)
        if os.listdir(directory):
            logging.warning("vocabulary serialization directory %s is not empty", directory)

        with codecs.open(os.path.join(directory, NAMESPACE_PADDING_FILE), 'w', 'utf-8') as namespace_file:
            for namespace_str in self._non_padded_namespaces:
                print(namespace_str, file=namespace_file)

        for namespace, mapping in self._index_to_token.items():
            # Each namespace gets written to its own file, in index order.
            with codecs.open(os.path.join(directory, namespace + '.txt'), 'w', 'utf-8') as token_file:
                num_tokens = len(mapping)
                # start_index = 1 if mapping[0] == self._padding_token else 0    ## 这里取消对is_pad的判断
                for i in range(0, num_tokens):
                    print(mapping[i].replace('\n', '@@NEWLINE@@'), file=token_file)
