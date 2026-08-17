import pandas as pd
import yfinance as yf
import requests

ticker = input("Enter a stock ticker: ").upper()
decision = input("Buy or Sell: ")
date = input("Enter the date (YYYY-MM-DD): ")

response = requests.post(
    "http://127.0.0.1:5000/api/picks",
    json={
        "ticker": ticker,
        "decision": decision,
        "date": date
    }
)

print("Status code:", response.status_code)
print("Response:", response.text)