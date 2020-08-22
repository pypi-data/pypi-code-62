import io
import decimal
import pickle
from dataclasses import dataclass
import time
from collections import OrderedDict, defaultdict
import datetime
from pathlib import Path
from os.path import getsize, getmtime
from typing import List
from pprint import pformat

from boto3.exceptions import RetriesExceededError
from botocore.exceptions import EndpointConnectionError, ClientError
from typeguard import typechecked

from awsimple import AWSAccess
from awsimple.aws import log

# don't require pillow, but convert images with it if it exists
pil_exists = False
try:
    from PIL import Image

    pil_exists = True
except ImportError:
    pass


# Handles Inexact error.
decimal_context = decimal.getcontext().copy()
decimal_context.prec = 38  # Numbers can have 38 digits precision
handle_inexact_error = True


@typechecked(always=True)
def dict_to_dynamodb(input_value, convert_images: bool = True, raise_exception: bool = True):
    """
    makes a dictionary follow boto3 item standards

    :param input_value: input dictionary
    :param convert_images: set to False to skip over images (they can be too large)
    :param raise_exception: set to False to not raise exceptions on issues

    :return: converted version of the original dictionary

    """
    resp = None
    if type(input_value) is dict or type(input_value) is OrderedDict or type(input_value) is defaultdict:
        resp = {}
        for k, v in input_value.items():
            if type(k) is int:
                k = str(k)  # allow int as key since it is unambiguous (e.g. bool and float are ambiguous)
            resp[k] = dict_to_dynamodb(v, convert_images, raise_exception)
    elif type(input_value) is list or type(input_value) is tuple:
        # converts tuple to list
        resp = [dict_to_dynamodb(v, convert_images, raise_exception) for v in input_value]
    elif type(input_value) is str:
        # DynamoDB does not allow zero length strings
        if len(input_value) > 0:
            resp = input_value
    elif type(input_value) is bool or input_value is None or type(input_value) is decimal.Decimal:
        resp = input_value  # native DynamoDB types
    elif type(input_value) is float or type(input_value) is int:
        # boto3 uses Decimal for numbers
        # Handle the 'inexact error' via decimal_context.create_decimal
        # 'casting' to str may work as well, but decimal_context.create_decimal should be better at maintaining precision
        if handle_inexact_error:
            resp = decimal_context.create_decimal(input_value)
        else:
            resp = decimal.Decimal(input_value)
    elif convert_images and pil_exists and isinstance(input_value, Image.Image):
        # save pillow (PIL) image as PNG binary
        image_byte_array = io.BytesIO()
        input_value.save(image_byte_array, format="PNG")
        resp = image_byte_array.getvalue()
    elif isinstance(input_value, datetime.datetime):
        resp = input_value.isoformat()
    else:
        if raise_exception:
            raise NotImplementedError(type(input_value), input_value)
    return resp


@typechecked(always=True)
def _is_valid_db_pickled_file(file_path: Path, cache_life: (float, int, None)) -> bool:
    is_valid = file_path.exists() and getsize(str(file_path)) > 0
    if is_valid and cache_life is not None:
        is_valid = time.time() <= getmtime(str(file_path)) + cache_life
    return is_valid


