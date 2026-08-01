import os

print(os.getcwd())

import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_excel("data/companies.xlsx")

years = ["EPS (2023)", "EPS (2024)", "EPS (2025)"]
hwm_eps = df.loc[df["Company Name"] == "Howmet", years].values[0]
knsl_eps = df.loc[df["Company Name"] == "Kinsale", years].values[0]
print(hwm_eps)
print(knsl_eps)

plt.plot(
    years,
    hwm_eps,
    marker="o"
)

plt.plot(
    years, 
    knsl_eps,
    marker="o"
)

plt.xlabel("Year")
plt.ylabel("EPS ($)")
plt.title("Howmet Aerospace EPS Growth (2023-2025)")

plt.grid(True)

plt.show()