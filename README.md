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


## Technologies
- Python Version: 3.8.5
- Jupyter Notebook: To install Juypter Notebook, please refer to https://jupyter.org/install
- Libraries used: `streamlit`, `pandas`, `yfinance`, `plotly`, `base64`

For further library descriptions refer to [Appendix - Libraries Description](#appendix---libraries-description).

## Setup
To run this application, it is recommended to use a Jupyter Notebook. 

The easiest way to get all required modules would be to run the [Startup](Startup.ipynb) file. This file runs the following commands:

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

