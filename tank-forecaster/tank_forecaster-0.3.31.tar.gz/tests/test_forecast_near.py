import numpy as np
import pandas as pd
import pytest

from tank_forecaster import forecaster_advanced
from tank_forecaster.decomp import generic_hh_seasonality


def is_a_valid_forecast_dataframe(df):
    return (
        type(df) is pd.core.frame.DataFrame
        and len(df) == 144
        and "ds" in df
        and "yhat" in df
        and type(df.ds.iloc[-1]) is pd._libs.tslibs.timestamps.Timestamp
        and type(df.yhat.iloc[-1]) is np.float64
    )


# @pytest.mark.parameterize(
#     "daily_lift_est,hh_seasonality", [(1000, generic_hh_seasonality), (None, None)]
# )
# def test_near_approx_returns_a_valid_dataframe(daily_lift_est, hh_seasonality):


def test_near_approx_returns_a_valid_dataframe():
    x = forecaster_advanced.forecast_near_approx(
        daily_lift_est=100, hh_seasonality=generic_hh_seasonality
    )
    assert is_a_valid_forecast_dataframe(x)


def test_near_approx_returns_a_valid_dataframe_for_generic_input():
    x = forecaster_advanced.forecast_near_approx(
        daily_lift_est=1000, hh_seasonality=generic_hh_seasonality
    )
    assert is_a_valid_forecast_dataframe(x)


def test_near_returns_none_when_no_data():
    assert forecaster_advanced.forecast_near(None) is None


def test_near_full_data_returns_a_valid_dataframe(tank_full_data):
    x = forecaster_advanced.forecast_near(tank_history=tank_full_data)
    assert is_a_valid_forecast_dataframe(x)


def test_near_approx_start_date():
    pass


def test_near_start_date():
    pass
