# Hot_Stocks

Hey there! You have stumbled upon the student project "Hot Stocks", which is part of the course "Skills: Programming - Introduction Level" by Mario Silic (Spring Semester 2021 at the University of St.Gallen).

The end goal of our group project was to create an application with which you can follow a common RSI buy/sell strategy. We limited our scope to the S&P 100 Stocks found on: https://de.wikipedia.org/wiki/S%26P_100

If you want to find out more about our project, check out our code and read more below. 

## Table of contents
- [General Information](#general-information)
- [Technologies](#technologies)
- [Setup](#setup)
- [Program Structure](#program-structure)
- [Authors](#authors)
- [Appendix - Libraries Description](#appendix---libraries-description)


## General Information
The goal of this project is to provide the user with an efficient way of receiving potential trade suggestions using the common RSI (Relative Strength Index) strategy. In this strategy stocks are classified as overbought, oversold or neither. Using this strategy we are interested in the oversold and overbought stocks. We identify those stocks by calculating the RSI. When a stock has an RSI of more than 70, the stock is considered overbought and a common strategy is shorting/selling the aforementioned stock. The same case applies when the stock has an RSI of less than 30. This means it is oversold and one should consider longing/buying this stock.

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

## Program Structure


## Authors

Christian Bernard Mathieu

Noah Nolè

## Appendix - Libraries Description

[Streamlit](https://docs.streamlit.io/en/stable/) is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science. In just a few minutes you can build and deploy powerful data apps.

[Pandas](https://pandas.pydata.org/pandas-docs/stable/index.html) is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.

[Yfinance](https://pypi.org/project/yfinance/) offers a reliable, threaded, and Pythonic way to download historical market data from Yahoo! finance.

[Plotly](https://plotly.com/) is an interactive, open-source plotting library that supports over 40 unique chart types covering a wide range of statistical, financial, geographic, scientific, and 3-dimensional use-cases.

[Base64](https://docs.python.org/3/library/base64.html) provides functions for encoding binary data to printable ASCII characters and decoding such encodings back to binary data. It provides encoding and decoding functions for the encodings specified in RFC 3548, which defines the Base16, Base32, and Base64 algorithms, and for the de-facto standard Ascii85 and Base85 encodings.
