"""
Time series-specific data testing and cleaning functions.
"""

import pandas as pd
import pandas_flavor as pf
from janitor import check


@pf.register_dataframe_method
def fill_missing_timestamps(
    df: pd.DataFrame,
    frequency: str,
    first_time_stamp: pd.Timestamp = None,
    last_time_stamp: pd.Timestamp = None,
) -> pd.DataFrame:
    """
    Fill dataframe with missing timestamps based on a defined frequency.

    If timestamps are missing,
    this function will reindex the dataframe.
    If timestamps are not missing,
    then the function will return the dataframe unmodified.
    Example usage:
    .. code-block:: python

        df = (
            pd.DataFrame(...)
            .fill_missing_timestamps(frequency="1H")
        )

    :param df: Dataframe which needs to be tested for missing timestamps
    :param frequency: frequency i.e. sampling frequency of the data.
        Acceptable frequency strings are available
        `here <https://pandas.pydata.org/pandas-docs/stable/>`_
        Check offset aliases under time series in user guide
    :param first_time_stamp: timestamp expected to start from
        Defaults to None.
        If no input is provided assumes the minimum value in time_series
    :param last_time_stamp: timestamp expected to end with.
        Defaults to None.
        If no input is provided, assumes the maximum value in time_series
    :returns: dataframe that has a complete set of contiguous datetimes.
    """
    # Check all the inputs are the correct data type
    check("frequency", frequency, [str])
    check("first_time_stamp", first_time_stamp, [pd.Timestamp, type(None)])
    check("last_time_stamp", last_time_stamp, [pd.Timestamp, type(None)])

    if first_time_stamp is None:
        first_time_stamp = df.index.min()
    if last_time_stamp is None:
        last_time_stamp = df.index.max()

    # Generate expected timestamps
    expected_timestamps = pd.date_range(
        start=first_time_stamp, end=last_time_stamp, freq=frequency
    )

    return df.reindex(expected_timestamps)


def _get_missing_timestamps(
    df: pd.DataFrame,
    frequency: str,
    first_time_stamp: pd.Timestamp = None,
    last_time_stamp: pd.Timestamp = None,
) -> pd.DataFrame:
    """
    Return the timestamps that are missing in a dataframe.

    This function takes in a dataframe,
    and checks its index against a dataframe
    that contains the expected timestamps.
    Here, we assume that the expected timestamps
    are going to be of a larger size
    than the timestamps available in the input dataframe ``df``.

    If there are any missing timestamps in the input dataframe,
    this function will return those missing timestamps
    from the expected dataframe.
    """
    expected_df = df.fill_missing_timestamps(
        frequency, first_time_stamp, last_time_stamp
    )

    missing_timestamps = expected_df.index.difference(df.index)

    return expected_df.loc[missing_timestamps]
