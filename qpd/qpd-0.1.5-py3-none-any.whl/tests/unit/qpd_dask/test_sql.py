from typing import Any

import dask.dataframe as pd
import pandas

from qpd.dataframe import Column, DataFrame
from qpd_dask import QPDDaskEngine
from qpd_test.sql_suite import SQLTests


class SQLTests(SQLTests.Tests):
    def test_agg_first_last(self):
        a = ([[1, "x", None], [2, None, 3.5]], ["a", "b", "c"])
        self.assert_eq(
            dict(a=a),
            """
            SELECT
                a,
                FIRST(b) AS a1,
                LAST(b) AS a2,
                FIRST_VALUE(c) AS a3,
                LAST_VALUE(c) AS a4
            FROM a GROUP BY a
            """,
            [[1, "x", "x", None, None], [2, None, None, 3.5, 3.5]],
            ["a", "a1", "a2", "a3", "a4"],
        )

    def test_agg_first_last_no_group_by(self):
        return

    def test_order_by_no_limit(self):
        return

    def test_window_count(self):
        return

    def test_window_lead_lag(self):
        return

    def test_window_min_max(self):
        return

    def test_window_ranks(self):
        return

    def test_window_row_number(self):
        return

    def test_window_sum_avg(self):
        return

    def to_pandas_df(self, df: Any) -> pandas.DataFrame:
        if isinstance(df, DataFrame):
            return self.op.to_native(df).compute()
        elif isinstance(df, pd.DataFrame):
            return df.compute()
        elif isinstance(df, pandas.DataFrame):
            return df
        else:
            raise ValueError(df)

    def to_pandas_series(self, col: Column) -> pandas.Series:
        return pandas.Series(col.native.to_dask_array().compute(), name=col.name)

    def make_qpd_engine(self):
        return QPDDaskEngine()

    def to_native_df(self, data: Any, columns: Any) -> Any:
        if isinstance(data, pd.DataFrame):
            return data
        if isinstance(data, pandas.DataFrame):
            return pd.from_pandas(data, npartitions=2)
        pdf = pandas.DataFrame(data, columns=columns)
        return pd.from_pandas(pdf, npartitions=2)
