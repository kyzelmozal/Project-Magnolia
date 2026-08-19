import pandas as pd
import yfinance as yf
import sys    

def fetch_stockinfo(company):

    ticker = yf.Ticker(company.upper())
    price = ticker.fast_info["last_price"]
    market_cap = ticker.fast_info["market_cap"]

    return ({
        "ticker": company,
        "price": price,
        "market_cap": market_cap
    })