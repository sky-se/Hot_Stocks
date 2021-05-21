# %%
import streamlit as st
import pandas as pd
import yfinance as yf
from plotly import graph_objs as go
import base64


st.set_page_config(layout="wide")
st.title("Trading Suggestion App")

#   Hot Stocks Calculation

st.markdown("""
This app retrieves the list of the **S&P 100** (from Wikipedia) and shows the current **Hot Stocks** based on the **Relative Strength Index**.
* **Python libraries:** streamlit, pandas, yfinance, plotly, base64.
* **S&P 100 Data Source:** [Wikipedia](https://en.wikipedia.org/wiki/S%26P_100).
* **Theory on Relative Strength Index Indicator (RSI):** [Wikipedia](https://en.wikipedia.org/wiki/Relative_strength_index).
""")

st.sidebar.header('User Input Features')


@st.cache
def load_sp_data():
    url = 'https://en.wikipedia.org/wiki/S%26P_100'
    html = pd.read_html(url, header=0)
    df = html[2]
    return df


sp_df = load_sp_data()


#   Show overview of S&P 100 companies
st.header('Companies in S&P 100')
st.write('Data Dimension: ' + str(sp_df.shape[0]) + ' rows and ' + str(
    sp_df.shape[1]) + ' columns.')
st.dataframe(sp_df)


# Download the data
@st.cache
def filedownload(df):
    csv = sp_df.to_csv(index=False)
    # strings <-> bytes conversions
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="SP100.csv">Download CSV File</a>'
    return href


#   Sidebar - Company selection
user_input = st.sidebar.text_input(
    "Input a Ticker Name (Symbol) to check the company's RSI development", "AAPL")

all_companies = st.sidebar.button(
    "GET ALL HOT STOCKS")


st.markdown(filedownload(all_companies), unsafe_allow_html=True)

#   https://pypi.org/project/yfinance/

data = yf.download(
    tickers=list(sp_df.Symbol),
    period="ytd",
    interval="1d",
    group_by='ticker',
    auto_adjust=True,
    prepost=True,
    threads=True,
    proxy=None
)
data.reset_index(inplace=True)


#   get hot stocks only


def compute_rsi(data, time_window):
    diff = data.diff(1).dropna()
    up_chg = 0 * diff
    down_chg = 0 * diff
    up_chg[diff > 0] = diff[diff > 0]
    down_chg[diff < 0] = diff[diff < 0]
    up_chg_avg = up_chg.ewm(com=time_window - 1,
                            min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(
        com=time_window - 1, min_periods=time_window).mean()
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi


sp_df = sp_df.reset_index()

Symbols = sp_df["Symbol"].tolist()
hot_stocks = []
for i in Symbols:
    y = compute_rsi(data[str(i)].Close, 14)
    y = y.tolist()
    if len(y) > 0:
        if y[-1] < 30 or y[-1] > 70:
            hot_stocks.append(str(i))
        else:
            continue
    else:
        continue

sp_df = sp_df.set_index('Symbol')


def draw_rsi(data):
    if all_companies == True:
        selected_ticker = hot_stocks
        for i in selected_ticker:
            close = data[str(i)].Close
            close = close.reset_index()
            close["RSI"] = compute_rsi(data[str(i)].Close, 14)
            close['low'] = 30
            close['high'] = 70
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['Date'], y=close['high'],
                                     fill=None,
                                     mode='lines',
                                     name='Overbought',
                                     line=dict(width=0.5, color='rgb(222, 196, 255)', dash='dash')))
            fig.add_trace(go.Scatter(x=data['Date'], y=close['low'],
                                     fill='tonexty',  # fill area between trace0 and trace1
                                     mode='lines',
                                     name='Oversold',
                                     line=dict(width=0.5, color='rgb(222, 196, 255)', dash='dash')))
            fig.add_trace(go.Scatter(x=data['Date'], y=close['RSI'],
                                     mode='lines',
                                     name=sp_df['Name'].loc[str(i)],
                                     line=dict(color="Yellow", width=2), ))
            # update axis ticks
            fig.update_yaxes(nticks=30, showgrid=True)
            fig.update_xaxes(nticks=12, showgrid=True)
            fig.layout.update(xaxis_rangeslider_visible=True)

            # update layout
            fig.update_layout(title=f"<b>Daily RSI for {sp_df['Name'].loc[str(i)]} YTD 2021</b>", height=700, width=1800, xaxis_title='Date', yaxis_title='Relative Strength Index', template="plotly"
                              )

            # update legend
            fig.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ))
            st.plotly_chart(fig)
    else:
        close = data[user_input].Close
        close = close.reset_index()
        close["RSI"] = compute_rsi(data[user_input].Close, 14)
        close['low'] = 30
        close['high'] = 70
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=close['high'],
                                 fill=None,
                                 mode='lines',
                                 name='Overbought',
                                 line=dict(width=0.5, color='rgb(222, 196, 255)', dash='dash')))
        fig.add_trace(go.Scatter(x=data['Date'], y=close['low'],
                                 fill='tonexty',  # fill area between trace0 and trace1
                                 mode='lines',
                                 name='Oversold',
                                 line=dict(width=0.5, color='rgb(222, 196, 255)', dash='dash')))
        fig.add_trace(go.Scatter(x=data['Date'], y=close['RSI'],
                                 mode='lines',
                                 name=sp_df['Name'].loc[user_input],
                                 line=dict(color="Yellow", width=2), ))
        # update axis ticks
        fig.update_yaxes(nticks=30, showgrid=True)
        fig.update_xaxes(nticks=12, showgrid=True)
        fig.layout.update(xaxis_rangeslider_visible=True)

        # update layout
        fig.update_layout(title=f"<b>Daily RSI for {sp_df['Name'].loc[user_input]} YTD 2021</b>", height=700, width=1800, xaxis_title='Date', yaxis_title='Relative Strength Index', template="plotly"
                          )

        # update legend
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
        st.plotly_chart(fig)


draw_rsi(data)
