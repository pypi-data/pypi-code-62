#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The following client is used to read data to and write data from the postgres
Meter Management System which includes TiescaleDB for meter metric data.
"""

# Built-in Modules
import logging
from io import StringIO
from datetime import timedelta

# Third Party Modules
import pandas as pd
import pytz
import psycopg2
from psycopg2 import sql

# Logging
logger = logging.getLogger('timescale')

# Local Timezone
brisbane_tz = pytz.timezone('Australia/Brisbane')


class TimescaleClientJSON:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def insert_df(self, df, table, use_index=True):
        """
        Write a pandas data frame into a timescale table (Row-By-Row).
        :param df: Data frame matching the schema of 'table' in the MMS.
        The index of the data frame will always be measurement_date
        :param table: The database table that the data will be inserted into
        :param use_index: True if the measurement_date is the index of the
        dataframe. If a generic integer index is used in df, use_index is False.
        """
        try:
            if use_index:
                df.index = df.index.tz_localize('UTC')
            with psycopg2.connect(**self.kwargs) as conn:
                # Write the points to simulated_device_metrics table
                df.to_sql(name=table,
                          con=conn,
                          index = use_index,
                          if_exists='append')
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s".format(error))

    def copy_df(self, df, use_index=True):
        """
        Write a pandas data frame into a timescale table.
        :param df: Data frame matching the schema of the
        simulated_device_metrics timescale table in the MMS.

        :param use_index: True if the measurement_date is the index of the
        dataframe. If a generic integer index is used in df, use_index is False.
        """
        if 'simulation' not in df:
            logger.error("Cannot write to device_metrics table.")
        else:
            df.index = df.index.tz_localize('UTC')
            with self.engine.connect() as conn:
                # Write the points to simulated_device_metrics table
                df.to_sql(name='simulated_device_metrics',
                          con=conn,
                          index=use_index,
                          if_exists='append')
