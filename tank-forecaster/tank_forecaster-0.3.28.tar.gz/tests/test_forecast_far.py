import pandas as pd
import numpy as np

from tank_forecaster import forecaster, forecaster_advanced


# before
forecaster.forecast_far(
    val,
    yearly_decomp=pd.Series(tc.yearly_seasonality),
    weekly_decomp=pd.Series(tc.dow_seasonality),
    forecast_length=90,
    daily_lift_est=tc.daily_lifting_estimate,
)

# after
forecaster_advanced.forecast_far(daily_lift_estimate = None, yearly_seasonality = None, weekly_seasonality = None,
             forecast_start = '2020-08-10', forecast_length = 90)





def test_far_none():
    x = forecaster.forecast_far(None, daily_lift_est=1000)
    assert type(x) is pd.core.frame.DataFrame
    assert 'ds' in x and 'yhat' in x
    assert len(x) == 90
    assert type(x.ds.iloc[-1]) is pd._libs.tslibs.timestamps.Timestamp
    assert type(x.yhat.iloc[-1]) is np.float64


def test_far_little_data(sales_little_data):
    x = forecaster.forecast_far(sales_little_data)
    assert type(x) is pd.core.frame.DataFrame
    assert 'ds' in x and 'yhat' in x
    assert len(x) == 90
    assert type(x.ds.iloc[-1]) is pd._libs.tslibs.timestamps.Timestamp
    assert type(x.yhat.iloc[-1]) is np.float64


def test_far_proper():
    pass



