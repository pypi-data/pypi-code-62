
import json
import logging
import math
import re
import sys
import uuid
from abc import abstractmethod
from collections import namedtuple
from datetime import datetime
from enum import Enum
from functools import wraps
from typing import Mapping, Sequence, Any, Callable

import stringcase

from bitmast_blockcypher.config import ConfigManager

from bitmast_blockcypher.errors import BaseError

http_code = namedtuple('HttpCode', ('code', 'status', 'message'))

logger = logging.getLogger(__file__)

block_cypher_config = ConfigManager(name='block_cypher')

user_config = ConfigManager(name='config')

crypto_currency_config = ConfigManager(name='crypto_currency')


class CryptoAssets(Enum):
    # ('btc', 'btc-testnet', 'doge', 'dash', 'ltc', 'bcy')
    BITCOIN = 'BITCOIN'
    BITCOIN_TESTNET = 'BITCOIN_TESTNET'
    LITECOIN = 'LITECOIN'
    DASH = 'DASH'
    ETHEREUM = 'ETHEREUM'


# define set of regex patterns for known field types

email_pattern = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
wallet_pattern = wallet_id_pattern = identifier_pattern = id_pattern = enterprise_pattern = \
    enterprise_pattern_id = key_id_pattern = pending_approval_id_pattern = user_id_pattern = \
    shared_id_pattern = transfer_id_pattern = webhook_id_pattern = r'^[0-9a-f]{32}$'


def validate_coin(coin: Any):
    if isinstance(coin, str):
        coin = crypto_currency_config.get_by_value('identifier', coin.upper())
    elif isinstance(coin, Enum):
        coin = crypto_currency_config.get_by_value('identifier', str(coin.value).upper())
    return coin or False


