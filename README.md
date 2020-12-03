# frankensteinprophet
Frankanstein Prophet

A put-together by duck tape kind of software system that gives you:
![](Screenshot%202020-12-03%20at%2011.48.06.png)
![](Screenshot%202020-12-03%20at%2011.45.32.png)

# Day 0
I was bored.

# Day 1
This week, yah, since 4 days ago, I started putting together a trading system. Obviously, I searched the internet for existing tools. Interestingly, I found blog posts by Eric Brown at https://pythondata.com/stock-market-forecasting-with-prophet/, and took a copy of https://github.com/urgedata/pythondata/blob/master/fbprophet/fbprophet_market_forecasts.ipynb to play with.
Previously, I was using Finance::QuoteHist by Gnucash from https://wiki.gnucash.org/wiki/Stocks/get_prices to get prices into a CSV, hence it became quite handy.
Very soon, I glued together the get_prices, and made a new version called get_quotes2prophet to change the format to be accepted by Facebook Prophet, and fbprophet_market_forecasts.ipynb, and I had predictions for NYSE:JNJ. I was then using a Bash loop with awk to fetch the new CSV, and ran each Jupyter Notebook manually. Ugly, I know.
# Day 2
Luckily, I found https://pypi.org/project/yfinance/ which allowed me to pull tickers directly into each Jupyter Notebook, that really reduces a lot of ugly work, and made the system faster. Still, it's ugly as hell.
# Day 3
I was experiementing minute-by-minute trade information, and have predictions for the next day. The biggest hurdle, actually, was getting rid of any prediction after 16:00 and before 9:30. At the end, I was glueing together 10:00-16:00 (which was easy), but then made 9:30-9:59 with intersection of 9 <= dt.hour < 10, and dt.minute >= 30. It was so ugly that I don't think I want to upload it.
# Day 4
First, I made the Jupyter Notebook run through a list of hard-coded symbols (ugly I know, but I was in a hurry helping a friend.) Now I'm pulling list of tickers from a file, and run in series each prediction model. This is the point where I'm going to upload it to GitHub so anyone non-technical can use it. Well, you might have to get a Jupyter Notebook container running, or run just run it on https://mybinder.org/v2/gh/jupyterlab/jupyterlab-demo/master?urlpath=lab/tree/demo

# TODO
Follow https://medium.com/spikelab/forecasting-multiples-time-series-using-prophet-in-parallel-2515abd1a245 to make calculations parallel. I know making a serial loop above defeats the purpose of making it parallel, but you always have to weigh up pros and cons.
