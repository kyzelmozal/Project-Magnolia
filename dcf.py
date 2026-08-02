import pandas as pd
overview = pd.read_excel("data/companies.xlsx", sheet_name="Overview")
companies = overview["Ticker"].tolist()
results = []

for company in companies: 
    df = pd.read_excel("data/companies.xlsx", sheet_name=company)

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
    futureStockPrice = futureMarketCap / df["SharesOut"].iloc[-1]
    results.append({
        "Ticker": company,
        "futureStockPrice": float(round(futureStockPrice, 2))
    })

print(*results, sep="\n")