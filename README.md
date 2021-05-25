# Hot_Stocks

Hey there! You have stumbled upon the student project "Hot Stocks", which is part of the course "Skills: Programming - Introduction Level" by Mario Silic (Spring Semester 2021 at the University of St.Gallen).

The end goal of our group project was to create an application with which you can follow a common RSI buy/sell strategy. We limited our scope to the S&P 100 Stocks found on: [S&P 100 - Wikipedia](https://de.wikipedia.org/wiki/S%26P_100)

If you want to find out more about our project, check out our code and read more below. 

## Table of contents
- [General Information](#general-information)
- [Technologies](#technologies)
- [Setup](#setup)
- [Program Structure](#program-structure)
- [Authors](#authors)
- [Appendix - Libraries Description](#appendix---libraries-description)


## General Information
The goal of this project is to provide the user with an efficient way of receiving potential trade suggestions using the common [oversold/overbought RSI (Relative Strength Index) strategy](https://www.dailyfx.com/education/technical-analysis-tools/overbought-vs-oversold-and-what-this-means-for-traders.html). In this strategy stocks are classified as overbought, oversold or neither. Using this strategy we are interested in the oversold and overbought stocks. We identify those stocks by calculating the RSI. When a stock has an RSI of more than 70, the stock is considered overbought and a common strategy is shorting/selling the aforementioned stock. The opposite case applies when the stock has an RSI of less than 30. This means it is oversold and one should consider longing/buying this stock.

Besides this the user can also select a stock from the S&P100 to and check the RSI and stockprice manually.

The reason we did not make a trading bot is that the common overbought/oversold strategy should not be the only factor that is considered for a trade. Volatility and other numerous factors play a big role and should not be reduced down to a small calculation.

The suggestions provided by our tool should be seen as what they are — suggestions. Trading is a complicated affair and our tool does not offer financial advice.

## Technologies
- Python Version: 3.8.5
- Jupyter Notebook: To install Juypter Notebook, please refer to https://jupyter.org/install
- Libraries used: `streamlit`, `pandas`, `yfinance`, `plotly`, `base64`

For further library descriptions refer to [Appendix - Libraries Description](#appendix---libraries-description).

## Setup
To run this application, it is recommended to use a Jupyter Notebook. 

The easiest way to get all required libraries would be to run the [Startup](Startup.ipynb) file. This file runs the following commands:

```
!pip install streamlit
!pip install pandas
!pip install yfinance
!pip install plotly
```
and 

```
!streamlit run Hot_Stocks.py
```

These commands install the necessary modules and run the [Hot Stocks](Hot_Stocks.py) application.

If you are having trouble opening the application, check if your [Hot Stocks](Hot_Stocks.py) file is in the right directory.
It needs to be in the default Anaconda run location to function, or you have to start it manually with the Anaconda Console by going to the right directory.

In most cases your default Anaconda directory is `C:\Users\Username`.

If you decide to run the application from the command prompt, use `streamlit run Hot_Stocks.py` after navigating to the right directory.

We recommend that you use the light theme of streamlit for readability. [How to change streamlit theme](https://blog.streamlit.io/introducing-theming/)

## Program Structure

### Chapter 0: Import Packages

Firstly, the user needs to import all required packages to run the code correctly and without errors.

- Packages to import: ```streamlit```, ```pandas```, ```yfinance```, ```plotly```, ```base64```

- No further data needs to be downloaded as the real time stock prices are retrieved using yfinance library and the company data is retrieved through web scraping [Wikipedia](https://de.wikipedia.org/wiki/S%26P_100).

### Chapter 1: Preliminary steps to create the app

The authors recommend to use ```streamlit``` as the main platform to show the data and engage with the user to provide him or her with a flexible and easy-to-use app. As streamlit enables the app to receive user inputs as well as to show the results in a website-like setting, users of this Trading Suggestion App can work intuitively in a very familiar environment. However, to achieve these results, we first need to do some preliminary steps to create this user-friendly environment:

- Set the page layout, title, and description

- Create a sidebar, where the app retrieves its user inputs

- Load  the company data through web scraping the Wikipedia page of the S&P 100 firms and show them in a table so that the user knows which ticker symbol represents which company

### Chapter 2: Real-time stock data retrieving and RSI calculation

In a third step, we need to retrieve the daily stock price of our companies. The ```yfinance``` library allows the user to do that pretty easily. However, it is important to include all Ticker Symbols (of all S&P 100 firms) and save the retrieved data in a separate variable, so that we can use them in our RSI calculation. The defined ```compute_rsi(data, time_window)``` function computes the RSI of each stock through the following calculations:

1) RS = Average Gain / Average Loss

2) RSI = 100 – (100 / (1+RS))

**First calculations:**

3) First Average Gain = Sum of Gains over the past 14 periods / 14

4) First Average Loss = Sum of Losses over the past 14 periods / 14

**Second calculations:**

5) Average Gain = [(previous Average Gain) * 13 + current Gain] / 14

6) Average Loss = [(previous Average Loss) * 13 + current Loss] / 14

As the RSI is a kind of moving average, the calculations should include a smoothing technique, which is achieved through the second calculations. In Python, using ```yfinance```, we can calculate the difference in stock price (on day) through the ```.diff(1)``` function. The up change should be equal to the positive difference (if ```difference``` = 0, the ```up_change``` should be 0 as well). The same for the negative difference ```down_change```. In order to get the mean of our changes ```up``` and ```down``` we can use the ```.mean()``` function in combination with the ```.ewm()``` function and set the com to the defined ```time_window``` (by default usually 14 days) minus 1, to get the decay of ```alpha=1/time_window``` (as values are related to exponential decay). To get to our RS we need to divide our ```up_change_average``` with our ```down_change_average``` (and take the absolute value of this result). Lastly, the RSI can be calculated with ```100 – 100/(1+RS)``` as stated above.

### Chapter 3: GET ALL HOT STOCKS

Now, it is important to separate the companies that have an RSI of lower than 30 or higher than 70, as they are considered hot and thereby relevant for the user.  He or she might want to execute some trades based on this information. To separate the hot stocks, we can iterate through our RSI computed stocks and append them to a new list if their current/newest RSI is either < 30 or > 70. This new list can be used in a last step to provide only the relevant data to our user.

### Chapter 4: Show the data in a user-friendly way

Lastly, it is important to show the data in a clear, easy-to-use and simple-to-understand way. In order to achieve this, the authors mainly used the ```.add_trace```, ```.update_yaxes```, ```.updates_xaxes```, ```.update_layout```, ```go.Scatter``` and ```.make_subplots``` functions of the ```plotly``` library to show the RSI development of a stock in a subplot underneath the corresponding stock price development plot. This is done because the RSI strategy is based on price and RSI development over a given timeframe.

## Authors

Christian Bernard Mathieu

Noah Nolè

## Appendix - Libraries Description

[Streamlit](https://docs.streamlit.io/en/stable/) is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science. In just a few minutes you can build and deploy powerful data apps.

[Pandas](https://pandas.pydata.org/pandas-docs/stable/index.html) is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.

[Yfinance](https://pypi.org/project/yfinance/) offers a reliable, threaded, and Pythonic way to download historical market data from Yahoo! finance.

[Plotly](https://plotly.com/) is an interactive, open-source plotting library that supports over 40 unique chart types covering a wide range of statistical, financial, geographic, scientific, and 3-dimensional use-cases.

[Base64](https://docs.python.org/3/library/base64.html) provides functions for encoding binary data to printable ASCII characters and decoding such encodings back to binary data. It provides encoding and decoding functions for the encodings specified in RFC 3548, which defines the Base16, Base32, and Base64 algorithms, and for the de-facto standard Ascii85 and Base85 encodings.
