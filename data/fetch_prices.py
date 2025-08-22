import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker="strucured", period="1mo ", interval="1d"):
    stock =yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    df.reset_index(inplace=True)
    df.to_csv(f"{ticker}_clean.csv", index=False)
    print(f"Saved {ticker} prices to structured_clean.csv")
    return df
if __name__ == "__main__":
    data = fetch_stock_data("Yahoo Finance")
    print(data.head())