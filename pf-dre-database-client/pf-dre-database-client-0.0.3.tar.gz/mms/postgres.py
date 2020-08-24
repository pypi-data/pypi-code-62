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


class MMSClientOld:
    def __init__(self, **kwargs):
        self.engine = {}

    def write_df(self, df, use_index=True):
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


    def get_ids_for_device_codes(self, codes):
        """
        :param codes: A list of device codes (strings) to return the
        device id's for.
        :return: A 1 to 1 dictionary with key (device code)
        and value (device id) (All strings)
        """
        query = "SELECT code, id FROM devices WHERE code IN ('{0}')"\
            .format("','".join(codes))
        logger.debug("Executing Query: {0}".format(query))
        with self.engine.connect() as conn:
            df = pd.read_sql(query, con=conn, index_col='code')
        df['id'] = df['id'].apply(str)
        return dict(zip(list(df.index.values), list(df['id'].values)))

    def check_simulation_exists(self, sim, start, end):
        """
        :param sim: The name of the simulation
        :param start: The start date of the simulation
        :param end: Then end date of the simulation
        :return:
        """
        query = "SELECT COUNT(*) as count " \
                "FROM simulated_device_metrics " \
                "WHERE simulation = '{0}' " \
                "AND measurement_date >= '{1}'::timestamptz " \
                "AND measurement_date <= '{2}'::timestamptz " \
                "LIMIT 1".format(sim, start, end)
        logger.debug("Executing Query: {0}".format(query))
        with self.engine.connect() as conn:
            df = pd.read_sql(query, con = conn, index_col = 'count')
        if list(df.index.values)[0] > 0:
            query = "DELETE FROM simulated_device_metrics " \
                    "WHERE simulation = '{0}' " \
                    "AND measurement_date >= '{1}'::timestamptz " \
                    "AND measurement_date <= '{2}'::timestamptz "\
                .format(sim, start, end)
            raise KeyError("Simulation results already exist "
                           "for {0}. To clear run the following query in MMS: "
                           "{1}".format(sim, query))
        return False

    def initialize_sim_device(self, ref_ts, device_id, metrics, values, sim):
        """
        :param ref_ts: Relative timestamp
        :param device_id: Integer corresponding to the required device
        :param metrics: List of metrics to write values to
        :param values: List of values corresponding to the metrics.
        :param sim: Name of the simulation
        :return:
        """
        # TODO: Currently Initial states are defined in each controller. If
        #  the yml file for simulations is updated to include initial state,
        #  this function would be valueble to use.
        df = pd.DataFrame({
            'measurement_date': [ref_ts],
            'simulation': [sim],
            'device_id': [device_id],
            'device_metric_type_id': metrics,
            'value': values,
            'received_date': [ref_ts]
        })
        df.set_index('measurement_date', inplace=True)
        self.write_df(df)

    def get_latest_metrics(self, device_ids, metrics, sim = None):  # TODO: Need to group result be device_id

        if sim:
            query = "SELECT device_metric_type_id, last(measurement_date, " \
                    "measurement_date) AS \"measurement_date\", last(value, " \
                    "measurement_date) AS \"last\" " \
                    "FROM simulated_device_metrics " \
                    "WHERE device_id IN ('{0}') " \
                    "AND device_metric_type_id IN ('{1}') " \
                    "AND simulation = '{2}' " \
                    "AND measurement_date = received_date " \
                    "GROUP BY device_metric_type_id;"\
                .format("','".join([str(i) for i in device_ids]),
                        "','".join(metrics),
                        sim)
        else:
            query = "SELECT device_metric_type_id, last(measurement_date, " \
                    "measurement_date) AS \"measurement_date\", last(value, " \
                    "measurement_date) AS \"last\" " \
                    "FROM device_metrics " \
                    "WHERE device_id IN ('{0}') " \
                    "AND device_metric_type_id IN ('{1}') " \
                    "GROUP BY device_metric_type_id;"\
                .format("','".join([str(i) for i in device_ids]),
                        "','".join(metrics))
        return self.query_metrics(query)

    def get_latest_metrics_for_ref_t(self, ref_t, device_ids, metrics,
                                       sim=None, buffer=5):
        # TODO: Need to group result be device_id

        ref_t_start = ref_t - timedelta(minutes=buffer)
        ref_t_end = ref_t
        if sim:
            query = "SELECT device_metric_type_id, last(measurement_date, " \
                    "measurement_date) AS \"measurement_date\", last(value, " \
                    "measurement_date) AS \"last\" " \
                    "FROM simulated_device_metrics " \
                    "WHERE measurement_date BETWEEN '{0}' AND '{1}' " \
                    "AND device_id IN ('{2}') " \
                    "AND device_metric_type_id IN ('{3}') " \
                    "AND simulation = '{4}' " \
                    "AND measurement_date = received_date " \
                    "GROUP BY device_id, device_metric_type_id;"\
                .format(ref_t_start,
                        ref_t_end,
                        "','".join([str(i) for i in device_ids]),
                        "','".join(metrics),
                        sim)
        else:
            query = "SELECT device_metric_type_id, last(measurement_date, " \
                    "measurement_date) AS \"measurement_date\", last(value, " \
                    "measurement_date) AS \"last\" " \
                    "FROM device_metrics " \
                    "WHERE measurement_date BETWEEN '{0}' AND '{1}' " \
                    "AND device_id IN ('{2}') " \
                    "AND device_metric_type_id IN ('{3}') " \
                    "GROUP BY device_id, device_metric_type_id;"\
                .format(ref_t_start,
                        ref_t_end,
                        "','".join([str(i) for i in device_ids]),
                        "','".join(metrics))
        return self.query_metrics(query)

    def query_metrics(self, query):
        """
        These are timescale DB queries and should be called for fetching timeseries
        data only
        :param query:
        :return:
        """

        logger.info("Running query: \n{0}".format(query))

        with self.engine.connect() as conn:
            df = pd.read_sql(query, con=conn, index_col='measurement_date')
            # Convert datetime columns to brisbane local time
            if df.empty:
                return df  # The data frame is empty, no metrics found
            df.index = pd.to_datetime(df.index).tz_convert(brisbane_tz)
            if 'received_date' in df and df['received_date'].values is not None:
                df['received_date'] = pd.to_datetime(df['received_date']) \
                    .tz_convert(brisbane_tz)
            if 'created_date' in df and df['created_date'].values is not None:
                df['created_date'] = pd.to_datetime(df['created_date']) \
                    .tz_convert(brisbane_tz)
            if 'modified_date' in df and df['modified_date'].values is not None:
                df['modified_date'] = pd.to_datetime(df['modified_date']) \
                    .tz_convert(brisbane_tz)
            # logger.info(df.dtypes)
            # logger.info(df.index.dtype)
            logger.debug("Query Finished")
            return df

    def close(self):
        self.engine.dispose()
