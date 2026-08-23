import pandas as pd
import yfinance as yf
import sys

def calc_margins(company):
    ticker = yf.Ticker(company)
    incomeStatement = ticker.income_stmt

    revenue = incomeStatement.loc["Total Revenue"] / 1000000

    if "Gross Profit" not in incomeStatement.index:
        raise ValueError(f"No Gross Profit for {ticker}")

    grossProfit = incomeStatement.loc["Gross Profit"] / 1000000
    netProfit = incomeStatement.loc["Net Income"] / 1000000

    df = pd.DataFrame({
        "revenue": revenue,
        "grossProfit": grossProfit,
        "netProfit": netProfit
    })

    df = df.sort_index()
    df = df.tail(3)

    df["grossMargin"] = df["grossProfit"] / df["revenue"]
    df["profitMargin"] = df["netProfit"] / df["revenue"]

    df = df.T
    df.columns = df.columns.strftime("%Y")

    return df