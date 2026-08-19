import pandas as pd
import yfinance as yf
import sys
from flask import Flask, jsonify

app = Flask(__name__)

print("Revenue, Gross Profit, and Net Profit are in millions")
company = input("Enter ticker: ").upper().strip()
ticker = yf.Ticker(company)
incomeStatement = ticker.income_stmt

revenue = incomeStatement.loc["Total Revenue"] / 1000000

if "Gross Profit" not in incomeStatement.index:
    sys.exit(f"No Gross Profit for {company}")

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

print(df)