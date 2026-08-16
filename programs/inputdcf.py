import pandas as pd
import yfinance as yf
results = []

company = input("Enter ticker symbol: ").upper().strip()

ticker = yf.Ticker(company)
currentPrice = ticker.fast_info["last_price"]

# Market Cap and shares outstanding converted to millions
marketCap = ticker.fast_info["market_cap"] / 1000000
sharesOut = ticker.fast_info["shares"] / 1000000

cashflow = ticker.cashflow
operatingCashFlow = cashflow.loc["Operating Cash Flow"] / 1000000
capEx = -cashflow.loc["Capital Expenditure"] / 1000000

df = pd.DataFrame({
    "OperatingCashFlow": operatingCashFlow,
    "CapEx": capEx
})

df = df.sort_index().tail(5)

df["FCF"] = df["OperatingCashFlow"] - df["CapEx"]
df["FCFGrowth"] = (df["FCF"].pct_change())
averageFCFGrowth = df["FCFGrowth"].mean()
if averageFCFGrowth > 1:
    averageFCFGrowth = df["FCFGrowth"].median()
    print(f"{company}: Average FCF Growth > 10, using median instead")
    
futureFCFs = []
if df["FCF"].iloc[-1] < 0:
    print(f"{company}: FCF is negative, company is not profitable.")
    fcf = 0
else:
    fcf = df["FCF"].iloc[-1]
for i in range(3):
    fcf = fcf * (1 + averageFCFGrowth)
    futureFCFs.append(float(round(fcf, 2)))

futureDCFs1Y = []
futureDCFs3Y = []
discountRate = 0.1

for j in range(1):
    dcf = futureFCFs[j] / ((1 + discountRate) ** (j+1))
    futureDCFs1Y.append(float(round(dcf, 2)))

for k in range(3):
    dcf = futureFCFs[k] / ((1 + discountRate) ** (k+1))
    futureDCFs3Y.append(float(round(dcf, 2)))

futureMarketCap1Y = marketCap + sum(futureDCFs1Y)
futurePrice1Y = futureMarketCap1Y / sharesOut

futureMarketCap3Y = marketCap + sum(futureDCFs3Y)
futurePrice3Y = futureMarketCap3Y / sharesOut

upside1Y = (futurePrice1Y - currentPrice) / currentPrice * 100
upside3Y = (futurePrice3Y - currentPrice) / currentPrice * 100

results.append({
    "ticker": company,
    "marketCap": float(round(marketCap, 2)),
    "sharesOutstanding": float(round(sharesOut, 2)),
    "currentPrice": float(round(currentPrice, 2)),
    "futurePrice1Y": float(round(futurePrice1Y, 2)),
    "upside1Y": float(round(upside1Y, 2)), 
    "futurePrice3Y": float(round(futurePrice3Y, 2)),
    "upside3Y": float(round(upside3Y, 2)),
    "averageFCFGrowth": float(round(averageFCFGrowth, 2))
})

# print(*results, sep="\n")

sortedResults = sorted(results, key=lambda x: x["upside1Y"], reverse=True)
sortedResults_df = pd.DataFrame(sortedResults)
sortedResults_df = sortedResults_df.sort_values(
    "upside1Y",
    ascending=False,
    na_position="last"
)

print(sortedResults_df)

