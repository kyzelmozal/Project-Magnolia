print("viewapp.py is running")

import sqlite3
import pandas as pd

connection = sqlite3.connect("magnolia.db")

# Fetch all picks from the database and print them as a DataFrame
df = pd.read_sql_query("SELECT * FROM picks", connection)
print(df)

connection.close()