def validate(data: Any, name: str, **kwargs):
    """Validate the various passphrase types used as parameters for url or form fields"""

    def _check_bool_types(a: bool):
        return isinstance(a, bool)

    def _check_list(a: Any):
        if isinstance(a, Sequence):
            return bool(a)

    def _check_datetime_types(a: datetime):
        return isinstance(a, datetime)

    def _check_dict_types(a: Mapping, keys: Sequence = None, values: Sequence = None):
        if not isinstance(a, Mapping):
            return False
        elif keys and values:
            allowed_keys = [x for x in keys if isinstance(x, str) and len(x) < 256]
            _dict = dict(zip(allowed_keys, values))
            return bool(_dict)

    def _check_float_types(arg: float, value: float = None, start: float = None,
                           end: float = None,
                           approved: Sequence = None):
        if not isinstance(arg, float):
            return False
        float_max = float('inf')
        float_min = float('-inf')

        try:
            _arg = arg if (arg < float_max) and (arg > float_min) else None
            if value:
                return math.isclose(_arg, value)
            if end:
                return _arg <= end
            if start:
                return _arg >= start

            approved_values = [x for x in approved if isinstance(x, float)] \
                if isinstance(approved, Sequence) else []
            if approved_values:
                return _arg in approved_values
            return bool(_arg)
        except ValueError:
            return False
        except Exception:
            return False

    def _check_int_types(arg: int, value: int = None, start: int = None, end: int = None,
                         approved: Sequence = None):
        if not isinstance(arg, int):
            return False
        int_min = -sys.maxsize - 1
        int_max = sys.maxsize
        try:
            _arg = int(arg) if (arg < int_max) and (arg > int_min) else None

            if value:
                return _arg == value
            if end:
                return _arg <= end
            if start:
                return _arg >= start

            approved_values = [x for x in approved if isinstance(x, int)] \
                if isinstance(approved, Sequence) else []
            if approved_values:
                return _arg in approved_values
            return bool(_arg)
        except ValueError:
            return False
        except Exception:
            return False

    def _check_str_list(a: Sequence, patterns: Any = None, length: int = None,
                        approved: Sequence = None):
        if not isinstance(a, (str, list, tuple)):
            return False

        if not (patterns or length or approved):
            return len(a) < 256

        if isinstance(patterns, (tuple, list)) and length:
            approved_patterns = map(lambda x: re.compile(x), patterns)
            return all([
                x for x in approved_patterns if
                x.match(a) and (len(a) < 256 or len(a) <= length)
            ])
        if isinstance(patterns, str):
            if re.compile(patterns).match(a):
                return True
            else:
                return False
        if isinstance(approved, Sequence):
            return a in approved
        return bool(a)

    def _check_uuid_types(a: uuid.UUID):
        if isinstance(a, uuid.UUID):
            return True
        elif isinstance(a, (str, int, bytes, tuple)):
            try:
                if isinstance(a, str):
                    return uuid.UUID(hex=a) and True
                elif isinstance(a, int):
                    return uuid.UUID(int=a) and True
                elif isinstance(a, bytes):
                    return (uuid.UUID(bytes=a) or uuid.UUID(bytes_le=a)) and True
                elif isinstance(a, tuple):
                    return uuid.UUID(fields=a)
            except ValueError:
                return False

    boolean_fields = ('double_spend', 'opt_in_rbf', 'spent', 'wait_guarantee', 'hasMore', 'has_more', 'hd',
                      'double_spend', 'enable_confirmations', 'finished', 'started', 'more')
    datetime_fields = ('time', 'received_time', 'received', 'confirmed', 'created_at', 'completed_at')
    mapping_fields = ('hd_wallet', 'args', 'tx', 'wallet',)
    float_fields = ('confidence', 'process_fees_percent',)
    int_fields = (
        'value', 'value_satoshis', 'amount', 'ver', 'callback_errors', 'process_fees_satoshis', 'mining_fees_satoshis',
        'page', 'height', 'peer_count', 'high_fee_per_kb', 'medium_fee_per_kb', 'low_fee_per_kb', 'unconfirmed_count',
        'last_fork_height', 'depth', 'total', 'fees', 'size', 'bits', 'nonce', 'n_tx', 'block_height', 'lock_time',
        'vin_sz', 'vout_sz', 'confirmations', 'receive_count', 'block_index', 'output_index', 'output_value',
        'sequence',
        'age', 'age_millis', 'tx_input_n', 'tx_output_n', 'ref_balance', 'total_received', 'total_sent', 'balance',
        'unconfirmed_balance', 'final_balance', 'unconfirmed_n_tx', 'final_n_tx', 'index')
    str_list_fields = ('txids', 'addresses', 'tosign', 'signatures', 'pubkeys', 'tosign_tx', 'txs')
    list_fields = (
        'errors', 'inputs', 'outputs', 'results', 'chain_addresses', 'chains', 'subchain_indexes', 'txs', 'inputs',
        'inputs', 'outputs', 'outputs', 'txrefs', 'unconfirmed_txrefs')
    str_fields = (
        'name', 'hash', 'previous_hash', 'last_fork_hash', 'chain', 'relayed_by', 'prev_block', 'mrkl_root',
        'preference', 'change_address', 'block_hash', 'double_of', 'data_protocol', 'hex', 'prev_hash', 'script_type',
        'script', 'wallet_name', 'wallet_token', 'spent_by', 'data_hex', 'data_string', 'txhash', 'address', 'tx_hash',
        'data', 'token', 'encoding', 'from_pubkey', 'from_private', 'from_wif', 'to_address', 'public', 'private',
        'wif', 'original_address', 'oap_address', 'extended_public_key', 'path', 'metadata', 'assetid', 'asset_id',
        'oap_meta', 'id', 'identifier', 'event', 'destination', 'input_address', 'process_fees_address',
        'input_transaction_hash', 'transaction_hash', 'analytics_engine', 'ticket', 'latest_url', 'previous_url',
        'prev_block_url', 'tx_url', 'next_txids', 'next_inputs', 'next_outputs', 'txurl', 'url', 'callback_url',
        'result_path', 'next_page',)

    if name in boolean_fields:
        return _check_bool_types(data)
    elif name in list_fields:
        return _check_list(data)
    elif name in datetime_fields:
        return _check_datetime_types(data)
    elif name in mapping_fields:
        return _check_dict_types(data, **kwargs)
    elif name in int_fields:
        return _check_int_types(data, **kwargs)
    elif name in float_fields:
        return _check_float_types(data, **kwargs)
    elif name in str_list_fields or data in str_fields:
        return _check_str_list(data, **kwargs)
    else:
        return False


class BusinessDataObject:
    # define a structure holding elements that can be updated only through a defined interface
    _fields = []
    data = dict()

    def __init__(self, *args, **kwargs):
        if kwargs:
            self._fields = list(kwargs.keys())
            self.data.update(kwargs)
            for k, v in kwargs.items():
                setattr(self, k, v)
            self.__bon__ = kwargs.get('business_object_name') or self.__class__.__qualname__
        super(BusinessDataObject, self).__init__()

    def as_dict(self):
        update = vars(self)
        self.data.update(update)
        return self.data

    @abstractmethod
    def send(self, url: str, query: Any = None, payload: Any = None, others: Any = None):
        # Sends a business object as request to specified url with payload, query being HTTP request data, files etc.
        return NotImplemented


