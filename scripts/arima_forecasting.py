import pandas as pd
import numpy as np
import os
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import warnings
warnings.filterwarnings("ignore")

def check_stationarity(series):
    """Perform Augmented Dickey-Fuller test"""
    result = adfuller(series.dropna())
    return result[1] < 0.05  # p-value < 0.05 means stationary

def make_stationary(series):
    """Apply differencing to make data stationary if needed"""
    if check_stationarity(series):
        return series
    return series.diff().dropna()

def train_arima(df, stock_name):
    """Train ARIMA model and forecast"""
    df.set_index('Datetime', inplace=True)
    df = df.asfreq('T')  # Ensure minute-by-minute frequency
    df['Close'] = df['Close'].fillna(method='ffill')  # Fill missing values
    
    # Make stationary
    stationary_series = make_stationary(df['Close'])
    
    # Fit ARIMA Model (p=1, d=1, q=1 as a starting point)
    model = ARIMA(stationary_series, order=(1, 1, 1))
    model_fit = model.fit()
    
    # Forecast next 10 minutes
    forecast_steps = 10
    forecast = model_fit.forecast(steps=forecast_steps)
    
    # Print results
    print(f"Stock: {stock_name}")
    print("Next 10 minutes forecast:")
    print(forecast)
    print("-" * 40)

def process_multiple_stocks(data_folder):
    """Run ARIMA forecasting on multiple stock files"""
    for file in os.listdir(data_folder):
        if file.endswith(".csv"):
            file_path = os.path.join(data_folder, file)
            df = pd.read_csv(file_path)
            df.rename(columns={df.columns[0]: 'Datetime'}, inplace=True)
            df['Datetime'] = pd.to_datetime(df['Datetime'])
            train_arima(df, file.replace(".csv", ""))

# Run the forecasting
if __name__ == "__main__":
    data_folder = "../data"  # Adjust folder path as needed
    process_multiple_stocks(data_folder)
