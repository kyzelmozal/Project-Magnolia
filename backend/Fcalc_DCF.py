import pandas as pd
import yfinance as yf
import sys

def calc_DCF(company):
    ticker = yf.Ticker(company)
    currentPrice = ticker.fast_info["last_price"]
    
    # Market Cap and shares outstanding converted to millions
    marketCap = ticker.fast_info["market_cap"] / 1000000
    sharesOut = ticker.fast_info["shares"] / 1000000

    cashflow = ticker.cashflow
    operatingCashFlow = cashflow.loc["Operating Cash Flow"] / 1000000

    if "Capital Expenditure" not in cashflow.index:
        error = "Missing Capital Expenditure"
        return ({
            "error" : error
        })
    capEx = -cashflow.loc["Capital Expenditure"] / 1000000

    df = pd.DataFrame({
        "OperatingCashFlow": operatingCashFlow,
        "CapEx": capEx
    })

    df = df.sort_index().tail(5)

    df["FCF"] = df["OperatingCashFlow"] - df["CapEx"]
    df["FCFGrowth"] = (df["FCF"].pct_change())
    averageFCFGrowth = df["FCFGrowth"].mean()
    if averageFCFGrowth > 10:
        averageFCFGrowth = df["FCFGrowth"].median()
        print(f"{company}: Average FCF Growth > 10, using median instead")
        error = "Average FCF Growth > 10, using median instead"
    
    futureFCFs = []
    if df["FCF"].iloc[-1] < 0:
        print(f"{company}: FCF is negative, company is not profitable.")
        error = "FCF is negative, company is not profitable"
        fcf = 0
    else:
        fcf = df["FCF"].iloc[-1]
        error = ""
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

    # Converted to percent because JS is buggy
    upside1Y = (futurePrice1Y - currentPrice) / currentPrice * 100
    upside3Y = (futurePrice3Y - currentPrice) / currentPrice * 100

    return ({
        "ticker": company,
        "currentPrice": currentPrice,
        "futurePrice1Y": futurePrice1Y,
        "upside1Y": upside1Y, 
        "futurePrice3Y": futurePrice3Y,
        "upside3Y": upside3Y,
        "error" : error
    })