def network_log(level=logging.WARNING, error=None, message=None):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.basicConfig(filename=user_config.option('logging', 'log'))
            logger = logging.getLogger(func.__name__)
            try:
                return func(*args, **kwargs)
            except error:
                log_msg = "%s: %s" % (error, message) if error and message else \
                    (error, str(error))
                logger.log(level, log_msg)
            except BaseError:
                app_error = BaseError(*args, **kwargs)
                logging.warning("Request: %s\nResponse: %s" % (
                    app_error.request, app_error.response))
            finally:
                logger.log(level, sys.exc_info()[0])

        return wrapper

    return decorate


def parser(*, encoder=None, target=None, bon=None):
    """
    Provide a convenient means of parsing server responses to target object types.
    The parsing operation will require that the outcome is either a dictionary or key-value
    pair, a string or bytes which can be parsed or dump by json (default) or any order
    encoding/decoding class.
    :param encoder: callable or function that can be used to parse returned object of the
    wrapped function to target object
    :param target: a class that can be used to parse returned object of wrapped function to
    target object.
    :param bon: a user defined name of the target business object
    :return: target object generated from parsing a server response
    """

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            outcome = func(*args, **kwargs)
            _target = None
            if isinstance(target, BusinessDataObject):
                _target = target.__class__(name=bon)
                if isinstance(outcome, Mapping):
                    _target.data.update(outcome)

            if callable(encoder) and isinstance(outcome, (str, bytes)):
                return encoder(outcome)
            elif isinstance(outcome, str) and isinstance(_target, BusinessDataObject):
                try:
                    params = json.loads(outcome)
                    return _target.__init__(**params)
                except ValueError:
                    logger.warning(ValueError)
            else:
                return outcome

        return wrapper

    return decorate


def data_converter(fields: Sequence, data: Mapping):
    # create dictionary from fields and corresponding values
    _fields = dict()
    if isinstance(data, Mapping):
        keys = data.keys()
        for k in keys:
            if stringcase.snakecase(k) in fields:
                _fields[(stringcase.snakecase(k))] = data[k]
            elif k in fields:
                _fields[k] = data[k]
        return _fields


def extract_data(field: str, data: Mapping, sentinel: Any = None):
    # Extract given field from possibly nested data structure
    if isinstance(data, Mapping):
        if field in data:
            return data.get(field, None)
        for k, v in data.items():
            if isinstance(v, Mapping):
                value = extract_data(field, v)
                if value is not sentinel:
                    return value


class Command:
    __slots__ = '_rank', '_label', '_cmd', '_group', '_args', '_kwargs'

    def __init__(self, cmd: Callable, group: Any, rank: Any, label: str = None, *args,
                 **kwargs) -> None:
        """
        @param cmd: defines the callable object which represents a command
        @param group: string identifying a command by friendly user name
        @param rank: a hashable type or int depicting the rank of a command
        where it belongs to a family or group.
        The rank can be used to order commands if a group of commands in
        the same family are to be prioritized and
        executed.
        @param args: list of positional parameters for the command
        @param kwargs: list of keyword parameters for the command
        """
        self._rank = None
        self._args = []
        self._kwargs = {}
        self._group = None
        self._cmd = None
        self._label = None
        if isinstance(rank, int) or isinstance(rank, Enum):
            self._rank = rank
        if isinstance(args, Sequence):
            self._args = [*args]
        if isinstance(kwargs, Mapping):
            self._kwargs = {**kwargs}
        if isinstance(label, str) and label.isalnum():
            self._label = label
        if isinstance(group, str):
            self._group = group if group.isalnum() and len(group) < 50 else None
        elif isinstance(group, Enum):
            self._group = group
        if callable(cmd):
            self._cmd = cmd

    def __call__(self, *args, **kwargs):
        if isinstance(args, Sequence):
            self._args += [*args]
        if isinstance(kwargs, dict):
            self._kwargs.update(**kwargs)
        _args = self._args.copy()
        _kwargs = self._kwargs.copy()
        return self._cmd(*_args, **_kwargs)

    @property
    def rank(self):
        return self._rank

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        raise RuntimeError('Attribute cannot be modified')

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, value):
        self._cmd = value if callable(value) else lambda: None

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        raise RuntimeError('Attribute cannot be modified')

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        if isinstance(value, Sequence) and len(value):
            self._args.append(*value)

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value):
        if isinstance(value, dict) and len(value):
            self._kwargs.update(**value)


class ServiceCommand(Command):

    def __init__(self, cmd: Callable, group: Any = None, rank: Any = None, label: str = None,
                 *args,
                 **kwargs) -> None:
        super(ServiceCommand, self).__init__(cmd, group, rank, label, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super(ServiceCommand, self).__call__(*args, **kwargs)
