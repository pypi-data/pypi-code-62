from datetime import datetime

import numpy as np
import pandas as pd
from sparkles import trunc_date

from tank_forecaster.decomp import generic_weekly_decomp, generic_yearly_decomp


def forecast_far(
    daily_lift_est,
    yearly_seasonality,
    weekly_seasonality,
    start_date=None,
    forecast_length=None,
):
    if start_date is None:
        start_date = trunc_date(datetime.now())

    if forecast_length is None:
        forecast_length = 90

    # generate predictions DataFrame, week of year and day of week used to match to generated future df
    predictions = pd.DataFrame(columns=["woy", "dow", "base", "weekly", "daily"])
    predictions["woy"] = np.repeat(range(1, 54), 7)  # 52.14 'week of year' -> 53
    predictions["dow"] = [0, 1, 2, 3, 4, 5, 6] * 53  # 7 'day of week' each week of year

    # base level is entered as argument in function, accounts for no seasonality
    predictions["base"] = daily_lift_est

    # weekly lifting estimates are calculated via base * 7 * weekly curve
    weekly = np.repeat(predictions.base.iloc[1] * 7 * generic_yearly_decomp, 7)
    weekly.index = range(0, 371)
    predictions["weekly"] = weekly

    # daily lifting estimates are calculated via weekly / 7 * day of week curve
    weekly_decomp_rep = pd.concat([generic_weekly_decomp] * 53, ignore_index=True)
    predictions["daily"] = predictions.weekly * (1 / 7) * weekly_decomp_rep

    # generate prediction interval as specified in function arguments
    future = pd.date_range(start=start_date, freq="1D", periods=forecast_length)
    future = pd.DataFrame(future)
    future.rename(columns={0: "ds"}, inplace=True)

    # need to generate day of week and week of year to match with predictions
    future["dow"] = future.ds.dt.weekday
    future["woy"] = future.ds.dt.week
    output = pd.merge(
        future, predictions, left_on=["woy", "dow"], right_on=["woy", "dow"]
    )

    # reduce output to datestamp, estimate, upper and lower
    output = output[["ds", "daily"]]
    output.rename(columns={"daily": "yhat"}, inplace=True)

    output["lower"] = output["yhat"] - 2 * output["yhat"].std()
    output["upper"] = output["yhat"] + 2 * output["yhat"].std()

    # non-negative predictions
    for field in ["yhat", "lower", "upper"]:
        output.loc[output[field] < 0, field] = 0

    return output


if __name__ == "__main__":
    forecast_far(
        daily_lift_est=5000,
        yearly_seasonality=generic_yearly_decomp,
        weekly_seasonality=generic_weekly_decomp,
    )
