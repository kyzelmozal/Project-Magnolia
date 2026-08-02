import pandas as pd
df = pd.read_excel("data/companies.xlsx", sheet_name="HWM_financials")

MarketCap = float(df.iloc[0, 10])
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
print(f"${futureStockPrice.round(2)}")