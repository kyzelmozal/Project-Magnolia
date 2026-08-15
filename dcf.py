import pandas as pd
import yfinance as yf
overview = pd.read_excel("data/companies.xlsx", sheet_name="Overview")
companies = overview["Ticker"].tolist()
results = []

for company in companies: 
    df = pd.read_excel("data/companies.xlsx", sheet_name=company)
    ticker = yf.Ticker(company)
    currentPrice = ticker.fast_info["last_price"]

    # In the line below, iloc[0] is needed to so the value extracted is singular instead of a series
    MarketCap = float(overview.loc[overview["Ticker"] == company, "MarketCap"].iloc[0])
    df["FCF"] = df["OperatingCashFlow"] - df["CapEx"]
    df["FCFGrowth"] = (df["FCF"].pct_change())
    averageFCFGrowth = df["FCFGrowth"].mean()

    futureFCFs = []
    fcf = df["FCF"].iloc[-1]
    for i in range(3):
        fcf = fcf * (1 + averageFCFGrowth)
        futureFCFs.append(float(round(fcf, 2)))

    futureDCFs = []
    discountRate = 0.1
    for j in range(3):
        dcf = futureFCFs[j] / ((1 + discountRate) ** (j+1))
        futureDCFs.append(float(round(dcf, 2)))

    futureMarketCap = MarketCap + sum(futureDCFs)
    futurePrice = futureMarketCap / df["SharesOut"].iloc[-1]

    upside = (futurePrice - currentPrice) / currentPrice * 100

    results.append({
        "ticker": company,
        "currentPrice": float(round(currentPrice, 2)),
        "futurePrice": float(round(futurePrice, 2)),
        "upside": float(round(upside, 2))
    })

print(*results, sep="\n")

import json

with open("website/results.json", "w") as f:
    json.dump(results, f, indent=4)
print("Results written to website/results.json")