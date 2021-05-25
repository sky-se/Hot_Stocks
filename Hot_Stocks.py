# %%
import streamlit as st
import pandas as pd
import yfinance as yf
from plotly import graph_objs as go
import base64
from plotly.subplots import make_subplots


st.set_page_config(layout="wide")
st.title("Trading Suggestion App")

#   Hot Stocks Calculation

st.markdown("""
This app retrieves the list of the **S&P 100** (from Wikipedia) and shows the current **Hot Stocks** based on the **Relative Strength Index**.
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib
* **S&P 100 Data Source:** [Wikipedia](https://en.wikipedia.org/wiki/S%26P_100).
* **Theory on Relative Strength Index Indicator (RSI):** [Wikipedia](https://en.wikipedia.org/wiki/Relative_strength_index).
* Stocks are considered **hot** when their **current RSI** is either **<30** (=oversold) or **>70** (=overbought).
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

user_input = st.sidebar.selectbox("Select a ticker from the S&P100 to check the stock and RSI development", sp_df)

all_companies = st.sidebar.button("GET ALL HOT STOCKS")


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


# Function to calculate RSI
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


# Get all Companies that are currently hot in a separate list
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

# Draw the Stock Price and RSI of the selected companies with Date (YTD) on x-axes.


def draw_rsi(data):
    if all_companies == True:
        selected_ticker = hot_stocks
        for i in selected_ticker:
            close = data[str(i)].Close
            close = close.reset_index()
            close["Stock"] = data[str(i)].Close
            close["RSI"] = compute_rsi(data[str(i)].Close, 14)
            close['low'] = 30
            close['high'] = 70
            fig = make_subplots(rows=2, cols=1, subplot_titles=(
                f"Daily Stock Price of {sp_df['Name'].loc[str(i)]} YTD 2021", f"RSI for {sp_df['Name'].loc[str(i)]}"))
            fig.add_trace(go.Scatter(x=data['Date'], y=close['Stock'],
                                     mode='lines',
                                     name=sp_df['Name'].loc[str(i)] +
                                     " (Stock Price)",
                                     line=dict(color="Orange", width=2.5), legendgroup="1"), row=1, col=1)
            fig.add_trace(go.Scatter(x=data['Date'], y=close['RSI'],
                                     mode='lines',
                                     name=sp_df['Name'].loc[str(i)] +
                                     " (RSI)",
                                     line=dict(color="Red", width=2.5), legendgroup="2"), row=2, col=1)
            fig.add_trace(go.Scatter(x=data['Date'], y=close['high'],
                                     fill=None,
                                     mode='lines',
                                     name='Overbought or Oversold',
                                     line=dict(width=0.5, color='rgb(222, 196, 200)', dash='dash'), legendgroup="2"), row=2, col=1)
            fig.add_trace(go.Scatter(x=data['Date'], y=close['low'],
                                     fill='tonexty',  # fill area between trace0 and trace1
                                     mode='lines',
                                     name='Neither Oversold Nor Overbought',
                                     line=dict(width=0.5, color='rgb(222, 196, 200)', dash='dash'), legendgroup="2"), row=2, col=1)


            # update axis ticks
            fig.update_yaxes(nticks=30, showgrid=True,
                             title_text="Closing Stock Price [USD]", row=1, col=1)
            fig.update_yaxes(nticks=30, showgrid=True,
                             title_text="RSI", row=2, col=1)
            fig.update_xaxes(nticks=12, showgrid=True, title_text="Date")
            fig.layout.update(xaxis_rangeslider_visible=True)
            fig.update_xaxes(matches='x')

            # update layout
            fig.update_layout(title=f"<b>Daily Stock Price & RSI for {sp_df['Name'].loc[str(i)]} YTD 2021</b>", template="plotly", height=1200, width=1800, legend_tracegroupgap=180
                              )

            # update legend
            fig.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ))

        return st.plotly_chart(fig)

    else:
        close = data[user_input].Close
        close = close.reset_index()
        close["Stock"] = data[user_input].Close
        close["RSI"] = compute_rsi(data[user_input].Close, 14)
        close['low'] = 30
        close['high'] = 70
        fig = make_subplots(rows=2, cols=1, subplot_titles=(
            f"Daily Stock Price of {sp_df['Name'].loc[user_input]} YTD 2021", f"RSI for {sp_df['Name'].loc[user_input]}"))
        fig.add_trace(go.Scatter(x=data['Date'], y=close['Stock'],
                                 mode='lines',
                                 name=sp_df['Name'].loc[user_input] +
                                 " (Stock Price)",
                                 line=dict(color="Orange", width=2.5), legendgroup="1"), row=1, col=1)
        fig.add_trace(go.Scatter(x=data['Date'], y=close['RSI'],
                                 mode='lines',
                                 name=sp_df['Name'].loc[user_input] + " (RSI)",
                                 line=dict(color="Red", width=2.5), legendgroup="2"), row=2, col=1)
        fig.add_trace(go.Scatter(x=data['Date'], y=close['high'],
                                 fill=None,
                                 mode='lines',
                                 name='Overbought',
                                 line=dict(width=0.5, color='rgb(222, 196, 200)', dash='dash'), legendgroup="2"), row=2, col=1)
        fig.add_trace(go.Scatter(x=data['Date'], y=close['low'],
                                 fill='tonexty',  # fill area between trace0 and trace1
                                 mode='lines',
                                 name='Oversold',
                                 line=dict(width=0.5, color='rgb(222, 196, 200)', dash='dash'), legendgroup="2"), row=2, col=1)

        # update axis ticks
        fig.update_yaxes(nticks=30, showgrid=True,
                         title_text="Closing Stock Price [USD]", row=1, col=1)
        fig.update_yaxes(nticks=30, showgrid=True,
                         title_text="RSI", row=2, col=1)
        fig.update_xaxes(nticks=12, showgrid=True, title_text="Date")
        fig.layout.update(xaxis_rangeslider_visible=True)
        fig.update_xaxes(matches='x')

        # update layout
        fig.update_layout(title=f"<b>Daily Stock Price & RSI of {sp_df['Name'].loc[user_input]} YTD 2021</b>", template="plotly", height=1200, width=1800, legend_tracegroupgap=180
                          )

        # update legend
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))

        return st.plotly_chart(fig)


# Call the function
draw_rsi(data)
