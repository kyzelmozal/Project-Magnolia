print("viewapp.py is running")

import sqlite3
import pandas as pd
import yfinance as yf

connection = sqlite3.connect("magnolia.db")

# Fetch all picks from the database and print them as a DataFrame
df = pd.read_sql_query("SELECT * FROM picks", connection)

for index, row in df.iterrows():
    stock = yf.Ticker(row["ticker"].upper())
    last_price = stock.fast_info["last_price"]
    percent_change = ((last_price - row["price"]) / row["price"]) * 100

    df.loc[index, "percent_change"] = percent_change

connection.close()
print(df)