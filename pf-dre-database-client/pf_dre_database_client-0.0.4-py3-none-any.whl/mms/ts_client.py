#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The following client is used to read data to and write data from the postgres
Meter Management System which includes TiescaleDB for meter metric data.
"""

# Built-in Modules
import logging
from io import StringIO

# Third Party Modules
import pandas as pd
import pytz
import psycopg2
from psycopg2 import sql

# Project Specific Modules
from mms.util import helpers

# Logging
logger = logging.getLogger('timescale')

# Local Timezone
brisbane_tz = pytz.timezone('Australia/Brisbane')


class TimescaleClient:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def insert_df(self, df, table, use_index=True):
        """
        Write a pandas data frame into a timescale table (Row-By-Row).
        :param df: Data frame matching the schema of 'table' in the MMS.
        :param table: The database table that the data will be inserted into
        :param use_index: True if the measurement_date is the index of the
        dataframe. If a generic pandas index is used in df, 'use_index' = False.
        """
        try:
            if use_index:
                df.index = df.index.tz_localize('UTC')
            with psycopg2.connect(**self.kwargs) as conn:
                # Write the points to simulated_device_metrics table
                df.to_sql(name = table,
                          con = conn,
                          index = use_index,
                          if_exists = 'append')
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s".format(error))

    def copy_df_from_stringio(self, df, table):
        """
        Save the dataframe in memory and use copy_from() to copy it to
        the table
        :param df: Data frame matching the schema of 'table' in the MMS.
        The index of the data frame will always be measurement_date
        :param table: The database table that the data will be inserted into
        :return: True if successful
        """
        s_buf = StringIO()
        df.to_csv(s_buf, index_label='measurement_date', header = False)

        try:
            conn = psycopg2.connect(**self.kwargs)
            with conn.cursor() as cursor:
                cursor.copy_from(s_buf, table, sep=',')
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s".format(error))


class TimeScaleClientNarrow(TimescaleClient):
    def __init__(self, **kwargs):
        TimescaleClient.__init__(**kwargs)

    def get_latest_metrics(self, device_ids, metrics):
        query = sql.SQL(
            "SELECT device_metric_type_id, "
            "last(measurement_date, measuremenet_date),"
            "last(value, measurement_date) AS \"last\" "
            "FROM device_metrics"
            "WHERE device_id IN ({}) "
            "AND device_metric_type_id IN ({}) "
            "GROUP BY device_id, device_metric_type_id")\
            .format(sql.SQL(',').join(sql.Placeholder() * len(device_ids)),
                    sql.SQL(',').join(sql.Placeholder() * len(metrics)))
        with psycopg2.connect(**self.kwargs) as conn:
            df = pd.read_sql(query,
                             con = conn,
                             index_col = 'measurement_date',
                             params=(device_ids, metrics))
            return helpers.localize_df_datetimes(df)

