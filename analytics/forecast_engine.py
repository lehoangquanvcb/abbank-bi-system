import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def simple_forecast(df, column, periods=3):
    data = df[["date", column]].dropna().copy()
    data["t"] = range(len(data))

    X = data[["t"]]
    y = data[column]

    model = LinearRegression()
    model.fit(X, y)

    future_t = np.arange(len(data), len(data) + periods).reshape(-1, 1)
    forecast = model.predict(future_t)

    last_date = data["date"].max()
    future_dates = pd.date_range(last_date, periods=periods + 1, freq="ME")[1:]

    return pd.DataFrame({
        "date": future_dates,
        "variable": column,
        "forecast": forecast
    })


def run_forecast(macro, abbank):
    fx_fc = simple_forecast(macro, "usd_vnd", 3)
    on_fc = simple_forecast(macro, "vnibor_on", 3)
    cpi_fc = simple_forecast(macro, "cpi", 3)
    nim_fc = simple_forecast(abbank, "nim", 3)

    return pd.concat([fx_fc, on_fc, cpi_fc, nim_fc], ignore_index=True)
