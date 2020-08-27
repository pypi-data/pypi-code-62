import numpy as np
import pandas as pd

from tank_forecaster import forecaster_advanced
from tank_forecaster.decomp import (generic_weekly_seasonality,
                                    generic_yearly_seasonality)


def test_far():
    x = forecaster_advanced.forecast_far(
        daily_lift_est=5000,
        yearly_seasonality=generic_yearly_seasonality,
        weekly_seasonality=generic_weekly_seasonality,
    )
    assert type(x) is pd.core.frame.DataFrame
    assert "ds" in x and "yhat" in x
    assert len(x) == 90
    assert type(x.ds.iloc[-1]) is pd._libs.tslibs.timestamps.Timestamp
    assert type(x.yhat.iloc[-1]) is np.float64


def test_far_start_date():
    x = forecaster_advanced.forecast_far(
        daily_lift_est=5000,
        yearly_seasonality=generic_yearly_seasonality,
        weekly_seasonality=generic_weekly_seasonality,
        start_date="2020-01-01",
    )
    assert str(x.ds.iloc[0]) == "2020-01-01 00:00:00"
    assert len(x) == 90
    assert str(x.ds.iloc[-1]) == "2020-03-30 00:00:00"


if __name__ == "__main__":
    pass
