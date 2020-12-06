def run_prophet(ticker,market_dfset,modelset,forecastset):
    import pandas as pd
    import numpy as np
    import yfinance as yf
    from fbprophet import Prophet
    from fbprophet.plot import add_changepoints_to_plot
    import multiprocessing as mp
    from datetime import date,timedelta
    import time as t
    import matplotlib.pyplot as plt
    market_df = yf.Ticker(ticker).history(period="max")
    df = market_df.reset_index().rename(columns={'Date':'ds', 'Close':'y'})
    df['y'] = np.log(df['y'])
    model = Prophet(daily_seasonality=False,weekly_seasonality=False,yearly_seasonality=20)
    model.fit(df)
    future = model.make_future_dataframe(periods=365) #forecasting for 1 year from now.
    forecast = model.predict(future) 
    modelset[ticker] = model
    market_dfset[ticker] = market_df
    forecastset[ticker] = forecast
