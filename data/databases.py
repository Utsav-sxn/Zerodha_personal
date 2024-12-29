import yfinance as yf
import pandas as pd

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NFLX", "NVDA", "BRK-B", "JPM"]

start_date = "2019-01-01"
end_date = "2023-12-31"

all_data = pd.DataFrame()

for ticker in tickers:
    data = yf.download(ticker, start=start_date, end=end_date)
    data['Ticker'] = ticker
    all_data = pd.concat([all_data, data])


all_data.to_csv("historical_data.csv", index=True)

print("Data saved to historical_data.csv")