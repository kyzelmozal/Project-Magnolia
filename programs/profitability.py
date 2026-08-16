import pandas as pd
import yfinance as yf
overview = pd.read_excel("data/companies.xlsx", sheet_name="Overview")
companies = overview["Ticker"].tolist()
results = []

for company in companies:
    ticker = yf.Ticker(company)
    incomeStatement = ticker.income_stmt

    revenue = incomeStatement.loc["Total Revenue"]
    # grossProfit = incomeStatement.loc["Gross Profit"]
    if "Gross Profit" in incomeStatement.index:
        grossProfit = incomeStatement.loc["Gross Profit"]
    else:
        grossProfit = None

    netIncome = incomeStatement.loc["Net Income"]

    df = pd.DataFrame({
        "Revenue": revenue,
        "GrossProfit": grossProfit,
        "NetIncome": netIncome
    })

    # Sort from oldest to newest
    df = df.sort_index() 
    # Keep only the last 3 years of data
    df = df.tail(3) 

    # Calculating margins over past 3 years
    df["GrossMargin"] = df["GrossProfit"] / df["Revenue"]
    df["ProfitMargin"] = df["NetIncome"] / df["Revenue"]

    # Caculating growth of margins over past 3 years
    df["GrossMarginGrowth"] = df["GrossMargin"].pct_change()
    df["ProfitMarginGrowth"] = df["ProfitMargin"].pct_change()

    for date, row in df.iterrows():

        results.append({
            "Ticker": company,
            "Date": date,
            "GrossMargin": float(round(row["GrossMargin"], 4)),
            "ProfitMargin": float(round(row["ProfitMargin"], 4)),
            "GrossMarginGrowth": float(round(row["GrossMarginGrowth"], 4)),
            "ProfitMarginGrowth": float(round(row["ProfitMarginGrowth"], 4))
        })

results_df = pd.DataFrame(results)
print(results_df)