import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 5 minutes (300000 ms)
st_autorefresh(interval=300000, key="data_refresh")

st.title("Oil & Gas Futures Dashboard - 15-Min Futures Prices & Volatility")

tickers = ("CL=F", "BZ=F", "NG=F","RB=F")
futures_data = yf.download(tickers, period="5d", interval="15m")

close_data = futures_data["Close"]

st.subheader("Latest Prices")
st.write(close_data.tail(1).T)

daily_change = {}
for col in close_data.columns:
    first_price = close_data[col].iloc[0]
    last_price = close_data[col].iloc[-1]
    pct_change = ((last_price - first_price) / first_price) * 100
    daily_change[col] = pct_change

st.subheader("Daily % Change")
st.write(pd.Series(daily_change).map("{:.2f}%".format))

st.subheader("Latest Volume & 15-day Average")
volume_data = futures_data["Volume"]
latest_volume = volume_data.iloc[-1]
avg_volume = volume_data.rolling(window=15).mean().iloc[-1]

volumes = pd.DataFrame({
    "Latest Volume": latest_volume,
    "15-Day Avg Volume": avg_volume
})
st.write(volumes)

st.subheader("Rolling Volatility - 1 trading day")
returns = np.log(close_data / close_data.shift(1))

rolling_vol = returns.rolling(window=26).std() * np.sqrt(252)

latest_vol = rolling_vol.iloc[-1].map(lambda x: f"{x:.2%}")
st.write("Latest Annualized Volatility")
st.write(latest_vol)

st.subheader("Volatility Over Time")
for col in rolling_vol.columns:
    st.line_chart(rolling_vol[col], height=200)

st.subheader("Price Charts (last 5 days)")
for col in close_data.columns:
    st.line_chart(close_data[col], height=250)


