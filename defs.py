def run_prophet(tickers,ticker,market_dfset,modelset,forecastset):
    from fbprophet import Prophet
    import numpy as np
    import yfinance as yf

    market_df = yf.Ticker(ticker).history(period="max",auto_adjust=True,prepost=True)
    if len(market_df) == 0:
        tickers.remove(ticker)
        #return
    #market_df = market_df[~market_df.index.duplicated()]
    df = market_df.reset_index().rename(columns={'Date':'ds', 'Close':'y'})
    df['y'] = np.log(df['y'])
    model = Prophet(weekly_seasonality=False,)
    model.fit(df)
    future = model.make_future_dataframe(periods=365) #forecasting for 1 year from now.
    forecast = model.predict(future) 
    modelset[ticker] = model
    market_dfset[ticker] = market_df
    forecastset[ticker] = forecast
    
def run_prophet_daily(tickers,ticker,market_dfset,modelset,forecastset):
    from fbprophet import Prophet
    import pandas as pd
    import numpy as np
    import yfinance as yf
    from datetime import date,timedelta
    
    market_df = yf.download(tickers=ticker,start=(date.today()+timedelta(days=-29)).strftime("%Y-%m-%d"),end=(date.today()+timedelta(days=-29+6)).strftime("%Y-%m-%d"),interval="1m").tz_localize(None)
    for i in range(1,5): market_df = market_df.append(yf.download(tickers=ticker,start=(date.today()+timedelta(days=-29+6*i)).strftime("%Y-%m-%d"),end=(date.today()+timedelta(days=-29+6+6*i)).strftime("%Y-%m-%d"),interval="1m").tz_localize(None))
    if len(market_df) == 0:
        tickers.remove(ticker)
        #return
    #market_df = market_df[~market_df.index.duplicated()]
    df = market_df.reset_index().rename(columns={'Datetime':'ds', 'Close':'y'})
    df['y'] = np.log(df['y'])
    model = Prophet(changepoint_prior_scale=0.01,daily_seasonality=True,weekly_seasonality=False,yearly_seasonality=False)
    model.fit(df);
    future = model.make_future_dataframe(periods=1*24*60,freq="1min") #forecasting for 1 day from now.
    future2 = future.copy()
    future2 = pd.merge(future2[future2['ds'].dt.hour > 9 ],future2[future2['ds'].dt.hour < 16],how='inner')
    future3 = future.copy()
    future3 = pd.merge(future3[future3['ds'].dt.hour >= 9 ],future3[future3['ds'].dt.hour < 10],how='inner')
    future3 = future3[future3['ds'].dt.minute >=30]
    future = future3.append(future2)
    forecast = model.predict(future)
    modelset[ticker] = model
    market_dfset[ticker] = market_df
    forecastset[ticker] = forecast

def run_neuralprophet(tickers,ticker,market_dfset,modelset,forecastset):
    from neuralprophet import NeuralProphet
    import yfinance as yf

    market_df = yf.Ticker(ticker).history(period="max",auto_adjust=True,prepost=True)[['Close']]
    if len(market_df) == 0:
        tickers.remove(ticker)
        #return
    #market_df = market_df[~market_df.index.duplicated()]
    df = market_df.reset_index().rename(columns={'Date':'ds', 'Close':'y'})
    future_periods = 30
    model = NeuralProphet(n_forecasts=future_periods,
    n_lags= future_periods * 2 - 1,
    #n_lags=len(df),
    n_changepoints=100,
    #yearly_seasonality=True,
    #weekly_seasonality=False,
    #daily_seasonality=False,
    batch_size=64,
    epochs=100,
    learning_rate=1.0)
    #model = NeuralProphet(    n_forecasts=future_periods,
    #n_lags=future_periods * 2 - 1,
    ##n_lags = len(df),
    ##n_lags=5,
    #yearly_seasonality=True,
    #weekly_seasonality=False,
    #daily_seasonality=False,)
    metrics = model.fit(df, validate_each_epoch=True, 
                    valid_p=0.2, freq='D', 
                    plot_live_loss=True, 
                    epochs=100)
    #metrics = model.fit(df, validate_each_epoch=True, valid_p=0.2, freq="D")
    #future = model.make_future_dataframe(df, periods=future_periods, n_historic_predictions=len(df))
    future = model.make_future_dataframe(df, periods=future_periods, n_historic_predictions=True)
    forecast = model.predict(future)
    model.highlight_nth_step_ahead_of_each_forecast(step_number=model.n_forecasts)
    modelset[ticker] = model
    market_dfset[ticker] = market_df
    forecastset[ticker] = forecast
    
def plot_forecast(model, data, periods, historic_pred=True, highlight_steps_ahead=None):
  
    """ plot_forecast function - generates and plots the forecasts for a NeuralProphet model
    - model -> a trained NeuralProphet model
    - data -> the dataframe used for training
    - periods -> the number of periods to forecast
    - historic_pred -> a flag indicating whether or not to plot the model's predictions on historic data
    - highlight_steps_ahead -> the number of steps ahead of the forecast line to highlight, used for autoregressive models only"""
    
    future = model.make_future_dataframe(data, 
                                         periods=periods, 
                                         n_historic_predictions=historic_pred)
    forecast = model.predict(future)
    
    if highlight_steps_ahead is not None:
        model = model.highlight_nth_step_ahead_of_each_forecast(highlight_steps_ahead)
        model.plot_last_forecast(forecast)
    else:    
        model.plot(forecast)