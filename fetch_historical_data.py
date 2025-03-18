import requests
import pandas as pd
import os
from datetime import datetime, timedelta
from google.cloud import storage

# Alpha Vantage API settings
API_KEY = "DmP_78xmQB7Ckt5mEFZ5ogIi_EdjWQzV"
BASE_URL = "https://www.alphavantage.co/query"
STOCK_SYMBOLS = ["SMCX", "IVVD", "DPST", "SPXL"]  # Removed ticker SPX
BUCKET_NAME = "stock-buy-alert-data"  # Google Cloud Storage bucket name
MARKET_OPEN = 8 * 60  # 8:00 AM in minutes
MARKET_CLOSE = 16 * 60  # 4:00 PM in minutes

# Initialize Google Cloud Storage client
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

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
    
    # Filter data to only include market hours (8:00 AM - 4:00 PM EST)
    df = df[(df.index.hour * 60 + df.index.minute >= MARKET_OPEN) & 
            (df.index.hour * 60 + df.index.minute <= MARKET_CLOSE)]
    
    df["symbol"] = symbol
    return df

def save_data(df, symbol):
    """Save data to Google Cloud Storage while keeping only the last 365 days of records."""
    file_name = f"{symbol}.csv"
    local_file_path = f"/tmp/{file_name}"  # Temporary storage
    
    # Check if file exists in GCS and load existing data
    blob = bucket.blob(file_name)
    if blob.exists():
        blob.download_to_filename(local_file_path)
        
        # Read existing data while handling index issues
        existing_df = pd.read_csv(local_file_path)
        
        # Ensure the index is set properly
        if "index" in existing_df.columns:
            existing_df["index"] = pd.to_datetime(existing_df["index"])
            existing_df.set_index("index", inplace=True)
        elif existing_df.shape[0] > 0:  # If not empty, assume the first column is the index
            existing_df.set_index(existing_df.columns[0], inplace=True)
            existing_df.index = pd.to_datetime(existing_df.index)
        
        # Merge existing and new data
        df = pd.concat([existing_df, df])
        df = df[~df.index.duplicated(keep='last')]  # Remove duplicate timestamps
    
    # Filter to keep only the last 365 days
    cutoff_date = datetime.now() - timedelta(days=365)
    df = df[df.index >= cutoff_date]
    
    # Save to local temp file
    df.to_csv(local_file_path, index=True)
    
    # Upload to GCS
    blob.upload_from_filename(local_file_path)
    print(f"Data saved for {symbol} in Google Cloud Storage bucket: {BUCKET_NAME}")

def main():
    for symbol in STOCK_SYMBOLS:
        df = fetch_stock_data(symbol)
        if df is not None:
            save_data(df, symbol)

if __name__ == "__main__":
    main()