@dataclass
class DynamoDBAccess(AWSAccess):
    table_name: str = None  # required

    def __post_init__(self):
        if self.table_name is None:
            log.error(f"{self.table_name=}")

    def get_dynamodb_resource(self):
        return self.get_resource("dynamodb")

    def get_dynamodb_client(self):
        return self.get_client("dynamodb")

    @typechecked(always=True)
    def get_table_names(self) -> List[str]:
        """
        get all DynamoDB tables
        :return: a list of DynamoDB table names
        """
        dynamodb_client = self.get_dynamodb_client()

        table_names = []
        more_to_evaluate = True
        last_evaluated_table_name = None
        while more_to_evaluate:
            if last_evaluated_table_name is None:
                response = dynamodb_client.list_tables()
            else:
                response = dynamodb_client.list_tables(ExclusiveStartTableName=last_evaluated_table_name)
            partial_table_names = response.get("TableNames")
            last_evaluated_table_name = response.get("LastEvaluatedTableName")
            if partial_table_names is not None and len(partial_table_names) > 0:
                table_names.extend(partial_table_names)
            if last_evaluated_table_name is None:
                more_to_evaluate = False
        table_names.sort()

        return table_names

    @typechecked(always=True)
    def scan_table(self) -> (list, None):
        """
        returns entire lookup table
        :param table_name: DynamoDB table name
        :param profile_name: AWS IAM profile name
        :return: table contents
        """

        items = []
        dynamodb = self.get_dynamodb_resource()
        table = dynamodb.Table(self.table_name)

        more_to_evaluate = True
        exclusive_start_key = None
        while more_to_evaluate:
            try:
                if exclusive_start_key is None:
                    response = table.scan()
                else:
                    response = table.scan(ExclusiveStartKey=exclusive_start_key)
            except EndpointConnectionError as e:
                log.warning(e)
                response = None
                more_to_evaluate = False
                items = None

            if response is not None:
                items.extend(response["Items"])
                if "LastEvaluatedKey" not in response:
                    more_to_evaluate = False
                else:
                    exclusive_start_key = response["LastEvaluatedKey"]

        if items is not None:
            log.info(f"read {len(items)} items from {self.table_name}")

        return items

    @typechecked(always=True)
    def scan_table_cached(self, cache_dir: Path = Path("cache"), invalidate_cache: bool = False, cache_life: float = None) -> (list, None):
        """

        Read data table(s) from AWS with caching.  This *requires* that the table not change during execution nor
        from run to run without setting invalidate_cache.

        :param table_name: DynamoDB table name
        :param profile_name: AWS IAM profile name
        :param cache_dir: cache dir
        :param invalidate_cache: True to initially invalidate the cache (forcing a table scan)
        :param cache_life: Life of cache in seconds (None=forever)
        :return: a list with the (possibly cached) table data
        """

        # todo: check the table size in AWS (since this is quick) and if it's different than what's in the cache, invalidate the cache first

        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file_path = Path(cache_dir, f"{self.table_name}.pickle")
        log.debug(f"cache_file_path : {cache_file_path.resolve()}")
        if invalidate_cache and cache_file_path.exists():
            cache_file_path.remove()

        output_data = None
        if _is_valid_db_pickled_file(cache_file_path, cache_life):
            with open(cache_file_path, "rb") as f:
                log.info(f"{self.table_name} : reading {cache_file_path}")
                output_data = pickle.load(f)
                log.debug(f"done reading {cache_file_path}")

        if not _is_valid_db_pickled_file(cache_file_path, cache_life):
            log.info(f"getting {self.table_name} from DB")

            try:
                table_data = self.scan_table()
            except RetriesExceededError:
                table_data = None

            if table_data is not None and len(table_data) > 0:
                output_data = table_data
                # update data cache
                with open(cache_file_path, "wb") as f:
                    pickle.dump(output_data, f)

        if output_data is None:
            log.error(f'table "{self.table_name}" not accessible')

        return output_data

    @typechecked(always=True)
    def create_table(self, hash_key: str, range_key: str = None) -> bool:

        def add_key(k, t, kt):
            assert t in ("S", "N", "B")  # DynamoDB key types (string, number, byte)
            assert kt in ("HASH", "RANGE")
            _d = {"AttributeName": k, "AttributeType": t}
            _s = {"AttributeName": k, "KeyType": kt}
            return _d, _s

        def type_to_attribute_type(v):
            if isinstance(v, str):
                t = "S"
            elif isinstance(v, int):
                t = "N"
            elif isinstance(v, bytes):
                t = "B"
            else:
                raise ValueError(type(v), v)
            return t

        client = self.get_dynamodb_client()
        d, s = add_key(hash_key, type_to_attribute_type(hash_key), "HASH")  # required
        attribute_definitions = [d]
        key_schema = [s]
        if range_key is not None:
            d, s = add_key(range_key, type_to_attribute_type(range_key), "RANGE")  # optional
            attribute_definitions.append(d)
            key_schema.append(s)
        log.info(pformat(key_schema, indent=4))

        try:
            client.create_table(AttributeDefinitions=attribute_definitions,
                                KeySchema=key_schema,
                                BillingMode="PAY_PER_REQUEST",  # on-demand
                                TableName=self.table_name)
            created = True
        except ClientError as e:
            log.warning(e)
            created = False

        return created

    def delete_table(self):
        client = self.get_dynamodb_client()
        client.delete_table(TableName=self.table_name)

    @typechecked(always=True)
    def table_exists(self) -> bool:
        assert self.table_name is not None
        return self.table_name in self.get_table_names()
