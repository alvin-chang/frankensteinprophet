# frankensteinprophet
Frankenstein Prophet

A put-together by duck tape kind of software system that gives you:
![](Screenshot%202020-12-03%20at%2011.48.06.png)
![](Screenshot%202020-12-03%20at%2011.45.32.png)

<details>
  <summary>History</summary>

# Day 0
I was bored.

# Day 1
I started putting together a trading system. Obviously, I searched the internet for existing tools. Interestingly, I found [blog posts by Eric Brown](https://pythondata.com/stock-market-forecasting-with-prophet/) and took a copy of his [Jupyter Notebook](https://github.com/urgedata/pythondata/blob/master/fbprophet/fbprophet_market_forecasts.ipynb) to play with.
Previously, I was using Finance::QuoteHist [get_quotes](https://wiki.gnucash.org/wiki/Stocks/get_prices) with GnuCash to get prices into a CSV; hence it became quite handy.
Very soon, I glued together the get_prices, and made a new version called get_quotes2prophet to change the format to be accepted by Facebook Prophet, and fbprophet_market_forecasts.ipynb, and I had predictions for NYSE:JNJ. I was then using a Bash loop with awk to fetch the new CSV and ran each Jupyter Notebook manually. Ugly, I know.
# Day 2
Luckily, I found [yfinance](https://pypi.org/project/yfinance/) which allowed me to pull tickers directly into each Jupyter Notebook, that reduces a lot of ugly work, and made the system faster. Still, it's ugly as hell.
# Day 3
I was experimenting minute-by-minute trade information, and have predictions for the next day. The biggest hurdle was getting rid of any prediction after 16:00 and before 9:30. In the end, I was glueing together 10:00-16:00 (which was easy), but then made 9:30-9:59 with the intersection of 9 <= dt.hour < 10, and dt.minute >= 30. It was so ugly that I don't think I want to upload it.
# Day 4
First, I made the Jupyter Notebook run through a list of hard-coded symbols (ugly I know, but I was in a hurry helping a friend.) Now I'm pulling a list of tickers from a file, and run in series each prediction model. This is the point where I'm going to upload it to GitHub so anyone non-technical can use it. Well, you might have to get a Jupyter Notebook container running, or just run it on [mybinder.org](https://mybinder.org/v2/gh/jupyterlab/jupyterlab-demo/master?urlpath=lab/tree/demo).
# Day 5
I tried to make the prediction run in parallel by using multiprocessing.Pool() as shown in [SpikeLab's blog](https://medium.com/spikelab/forecasting-multiples-time-series-using-prophet-in-parallel-2515abd1a245). However, it doesn't work because of Python uses spawn instead of fork on Mac. Anyway, I had to use multiprocessing.Process() and do what the Pool() does, but manually because only Process() supports a shared dictionary between the main programme and the spawned process.
# Day 6
Programming is addictive, and now I made a rudimentary queue of the size of the number of CPU cores. What happened was instead of running all 32 predictions simultaneously from the day before, it now runs in the batches of the number of CPU you have.
# Day 7
Well, it's never done until it's done. In order to debug the mysterious failure, I've installed Jupyter Lab directly on my Mac Mini server. That comes with strange ["Python doesn't consider it a bug" **feature**](https://bugs.python.org/issue25053) that function must be defined in a separate file. Nevertheless, it's now reliably churning out S&P 500 and FTSE 100.
</details>
