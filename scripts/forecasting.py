import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# Load historical stock data (CSV file)
def load_stock_data(file_path):
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])  # Ensure timestamp is datetime format
    df = df.sort_values(by='timestamp')  # Sort by time
    return df

# Feature engineering: Create time-based features
def create_features(df):
    df['minute'] = df['timestamp'].dt.minute
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    return df

# Train a simple linear regression model
def train_model(df):
    df = create_features(df)
    X = df[['minute', 'hour', 'day_of_week']]
    y = df['close']  # Predict closing price
    model = LinearRegression()
    model.fit(X, y)
    return model

# Predict stock movement
def predict_next_move(model, latest_data):
    latest_features = create_features(latest_data)
    predicted_price = model.predict(latest_features[['minute', 'hour', 'day_of_week']])
    return predicted_price

# Check if stock is expected to increase by at least 5%
def check_stock_increase(current_price, predicted_price):
    increase_percentage = ((predicted_price - current_price) / current_price) * 100
    return increase_percentage >= 5

# Main execution
if __name__ == "__main__":
    file_path = "../data/TSLA.csv"  # Change to the actual file path
    df = load_stock_data(file_path)
    model = train_model(df)
    
    # Simulate checking latest stock data
    latest_data = df.tail(1)  # Use last known data point as example
    predicted_price = predict_next_move(model, latest_data)
    
    if check_stock_increase(latest_data['close'].values[0], predicted_price):
        print("ALERT: Stock is predicted to rise by at least 5%!")
