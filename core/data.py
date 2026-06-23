import yfinance as yf
import pandas as pd

class DataFeed:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    def fetch_data(self):
        print(f"Fetching data for {self.ticker}...")
        data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        data.dropna(inplace=True)
        return data