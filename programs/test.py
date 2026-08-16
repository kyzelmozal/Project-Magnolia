import pandas as pd
import yfinance as yf

ticker = yf.Ticker("ABNB")
cashflow = ticker.cashflow

print(cashflow.index.tolist())
print(cashflow)