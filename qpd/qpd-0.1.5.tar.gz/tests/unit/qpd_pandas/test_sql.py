from typing import Any

import pandas as pd

from qpd.dataframe import Column, DataFrame
from qpd_pandas import QPDPandasEngine
from qpd_test.sql_suite import SQLTests


class SQLTests(SQLTests.Tests):
    def to_pandas_df(self, df: Any) -> pd.DataFrame:
        if isinstance(df, DataFrame):
            return self.op.to_native(df)
        elif isinstance(df, pd.DataFrame):
            return df
        else:
            raise ValueError(df)

    def to_pandas_series(self, col: Column) -> pd.Series:
        return col.native

    def make_qpd_engine(self):
        return QPDPandasEngine()

    def to_native_df(self, data: Any, columns: Any) -> Any:  # pragma: no cover
        if isinstance(data, pd.DataFrame):
            return data
        return pd.DataFrame(data, columns=columns)
