print("app.py is running")

import sqlite3
from flask import Flask, jsonify, request
import yfinance as yf
import pandas as pd

app = Flask(__name__)

database = "magnolia.db"
def init_database():
    # Establish the connection to the database and create picks table
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS picks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            decision TEXT NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL,
            actual_date TEXT NOT NULL
        )
    """)
 

    connection.commit()
    connection.close()

    print("Database started:", database)

@app.route("/")
def home():
    return "Magnolia backend is running!"

# Get ticker information
@app.route("/api/stock/<ticker>")
def get_stock(ticker):

    stock = yf.Ticker(ticker.upper())
    info = stock.fast_info 
    price = info["last_price"]

    return jsonify({
        "ticker": ticker.upper(),
        "price": price
    })

# Add a new pick to the database
@app.route("/api/picks", methods=["POST"])
def add_pick():

    data = request.get_json()

    date = data["date"]
    ticker = data["ticker"]
    decision = data["decision"]
    stock = yf.Ticker(ticker.upper())

    # Find closing price for the closest valid date 
    history = stock.history(
        start = (pd.Timestamp(date) - pd.Timedelta(days=5)).strftime("%Y-%m-%d"),
        end = (pd.Timestamp(date) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    )

    price = history["Close"].iloc[-1]
    actual_date = history.index[-1].strftime("%Y-%m-%d")

    # Connecting to database and inserting the new pick
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO picks (ticker, decision, price, date, actual_date)
    VALUES (?, ?, ?, ?, ?)
    """, (ticker.upper(), decision, price, date, actual_date))

    print(f"Pick saved to {database}: {ticker.upper()} - {decision} at ${price}")

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Pick saved!", 
        "ticker": ticker.upper(),
        "decision": decision,
        "price": price,
        "date": date,
        "actual_date": actual_date
    })

if __name__ == "__main__":
    init_database()
    app.run(debug=True)