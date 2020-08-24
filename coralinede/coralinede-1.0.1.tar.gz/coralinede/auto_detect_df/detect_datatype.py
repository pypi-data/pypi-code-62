import operator
import sqlalchemy
import pandas as pd
import numpy as np
from math import ceil

DEFAULT_VARCHAR_LENGTH=100

def get_detected_column_types(df):
    """ Get data type of each columns ('DATETIME', 'NUMERIC' or 'STRING')

    Parameters:
        df (df): pandas dataframe

    Returns
        df (df): dataframe that all datatypes are converted (df)
    """

    assert isinstance(df, pd.DataFrame), 'Parameter must be DataFrame'

    for c in df.columns:
        # Convert column to string
        col_data = df[c].map(str)
        col_data = col_data.replace("NaT", None)
        col_data = col_data.replace("NaN", None)

        # Check NULL column
        if(df[c].isnull().values.all()):
            continue

        # Check DATETIME
        try:
            # Check if it's able to convert column to datetime

            # if column is datetime, then skip to convert
            if 'datetime' in str(col_data.dtype):
                continue

            df[c] = pd.to_datetime(col_data)
            continue
        except ValueError:
            pass

        # Check NUMERIC
        try:
            # Drop NaN rows
            series = df[c].dropna()

            # if column_name is int or float, then skip to convert
            if 'int' in str(col_data.dtype) or 'float' in str(col_data.dtype):
                continue

            # Check if it can be converted to numeric
            df[c] = pd.to_numeric(series)

        except ValueError:
            pass

    return df


def get_max_length_columns(df):
    """ find maximum length of value in each column and ceil it

    Parameters:
        df (df): dataframe
    Returns
        arr_max_len_columns (array): array of length for each column
        arr_max_decimal (array): array of maximum decimal for float, double, and decimal datatype, otherwise its value is zero
    """

    assert isinstance(df, pd.DataFrame), 'Parameter must be DataFrame'

    measurer = np.vectorize(len)
    arr_max_len_columns = []
    arr_max_decimal = []

    for i, x in enumerate(measurer(df.values.astype(str)).max(axis=0)):

        if 'float' in str(df.iloc[:, i].dtype):
            col_data = df.iloc[:, i].map(str).str.extract('\.(.*)')
            max_decimal = measurer(col_data.values.astype(str)).max(axis=0)[0]
            arr_max_decimal.append(max_decimal)
        else:
            arr_max_decimal.append(0)

        arr_max_len_columns.append(ceil(x / 10) * 10)

    return arr_max_len_columns, arr_max_decimal


def convert_df_datatype_to_sqlalchemy_datatype(df):
    """ convert dataframe's data type into SQLAlchemy's data type

    Parameters:
        df (df): dataframe

    Returns:
        dtype_dict (dict): dict of data type of each column in SQLAlchemy standard
    """

    assert isinstance(df, pd.DataFrame), 'Parameter must be DataFrame'

    arr_max_len_columns, arr_max_decimal = get_max_length_columns(df)

    dtype_dict = {}

    for i, col_name in enumerate(df.columns):
        if(df[col_name].isnull().values.all()):
            dtype_dict[col_name] = sqlalchemy.types.VARCHAR(DEFAULT_VARCHAR_LENGTH)
        elif 'bool' in str(df[col_name].dtype):
            # Compatible with SQL-Server and MySQL, since MySQL doesn't have BOOLEAN.
            dtype_dict[col_name] = sqlalchemy.types.INTEGER()
        elif 'int' in str(df[col_name].dtype):
            dtype_dict[col_name] = sqlalchemy.types.INTEGER()
        elif 'float' in str(df[col_name].dtype):
            if df[col_name].dropna().apply(float.is_integer).all():
                dtype_dict[col_name] = sqlalchemy.types.INTEGER()
            else:
                dtype_dict[col_name] = sqlalchemy.types.DECIMAL(precision=arr_max_len_columns[i], scale=arr_max_decimal[i])
        elif 'datetime' in str(df[col_name].dtype):
            dtype_dict[col_name] = sqlalchemy.types.DateTime()
        elif 'object' in str(df[col_name].dtype):
            # check the limit of varhcar, if the length exeeds, then use TEXT
            if arr_max_len_columns[i] > 1000:
                dtype_dict[col_name] = sqlalchemy.types.Text()
            else:
                dtype_dict[col_name] = sqlalchemy.types.VARCHAR(length=arr_max_len_columns[i])
        else:
            dtype_dict[col_name] = sqlalchemy.types.VARCHAR(length=arr_max_len_columns[i])

    return dtype_dict


def get_datatype_each_col(df):
    """ main function to call sub-function in order to find data type and data length for each column

    Parameters:
        df (df): dataframe

    Returns:
        dtype_dict (dict): dict of data type of each column in SQLAlchemy standard (dict)
    """

    assert isinstance(df, pd.DataFrame), 'Parameter must be DataFrame'

    df = get_detected_column_types(df)

    dtype_dict = convert_df_datatype_to_sqlalchemy_datatype(df)

    del df

    return dtype_dict