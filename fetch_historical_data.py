import requests
import pandas as pd
import os
from datetime import datetime, timedelta
from flask import Flask

# Alpha Vantage API settings
API_KEY = "84G51LOMCWHULE86"
BASE_URL = "https://www.alphavantage.co/query"
STOCK_SYMBOLS = ["SMCX", "IVVD", "DPST", "SPXL"]  # Update this list with desired stock symbols
DATA_DIR = "historical_data"  # Folder to store CSV files

def fetch_stock_data(symbol):
    """Fetch minute-level historical data for the last 30 days from Alpha Vantage."""
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "1min",
        "apikey": API_KEY,
        "outputsize": "full"
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if "Time Series (1min)" not in data:
        print(f"Error fetching data for {symbol}: {data}")
        return None
    
    df = pd.DataFrame.from_dict(data["Time Series (1min)"], orient="index")
    df = df.rename(columns={
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume"
    })
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    df["symbol"] = symbol
    return df

def save_data(df, symbol):
    """Save data to CSV while keeping only the last 365 days of records."""
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = os.path.join(DATA_DIR, f"{symbol}.csv")
    
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path, parse_dates=["index"], index_col="index")
        df = pd.concat([existing_df, df])
        df = df[~df.index.duplicated(keep='last')]  # Remove duplicate timestamps
    
    cutoff_date = datetime.now() - timedelta(days=365)
    df = df[df.index >= cutoff_date]
    
    df.to_csv(file_path, index=True)
    print(f"Data saved for {symbol} in {file_path}")

def main():
    """Fetch and save stock data for all symbols."""
    for symbol in STOCK_SYMBOLS:
        df = fetch_stock_data(symbol)
        if df is not None:
            save_data(df, symbol)

# Create Flask app to keep Cloud Run service running
app = Flask(__name__)

@app.route('/')
def home():
    return "Stock Data Fetching Service is Running"

@app.route('/run-fetch')
def run_fetch():
    """Trigger fetching stock data manually via a URL."""
    main()
    return "Stock data fetched successfully!"

if __name__ == '__main__':
    # Run main() once at startup
    main()
    # Start Flask server to keep the container alive
    app.run(host='0.0.0.0', port=8080)
