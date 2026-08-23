import pandas as pd
import yfinance as yf
import sys

def fetch_EPS(company):
    ticker = yf.Ticker(company)
    incomeStatement = ticker.income_stmt
    quarterlyIncomeStatement = ticker.quarterly_income_stmt

    yearlyBasicEPS = incomeStatement.loc["Basic EPS"]
    quarterlyBasicEPS = quarterlyIncomeStatement.loc["Basic EPS"]

    yearly_df = pd.DataFrame({
        "yearlyBasicEPS": yearlyBasicEPS
    })

    quarterly_df = pd.DataFrame({
        "quarterlyBasicEPS": quarterlyBasicEPS
    })

    yearly_df = yearly_df.sort_index()
    quarterly_df = quarterly_df.sort_index()

    yearly_df["yearlyEPSgrowth"] = yearly_df["yearlyBasicEPS"].pct_change()
    quarterly_df["quarterlyEPSgrowth"] = quarterly_df["quarterlyBasicEPS"].pct_change()

    lastQuarterEPSGrowth = quarterly_df["quarterlyEPSgrowth"].iloc[-1]
    lastYearEPSGrowth = yearly_df["yearlyEPSgrowth"].iloc[-1]
    last3YearEPSGrowth = ((yearly_df["yearlyBasicEPS"].iloc[-1] - yearly_df["yearlyBasicEPS"].iloc[-3]) / yearly_df["yearlyBasicEPS"].iloc[-3] )

    def replaceNan(value):
        return "Not a number" if pd.isna(value) else value * 100 
        # Converted to percent because JS is buggy
    
    lastQuarterEPSGrowth = replaceNan(lastQuarterEPSGrowth) 
    lastYearEPSGrowth = replaceNan(lastYearEPSGrowth)
    last3YearEPSGrowth = replaceNan(last3YearEPSGrowth)

    return({
        "lastQuarterEPSGrowth": lastQuarterEPSGrowth,
        "lastYearEPSGrowth": lastYearEPSGrowth,
        "last3YearEPSGrowth": last3YearEPSGrowth
    })




