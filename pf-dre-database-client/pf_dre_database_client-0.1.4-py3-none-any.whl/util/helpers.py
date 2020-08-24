# Built-in Modules
import os
from datetime import datetime, timedelta
from pathlib import Path

# Third Party Modules
import pandas as pd
import pytz
from dotenv import load_dotenv

# Local Timezone
brisbane_tz = pytz.timezone('Australia/Brisbane')

def get_db_client_kwargs():
    if os.environ.get('host') is None:
        __load_env()

    return {
        'dbname': os.environ.get('dbname'),
        'user': os.environ.get('user'),
        'password': os.environ.get('password'),
        'host': os.environ.get('host'),
        'port': os.environ.get('port'),
    }


def __load_env():
    env_path = Path('./') / '.env'
    load_dotenv(dotenv_path = env_path)


def offset_df(df, offset=10):
    """
    :param df: Dataframe to be updated
    :param offset: Offset in milliseconds
    """
    for index, row in df.iterrows():
        dt = datetime.strptime(row["measurement_date"],
                               "%Y-%m-%d %H:%M:%S +10:00") + \
             timedelta(milliseconds = offset)
        row["measurement_date"] = "{0} {1}".format(
            dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "+10:00")


def localize_df_datetimes(df):
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
    return df
