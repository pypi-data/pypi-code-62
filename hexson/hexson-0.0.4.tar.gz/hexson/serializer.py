#!/usr/bin/env python3
# Json library support hex escape.
from .dumpper import Dumpper
from .parser import Parser
import uuid
from datetime import date, datetime
from decimal import Decimal

INTEGER_TYPES = ()
FLOAT_TYPES = (Decimal,)
TIME_TYPES = (date, datetime)

try:
    import numpy as np

    INTEGER_TYPES += (
        np.int_,
        np.intc,
        np.int8,
        np.int16,
        np.int32,
        np.int64,
        np.uint8,
        np.uint16,
        np.uint32,
        np.uint64,
    )
    FLOAT_TYPES += (
        np.float_,
        np.float16,
        np.float32,
        np.float64,
    )
except ImportError:
    np = None

try:
    import pandas as pd

    TIME_TYPES += (pd.Timestamp,)
except ImportError:
    pd = None


class JSONSerializer(object):
    mimetype = "application/json"

    def default(self, data):
        if isinstance(data, TIME_TYPES):
            return data.isoformat()
        elif isinstance(data, uuid.UUID):
            return str(data)
        elif isinstance(data, FLOAT_TYPES):
            return float(data)
        elif INTEGER_TYPES and isinstance(data, INTEGER_TYPES):
            return int(data)

        # Special cases for numpy and pandas types
        elif np:
            if isinstance(data, np.bool_):
                return bool(data)
            elif isinstance(data, np.datetime64):
                return data.item().isoformat()
            elif isinstance(data, np.ndarray):
                return data.tolist()
        if pd:
            if isinstance(data, (pd.Series, pd.Categorical)):
                return data.tolist()
            elif hasattr(pd, "NA") and pd.isna(data):
                return None

        raise TypeError("Unable to serialize %r (type: %s)" % (data, type(data)))

    def loads(self, s):
        return Parser(s).parse_from_json()
    
    def dumps(self, data):
        return Dumpper(data).dump_to_json()
