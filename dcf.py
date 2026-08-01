import pandas as pd
df = pd.read_excel("data/companies.xlsx", sheet_name="HWM_financials")

df["FCF"] = df["OperatingCashFlow"] - df["CapEx"]
df["RevenueGrowth"] = (df["Revenue"].pct_change() * 100).round(2)
df["FCFGrowth"] = (df["FCF"].pct_change() * 100).round(2)
print(df[["Revenue", "FCF", "RevenueGrowth", "FCFGrowth"]])

average_revenue_growth = df["RevenueGrowth"].mean().round(2)
last_revenue = df["Revenue"].iloc[-1]
forecast_2026 = last_revenue * (1 + (average_revenue_growth / 100))
# print(f"Forecasted Revenue for 2026: ${forecast_2026.round(2)}")

forecast = []
revenue = last_revenue
for i in range(5):
    revenue = revenue * (1 + average_revenue_growth / 100)
    forecast.append(float(round(revenue, 2)))
# print(f"Revenue Growth Forecast for the next 5 years: {forecast}")

df["FCF Margin"] = df["FCF"] / df["Revenue"]
average_fcf_margin = df["FCF Margin"].iloc[-3:].mean().round(2)
print(f"Average FCF Margin: {average_fcf_margin}")
forecast_fcf = []
for j in forecast:
    fcf = j * average_fcf_margin 
    forecast_fcf.append(float(round(fcf, 2)))
# print(f"Forecasted FCF for the next 5 years: {forecast_fcf}")

discount_rate = 0.1
discounted_fcf = []
for t, fcf in enumerate(forecast_fcf, start=1):
    pv = fcf / ((1 + discount_rate) ** t)
    discounted_fcf.append(float(round(pv, 2)))
print(f"Discounted FCF for the next 5 years: {discounted_fcf}")
print(f"Sum of Discounted FCF: {sum(discounted_fcf)}")

growth_rate = 0.04
terminal_value = (
    forecast_fcf[-1] * (1 + growth_rate) / (discount_rate - growth_rate)
)
print(f"Forecasted FCF for terminal value calculation: {forecast_fcf[-1]}")
print(f"Terminal Value: {terminal_value}")

enterprise_value = sum(discounted_fcf) + terminal_value
print(f"Enterprise Value: {enterprise_value}")

cash = df["Cash"].iloc[-1]
debt = df["TotalDebt"].iloc[-1]
equity_value = enterprise_value + cash - debt
print(f"Equity Value: {equity_value}")

shares_outstanding = df["SharesOut"].iloc[-1]
price_per_share = equity_value / shares_outstanding
print(f"Price per Share: {price_per_share}")

print("Revenue Growth:", average_revenue_growth)
print("FCF Margin:", average_fcf_margin)
print("Forecast FCF:", forecast_fcf)
print("Terminal Value:", terminal_value)
print("Enterprise Value:", enterprise_value)

print(df[["Revenue", "FCF", "FCF Margin"]])